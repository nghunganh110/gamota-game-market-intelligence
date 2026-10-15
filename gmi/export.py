from .models import Run


def result_summary(run: Run) -> dict:
    """Present validated findings without inventing a new model conclusion."""
    findings = run.extraction.findings if run.status != 'failed' else []
    claim_ids = list(dict.fromkeys(cid for f in findings for cid in f.claim_ids))
    eligible_count = sum(c.status in {'mechanically_checked', 'human_verified'} for c in run.extraction.claims)
    action = next((g.action for g in run.extraction.gaps if g.action),
                  'Kiểm tra các claim trọng yếu và quyết định bước nghiên cứu tiếp theo.')
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
            + (f' Có {eligible_count} claim qua kiểm tra cơ học, nhưng chưa có kết luận nào được hỗ trợ đầy đủ.'
               if eligible_count else '')
        ),
        'next_action': action,
        'reviewed': reviewed_answer,
        'answer_basis': run.review.answer_basis if reviewed_answer else None,
    }

def brief_markdown(run: Run) -> str:
    summary = result_summary(run)
    lines = [f'# {run.scope.subject} — research brief', f'Question: {run.scope.question}',
             f'Mode: **{run.evidence_mode}** | Status: **{run.status}**',
             f'Scope: {run.scope.market}; {run.scope.period}; cutoff {run.scope.cutoff}',
             f'Recommendation: {run.recommendation or "Research only"}',
             'Quote matching proves traceability only. Semantic support requires human review.',
             '\n## Câu trả lời sơ bộ', summary['answer'],
             f'Căn cứ: {", ".join(summary["claim_ids"]) or "chưa có"}',
             f'Bước tiếp theo (AI đề xuất): {summary["next_action"]}', '\n## Findings']
    if run.scope.criteria:
        lines.insert(4, f'Evaluation criteria: {run.scope.criteria}')
    if run.scope.period_start:
        lines.insert(4, f'Measurement window: {run.scope.period_start} to {run.scope.period_end}; subperiod evidence does not prove full-window coverage.')
    for f in run.extraction.findings:
        lines.append(f'- {f.text} [{", ".join(f.claim_ids)}] (AI inference: {f.inference})')
    lines.append('\n## Claim ledger')
    sources = {s.id: s for s in run.sources}
    for c in run.extraction.claims:
        s = sources.get(c.source_id)
        reviews = [x for x in run.claim_reviews if x.claim_id == c.id]
        original = next((item for item in run.proposed_extraction.claims if item.id == c.id), None) if run.proposed_extraction else None
        lines += [f'### {c.id}: {c.text}', f'{c.kind}; {c.status}; {c.market}; {c.period}; metric: {c.metric}',
                  f'Measurement bounds: {c.period_start or "unknown"} to {c.period_end or "unknown"}',
                  f'> {c.quote}', f'Source: {s.url if s else "MISSING"}', f'Limitations: {c.limitations}', f'Issues: {"; ".join(c.issues) or "None mechanically detected"}']
        if original and (original.text != c.text or original.metric != c.metric):
            lines.append(f'Original claim in run: {original.text}; metric: {original.metric}')
        if reviews:
            latest = reviews[-1]
            lines.append(f'Reviewer: {latest.reviewer}; verdict: {latest.verdict}; reason: {latest.reason}')
    lines.append('\n## Source assessments')
    for s in run.sources:
        lines.append(f'- {s.id}: {s.title}; quality: {s.quality}; relevance: {s.relevance} ({s.relevance_reason}); publication: {s.published}; read: {s.read_status}; duplicate of: {s.origin_id or "none detected"}')
    lines.append('\n## Conflicts')
    for x in run.extraction.conflicts:
        lines.append(f'- {x.relation} [{", ".join(x.claim_ids)}]: {x.explanation} Next: {x.next_action}')
    lines.append('\n## Unknowns and next actions')
    for g in run.extraction.gaps:
        lines.append(f'- {g.missing}: {g.impact}. Action: {g.action}. Owner: {g.owner}. Revisit: {g.revisit}.')
    lines.append('\n## Collection errors')
    lines.extend(f'- {e}' for e in run.errors)
    if run.review:
        lines += ['\n## Human decision', f'{run.review.decision}: {run.review.reason} (reviewer: {run.review.reviewer})']
        if run.review.final_answer:
            lines += ['\n## Reviewed answer', run.review.final_answer,
                      f'Basis: {run.review.answer_basis}',
                      f'Human-verified claims: {", ".join(run.review.answer_claim_ids) or "none; evidence insufficient"}']
    return '\n\n'.join(lines)
