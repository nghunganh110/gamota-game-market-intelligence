from types import SimpleNamespace
import pytest
from gmi.pipeline import run_research
from gmi.models import Source, Extraction
from gmi.replay import replay
from gmi.gemini import GeminiProvider, LivePolicy

class FaultProvider:
    usage={}
    def search(self, scope):
        raise TimeoutError('Injected fault')

class EmptyReader:
    def read(self,url,source_id):
        return Source(id=source_id,url=url,title='Unreadable',read_status='failed',error='Injected unreadable document')

class Provider:
    usage={}
    def search(self,scope): return [{'url':'https://example.org/document'}]
    def extract(self,scope,sources): raise AssertionError('Must not extract unreadable documents')


def test_timeout_is_run_failure_not_stop():
    r=run_research(replay('good').scope,FaultProvider(),EmptyReader())
    assert r.status=='failed' and r.recommendation=='Tạm giữ'
    assert not r.extraction.claims and 'TimeoutError' in r.errors[0]


def test_all_documents_unreadable_no_fake_narrative():
    r=run_research(replay('good').scope,Provider(),EmptyReader())
    assert r.status=='failed' and not r.extraction.findings and not r.extraction.claims


def test_live_default_off_even_with_model_and_fake_client():
    p=GeminiProvider(LivePolicy(),client=SimpleNamespace(),model='test-model')
    with pytest.raises(PermissionError): p.search(replay('good').scope)
    assert p.policy.calls==0


def test_budget_attempt_limit_includes_errors():
    policy=LivePolicy(enabled=True,authorized=True,budget_note='Synthetic test limit',max_calls=2)
    policy.reserve(); policy.reserve()
    with pytest.raises(PermissionError): policy.reserve()
    assert policy.calls==2


def test_sdk_search_attribution_and_schema_parse_offline():
    from google.genai import types
    scope=replay('good').scope
    search_response=types.GenerateContentResponse(candidates=[types.Candidate(grounding_metadata=types.GroundingMetadata(web_search_queries=['fixture query'],grounding_chunks=[types.GroundingChunk(web=types.GroundingChunkWeb(uri='https://example.org/source',title='Fixture source'))]))])
    ext=replay('good').extraction
    extraction_response=types.GenerateContentResponse(candidates=[types.Candidate(content=types.Content(parts=[types.Part(text=ext.model_dump_json())]))])
    calls=[]
    responses=iter([search_response,extraction_response])
    def generate_content(**kwargs):
        calls.append(kwargs); return next(responses)
    p=GeminiProvider(LivePolicy(enabled=True,authorized=True,budget_note='Mock only',max_calls=2),client=SimpleNamespace(models=SimpleNamespace(generate_content=generate_content)),model='test-model')
    links=p.search(scope)
    assert links==[{'url':'https://example.org/source','title':'Fixture source'}]
    assert p.extract(scope,replay('good').sources).claims[0].id=='C1'
    assert calls[0]['config'].tools[0].google_search is not None
    assert calls[1]['config'].response_json_schema
    assert p.usage['api_calls']==2


def test_full_mocked_pipeline_applies_distinct_source_assessments():
    from gmi.models import SourceAssessment
    base=replay('good')
    class MockProvider:
        usage={'api_calls':0,'mode':'mock'}
        def search(self,scope): return [{'url':s.url} for s in base.sources]
        def extract(self,scope,sources):
            ex=base.extraction.model_copy(deep=True)
            ex.source_assessments=[SourceAssessment(source_id=s.id,quality='Synthetic publisher; no real factual authority',relevance='direct',relevance_reason='Matching synthetic scope') for s in sources]
            return ex
    class MockReader:
        def read(self,url,source_id): return next(s.model_copy(deep=True) for s in base.sources if s.url==url)
    r=run_research(base.scope,MockProvider(),MockReader())
    assert r.status=='completed' and r.recommendation=='Tiếp tục'
    assert all(s.relevance=='direct' and 'human review pending' in s.quality for s in r.sources)
