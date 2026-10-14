from datetime import date
import json
import os
import streamlit as st
from gmi.models import Scope, Review, SourceReview
from gmi.replay import replay
from gmi.gemini import LivePolicy, GeminiProvider
from gmi.reader import DocumentReader
from gmi.pipeline import run_research
from gmi.validation import apply_review, revise_source
from gmi.export import brief_markdown

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
    ready = os.environ.get('GMI_LIVE_ENABLED') == '1' and os.environ.get('GMI_KEY_AUTHORIZED') == '1' and bool(os.environ.get('GMI_BUDGET_NOTE')) and bool(os.environ.get('GEMINI_MODEL')) and bool(os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY'))
    if not ready:
        st.warning('Live chưa sẵn sàng: cần quyền dùng key, giới hạn sử dụng, model và cấu hình riêng trên máy. Không nhập key vào giao diện.')
    with st.form('research'):
        question = st.text_area('Câu hỏi nghiên cứu', placeholder='Bạn muốn kiểm chứng tín hiệu nào?')
        subject = st.text_input('Game hoặc thể loại')
        market = st.text_input('Thị trường', value='Vietnam')
        period = st.text_input('Kỳ đo', placeholder='Q1 2025, launch window…')
        cutoff = st.date_input('Ngày cutoff', value=date.today())
        kind = st.selectbox('Mục đích', ['research','screening'])
        blocker_definition = st.text_area('Hard blocker xác định trước (nếu Screening)', placeholder='Ví dụ: chủ quyền xác nhận territory không khả dụng')
        strict = st.checkbox('Chỉ dùng evidence xác định được trước cutoff', value=True)
        submitted = st.form_submit_button('Nghiên cứu', disabled=not ready)
    if submitted:
        try:
            scope = Scope(question=question,subject=subject,market=market,period=period,cutoff=cutoff,mode=kind,strict_cutoff=strict,blocker_definition=blocker_definition)
            # A session attempt limit survives Streamlit reruns; public demo must keep live disabled.
            if 'live_policy' not in st.session_state:
                st.session_state.live_policy = LivePolicy(enabled=True,authorized=True,budget_note=os.environ['GMI_BUDGET_NOTE'],max_calls=int(os.environ.get('GMI_MAX_CALLS','2')))
            provider = GeminiProvider(st.session_state.live_policy)
            with st.spinner('Tìm nguồn và đọc bằng chứng…'):
                st.session_state.run = run_research(scope,provider,DocumentReader())
        except Exception as exc:
            st.error(f'Không thể chạy ({type(exc).__name__}). Kiểm tra scope/cấu hình local; không có kết quả thay thế.')

run = st.session_state.get('run')
if run:
    st.subheader(run.scope.question)
    a,b,c = st.columns(3)
    a.metric('Chế độ evidence',run.evidence_mode)
    b.metric('Trạng thái xử lý',run.status)
    c.metric('Khuyến nghị AI',run.recommendation or 'Research only')
    st.caption(f'{run.scope.subject} · {run.scope.market} · {run.scope.period} · Cutoff {run.scope.cutoff}')
    st.warning('Đoạn trích khớp nguồn chỉ xác nhận khả năng truy vết. Cần kiểm tra claim có diễn giải đúng đoạn trích trước khi quyết định.')
    if run.errors:
        for error in run.errors:
            st.error(error)
    for f in run.extraction.findings:
        st.write(f'{f.text} — {", ".join(f.claim_ids)}' + (' · AI inference' if f.inference else ''))
    if not run.extraction.findings:
        st.info('Chưa có nhận định đủ cơ sở để trả lời câu hỏi.')
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
        eligible = [c.id for c in run.extraction.claims if c.status in {'mechanically_checked','human_verified'}]
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
