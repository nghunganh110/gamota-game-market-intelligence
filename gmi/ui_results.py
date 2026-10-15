"""Streamlit presentation and reviewer actions for a research run."""

from collections import Counter
import streamlit as st

from .models import Run, Review, SourceReview, ClaimReview
from .validation import apply_review, revise_source, apply_claim_review
from .export import brief_markdown, result_summary

STATUS_LABELS = {'completed': 'Đã xử lý', 'partial': 'Một phần', 'failed': 'Chưa xử lý được',
                 'mechanically_checked': 'Qua kiểm tra tự động', 'human_verified': 'Đã được xác nhận',
                 'rejected': 'Bị loại', 'ai_extracted': 'AI đề xuất'}
EVIDENCE_LABELS = {'live': 'Nghiên cứu mới', 'replay': 'Ví dụ đã lưu', 'synthetic': 'Dữ liệu mô phỏng'}
RELEVANCE_LABELS = {'direct': 'Phù hợp trực tiếp', 'indirect': 'Liên quan gián tiếp',
                    'unsuitable': 'Không phù hợp'}
KIND_LABELS = {'reported': 'Số liệu được công bố', 'estimate': 'Số liệu ước tính',
               'qualitative': 'Nhận xét định tính', 'observed': 'Quan sát được'}
VERDICT_LABELS = {'unclear': 'Chưa rõ', 'supported': 'Đoạn trích hỗ trợ ý này',
                  'unsupported': 'Đoạn trích không hỗ trợ ý này'}
ISSUE_LABELS = {
    'Source missing or unreadable': 'Không đọc được nguồn',
    'Quote absent from captured content': 'Không tìm thấy đoạn trích trong nội dung đã lưu',
    'Published after cutoff': 'Nguồn công bố sau ngày chốt thông tin',
    'Publication date unknown': 'Chưa rõ ngày công bố nguồn',
    'No snapshot proving content existed at historical cutoff': 'Không có bản lưu chứng minh nội dung đã tồn tại vào ngày chốt',
    'Subject mismatch': 'Không đúng game hoặc thể loại được hỏi',
    'Market mismatch; context only': 'Không đúng thị trường được hỏi',
    'Measurement bounds unknown; context only': 'Chưa rõ khoảng thời gian đo',
    'Period outside requested window; context only': 'Dữ liệu nằm ngoài kỳ đo được hỏi',
    'Period mismatch; context only': 'Không đúng kỳ đo được hỏi',
    'Source not directly relevant': 'Nguồn không trả lời trực tiếp câu hỏi',
}


def _issue_label(issue: str) -> str:
    if issue.startswith('Reviewer marked '):
        return 'Người kiểm chứng đã đánh giá: ' + issue.removeprefix('Reviewer marked ')
    return ISSUE_LABELS.get(issue, issue)


