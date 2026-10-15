from datetime import date
from collections import Counter
import hashlib
import hmac
import importlib
import inspect
import json
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
                or 'criteria' not in inspect.signature(_scope_module.scope_input_errors).parameters
                or 'source_urls' not in inspect.signature(_pipeline_module.run_research).parameters)
if _old_mvp_api or (_loaded_version is not None and _loaded_version != _runtime_version):
    for _name in ('gmi.models', 'gmi.scope_input', 'gmi.source_input',
                  'gmi.reader', 'gmi.validation', 'gmi.replay',
                  'gmi.gemini', 'gmi.pipeline', 'gmi.export'):
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

from gmi.models import Run, Scope, Review, SourceReview, ClaimReview
from gmi.replay import replay
from gmi.gemini import LivePolicy, GeminiProvider
from gmi.reader import DocumentReader
from gmi.pipeline import run_research
from gmi.validation import apply_review, revise_source, apply_claim_review
from gmi.export import brief_markdown, result_summary
from gmi.config import load_local_env
from gmi.scope_input import scope_input_errors, scope_bounds
from gmi.source_input import parse_source_urls

load_local_env()

st.title('Game Market Intelligence')
st.caption('Từ câu hỏi đến bằng chứng có thể kiểm tra. Người phụ trách quyết định cuối.')
if st.session_state.pop('_run_cleared_for_update', False):
    st.info('Ứng dụng vừa cập nhật mã nguồn. Run trong bộ nhớ phiên cũ đã được xóa; mở lại từ JSON đã tải nếu cần tiếp tục review.')
labels = {'good':'Tín hiệu đủ cho sàng lọc', 'conflict':'Hai nguồn mâu thuẫn', 'missing':'Thiếu D30 retention', 'semantic_failure':'Giới hạn: diễn giải sai đoạn trích', 'other_game':'Game khác, thị trường khác'}
mode = st.radio('Cách chạy', ['Demo offline — synthetic', 'Nghiên cứu Gemini', 'Mở run đã lưu'], horizontal=True)
if mode.startswith('Demo'):
    st.info('Dữ liệu dưới đây được tạo để kiểm thử phần mềm. Không phải dữ kiện thị trường hay kết quả Gemini.')
    case = st.selectbox('Tình huống', list(labels), format_func=labels.get)
    if st.button('Chạy tình huống', type='primary'):
        st.session_state.run = replay(case)
elif mode == 'Mở run đã lưu':
    st.caption('Tải lại JSON đã xuất từ app để tiếp tục kiểm tra nguồn và claim; thao tác này không gọi Gemini.')
    saved_run = st.file_uploader('Run JSON', type='json')
    if st.button('Mở run'):
        if not saved_run:
            st.error('Chọn một file run JSON trước.')
        elif saved_run.size > 5_000_000:
            st.error('File vượt giới hạn 5 MB.')
        else:
            try:
                st.session_state.run = Run.model_validate_json(saved_run.getvalue())
                st.rerun()
            except Exception:
                st.error('Run JSON không đúng định dạng của ứng dụng.')
