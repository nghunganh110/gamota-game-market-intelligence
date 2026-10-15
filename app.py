from datetime import date
import hashlib
import hmac
import importlib
import inspect
import os
from pathlib import Path
import sys
import streamlit as st

st.set_page_config(page_title='Gamota Market Intelligence', layout='wide')

# Streamlit reruns app.py in an existing process. A Cloud pull can replace local
# modules while Python still has their old classes/functions in sys.modules.
import gmi as _gmi_package
_code_hash = hashlib.sha256()
for _path in sorted((Path(__file__).resolve().parent / 'gmi').glob('*.py')):
    _code_hash.update(_path.name.encode())
    _code_hash.update(_path.read_bytes())
_runtime_version = _code_hash.hexdigest()
_loaded_version = getattr(_gmi_package, '_runtime_version', None)
_models_module = importlib.import_module('gmi.models')
_scope_module = importlib.import_module('gmi.scope_input')
_pipeline_module = importlib.import_module('gmi.pipeline')
_old_mvp_api = ('criteria' not in _models_module.Scope.model_fields
                or 'answer_basis' not in _models_module.Review.model_fields
                or 'corrected_text' not in _models_module.ClaimReview.model_fields
                or 'criteria' not in inspect.signature(_scope_module.scope_input_errors).parameters
                or 'source_urls' not in inspect.signature(_pipeline_module.run_research).parameters)
if _old_mvp_api or (_loaded_version is not None and _loaded_version != _runtime_version):
    for _name in ('gmi.models', 'gmi.scope_input', 'gmi.source_input',
                  'gmi.reader', 'gmi.validation', 'gmi.replay',
                  'gmi.gemini', 'gmi.pipeline', 'gmi.export', 'gmi.ui_results'):
        if _name in sys.modules:
            importlib.reload(sys.modules[_name])
    _gmi_package._runtime_version = _runtime_version
if st.session_state.get('_runtime_version') != _runtime_version:
    _had_run = 'run' in st.session_state
    st.session_state.pop('run', None)
    st.session_state.pop('live_policy', None)
    st.session_state['_runtime_version'] = _runtime_version
    if _had_run:
        st.session_state['_run_cleared_for_update'] = True

from gmi.models import Run, Scope
from gmi.replay import replay
from gmi.gemini import LivePolicy, GeminiProvider
from gmi.reader import DocumentReader
from gmi.pipeline import run_research
from gmi.config import load_local_env
from gmi.scope_input import scope_input_errors, scope_bounds
from gmi.source_input import parse_source_urls

load_local_env()

st.title('Game Market Intelligence')
st.caption('Từ câu hỏi đến bằng chứng có thể kiểm tra. Người phụ trách quyết định cuối.')
st.write('**Cách xem:** mở một ví dụ → đọc câu trả lời sơ bộ → đối chiếu từng ý với đoạn trích và nguồn → xem thông tin còn thiếu. Người phụ trách đưa ra kết luận cuối.')
if st.session_state.pop('_run_cleared_for_update', False):
    st.info('Ứng dụng vừa cập nhật. Kết quả trong phiên cũ đã được xóa; có thể mở lại từ tệp JSON đã tải để tiếp tục kiểm chứng.')
labels = {'good':'Tín hiệu đủ cho sàng lọc', 'conflict':'Hai nguồn mâu thuẫn', 'missing':'Thiếu D30 retention', 'semantic_failure':'Giới hạn: diễn giải sai đoạn trích', 'other_game':'Game khác, thị trường khác'}
mode = st.radio('Cách sử dụng', ['Ví dụ từ nguồn thật', 'Tình huống mô phỏng', 'Nghiên cứu bằng Gemini', 'Mở kết quả đã lưu'], horizontal=True)
if st.session_state.get('_last_mode') not in (None, mode):
    st.session_state.pop('run', None)
