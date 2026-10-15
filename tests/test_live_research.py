from scripts.live_research import preflight, main, audit_markdown
from gmi.replay import replay


def test_preflight_reports_only_flags_and_rejects_invalid_cap():
    env = dict(GEMINI_API_KEY='secret-fixture', GEMINI_MODEL='test-model',
               GMI_LIVE_ENABLED='1', GMI_KEY_AUTHORIZED='1',
               GMI_BUDGET_NOTE='One two-call run', GMI_MAX_CALLS='2')
    assert all(preflight(env).values())
    for cap in ['3', 'invalid', '0']:
        assert not preflight(dict(env, GMI_MAX_CALLS=cap))['two_call_limit']
    assert 'secret-fixture' not in str(preflight(env))


def test_unconfigured_run_never_constructs_provider(monkeypatch):
    monkeypatch.setattr('scripts.live_research.load_local_env', lambda: None)
    for name in ['GEMINI_API_KEY', 'GOOGLE_API_KEY', 'GMI_LIVE_ENABLED']:
        monkeypatch.delenv(name, raising=False)
    def forbidden(*args, **kwargs):
        raise AssertionError('Provider must not be constructed')
    monkeypatch.setattr('scripts.live_research.GeminiProvider', forbidden)
    assert main(['--scope', 'docs/mission2/live-T01-scope.json', '--run']) == 2


def test_audit_template_does_not_confirm_semantically_wrong_claim():
    run = replay('semantic_failure')
    audit = audit_markdown(run)
    assert run.extraction.claims[0].quote in audit
    assert 'Verdict (supported / partial / unsupported / unclear): PENDING' in audit
    assert 'No claim is human-verified' in audit


def test_saved_extraction_uses_snapshots_once_and_preserves_parent(tmp_path):
    from scripts.live_research import extract_saved_sources
    from gmi.models import Source
    parent = replay('good')
    parent.sources += [parent.sources[0].model_copy(update={'id': 'DUP'}),
                       Source(id='NAV',url='https://example.org/nav',title='Menu',text='menu '*100,relevance='unsuitable')]
    path = tmp_path/'run.json'
    path.write_text(parent.model_dump_json())
    before = path.read_bytes()
    class Provider:
        usage = {'api_calls': 0}
        def extract(self, scope, sources):
            self.usage['api_calls'] += 1
            assert len(sources) == 3
            assert [s.id for s in sources] == ['S1', 'S2', 'S3']
            assert sources[0].text == parent.sources[0].text
            return parent.proposed_extraction.model_copy(deep=True)
    result = extract_saved_sources(parent.scope, path, Provider())
    assert result.evidence_mode == 'replay'
    assert result.usage['api_calls'] == 1
    assert result.usage['new_model_extraction'] is True
    assert result.usage['parent_run_id'] == parent.id
    assert path.read_bytes() == before


def test_saved_extraction_rejects_different_question_before_api(tmp_path):
    import pytest
    from scripts.live_research import extract_saved_sources
    parent = replay('good')
    path=tmp_path/'run.json'
    path.write_text(parent.model_dump_json())
    scope=parent.scope.model_copy(update={'question': 'Different research question entirely?'})
    with pytest.raises(ValueError, match='same research question'):
        extract_saved_sources(scope, path, object())