else:
    access_code = os.environ.get('GMI_LIVE_ACCESS_CODE', '')
    ready = os.environ.get('GMI_LIVE_ENABLED') == '1' and os.environ.get('GMI_KEY_AUTHORIZED') == '1' and bool(os.environ.get('GMI_BUDGET_NOTE', '').strip()) and bool(os.environ.get('GEMINI_MODEL', '').strip()) and bool(os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')) and len(access_code) >= 12
    access_fingerprint = hashlib.sha256(access_code.encode()).hexdigest()
    live_unlocked = st.session_state.get('live_unlocked_for') == access_fingerprint
    if not ready:
        st.warning('Live chưa sẵn sàng: cần key, model, giới hạn sử dụng và mã truy cập riêng dài ít nhất 12 ký tự trong cấu hình server. Không nhập API key vào giao diện.')
    elif not live_unlocked:
        st.info('Chế độ Gemini dùng API key của chủ app. Nhập mã truy cập được cấp riêng để mở trong phiên này.')
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
        source_method = st.radio('Cách lấy nguồn', ['Gemini tìm nguồn', 'Tôi cung cấp URL nguồn'], horizontal=True)
        source_text = st.text_area('URL nguồn công khai (mỗi dòng một URL, tối đa 6)', placeholder='https://example.org/report',
                                   help='Dùng khi đã biết bài báo hoặc báo cáo cần kiểm tra. Chỉ gọi Gemini để trích xuất sau khi đọc được ít nhất một nguồn.') if source_method == 'Tôi cung cấp URL nguồn' else ''
        subject = st.text_input('Đối tượng nghiên cứu', help='Nhập đúng tên game hoặc thể loại xuất hiện trong câu hỏi. Nếu hỏi Liên Quân Mobile, không nhập MOBA.')
        market = st.text_input('Thị trường', value='Vietnam')
        period = st.text_input('Kỳ đo', placeholder='Q1 2025, launch window…')
        st.caption('Q1–Q4 YYYY được tự đổi thành ngày đầu/cuối quý để nhận cả dữ kiện trong kỳ con.')
        bounded_period = st.checkbox('Tự nhập khoảng ngày đo (chỉ dùng khi ô này được chọn)', value=False)
        period_start = st.date_input('Bắt đầu kỳ đo') if bounded_period else None
        period_end = st.date_input('Kết thúc kỳ đo') if bounded_period else None
        cutoff = st.date_input('Ngày cutoff', value=date.today())
        kind = st.selectbox('Mục đích', ['research','screening'])
        blocker_definition = st.text_area('Hard blocker xác định trước (nếu Screening)', placeholder='Ví dụ: chủ quyền xác nhận territory không khả dụng')
        strict = st.checkbox('Chỉ dùng evidence xác định được trước cutoff', value=True, help='Cutoff cũ hơn hôm nay cần snapshot lịch sử; reader live chưa tự lấy archive.')
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
                source_urls = parse_source_urls(source_text) if source_method == 'Tôi cung cấp URL nguồn' else None
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
                st.error(f'Không thể chạy ({type(exc).__name__}). Kiểm tra scope/cấu hình server; không có kết quả thay thế.')

run = st.session_state.get('run')
if run:
    st.subheader(run.scope.question)
    a,b,c = st.columns(3)
    a.metric('Chế độ evidence',run.evidence_mode)
    b.metric('Trạng thái pipeline',run.status)
    c.metric('Khuyến nghị AI',run.recommendation or 'Research only')
    bounds = (f'{run.scope.period_start}–{run.scope.period_end}' if run.scope.period_start else 'theo nhãn kỳ đo')
    st.caption(f'{run.scope.subject} · {run.scope.market} · {run.scope.period} ({bounds}) · Cutoff {run.scope.cutoff} · Strict {run.scope.strict_cutoff}')
    if run.scope.criteria:
        st.caption(f'Tiêu chí đánh giá: {run.scope.criteria}')
    st.caption('Trạng thái pipeline chỉ phản ánh thu thập và kiểm tra cơ học; nhận định chỉ được xác nhận sau review ngữ nghĩa.')
    summary = result_summary(run)
    with st.container(border=True):
        st.subheader('Nhận định đã review' if summary['reviewed'] else 'Câu trả lời sơ bộ từ AI')
        st.write(summary['answer'])
        if summary['reviewed']:
            st.caption('Mức căn cứ do người review chọn: ' + ('có claim đã duyệt' if summary['answer_basis'] == 'supported' else 'chưa đủ căn cứ'))
        if not summary['reviewed']:
            for finding in summary['findings'][1:]:
                st.write(finding.text)
        st.caption('Claim hỗ trợ: ' + (', '.join(summary['claim_ids']) or 'chưa có'))
        for claim_id in summary['claim_ids']:
            claim = next((item for item in run.extraction.claims if item.id == claim_id), None)
            source = next((item for item in run.sources if claim and item.id == claim.source_id), None)
            if claim and source:
                st.write(f'{claim_id}: {claim.text} — {source.title}')
                if source.url.startswith(('https://', 'http://')):
                    st.link_button(f'Mở nguồn của {claim_id}', source.url)
        if run.scope.mode == 'screening':
            st.write(f'Đề xuất sàng lọc: **{run.recommendation or "chưa có"}**')
        if not summary['reviewed']:
            st.write(f'Bước kiểm chứng tiếp (AI đề xuất): {summary["next_action"]}')
        if not summary['reviewed']:
            st.info('Kết luận sơ bộ; người phụ trách chưa xác nhận. Mở từng claim bên dưới để kiểm tra nguồn và ý nghĩa.')
    st.warning('Đoạn trích khớp nguồn chỉ xác nhận khả năng truy vết. Cần kiểm tra claim có diễn giải đúng đoạn trích trước khi quyết định.')
    if run.errors:
        for error, count in Counter(run.errors).items():
            st.error(error + (f' (×{count})' if count > 1 else ''))
    if run.scope.mode == 'screening':
        st.dataframe([{'Chiều':d.name,'Trạng thái':d.state,'Claim':', '.join(d.claim_ids),'Lý do':d.reason} for d in run.extraction.dimensions], hide_index=True)
    with st.expander(f'Nguồn đã thu ({len(run.sources)})'):
        for source in run.sources:
            st.write(f'**{source.id} · {source.title}** — {source.read_status}')
            if source.url.startswith(('https://', 'http://')):
                st.link_button(f'Mở {source.id}', source.url)
            st.write(f'Chất lượng: {source.quality}')
            st.write(f'Độ phù hợp: {source.relevance} — {source.relevance_reason}')
            st.caption(f'Ngày công bố: {source.published or "chưa rõ"} · Lỗi đọc: {source.error or "không có"}')
    st.subheader('Kiểm tra claim và nguồn')
    issue_counts = Counter(issue for claim in run.extraction.claims for issue in claim.issues)
    if issue_counts:
        st.write('Lý do claim chưa được dùng làm bằng chứng:')
        st.dataframe([{'Lý do': issue, 'Số claim': count} for issue, count in issue_counts.items()], hide_index=True)
    sources = {s.id:s for s in run.sources}
    for claim in run.extraction.claims:
        with st.expander(f'{claim.id} · {claim.status} · {claim.text}'):
            st.write(f'Loại: {claim.kind} · {claim.market} · {claim.period} · Chỉ số: {claim.metric}')
            st.text(claim.quote)
            s = sources.get(claim.source_id)
            if s:
                if s.url.startswith(('https://','http://')):
                    st.link_button('Mở nguồn',s.url)
                st.write(f'Chất lượng: {s.quality}')
                st.write(f'Độ phù hợp: {s.relevance} — {s.relevance_reason}')
                st.write(f'Ngày công bố: {s.published or "Unknown"} · Duplicate: {s.origin_id or "None detected"}')
            st.write('Giới hạn:',claim.limitations)
            for issue in claim.issues:
                st.error(issue)
            latest = next((x for x in reversed(run.claim_reviews) if x.claim_id == claim.id), None)
            if latest:
                st.write(f'Review gần nhất: {latest.verdict} — {latest.reason} ({latest.reviewer})')
            with st.form(f'claim_review_{claim.id}'):
                reviewer_name = st.text_input('Người kiểm tra claim', key=f'claim_reviewer_{claim.id}')
                verdict = st.selectbox('Đoạn trích có hỗ trợ claim?', ['unclear', 'supported', 'unsupported'], key=f'claim_verdict_{claim.id}')
                claim_reason = st.text_area('Lý do đánh giá', key=f'claim_reason_{claim.id}')
                claim_submit = st.form_submit_button('Lưu đánh giá claim')
            if claim_submit:
                try:
                    st.session_state.run = apply_claim_review(run, ClaimReview(claim_id=claim.id, reviewer=reviewer_name, verdict=verdict, reason=claim_reason))
                    st.rerun()
                except Exception:
                    st.error('Cần tên và lý do ít nhất 10 ký tự; không thể duyệt claim đã bị kiểm tra cơ học loại.')
    with st.expander('Sửa đánh giá chất lượng/độ phù hợp nguồn'):
        if run.sources:
            with st.form('source_review'):
                source_id = st.selectbox('Nguồn cần sửa', list(sources))
                source_reviewer = st.text_input('Người kiểm tra nguồn')
                quality = st.text_area('Đánh giá chất lượng mới (publisher, phương pháp, độc lập, giới hạn)')
                relevance = st.selectbox('Độ phù hợp mới', ['direct','indirect','unsuitable'])
                relevance_reason = st.text_area('Lý do sửa đánh giá nguồn')
                source_submit = st.form_submit_button('Lưu đánh giá và tính lại')
            if source_submit:
                try:
                    st.session_state.run = revise_source(run,SourceReview(source_id=source_id,reviewer=source_reviewer,quality=quality,relevance=relevance,reason=relevance_reason))
                    st.rerun()
                except Exception:
                    st.error('Cần tên người kiểm tra, chất lượng và lý do ít nhất 10 ký tự. Sau thay đổi, cần review quyết định lại.')
    st.subheader('Mâu thuẫn và điều chưa biết')
    for x in run.extraction.conflicts:
        st.write(f'{x.relation} [{", ".join(x.claim_ids)}]: {x.explanation}')
        st.write('Bước phân xử:',x.next_action)
    for g in run.extraction.gaps:
        st.write(f'**{g.missing}** — {g.impact}')
        st.write(f'{g.action} · Người review: {g.owner} · Xem lại: {g.revisit}')
    with st.expander('Người phụ trách review và quyết định'):
        eligible = [c.id for c in run.extraction.claims if c.status == 'human_verified']
        with st.form('review'):
            reviewer = st.text_input('Người review')
            verified = st.multiselect('Claim đã kiểm tra ngữ nghĩa',eligible)
            final_answer = st.text_area('Nhận định cuối của người review', help='Viết kết luận đúng phạm vi nguồn. Nếu thiếu evidence, nêu rõ không thể kết luận.')
            answer_basis_label = st.selectbox('Mức căn cứ của nhận định cuối', ['Chưa đủ căn cứ', 'Có claim đã duyệt'])
            answer_claim_ids = st.multiselect('Claim hỗ trợ nhận định cuối', eligible,
                                               help='Chỉ chọn claim đã được review Supported ở phía trên.')
            decision = st.selectbox('Quyết định', ['Tiếp tục','Tạm giữ','Dừng'] if run.scope.mode=='screening' else ['Reviewed research'])
            reason = st.text_area('Lý do (bắt buộc)')
            blocker = st.checkbox('Đã xác nhận blocker có bằng chứng')
            review_submit = st.form_submit_button('Lưu review')
        if review_submit:
            try:
                st.session_state.run = apply_review(run,Review(reviewer=reviewer,decision=decision,reason=reason,verified_claim_ids=verified,blocker_confirmed=blocker,
                                                                final_answer=final_answer,answer_claim_ids=answer_claim_ids,
                                                                answer_basis='supported' if answer_basis_label == 'Có claim đã duyệt' else 'insufficient'))
                st.rerun()
            except ValueError as exc:
                st.error(f'Review chưa hợp lệ: {exc}')
    if run.review:
        st.success(f'Quyết định người phụ trách: {run.review.decision} — {run.review.reason}')
    # Full snapshots stay local; download is for reviewer use, never automatically published.
    st.download_button('Tải run JSON (gồm snapshot nguồn)',run.model_dump_json(indent=2),file_name=f'{run.id}.json',mime='application/json')
    st.download_button('Tải brief Markdown',brief_markdown(run),file_name=f'{run.id}.md',mime='text/markdown')
    with st.expander('Thông tin lần chạy'):
        st.json(run.usage)
