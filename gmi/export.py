from .models import Run

def brief_markdown(run: Run) -> str:
    lines = [f'# {run.scope.subject} — research brief', f'Question: {run.scope.question}',
             f'Mode: **{run.evidence_mode}** | Status: **{run.status}**',
             f'Scope: {run.scope.market}; {run.scope.period}; cutoff {run.scope.cutoff}',
             f'Recommendation: {run.recommendation or "Research only"}',
             'Quote matching proves traceability only. Semantic support requires human review.', '\n## Findings']
    for f in run.extraction.findings:
        lines.append(f'- {f.text} [{", ".join(f.claim_ids)}] (AI inference: {f.inference})')
    lines.append('\n## Claim ledger')
    sources = {s.id: s for s in run.sources}
    for c in run.extraction.claims:
        s = sources.get(c.source_id)
        lines += [f'### {c.id}: {c.text}', f'{c.kind}; {c.status}; {c.market}; {c.period}; metric: {c.metric}',
                  f'> {c.quote}', f'Source: {s.url if s else "MISSING"}', f'Limitations: {c.limitations}', f'Issues: {"; ".join(c.issues) or "None mechanically detected"}']
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
    return '\n\n'.join(lines)
