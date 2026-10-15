import hashlib
import re
from datetime import datetime, timezone
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from .models import Run, Gap, Review, SourceReview, ClaimReview


def canonical_url(url):
    p = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(p.query) if not k.startswith('utm_') and k not in {'fbclid','gclid'}]
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip('/'), urlencode(sorted(query)), ''))


def normalize(text):
    return re.sub(r'\s+', ' ', text).strip().casefold()


def subject_matches(scope_subject: str, claim_subject: str) -> bool:
    """Accept an exact subject or its explicit membership in a comma-separated group.

    Group evidence still needs semantic review; it cannot establish a metric for
    the requested subject alone.
    """
    wanted = normalize(scope_subject)
    return wanted in {normalize(part) for part in claim_subject.split(',')}


def validate_run(run: Run) -> Run:
    """Mechanical traceability checks. Does not prove semantic entailment."""
    run = run.model_copy(deep=True)
    if run.proposed_extraction is None:
        run.proposed_extraction = run.extraction.model_copy(deep=True)
    ids = [s.id for s in run.sources]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate source IDs')
    sources = {s.id: s for s in run.sources}
    latest_claim_reviews = {review.claim_id: review for review in run.claim_reviews}
    revised_claim_ids = set()
    seen_urls, seen_text = {}, {}
    for s in run.sources:
        s.sha256 = hashlib.sha256(s.text.encode()).hexdigest()
        url = canonical_url(s.url)
        content = hashlib.sha256(normalize(s.text).encode()).hexdigest()
        duplicate = seen_urls.get(url) or (seen_text.get(content) if s.text else None)
        if duplicate:
            s.origin_id = duplicate
        else:
            seen_urls[url] = s.id
            if s.text:
                seen_text[content] = s.id
    for c in run.extraction.claims:
        c.issues = []
        assessment = latest_claim_reviews.get(c.id)
        if assessment and assessment.verdict == 'supported':
            if assessment.corrected_text and assessment.corrected_text != c.text:
                c.text = assessment.corrected_text
                revised_claim_ids.add(c.id)
            if assessment.corrected_metric and assessment.corrected_metric != c.metric:
                c.metric = assessment.corrected_metric
                revised_claim_ids.add(c.id)
        s = sources.get(c.source_id)
        if not s or s.read_status != 'read' or not s.text:
            c.issues.append('Source missing or unreadable')
        else:
            if normalize(c.quote) not in normalize(s.text):
                c.issues.append('Quote absent from captured content')
            if s.published and s.published > run.scope.cutoff:
                c.issues.append('Published after cutoff')
            if run.scope.strict_cutoff and not s.published:
                c.issues.append('Publication date unknown')
            today = datetime.now(timezone.utc).date()
            if run.scope.strict_cutoff and run.scope.cutoff < today and not s.historical_snapshot:
                c.issues.append('No snapshot proving content existed at historical cutoff')
            if not subject_matches(run.scope.subject, c.subject):
                c.issues.append('Subject mismatch')
            if normalize(c.market) != normalize(run.scope.market):
                c.issues.append('Market mismatch; context only')
            if run.scope.period_start is not None:
                if c.period_start is None:
                    c.issues.append('Measurement bounds unknown; context only')
                elif not (run.scope.period_start <= c.period_start <= c.period_end <= run.scope.period_end):
                    c.issues.append('Period outside requested window; context only')
            elif normalize(c.period) != normalize(run.scope.period):
                c.issues.append('Period mismatch; context only')
            if s.relevance != 'direct':
                c.issues.append('Source not directly relevant')
        if assessment and assessment.verdict != 'supported':
            c.issues.append(f'Reviewer marked {assessment.verdict}: {assessment.reason}')
        c.status = ('rejected' if c.issues else
                    'human_verified' if assessment and assessment.verdict == 'supported' else
                    'mechanically_checked')
    valid = {c.id for c in run.extraction.claims if c.status in {'mechanically_checked', 'human_verified'}}
    sanitized = []
    for f in run.extraction.findings:
        if set(f.claim_ids) & revised_claim_ids:
            run.errors.append('Finding excluded: supporting claim was revised by reviewer')
        elif set(f.claim_ids) <= valid:
            sanitized.append(f)
        else:
            run.errors.append('Finding excluded: invalid claim references')
    run.extraction.findings = sanitized
    for d in run.extraction.dimensions:
        if not d.claim_ids or not set(d.claim_ids) <= valid:
            d.state = 'unknown'
            d.reason = 'Insufficient eligible evidence: ' + d.reason
    for x in run.extraction.conflicts:
        if not set(x.claim_ids) <= valid:
            x.relation = 'unresolved'
            x.explanation += ' (One or more claims ineligible.)'
    run.extraction.blocker_claim_ids = [i for i in run.extraction.blocker_claim_ids if i in valid] if run.scope.blocker_definition.strip() else []
    readable = any(s.read_status == 'read' and s.text for s in run.sources)
    run.status = 'failed' if not readable else ('partial' if run.errors or not valid or any(c.issues for c in run.extraction.claims) else 'completed')
    if not valid:
        run.extraction.gaps.append(Gap(missing='No eligible evidence', impact='Question cannot be answered reliably', action='Obtain readable, dated sources matching scope'))
    run.recommendation = None
    if run.scope.mode == 'screening':
        dims = {d.name: d for d in run.extraction.dimensions}
        required = {'market_potential', 'business_accessibility', 'feasibility'}
        unresolved = any(x.material and x.relation in {'conflict','unresolved'} for x in run.extraction.conflicts)
        supported = required <= dims.keys() and all(dims[n].state == 'supported' for n in required)
        run.recommendation = 'Tiếp tục' if supported and not unresolved and not run.extraction.blocker_claim_ids and run.status == 'completed' else 'Tạm giữ'
        for name in sorted(required):
            if name not in dims or dims[name].state != 'supported':
                run.extraction.gaps.append(Gap(missing=name, impact='Could change screening decision', action='Collect direct evidence and review this dimension'))
    run.review = None
    return run


