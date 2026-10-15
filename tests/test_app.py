from pathlib import Path
import subprocess
import sys
from streamlit.testing.v1 import AppTest
from gmi.models import Run
from gmi.validation import validate_run


def test_curated_real_cases_keep_short_source_excerpts_and_no_review():
    root = Path(__file__).resolve().parent.parent / 'fixtures' / 'real_cases'
    for name in ('a01.json', 'a02.json'):
        run = Run.model_validate_json((root / name).read_text())
        assert run.evidence_mode == 'replay'
        assert run.review is None and not run.claim_reviews
        assert run.usage['api_calls_new'] == 0
        assert all(len(source.text.split()) <= 25 for source in run.sources)
        checked = validate_run(run)
        assert all(not claim.issues for claim in checked.extraction.claims)


def test_one_click_real_case_replay_renders_two_questions_without_gemini():
    app = AppTest.from_file(Path(__file__).resolve().parent.parent/'app.py').run(timeout=20)
    app.radio[0].set_value('Ví dụ đã lưu — nguồn thật').run()
    next(x for x in app.button if x.label == 'Mở case').click().run()
    assert not app.exception
    assert app.session_state['run'].id == 'curated-real-a01-20261015'
    assert len(app.session_state['run'].extraction.claims) == 3
    next(x for x in app.selectbox if x.label == 'Case thật').select('A02')
    next(x for x in app.button if x.label == 'Mở case').click().run()
    assert not app.exception
    assert app.session_state['run'].id == 'curated-real-a02-20261015'
    assert app.session_state['run'].extraction.gaps


def test_switching_demo_mode_clears_previous_result():
    app = AppTest.from_file(Path(__file__).resolve().parent.parent/'app.py').run(timeout=20)
    next(x for x in app.button if x.label == 'Mở case').click().run()
    assert app.session_state['run'].id.startswith('curated-real-')
    app.radio[0].set_value('Demo offline — synthetic').run()
    assert 'run' not in app.session_state

def test_replay_ui_and_review():
    app=AppTest.from_file(Path(__file__).resolve().parent.parent/'app.py').run(timeout=20)
    assert not app.exception
    app.radio[0].set_value('Demo offline — synthetic').run()
    app.button[0].click().run()
    assert not app.exception
    assert app.metric[0].value=='Giả lập'
    assert app.metric[2].value=='Tiếp tục'
    assert any('Câu trả lời sơ bộ' in x.value for x in app.subheader)
    next(x for x in app.text_input if x.label=='Người review').set_value('Offline test reviewer')
    next(x for x in app.text_area if x.label=='Lý do (bắt buộc)').set_value('Need more evidence before proceeding.')
    next(x for x in app.selectbox if x.label=='Quyết định').select('Tạm giữ')
    next(x for x in app.button if x.label=='Lưu review').click().run()
    assert not app.exception
    assert app.session_state['run'].review.decision=='Tạm giữ'
    assert app.session_state['run'].recommendation=='Tiếp tục'


def test_live_ui_disabled_by_default(monkeypatch):
    monkeypatch.setattr('gmi.config.load_local_env', lambda: None)
    monkeypatch.delenv('GMI_LIVE_ENABLED',raising=False)
    app=AppTest.from_file(Path(__file__).resolve().parent.parent/'app.py').run()
    app.radio[0].set_value('Nghiên cứu Gemini').run()
    assert not app.exception
    assert app.button[0].disabled


def test_live_ui_requires_access_code(monkeypatch):
    monkeypatch.setattr('gmi.config.load_local_env', lambda: None)
    settings = {
        'GMI_LIVE_ENABLED': '1', 'GMI_KEY_AUTHORIZED': '1',
        'GMI_BUDGET_NOTE': 'One browser session, at most two attempts',
        'GEMINI_MODEL': 'mock-model', 'GEMINI_API_KEY': 'mock-key',
        'GMI_LIVE_ACCESS_CODE': 'a-long-test-access-code',
    }
    for key, value in settings.items():
        monkeypatch.setenv(key, value)
    app = AppTest.from_file(Path(__file__).resolve().parent.parent/'app.py').run()
    app.radio[0].set_value('Nghiên cứu Gemini').run()
    assert next(x for x in app.button if x.label == 'Nghiên cứu').disabled
    next(x for x in app.text_input if x.label == 'Mã truy cập Gemini').set_value('wrong-code')
    next(x for x in app.button if x.label == 'Mở Gemini').click().run()
    assert next(x for x in app.button if x.label == 'Nghiên cứu').disabled
    next(x for x in app.text_input if x.label == 'Mã truy cập Gemini').set_value(settings['GMI_LIVE_ACCESS_CODE'])
    next(x for x in app.button if x.label == 'Mở Gemini').click().run()
    assert not app.exception
    assert not next(x for x in app.button if x.label == 'Nghiên cứu').disabled


def test_live_ui_rejects_subject_mismatch_before_provider(monkeypatch):
    monkeypatch.setattr('gmi.config.load_local_env', lambda: None)
    for key, value in {
        'GMI_LIVE_ENABLED': '1', 'GMI_KEY_AUTHORIZED': '1',
        'GMI_BUDGET_NOTE': 'Mock-only scope check', 'GEMINI_MODEL': 'mock-model',
        'GEMINI_API_KEY': 'mock-key', 'GMI_LIVE_ACCESS_CODE': 'a-long-test-access-code',
    }.items():
        monkeypatch.setenv(key, value)
    app = AppTest.from_file(Path(__file__).resolve().parent.parent/'app.py').run()
    app.radio[0].set_value('Nghiên cứu Gemini').run()
    next(x for x in app.text_input if x.label == 'Mã truy cập Gemini').set_value('a-long-test-access-code')
    next(x for x in app.button if x.label == 'Mở Gemini').click().run()
    monkeypatch.setattr('gmi.gemini.GeminiProvider', lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError('Gemini must not run')))
    next(x for x in app.text_area if x.label == 'Câu hỏi nghiên cứu').set_value('Liên Quân Mobile có phải 1 game thành công')
    next(x for x in app.text_input if x.label == 'Đối tượng nghiên cứu').set_value('MOBA')
    next(x for x in app.text_input if x.label == 'Kỳ đo').set_value('Q1 2025')
    next(x for x in app.button if x.label == 'Nghiên cứu').click().run()
    assert not app.exception
    assert any('Đối tượng nghiên cứu phải xuất hiện' in error.value for error in app.error)
    assert 'run' not in app.session_state