st.session_state['_last_mode'] = mode
if mode == 'Tình huống mô phỏng':
    st.info('Dữ liệu trong mục này là giả định để kiểm thử phần mềm, không phải thông tin thị trường.')
    case = st.selectbox('Tình huống', list(labels), format_func=labels.get)
    if st.button('Chạy tình huống', type='primary'):
        st.session_state.run = replay(case)
elif mode == 'Ví dụ từ nguồn thật':
    st.info('Hai ví dụ rút gọn từ các lần nghiên cứu bằng Gemini đã lưu. Mở ví dụ không tốn lượt gọi Gemini; các ý rút ra từ nguồn chưa được người phụ trách xác nhận.')
    cases = {
        'A01': ('MABINOGI MOBILE · Hàn Quốc · tín hiệu ra mắt', 'a01.json'),
        'A02': ('Mobile MMORPG · Việt Nam · giới hạn dữ liệu', 'a02.json'),
    }
    selected = st.selectbox('Chọn ví dụ', list(cases), format_func=lambda key: cases[key][0])
    if st.button('Mở ví dụ', type='primary'):
        example_path = Path(__file__).resolve().parent / 'fixtures' / 'real_cases' / cases[selected][1]
        st.session_state.run = Run.model_validate_json(example_path.read_text())
elif mode == 'Mở kết quả đã lưu':
    st.caption('Tải tệp JSON đã xuất từ ứng dụng để tiếp tục đối chiếu nguồn và các ý rút ra; thao tác này không gọi Gemini.')
    saved_run = st.file_uploader('Tệp kết quả JSON', type='json')
    if st.button('Mở kết quả'):
        if not saved_run:
            st.error('Chọn một tệp JSON trước.')
        elif saved_run.size > 5_000_000:
            st.error('File vượt giới hạn 5 MB.')
        else:
            try:
                st.session_state.run = Run.model_validate_json(saved_run.getvalue())
                st.rerun()
            except Exception:
                st.error('Tệp JSON không đúng định dạng của ứng dụng.')