def apply_review(run: Run, review: Review) -> Run:
    if run.scope.mode == 'research' and review.decision != 'Reviewed research':
        raise ValueError('Research review must not assign a screening decision')
    human_verified = {c.id for c in run.extraction.claims if c.status == 'human_verified'}
    if not set(review.verified_claim_ids) <= human_verified:
        raise ValueError('Decision may use only semantically reviewed claims')
    if review.answer_claim_ids and not review.final_answer.strip():
        raise ValueError('Answer citations require a final answer')
    if review.answer_basis == 'supported' and (not review.final_answer.strip() or not review.answer_claim_ids):
        raise ValueError('Supported answer requires a final answer and reviewed citations')
    if not set(review.answer_claim_ids) <= human_verified:
        raise ValueError('Final answer may cite only semantically reviewed claims')
    if review.final_answer.strip() and len(review.final_answer.strip()) < 10:
        raise ValueError('Final answer must explain the assessment')
    if review.decision == 'Dừng':
        blockers = set(run.extraction.blocker_claim_ids)
        if not review.blocker_confirmed or not blockers or not blockers <= set(review.verified_claim_ids):
            raise ValueError('Stop requires a reviewed evidence-backed blocker')
    result = run.model_copy(deep=True)
    if result.review:
        result.review_history.append(result.review)
    result.review = review
    for c in result.extraction.claims:
        if c.id in review.verified_claim_ids:
            c.status = 'human_verified'
    # Keep the AI recommendation intact; the final human decision is a separate field.
    return result


def apply_claim_review(run: Run, assessment: ClaimReview) -> Run:
    claim = next((c for c in run.extraction.claims if c.id == assessment.claim_id), None)
    if claim is None:
        raise ValueError('Claim missing')
    if assessment.verdict == 'supported' and claim.status == 'rejected' and not any(
        issue.startswith('Reviewer marked') for issue in claim.issues
    ):
        raise ValueError('Cannot approve a claim rejected by mechanical checks')
    result = run.model_copy(deep=True)
    result.claim_reviews.append(assessment)
    if result.review:
        result.review_history.append(result.review)
    if result.proposed_extraction:
        result.extraction = result.proposed_extraction.model_copy(deep=True)
    result.errors = [e for e in result.errors if e not in {
        'Finding excluded: invalid claim references',
        'Finding excluded: supporting claim was revised by reviewer'}]
    return validate_run(result)


def revise_source(run: Run, revision: SourceReview) -> Run:
    result = run.model_copy(deep=True)
    source = next((s for s in result.sources if s.id == revision.source_id), None)
    if source is None:
        raise ValueError('Source missing')
    source.quality = revision.quality + ' (reviewer: ' + revision.reviewer + ')'
    source.relevance = revision.relevance
    source.relevance_reason = revision.reason
    result.source_reviews.append(revision)
    if result.review:
        result.review_history.append(result.review)
    if result.proposed_extraction:
        result.extraction = result.proposed_extraction.model_copy(deep=True)
    result.errors = [e for e in result.errors if e not in {
        'Finding excluded: invalid claim references',
        'Finding excluded: supporting claim was revised by reviewer'}]
    return validate_run(result)
