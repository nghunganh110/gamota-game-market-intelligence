"""Streamlit presentation and reviewer actions for a research run."""

from collections import Counter
import streamlit as st

from .models import Run, Review, SourceReview, ClaimReview
from .validation import apply_review, revise_source, apply_claim_review
from .export import brief_markdown, result_summary

STATUS_LABELS = {'completed': 'Đã xử lý', 'partial': 'Một phần', 'failed': 'Chưa xử lý được',
                 'mechanically_checked': 'Qua kiểm tra cơ học', 'human_verified': 'Đã xác nhận',
                 'rejected': 'Bị loại', 'ai_extracted': 'AI đề xuất'}
EVIDENCE_LABELS = {'live': 'Gemini live', 'replay': 'Ví dụ đã lưu', 'synthetic': 'Giả lập'}


def render_result(run: Run) -> None:
    st.divider()
    st.subheader(run.scope.question)
    if run.id.startswith('curated-real-'):
        st.info('Case này được biên tập từ snapshot của lượt live để dễ xem trên demo. Chỉ có đoạn nguồn ngắn; mở trang gốc để kiểm tra. Bản mẫu ban đầu chưa có human review.')
        st.caption('Đọc nhận định → kiểm tra claim và trang gốc → xem điều chưa biết → người phụ trách review.')
    a,b,c = st.columns(3)
    a.metric('Chế độ evidence', EVIDENCE_LABELS.get(run.evidence_mode, run.evidence_mode))
    b.metric('Trạng thái ví dụ' if run.id.startswith('curated-real-') else 'Trạng thái pipeline',
             STATUS_LABELS.get(run.status, run.status))
    c.metric('Khuyến nghị AI',run.recommendation or 'Chỉ nghiên cứu')
    bounds = (f'{run.scope.period_start}–{run.scope.period_end}' if run.scope.period_start else 'theo nhãn kỳ đo')
    st.caption(f'{run.scope.subject} · {run.scope.market} · {run.scope.period} ({bounds}) · Cutoff {run.scope.cutoff}')
    if run.scope.criteria:
        st.caption(f'Tiêu chí đánh giá: {run.scope.criteria}')
    st.caption('Pipeline chỉ kiểm tra thu thập và trích dẫn cơ học; kết luận chỉ được xác nhận sau review ngữ nghĩa.')
    if run.id.startswith('curated-real-'):
        st.caption('Trạng thái này chỉ áp dụng cho bản ví dụ đã biên tập; run Gemini gốc có thể có trạng thái khác.')
    summary = result_summary(run)
    with st.container(border=True):
        st.subheader('Nhận định đã review' if summary['reviewed'] else 'Câu trả lời sơ bộ từ AI')
        st.write(summary['answer'])
        if summary['reviewed']:
            st.caption('Mức căn cứ do người review chọn: ' + ('có claim đã duyệt' if summary['answer_basis'] == 'supported' else 'chưa đủ căn cứ'))
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
    if run.extraction.gaps:
        st.markdown('**Điều chưa biết trước khi quyết định**')
        for gap in run.extraction.gaps:
            st.write(f'• {gap.missing} — {gap.impact}')
    st.caption('Xem claim và đoạn trích, so chất lượng nguồn, rồi mới lưu nhận định của người review.')
    claim_tab, source_tab, review_tab, detail_tab = st.tabs(['Claim & đoạn trích', 'Nguồn & độ tin cậy', 'Người review quyết định', 'Giới hạn & kỹ thuật'])
    with claim_tab:
        st.warning('Đoạn trích khớp nguồn chỉ xác nhận khả năng truy vết. Người review cần kiểm tra claim có diễn giải đúng đoạn trích.')
        st.subheader('Claim và đoạn trích')
        if not run.extraction.claims:
            st.info('Chưa có claim để kiểm tra trong lượt này. Xem tab Giới hạn & kỹ thuật để biết nguyên nhân.')
        issue_counts = Counter(issue for claim in run.extraction.claims for issue in claim.issues)
        if issue_counts:
            st.write('Lý do claim chưa được dùng làm bằng chứng:')
            st.dataframe([{'Lý do': issue, 'Số claim': count} for issue, count in issue_counts.items()], hide_index=True)
        sources = {s.id:s for s in run.sources}
        for claim in run.extraction.claims:
            with st.expander(f'{claim.id} · {STATUS_LABELS.get(claim.status, claim.status)} · {claim.text}'):
                original = next((item for item in run.proposed_extraction.claims if item.id == claim.id), None) if run.proposed_extraction else None
                if original and (original.text != claim.text or original.metric != claim.metric):
                    st.caption(f'Claim ban đầu trong run: {original.text} · Chỉ số: {original.metric}')
                st.write(f'Loại: {claim.kind} · {claim.market} · {claim.period} · Chỉ số: {claim.metric}')
                st.write(f'**Đoạn trích:** {claim.quote}')
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
                    verdict = st.selectbox('Đoạn trích có hỗ trợ claim sau khi chỉnh?', ['unclear', 'supported', 'unsupported'], key=f'claim_verdict_{claim.id}')
                    corrected_text = st.text_area('Câu claim sau khi chỉnh (chỉ giữ điều quote hỗ trợ)', value=claim.text, key=f'claim_corrected_text_{claim.id}')
                    corrected_metric = st.text_input('Chỉ số sau khi chỉnh', value=claim.metric, key=f'claim_corrected_metric_{claim.id}')
                    claim_reason = st.text_area('Lý do đánh giá', key=f'claim_reason_{claim.id}')
                    claim_submit = st.form_submit_button('Lưu đánh giá claim')
                if claim_submit:
                    try:
                        st.session_state.run = apply_claim_review(run, ClaimReview(claim_id=claim.id, reviewer=reviewer_name, verdict=verdict, reason=claim_reason,
                                                                                   corrected_text=corrected_text.strip() if verdict == 'supported' else None,
                                                                                   corrected_metric=corrected_metric.strip() if verdict == 'supported' else None))
                        st.rerun()
                    except Exception:
                        st.error('Cần tên, lý do và claim/chỉ số hợp lệ; không thể duyệt claim đã bị kiểm tra cơ học loại.')
    with source_tab:
        st.caption('Chất lượng nguồn và độ phù hợp với câu hỏi là hai đánh giá riêng.')
        st.subheader(f'Nguồn đã thu ({len(run.sources)})')
        if not run.sources:
            st.info('Chưa có nguồn nào đọc được trong lượt này.')
        for source in run.sources:
            with st.container(border=True):
                st.write(f'**{source.id} · {source.title}** — {source.read_status}')
                if source.url.startswith(('https://', 'http://')):
                    st.link_button(f'Mở {source.id}', source.url)
                st.write(f'Chất lượng: {source.quality}')
                st.write(f'Độ phù hợp: {source.relevance} — {source.relevance_reason}')
                st.caption(f'Ngày công bố: {source.published or "chưa rõ"} · Lỗi đọc: {source.error or "không có"}')
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
    with review_tab:
        st.write('1. Kiểm tra claim với trang gốc. 2. Ghi nhận claim được nguồn hỗ trợ. 3. Viết nhận định cuối và lý do.')
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
    with detail_tab:
        if run.errors:
            for error, count in Counter(run.errors).items():
                st.error(error + (f' (×{count})' if count > 1 else ''))
        if run.scope.mode == 'screening':
            st.dataframe([{'Chiều':d.name,'Trạng thái':d.state,'Claim':', '.join(d.claim_ids),'Lý do':d.reason} for d in run.extraction.dimensions], hide_index=True)
        st.subheader('Mâu thuẫn và điều chưa biết')
        for x in run.extraction.conflicts:
            st.write(f'{x.relation} [{", ".join(x.claim_ids)}]: {x.explanation}')
            st.write('Bước phân xử:',x.next_action)
        for g in run.extraction.gaps:
            st.write(f'**{g.missing}** — {g.impact}')
            st.write(f'{g.action} · Người review: {g.owner} · Xem lại: {g.revisit}')
        # Full snapshots stay local; download is for reviewer use, never automatically published.
        st.download_button('Tải run JSON (gồm snapshot nguồn)',run.model_dump_json(indent=2),file_name=f'{run.id}.json',mime='application/json')
        st.download_button('Tải brief Markdown',brief_markdown(run),file_name=f'{run.id}.md',mime='text/markdown')
        with st.expander('Thông tin lần chạy'):
            st.json(run.usage)
