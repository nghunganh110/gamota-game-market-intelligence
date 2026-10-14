from pathlib import Path
from streamlit.testing.v1 import AppTest

def test_replay_ui_and_review():
    app=AppTest.from_file(Path(__file__).resolve().parent.parent/'app.py').run(timeout=20)
    assert not app.exception
    app.button[0].click().run()
    assert not app.exception
    assert app.metric[0].value=='synthetic'
    assert app.metric[2].value=='Tiếp tục'
    app.text_input[1].set_value('Offline test reviewer')
    app.text_area[2].set_value('Need more evidence before proceeding.')
    app.selectbox[3].select('Tạm giữ')
    app.button[2].click().run()
    assert not app.exception
    assert app.session_state['run'].review.decision=='Tạm giữ'
    assert app.session_state['run'].recommendation=='Tiếp tục'


def test_live_ui_disabled_by_default(monkeypatch):
    monkeypatch.delenv('GMI_LIVE_ENABLED',raising=False)
    app=AppTest.from_file(Path(__file__).resolve().parent.parent/'app.py').run()
    app.radio[0].set_value('Nghiên cứu Gemini').run()
    assert not app.exception
    assert app.button[0].disabled
