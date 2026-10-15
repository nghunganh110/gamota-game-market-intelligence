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
