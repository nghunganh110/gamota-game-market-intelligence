from datetime import date
import hashlib
import hmac
import json
import os
import streamlit as st
from gmi.models import Scope, Review, SourceReview, ClaimReview
from gmi.replay import replay
from gmi.gemini import LivePolicy, GeminiProvider
from gmi.reader import DocumentReader
from gmi.pipeline import run_research
from gmi.validation import apply_review, revise_source, apply_claim_review
from gmi.export import brief_markdown, result_summary
from gmi.config import load_local_env

load_local_env()

st.set_page_config(page_title='Gamota Market Intelligence', layout='wide')
st.title('Game Market Intelligence')
st.caption('Từ câu hỏi đến bằng chứng có thể kiểm tra. Người phụ trách quyết định cuối.')
labels = {'good':'Tín hiệu đủ cho sàng lọc', 'conflict':'Hai nguồn mâu thuẫn', 'missing':'Thiếu D30 retention', 'semantic_failure':'Giới hạn: diễn giải sai đoạn trích', 'other_game':'Game khác, thị trường khác'}
mode = st.radio('Cách chạy', ['Demo offline — synthetic', 'Nghiên cứu Gemini'], horizontal=True)
if mode.startswith('Demo'):
    st.info('Dữ liệu dưới đây được tạo để kiểm thử phần mềm. Không phải dữ kiện thị trường hay kết quả Gemini.')
    case = st.selectbox('Tình huống', list(labels), format_func=labels.get)
    if st.button('Chạy tình huống', type='primary'):
        st.session_state.run = replay(case)
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
        question = st.text_area('Câu hỏi nghiên cứu', placeholder='Bạn muốn kiểm chứng tín hiệu nào?')
        subject = st.text_input('Game hoặc thể loại')
        market = st.text_input('Thị trường', value='Vietnam')
        period = st.text_input('Kỳ đo', placeholder='Q1 2025, launch window…')
        bounded_period = st.checkbox('Xác định khoảng ngày đo để nhận cả kỳ con', value=False)
        period_start = st.date_input('Bắt đầu kỳ đo')
        period_end = st.date_input('Kết thúc kỳ đo')
        cutoff = st.date_input('Ngày cutoff', value=date.today())
        kind = st.selectbox('Mục đích', ['research','screening'])
        blocker_definition = st.text_area('Hard blocker xác định trước (nếu Screening)', placeholder='Ví dụ: chủ quyền xác nhận territory không khả dụng')
        strict = st.checkbox('Chỉ dùng evidence xác định được trước cutoff', value=True)
        submitted = st.form_submit_button('Nghiên cứu', disabled=not (ready and live_unlocked))
    if submitted and ready and live_unlocked:
        try:
            scope = Scope(question=question,subject=subject,market=market,period=period,cutoff=cutoff,mode=kind,strict_cutoff=strict,blocker_definition=blocker_definition,period_start=period_start if bounded_period else None,period_end=period_end if bounded_period else None)
            # This limit belongs to one browser session; use provider-side quota for an account-wide cap.
            if 'live_policy' not in st.session_state:
                st.session_state.live_policy = LivePolicy(enabled=True,authorized=True,budget_note=os.environ['GMI_BUDGET_NOTE'],max_calls=int(os.environ.get('GMI_MAX_CALLS','2')))
            provider = GeminiProvider(st.session_state.live_policy)
            with st.spinner('Tìm nguồn và đọc bằng chứng…'):
                st.session_state.run = run_research(scope,provider,DocumentReader())
        except Exception as exc:
            st.error(f'Không thể chạy ({type(exc).__name__}). Kiểm tra scope/cấu hình server; không có kết quả thay thế.')

run = st.session_state.get('run')
if run:
    st.subheader(run.scope.question)
    a,b,c = st.columns(3)
    a.metric('Chế độ evidence',run.evidence_mode)
    b.metric('Trạng thái xử lý',run.status)
    c.metric('Khuyến nghị AI',run.recommendation or 'Research only')
    st.caption(f'{run.scope.subject} · {run.scope.market} · {run.scope.period} · Cutoff {run.scope.cutoff}')
    summary = result_summary(run)
    with st.container(border=True):
        st.subheader('Câu trả lời sơ bộ từ AI')
        st.write(summary['answer'])
        for finding in summary['findings'][1:]:
            st.write(finding.text)
        st.caption('Claim hỗ trợ: ' + (', '.join(summary['claim_ids']) or 'chưa có'))
        if run.scope.mode == 'screening':
            st.write(f'Đề xuất sàng lọc: **{run.recommendation or "chưa có"}**')
        st.write(f'Bước kiểm chứng tiếp (AI đề xuất): {summary["next_action"]}')
        if not summary['reviewed']:
            st.info('Kết luận sơ bộ; người phụ trách chưa xác nhận. Mở từng claim bên dưới để kiểm tra nguồn và ý nghĩa.')
    st.warning('Đoạn trích khớp nguồn chỉ xác nhận khả năng truy vết. Cần kiểm tra claim có diễn giải đúng đoạn trích trước khi quyết định.')
    if run.errors:
        for error in run.errors:
            st.error(error)
    if run.scope.mode == 'screening':
        st.dataframe([{'Chiều':d.name,'Trạng thái':d.state,'Claim':', '.join(d.claim_ids),'Lý do':d.reason} for d in run.extraction.dimensions], hide_index=True)
    st.subheader('Kiểm tra claim và nguồn')
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
            decision = st.selectbox('Quyết định', ['Tiếp tục','Tạm giữ','Dừng'] if run.scope.mode=='screening' else ['Reviewed research'])
            reason = st.text_area('Lý do (bắt buộc)')
            blocker = st.checkbox('Đã xác nhận blocker có bằng chứng')
            review_submit = st.form_submit_button('Lưu review')
        if review_submit:
            try:
                st.session_state.run = apply_review(run,Review(reviewer=reviewer,decision=decision,reason=reason,verified_claim_ids=verified,blocker_confirmed=blocker))
                st.rerun()
            except Exception:
                st.error('Review chưa hợp lệ. Dừng cần blocker có bằng chứng và claim đã được người review kiểm tra; lý do cần ít nhất 10 ký tự.')
    if run.review:
        st.success(f'Quyết định người phụ trách: {run.review.decision} — {run.review.reason}')
    # Full snapshots stay local; download is for reviewer use, never automatically published.
    st.download_button('Tải run JSON (gồm snapshot nguồn)',run.model_dump_json(indent=2),file_name=f'{run.id}.json',mime='application/json')
    st.download_button('Tải brief Markdown',brief_markdown(run),file_name=f'{run.id}.md',mime='text/markdown')
    with st.expander('Thông tin lần chạy'):
        st.json(run.usage)
