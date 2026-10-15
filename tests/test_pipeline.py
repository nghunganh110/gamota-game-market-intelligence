from types import SimpleNamespace
import json
import pytest
from gmi.pipeline import run_research
from gmi.models import Source, Extraction
from gmi.replay import replay
from gmi.gemini import GeminiProvider, LivePolicy, parse_extraction

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


def test_invalid_gemini_claim_does_not_discard_valid_records_or_leak_content():
    base = replay('good')
    payload = base.extraction.model_dump(mode='json')
    payload['claims'][1]['period_start'] = 'not-a-date'
    extraction, diagnostic = parse_extraction(json.dumps(payload))
    assert [claim.id for claim in extraction.claims] == ['C1', 'C3']
    assert diagnostic['dropped'] == {'claims': 1}
    assert any(issue['path'].startswith('claims.1') for issue in diagnostic['issues'])
    assert 'not-a-date' not in str(diagnostic)
    assert 'not-a-date' not in str(extraction)


def test_gemini_adapter_reports_partial_schema_without_extra_api_call():
    from google.genai import types
    base = replay('good')
    payload = base.extraction.model_dump(mode='json')
    payload['claims'][1]['period_start'] = 'not-a-date'
    response = types.GenerateContentResponse(candidates=[types.Candidate(
        content=types.Content(parts=[types.Part(text=json.dumps(payload))])
    )])
    calls = []
    def generate_content(**kwargs):
        calls.append(kwargs)
        return response
    provider = GeminiProvider(
        LivePolicy(enabled=True, authorized=True, budget_note='Mock only', max_calls=2),
        client=SimpleNamespace(models=SimpleNamespace(generate_content=generate_content)),
        model='test-model',
    )
    extraction = provider.extract(base.scope, base.sources)
    assert [claim.id for claim in extraction.claims] == ['C1', 'C3']
    assert provider.usage['api_calls'] == len(calls) == 1
    assert provider.usage['extraction_validation']['dropped'] == {'claims': 1}


def test_partial_gemini_extraction_keeps_evidence_but_excludes_invalid_finding():
    base = replay('good')
    payload = base.extraction.model_dump(mode='json')
    payload['claims'][1]['period_start'] = 'not-a-date'
    extraction, diagnostic = parse_extraction(json.dumps(payload))

    class PartialProvider:
        usage = {'extraction_validation': diagnostic, 'api_calls': 2}
        def search(self, scope): return [{'url': source.url} for source in base.sources]
        def extract(self, scope, sources): return extraction

    class BaseReader:
        def read(self, url, source_id):
            return next(source.model_copy(deep=True) for source in base.sources if source.url == url)

    run = run_research(base.scope, PartialProvider(), BaseReader())
    assert run.status == 'partial'
    assert [claim.id for claim in run.extraction.claims] == ['C1', 'C3']
    assert not run.extraction.findings  # The model's finding depended on discarded C2.
    assert 'invalid records' in ' '.join(run.errors)
    assert run.usage['extraction_validation']['dropped'] == {'claims': 1}


def test_reviewer_sources_skip_discovery_and_extract_only_readable_documents():
    base = replay('good')
    calls = []

    class GuidedProvider:
        usage = {'api_calls': 0}
        def search(self, scope):
            raise AssertionError('Guided research must not spend a discovery call')
        def extract(self, scope, sources):
            calls.append([source.url for source in sources])
            return base.extraction.model_copy(deep=True)

    class GuidedReader:
        def read(self, url, source_id):
            if url.endswith('/blocked'):
                return Source(id=source_id, url=url, title='Blocked', read_status='failed', error='HTTP 403')
            source = next(s.model_copy(deep=True) for s in base.sources if s.url == url)
            source.id = source_id
            return source

    urls = [s.url for s in base.sources] + ['https://example.org/blocked']
    run = run_research(base.scope, GuidedProvider(), GuidedReader(), source_urls=urls)
    assert len(calls) == 1 and calls[0] == urls[:3]
    assert run.usage['discovery'] == 'reviewer_supplied_urls'
    assert run.status == 'partial'  # One failed source remains visible.
    assert run.extraction.findings  # Valid evidence is still usable.


def test_unreadable_reviewer_sources_do_not_call_gemini():
    class NoCallProvider:
        usage = {'api_calls': 0}
        def search(self, scope): raise AssertionError('No discovery call')
        def extract(self, scope, sources): raise AssertionError('No extraction without source text')

    run = run_research(replay('good').scope, NoCallProvider(), EmptyReader(),
                       source_urls=['https://example.org/unreadable'])
    assert run.status == 'failed' and run.usage['api_calls'] == 0