def test_reviewer_can_reject_semantically_false_claim_in_ui():
    app=AppTest.from_file(Path(__file__).resolve().parent.parent/'app.py').run(timeout=20)
    app.radio[0].set_value('Demo offline — synthetic').run()
    next(x for x in app.selectbox if x.label=='Tình huống').select('semantic_failure')
    next(x for x in app.button if x.label=='Chạy tình huống').click().run()
    assert app.session_state['run'].extraction.findings
    next(x for x in app.text_input if x.key=='claim_reviewer_C1').set_value('Reviewer')
    next(x for x in app.selectbox if x.key=='claim_verdict_C1').select('unsupported')
    next(x for x in app.text_area if x.key=='claim_reason_C1').set_value('Quote negates the positive demand claim.')
    next(x for x in app.button if x.key=='FormSubmitter:claim_review_C1-Lưu đánh giá claim').click().run()
    run=app.session_state['run']
    assert not run.extraction.findings
    assert run.extraction.claims[0].status=='rejected'
    assert run.claim_reviews[-1].verdict=='unsupported'


def test_research_reviewer_can_publish_narrow_answer_with_checked_source():
    app = AppTest.from_file(Path(__file__).resolve().parent.parent/'app.py').run(timeout=20)
    app.radio[0].set_value('Demo offline — synthetic').run()
    next(x for x in app.selectbox if x.label == 'Tình huống').select('other_game')
    next(x for x in app.button if x.label == 'Chạy tình huống').click().run()
    next(x for x in app.text_input if x.key == 'claim_reviewer_C1').set_value('Fixture reviewer')
    next(x for x in app.selectbox if x.key == 'claim_verdict_C1').select('supported')
    next(x for x in app.text_area if x.key == 'claim_reason_C1').set_value('The synthetic quote supports this narrow claim.')
    next(x for x in app.button if x.key == 'FormSubmitter:claim_review_C1-Lưu đánh giá claim').click().run()
    next(x for x in app.text_input if x.label == 'Người review').set_value('Fixture reviewer')
    next(x for x in app.text_area if x.label == 'Nhận định cuối của người review').set_value('Synthetic China demand signal only; real demand remains untested.')
    next(x for x in app.selectbox if x.label == 'Mức căn cứ của nhận định cuối').select('Có claim đã duyệt')
    next(x for x in app.multiselect if x.label == 'Claim hỗ trợ nhận định cuối').set_value(['C1'])
    next(x for x in app.text_area if x.label == 'Lý do (bắt buộc)').set_value('Keep the conclusion limited to the reviewed synthetic claim.')
    next(x for x in app.button if x.label == 'Lưu review').click().run()
    assert not app.exception
    assert app.session_state['run'].review.answer_claim_ids == ['C1']
    assert any('Nhận định đã review' in x.value for x in app.subheader)


def test_reviewer_can_narrow_claim_in_ui_before_final_answer():
    app = AppTest.from_file(Path(__file__).resolve().parent.parent/'app.py').run(timeout=20)
    app.radio[0].set_value('Demo offline — synthetic').run()
    next(x for x in app.selectbox if x.label == 'Tình huống').select('other_game')
    next(x for x in app.button if x.label == 'Chạy tình huống').click().run()
    revised = 'Fictional Game Beta has a positive demand signal in the China concept study for Q1 2025.'
    next(x for x in app.text_input if x.key == 'claim_reviewer_C1').set_value('Fixture reviewer')
    next(x for x in app.selectbox if x.key == 'claim_verdict_C1').select('supported')
    next(x for x in app.text_area if x.key == 'claim_corrected_text_C1').set_value(revised)
    next(x for x in app.text_input if x.key == 'claim_corrected_metric_C1').set_value('concept-study demand signal')
    next(x for x in app.text_area if x.key == 'claim_reason_C1').set_value('Narrowed the statement to what the quote supports.')
    next(x for x in app.button if x.key == 'FormSubmitter:claim_review_C1-Lưu đánh giá claim').click().run()
    assert not app.exception
    run = app.session_state['run']
    assert run.extraction.claims[0].text == revised
    assert run.extraction.claims[0].status == 'human_verified'
    assert not run.extraction.findings
    assert run.proposed_extraction.claims[0].text != revised


def test_cloud_hot_update_recovers_stale_imported_modules():
    # Isolate the simulated old process so reloaded Pydantic classes do not
    # affect other tests holding module-level class references.
    code = '''
import inspect
import gmi.models as models
import gmi.scope_input as scope_input
class OldScope:
    model_fields = {}
models.Scope = OldScope
scope_input.scope_input_errors = lambda question, subject, period, bounded, start, end, cutoff, strict: []
from streamlit.testing.v1 import AppTest
app = AppTest.from_file('app.py').run(timeout=20)
assert not app.exception
assert 'criteria' in models.Scope.model_fields
assert 'criteria' in inspect.signature(scope_input.scope_input_errors).parameters
'''
    project = Path(__file__).resolve().parent.parent
    result = subprocess.run([sys.executable, '-c', code], cwd=project,
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
