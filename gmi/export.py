from .models import Run


DATA_LABELS = {'live': 'Nghiên cứu mới', 'replay': 'Ví dụ đã lưu', 'synthetic': 'Dữ liệu mô phỏng'}
STATUS_LABELS = {'completed': 'Đã xử lý', 'partial': 'Một phần', 'failed': 'Chưa xử lý được',
                 'mechanically_checked': 'Qua kiểm tra tự động', 'human_verified': 'Đã được xác nhận',
                 'rejected': 'Bị loại', 'ai_extracted': 'AI đề xuất'}
RELEVANCE_LABELS = {'direct': 'Phù hợp trực tiếp', 'indirect': 'Liên quan gián tiếp',
                    'unsuitable': 'Không phù hợp'}
KIND_LABELS = {'reported': 'Số liệu được công bố', 'estimate': 'Số liệu ước tính',
               'qualitative': 'Nhận xét định tính', 'observed': 'Quan sát được'}
VERDICT_LABELS = {'unclear': 'Chưa rõ', 'supported': 'Đoạn trích hỗ trợ ý này',
                  'unsupported': 'Đoạn trích không hỗ trợ ý này'}


def result_summary(run: Run) -> dict:
    """Present validated findings without inventing a new model conclusion."""
    findings = run.extraction.findings if run.status != 'failed' else []
    claim_ids = list(dict.fromkeys(cid for f in findings for cid in f.claim_ids))
    eligible_count = sum(c.status in {'mechanically_checked', 'human_verified'} for c in run.extraction.claims)
    action = next((g.action for g in run.extraction.gaps if g.action),
                  'Đối chiếu các ý quan trọng với nguồn rồi quyết định có cần nghiên cứu thêm.')
    reviewed_answer = bool(run.review and run.review.final_answer.strip())
    preliminary_answer = '\n'.join(
        f'- {finding.text} [{", ".join(finding.claim_ids)}]'
        for finding in findings
    )
    return {
        'findings': findings,
        'claim_ids': run.review.answer_claim_ids if reviewed_answer else claim_ids,
        'answer': run.review.final_answer if reviewed_answer else preliminary_answer if findings else (
            'Chưa đủ bằng chứng hợp lệ để trả lời câu hỏi này.'
            + (f' Có {eligible_count} ý qua kiểm tra tự động, nhưng chưa có kết luận nào được nguồn hỗ trợ đầy đủ.'
               if eligible_count else '')
        ),
        'next_action': action,
        'reviewed': reviewed_answer,
        'answer_basis': run.review.answer_basis if reviewed_answer else None,
    }

def brief_markdown(run: Run) -> str:
    summary = result_summary(run)
    lines = [f'# {run.scope.subject} — báo cáo nghiên cứu', f'Câu hỏi: {run.scope.question}',
             f'Loại dữ liệu: **{DATA_LABELS.get(run.evidence_mode, run.evidence_mode)}** | Trạng thái xử lý: **{STATUS_LABELS.get(run.status, run.status)}**',
             f'Phạm vi: {run.scope.market}; {run.scope.period}; ngày chốt thông tin {run.scope.cutoff}',
             f'Gợi ý của AI: {run.recommendation or "Chỉ nghiên cứu"}',
             'Tìm thấy đoạn trích trong nguồn chỉ chứng minh khả năng truy vết. Người phụ trách cần đọc nguồn để xác nhận ý nghĩa.',
             '\n## Câu trả lời', summary['answer'],
             f'Các ý làm căn cứ: {", ".join(summary["claim_ids"]) or "chưa có"}',
             f'Bước tiếp theo (AI đề xuất): {summary["next_action"]}', '\n## Các ý AI rút ra']
    if run.scope.criteria:
        lines.insert(4, f'Tiêu chí đánh giá: {run.scope.criteria}')
    if run.scope.period_start:
        lines.insert(4, f'Khoảng thời gian đo: {run.scope.period_start} đến {run.scope.period_end}; số liệu một kỳ nhỏ không đại diện cho toàn kỳ.')
    for f in run.extraction.findings:
        lines.append(f'- {f.text} [ý {", ".join(f.claim_ids)}] (AI diễn giải: {f.inference})')
    lines.append('\n## Từng ý và nguồn đi kèm')
    sources = {s.id: s for s in run.sources}
    for c in run.extraction.claims:
        s = sources.get(c.source_id)
        reviews = [x for x in run.claim_reviews if x.claim_id == c.id]
        original = next((item for item in run.proposed_extraction.claims if item.id == c.id), None) if run.proposed_extraction else None
        lines += [f'### Ý {c.id}: {c.text}', f'Loại: {KIND_LABELS.get(c.kind, c.kind)}; trạng thái: {STATUS_LABELS.get(c.status, c.status)}; thị trường: {c.market}; kỳ đo: {c.period}; chỉ số: {c.metric}',
                  f'Thời gian đo: {c.period_start or "chưa rõ"} đến {c.period_end or "chưa rõ"}',
                  f'Đoạn trích: {c.quote}', f'Nguồn: {s.url if s else "KHÔNG CÓ"}', f'Giới hạn: {c.limitations}', f'Lỗi/điểm cần xem lại: {"; ".join(c.issues) or "Chưa phát hiện qua kiểm tra tự động"}']
        if original and (original.text != c.text or original.metric != c.metric):
            lines.append(f'Ý ban đầu do AI viết: {original.text}; chỉ số: {original.metric}')
        if reviews:
            latest = reviews[-1]
            lines.append(f'Người kiểm chứng: {latest.reviewer}; đánh giá: {VERDICT_LABELS.get(latest.verdict, latest.verdict)}; lý do: {latest.reason}')
    lines.append('\n## Đánh giá các nguồn')
    for s in run.sources:
        lines.append(f'- {s.id}: {s.title}; chất lượng: {s.quality}; độ phù hợp: {RELEVANCE_LABELS.get(s.relevance, s.relevance)} ({s.relevance_reason}); ngày công bố: {s.published}; trạng thái đọc: {"Đã đọc được" if s.read_status == "read" else "Không đọc được"}; trùng nguồn: {s.origin_id or "chưa phát hiện"}')
    lines.append('\n## Thông tin mâu thuẫn')
    for x in run.extraction.conflicts:
        lines.append(f'- {x.relation} [ý {", ".join(x.claim_ids)}]: {x.explanation} Bước kiểm tra tiếp: {x.next_action}')
    lines.append('\n## Thông tin còn thiếu và việc cần làm')
    for g in run.extraction.gaps:
        lines.append(f'- {g.missing}: {g.impact}. Việc cần làm: {g.action}. Người phụ trách: {g.owner}. Xem lại: {g.revisit}.')
    lines.append('\n## Lỗi thu thập dữ liệu')
    lines.extend(f'- {e}' for e in run.errors)
    if run.review:
        lines += ['\n## Kết luận của người phụ trách', f'{run.review.decision}: {run.review.reason} (người kiểm chứng: {run.review.reviewer})']
        if run.review.final_answer:
            lines += ['\n## Câu trả lời đã được kiểm chứng', run.review.final_answer,
                      f'Mức căn cứ: {run.review.answer_basis}',
                      f'Các ý đã được đối chiếu: {", ".join(run.review.answer_claim_ids) or "chưa có; chưa đủ căn cứ"}']
    return '\n\n'.join(lines)
