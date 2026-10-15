from pathlib import Path
from streamlit.testing.v1 import AppTest

def test_replay_ui_and_review():
    app=AppTest.from_file(Path(__file__).resolve().parent.parent/'app.py').run(timeout=20)
    assert not app.exception
    app.button[0].click().run()
    assert not app.exception
    assert app.metric[0].value=='synthetic'
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