def render_result(run: Run) -> None:
    st.divider()
    st.subheader(run.scope.question)
    if run.id.startswith('curated-real-'):
        st.info('Ví dụ này được biên tập từ kết quả Gemini đã lưu. Chỉ có đoạn trích ngắn; hãy mở trang gốc để đối chiếu. Chưa có người phụ trách xác nhận nội dung.')
        st.caption('Đọc câu trả lời → đối chiếu từng ý với nguồn → xem điều chưa biết → người phụ trách kết luận.')
    a,b,c = st.columns(3)
    a.metric('Loại dữ liệu', EVIDENCE_LABELS.get(run.evidence_mode, run.evidence_mode))
    b.metric('Trạng thái ví dụ' if run.id.startswith('curated-real-') else 'Trạng thái xử lý',
             STATUS_LABELS.get(run.status, run.status))
    c.metric('Gợi ý của AI',run.recommendation or 'Chỉ nghiên cứu')
    bounds = (f'{run.scope.period_start}–{run.scope.period_end}' if run.scope.period_start else 'theo nhãn kỳ đo')
    st.caption(f'{run.scope.subject} · {run.scope.market} · {run.scope.period} ({bounds}) · Chốt thông tin {run.scope.cutoff}')
    if run.scope.criteria:
        st.caption(f'Tiêu chí đánh giá: {run.scope.criteria}')
    st.caption('Trạng thái xử lý chỉ nói ứng dụng đã thu thập và kiểm tra tự động đến đâu; người phụ trách vẫn cần đọc nguồn trước khi kết luận.')
    if run.id.startswith('curated-real-'):
        st.caption('Trạng thái này chỉ áp dụng cho ví dụ đã biên tập; lần nghiên cứu Gemini ban đầu có thể có trạng thái khác.')
    summary = result_summary(run)
    with st.container(border=True):
        st.subheader('Kết luận đã được người phụ trách kiểm chứng' if summary['reviewed'] else 'Câu trả lời sơ bộ từ AI')
        st.write(summary['answer'])
        if summary['reviewed']:
            st.caption('Mức căn cứ do người phụ trách chọn: ' + ('có thông tin đã đối chiếu với nguồn' if summary['answer_basis'] == 'supported' else 'chưa đủ căn cứ'))
        st.caption('Các ý làm căn cứ: ' + (', '.join(summary['claim_ids']) or 'chưa có'))
        for claim_id in summary['claim_ids']:
            claim = next((item for item in run.extraction.claims if item.id == claim_id), None)
            source = next((item for item in run.sources if claim and item.id == claim.source_id), None)
            if claim and source:
                st.write(f'Ý {claim_id}: {claim.text} — {source.title}')
                if source.url.startswith(('https://', 'http://')):
                    st.link_button(f'Mở nguồn của ý {claim_id}', source.url)
        if run.scope.mode == 'screening':
            st.write(f'Đề xuất sàng lọc: **{run.recommendation or "chưa có"}**')
        if not summary['reviewed']:
            st.write(f'Bước kiểm chứng tiếp (AI đề xuất): {summary["next_action"]}')
        if not summary['reviewed']:
            st.info('Đây là câu trả lời sơ bộ. Người phụ trách cần mở từng ý bên dưới, đọc đoạn trích và trang gốc trước khi sử dụng.')
    if run.extraction.gaps:
        st.markdown('**Điều chưa biết trước khi quyết định**')
        for gap in run.extraction.gaps:
            st.write(f'• {gap.missing} — {gap.impact}')
    st.caption('Các ý được rút ra từ nguồn có thể đúng, sai hoặc chưa đủ rõ. Hãy kiểm tra từng ý trước khi viết kết luận.')
    claim_tab, source_tab, review_tab, detail_tab = st.tabs(['Ý rút ra & đoạn trích', 'Nguồn & độ tin cậy', 'Người phụ trách kết luận', 'Điều chưa rõ & chi tiết'])
    with claim_tab:
        st.warning('Tìm thấy đoạn trích trong nguồn chưa chứng minh AI hiểu đúng đoạn đó. Cần đọc cả trang gốc trước khi xác nhận.')
        st.subheader('Các ý được rút ra từ nguồn')
        if not run.extraction.claims:
            st.info('Chưa có thông tin nào được rút ra để kiểm tra. Xem tab Điều chưa rõ & chi tiết để biết nguyên nhân.')
        issue_counts = Counter(issue for claim in run.extraction.claims for issue in claim.issues)
        if issue_counts:
            st.write('Lý do một số ý chưa được dùng làm căn cứ:')
            st.dataframe([{'Lý do': _issue_label(issue), 'Số ý': count} for issue, count in issue_counts.items()], hide_index=True)
        sources = {s.id:s for s in run.sources}
        for claim in run.extraction.claims:
            with st.expander(f'Ý {claim.id} · {STATUS_LABELS.get(claim.status, claim.status)} · {claim.text}'):
                original = next((item for item in run.proposed_extraction.claims if item.id == claim.id), None) if run.proposed_extraction else None
                if original and (original.text != claim.text or original.metric != claim.metric):
                    st.caption(f'Bản AI viết ban đầu: {original.text} · Chỉ số: {original.metric}')
                st.write(f'Loại thông tin: {KIND_LABELS.get(claim.kind, claim.kind)} · {claim.market} · {claim.period} · Chỉ số: {claim.metric}')
                st.write(f'**Đoạn trích:** {claim.quote}')
                s = sources.get(claim.source_id)
                if s:
                    if s.url.startswith(('https://','http://')):
                        st.link_button('Mở nguồn',s.url)
                    st.write(f'Chất lượng: {s.quality}')
                    st.write(f'Độ phù hợp: {RELEVANCE_LABELS.get(s.relevance, s.relevance)} — {s.relevance_reason}')
                    st.write(f'Ngày công bố: {s.published or "chưa rõ"}' + (f' · Trùng nguồn {s.origin_id}' if s.origin_id else ''))
                st.write('Giới hạn:',claim.limitations)
                for issue in claim.issues:
                    st.error(_issue_label(issue))
                latest = next((x for x in reversed(run.claim_reviews) if x.claim_id == claim.id), None)
                if latest:
                    st.write(f'Lần kiểm chứng gần nhất: {VERDICT_LABELS.get(latest.verdict, latest.verdict)} — {latest.reason} ({latest.reviewer})')
                with st.form(f'claim_review_{claim.id}'):
                    reviewer_name = st.text_input('Người kiểm chứng ý này', key=f'claim_reviewer_{claim.id}')
                    verdict = st.selectbox('Đoạn trích có hỗ trợ ý này không?', ['unclear', 'supported', 'unsupported'], format_func=lambda value: VERDICT_LABELS[value], key=f'claim_verdict_{claim.id}')
                    corrected_text = st.text_area('Viết lại ý này nếu cần (chỉ giữ điều nguồn hỗ trợ)', value=claim.text, key=f'claim_corrected_text_{claim.id}')
                    corrected_metric = st.text_input('Chỉ số sau khi chỉnh', value=claim.metric, key=f'claim_corrected_metric_{claim.id}')
                    claim_reason = st.text_area('Lý do đánh giá', key=f'claim_reason_{claim.id}')
                    claim_submit = st.form_submit_button('Lưu đánh giá ý này')
                if claim_submit:
                    try:
                        st.session_state.run = apply_claim_review(run, ClaimReview(claim_id=claim.id, reviewer=reviewer_name, verdict=verdict, reason=claim_reason,
                                                                                   corrected_text=corrected_text.strip() if verdict == 'supported' else None,
                                                                                   corrected_metric=corrected_metric.strip() if verdict == 'supported' else None))
                        st.rerun()
                    except Exception:
                        st.error('Cần tên, lý do và nội dung hợp lệ. Ý đã bị kiểm tra tự động loại không thể xác nhận ở bước này.')
    with source_tab:
        st.caption('Một nguồn có uy tín vẫn có thể không trả lời đúng câu hỏi. Vì vậy hai tiêu chí này được xem riêng.')
        st.subheader(f'Nguồn đã thu ({len(run.sources)})')
        if not run.sources:
            st.info('Chưa có nguồn nào được thu thập trong lượt này.')
        for source in run.sources:
            with st.container(border=True):
                st.write(f'**{source.id} · {source.title}** — {"Đã đọc được" if source.read_status == "read" else "Không đọc được"}')
                if source.url.startswith(('https://', 'http://')):
                    st.link_button(f'Mở {source.id}', source.url)
                st.write(f'Chất lượng: {source.quality}')
                st.write(f'Độ phù hợp: {RELEVANCE_LABELS.get(source.relevance, source.relevance)} — {source.relevance_reason}')
                st.caption(f'Ngày công bố: {source.published or "chưa rõ"} · Lỗi đọc: {source.error or "không có"}')
        with st.expander('Sửa đánh giá chất lượng/độ phù hợp nguồn'):
            if run.sources:
                with st.form('source_review'):
                    source_id = st.selectbox('Nguồn cần sửa', list(sources))
                    source_reviewer = st.text_input('Người kiểm chứng nguồn')
                    quality = st.text_area('Đánh giá chất lượng mới (đơn vị công bố, cách đo, mức độc lập, giới hạn)')
                    relevance = st.selectbox('Độ phù hợp mới', ['direct','indirect','unsuitable'], format_func=lambda value: RELEVANCE_LABELS[value])
                    relevance_reason = st.text_area('Lý do sửa đánh giá nguồn')
                    source_submit = st.form_submit_button('Lưu đánh giá và tính lại')
                if source_submit:
                    try:
                        st.session_state.run = revise_source(run,SourceReview(source_id=source_id,reviewer=source_reviewer,quality=quality,relevance=relevance,reason=relevance_reason))
                        st.rerun()
                    except Exception:
                        st.error('Cần tên người kiểm chứng, đánh giá chất lượng và lý do ít nhất 10 ký tự. Sau khi sửa nguồn, cần xem lại kết luận.')
    with review_tab:
        st.write('1. Đọc trang gốc. 2. Xác nhận hoặc bác từng ý ở tab đầu. 3. Viết kết luận cuối cùng và giải thích lý do.')
        with st.expander('Ghi kết luận của người phụ trách'):
            eligible = [c.id for c in run.extraction.claims if c.status == 'human_verified']
            with st.form('review'):
                reviewer = st.text_input('Người phụ trách kiểm chứng')
                verified = st.multiselect('Các ý đã đối chiếu với nguồn',eligible)
                final_answer = st.text_area('Kết luận cuối của người phụ trách', help='Chỉ kết luận trong phạm vi nguồn hỗ trợ. Nếu thiếu thông tin, nói rõ chưa thể kết luận.')
                answer_basis_label = st.selectbox('Mức căn cứ của kết luận', ['Chưa đủ căn cứ', 'Có ý đã kiểm chứng'])
                answer_claim_ids = st.multiselect('Các ý làm căn cứ cho kết luận', eligible,
                                                   help='Chỉ chọn các ý đã được xác nhận ở tab đầu.')
                decision = st.selectbox('Quyết định', ['Tiếp tục','Tạm giữ','Dừng'] if run.scope.mode=='screening' else ['Reviewed research'],
                                        format_func=lambda value: 'Đã ghi kết luận nghiên cứu' if value == 'Reviewed research' else value)
                reason = st.text_area('Lý do (bắt buộc)')
                blocker = st.checkbox('Đã xác nhận điều kiện loại trừ bằng nguồn')
                review_submit = st.form_submit_button('Lưu kết luận')
            if review_submit:
                try:
                    st.session_state.run = apply_review(run,Review(reviewer=reviewer,decision=decision,reason=reason,verified_claim_ids=verified,blocker_confirmed=blocker,
                                                                    final_answer=final_answer,answer_claim_ids=answer_claim_ids,
                                                                    answer_basis='supported' if answer_basis_label == 'Có ý đã kiểm chứng' else 'insufficient'))
                    st.rerun()
                except ValueError as exc:
                    st.error(f'Chưa thể lưu kết luận: {exc}')
        if run.review:
            st.success(f'Kết luận của người phụ trách: {run.review.decision if run.scope.mode == "screening" else "Đã ghi kết luận nghiên cứu"} — {run.review.reason}')
    with detail_tab:
        if run.errors:
            for error, count in Counter(run.errors).items():
                st.error(error + (f' (×{count})' if count > 1 else ''))
        if run.scope.mode == 'screening':
            st.dataframe([{'Khía cạnh':d.name,'Trạng thái':d.state,'Các ý liên quan':', '.join(d.claim_ids),'Lý do':d.reason} for d in run.extraction.dimensions], hide_index=True)
        st.subheader('Mâu thuẫn và điều chưa biết')
        for x in run.extraction.conflicts:
            st.write(f'{x.relation} [ý {", ".join(x.claim_ids)}]: {x.explanation}')
            st.write('Bước phân xử:',x.next_action)
        for g in run.extraction.gaps:
            st.write(f'**{g.missing}** — {g.impact}')
            st.write(f'{g.action} · Người phụ trách: {g.owner} · Xem lại: {g.revisit}')
        # Full snapshots stay local; download is for reviewer use, never automatically published.
        st.download_button('Tải dữ liệu kỹ thuật JSON (có thể chứa nội dung nguồn)',run.model_dump_json(indent=2),file_name=f'{run.id}.json',mime='application/json')
        st.download_button('Tải báo cáo Markdown',brief_markdown(run),file_name=f'{run.id}.md',mime='text/markdown')
        with st.expander('Chi tiết kỹ thuật của lần chạy'):
            st.json(run.usage)