else:
    access_code = os.environ.get('GMI_LIVE_ACCESS_CODE', '')
    ready = os.environ.get('GMI_LIVE_ENABLED') == '1' and os.environ.get('GMI_KEY_AUTHORIZED') == '1' and bool(os.environ.get('GMI_BUDGET_NOTE', '').strip()) and bool(os.environ.get('GEMINI_MODEL', '').strip()) and bool(os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')) and len(access_code) >= 12
    access_fingerprint = hashlib.sha256(access_code.encode()).hexdigest()
    live_unlocked = st.session_state.get('live_unlocked_for') == access_fingerprint
    if not ready:
        st.warning('Nghiên cứu bằng Gemini chưa sẵn sàng: chủ ứng dụng cần cấu hình khóa API, mô hình, giới hạn sử dụng và mã truy cập. Không nhập khóa API vào giao diện.')
    elif not live_unlocked:
        st.info('Chế độ này dùng khóa API của chủ ứng dụng. Nhập mã truy cập được cấp riêng để mở trong phiên này.')
        with st.form('live_unlock'):
            entered_code = st.text_input('Mã truy cập Gemini', type='password')
            unlock = st.form_submit_button('Mở Gemini')
        if unlock:
            if hmac.compare_digest(entered_code, access_code):
                st.session_state.live_unlocked_for = access_fingerprint
                st.rerun()
            else:
                st.error('Mã truy cập không đúng.')
    with st.form('research'):
        question = st.text_area('Câu hỏi nghiên cứu', placeholder='Ví dụ: Liên Quân Mobile có thành công tại Việt Nam trong Q1 2025 xét theo người chơi và doanh thu?')
        st.caption('Nêu rõ tiêu chí “thành công” nếu muốn kết luận theo một chỉ số cụ thể.')
        criteria = st.text_input('Tiêu chí đánh giá (khi câu hỏi mang tính đánh giá)', placeholder='Ví dụ: quy mô người chơi và xu hướng doanh thu; không yêu cầu hạng 1')
        source_method = st.radio('Cách lấy nguồn', ['Gemini tìm nguồn', 'Tôi cung cấp đường dẫn nguồn'], horizontal=True)
        source_text = st.text_area('Đường dẫn bài viết hoặc báo cáo (mỗi dòng một đường dẫn, tối đa 6)', placeholder='https://example.org/report',
                                   help='Dùng khi đã biết bài báo hoặc báo cáo cần kiểm tra. Chỉ gọi Gemini để trích xuất sau khi đọc được ít nhất một nguồn.') if source_method == 'Tôi cung cấp đường dẫn nguồn' else ''
        subject = st.text_input('Đối tượng nghiên cứu', help='Nhập đúng tên game hoặc thể loại xuất hiện trong câu hỏi. Nếu hỏi Liên Quân Mobile, không nhập MOBA.')
        market = st.text_input('Thị trường', value='Vietnam')
        period = st.text_input('Kỳ đo', placeholder='Q1 2025, giai đoạn ra mắt…')
        st.caption('Q1–Q4 YYYY được tự đổi thành ngày đầu/cuối quý để nhận cả dữ kiện trong kỳ con.')
        cutoff = st.date_input('Ngày chốt thông tin', value=date.today(), help='Chỉ xem thông tin đã công bố trước hoặc vào ngày này.')
        with st.expander('Tùy chọn nâng cao: kỳ đo và sàng lọc'):
            bounded_period = st.checkbox('Tự nhập khoảng ngày đo (chỉ dùng khi ô này được chọn)', value=False)
            period_start = st.date_input('Bắt đầu kỳ đo') if bounded_period else None
            period_end = st.date_input('Kết thúc kỳ đo') if bounded_period else None
            kind = st.selectbox('Mục đích', ['research','screening'], format_func=lambda value: 'Nghiên cứu' if value == 'research' else 'Sàng lọc cơ hội')
            blocker_definition = st.text_area('Điều kiện loại trừ xác định trước (khi sàng lọc)', placeholder='Ví dụ: không có quyền phát hành tại thị trường này')
            strict = st.checkbox('Chỉ dùng thông tin có trước ngày chốt', value=True, help='Ngày chốt trong quá khứ cần bản lưu tài liệu tại thời điểm đó; ứng dụng chưa tự lấy bản lưu lịch sử.')
        submitted = st.form_submit_button('Nghiên cứu', disabled=not (ready and live_unlocked))
    if submitted and ready and live_unlocked:
        st.session_state.pop('run', None)
        errors = scope_input_errors(question, subject, period, bounded_period,
                                    period_start, period_end, cutoff, strict, criteria=criteria)
        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                start, end = scope_bounds(period, bounded_period, period_start, period_end)
                source_urls = parse_source_urls(source_text) if source_method == 'Tôi cung cấp đường dẫn nguồn' else None
                scope = Scope(question=question,criteria=criteria,subject=subject,market=market,period=period,cutoff=cutoff,mode=kind,strict_cutoff=strict,blocker_definition=blocker_definition,period_start=start,period_end=end)
                # This limit belongs to one browser session; use provider-side quota for an account-wide cap.
                if 'live_policy' not in st.session_state:
                    st.session_state.live_policy = LivePolicy(enabled=True,authorized=True,budget_note=os.environ['GMI_BUDGET_NOTE'],max_calls=int(os.environ.get('GMI_MAX_CALLS','2')))
                provider = GeminiProvider(st.session_state.live_policy)
                with st.spinner('Tìm nguồn và đọc bằng chứng…'):
                    st.session_state.run = run_research(scope,provider,DocumentReader(),source_urls=source_urls)
            except ValueError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f'Không thể hoàn thành nghiên cứu ({type(exc).__name__}). Kiểm tra phạm vi câu hỏi và cấu hình; ứng dụng không tự tạo kết quả thay thế.')

from gmi.ui_results import render_result

run = st.session_state.get('run')
if run:
    render_result(run)
