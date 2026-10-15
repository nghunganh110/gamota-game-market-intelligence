from pathlib import Path
import pytest
from gmi.models import Run, Review, Finding
from gmi.replay import replay, FIXTURES
from gmi.validation import validate_run, apply_review, subject_matches
from gmi.export import brief_markdown


def raw():
    return Run.model_validate_json((FIXTURES/'good.json').read_text())


def test_sufficient_screening_and_export_roundtrip():
    r = replay('good')
    assert (r.status, r.recommendation) == ('completed','Tiếp tục')
    assert all(c.status=='mechanically_checked' for c in r.extraction.claims)
    assert Run.model_validate_json(r.model_dump_json()) == r
    assert 'C1' in brief_markdown(r) and 'synthetic' in brief_markdown(r)


def test_conflict_keeps_both_sides_and_holds():
    r = replay('conflict')
    assert r.recommendation == 'Tạm giữ'
    assert r.extraction.conflicts[0].claim_ids == ['C1','C4']
    assert r.extraction.conflicts[0].next_action


def test_retention_question_not_replaced_by_revenue():
    r = replay('missing')
    assert r.status=='partial' and not r.extraction.findings
    assert 'D30' in r.extraction.gaps[0].missing
    assert r.recommendation is None


@pytest.mark.parametrize('field,value', [('source_id','FAKE'),('quote','This invented quote is absent from content')])
def test_false_citations_rejected(field,value):
    r=raw()
    setattr(r.extraction.claims[0],field,value)
    out=validate_run(r)
    assert out.extraction.claims[0].status=='rejected'
    assert out.recommendation=='Tạm giữ'
    assert not out.extraction.findings


@pytest.mark.parametrize('mutation', ['wrong_market','wrong_subject','wrong_period','unknown_date','future_date','no_snapshot','irrelevant'])
def test_scope_and_cutoff_gates(mutation):
    r=raw()
    if mutation=='wrong_market': r.extraction.claims[0].market='Korea'
    if mutation=='wrong_subject': r.extraction.claims[0].subject='Another game'
    if mutation=='wrong_period': r.extraction.claims[0].period='Q2 2025'
    if mutation=='unknown_date': r.sources[0].published=None
    if mutation=='future_date': r.sources[0].published=r.scope.cutoff.replace(year=2026)
    if mutation=='no_snapshot': r.sources[0].historical_snapshot=False
    if mutation=='irrelevant': r.sources[0].relevance='unsuitable'
    out=validate_run(r)
    assert out.extraction.claims[0].status=='rejected'
    assert out.recommendation=='Tạm giữ'


def test_duplicate_tracking_and_repost_exact_content():
    r=raw()
    s=r.sources[0].model_copy(update={'id':'S4','url':r.sources[0].url+'?utm_source=test#top'})
    r.sources.append(s)
    r.sources.append(r.sources[0].model_copy(update={'id':'S5','url':'https://example.org/repost'}))
    out=validate_run(r)
    assert out.sources[3].origin_id=='S1'
    assert out.sources[4].origin_id=='S1'


def test_stop_requires_human_confirmed_evidence():
    from gmi.models import ClaimReview
    from gmi.validation import apply_claim_review
    r=raw()
    r.scope.blocker_definition='Rights holder confirms territory unavailable'
    r.extraction.blocker_claim_ids=['C2']
    r=validate_run(r)
    assert r.recommendation=='Tạm giữ'
    with pytest.raises(ValueError):
        apply_review(r,Review(reviewer='Test reviewer',decision='Dừng',reason='Confirmed territory blocker',verified_claim_ids=['C2']))
    r=apply_claim_review(r,ClaimReview(claim_id='C2',reviewer='Test reviewer',
                         verdict='supported',reason='The synthetic quote explicitly confirms this blocker.'))
    out=apply_review(r,Review(reviewer='Test reviewer',decision='Dừng',reason='Confirmed territory blocker',verified_claim_ids=['C2'],blocker_confirmed=True))
    assert out.review.decision=='Dừng'
    assert out.recommendation=='Tạm giữ'
    assert out.extraction.claims[1].status=='human_verified'


def test_override_reason_and_invalid_verification():
    with pytest.raises(ValueError):
        Review(reviewer='Reviewer',decision='Tạm giữ',reason='short')
    with pytest.raises(ValueError):
        apply_review(replay('good'),Review(reviewer='Reviewer',decision='Tiếp tục',reason='Explicit reviewed rationale',verified_claim_ids=['FAKE']))


def test_multiple_game_questions_without_hardcoding():
    a,b=replay('good'),replay('other_game')
    assert a.scope.subject != b.scope.subject and a.scope.question != b.scope.question
    assert all(c.status=='mechanically_checked' for c in b.extraction.claims)
    assert b.recommendation is None


def test_group_subject_accepts_exact_member_without_matching_broader_market():
    assert subject_matches('Mobile MMORPG', 'Mobile MMORPG, 4X Strategy, Team Battle')
    assert not subject_matches('Mobile MMORPG', 'Vietnam Mobile Gaming Market')
    assert not subject_matches('Game Alpha', 'Game Alphabet, Game Beta')
    r = raw()
    r.scope.subject = 'Mobile MMORPG'
    r.extraction.claims[0].subject = 'Mobile MMORPG, 4X Strategy, Team Battle'
    assert 'Subject mismatch' not in validate_run(r).extraction.claims[0].issues


def test_known_semantic_failure_is_exposed_not_mislabeled_verified():
    # This passes as a regression documenting a PRODUCT FAILURE, not entailment success.
    r=replay('semantic_failure')
    c=r.extraction.claims[0]
    assert c.status=='mechanically_checked'
    assert 'does not have strong demand' in c.quote
    assert 'has strong demand' in c.text
    assert c.status != 'human_verified'


def test_fabricated_finding_excluded():
    r=raw(); r.extraction.findings=[Finding(text='Unsupported synthesis',claim_ids=['FAKE'])]
    out=validate_run(r)
    assert not out.extraction.findings and out.status=='partial'


def test_preliminary_answer_shows_each_finding_with_its_own_claims():
    from gmi.export import result_summary
    r = replay('good')
    r.extraction.findings.append(Finding(text='A second, narrower signal.', claim_ids=['C1']))
    summary = result_summary(r)
    for finding in r.extraction.findings:
        assert f'- {finding.text} [{", ".join(finding.claim_ids)}]' in summary['answer']


def test_source_review_recomputes_gates_and_keeps_history():
    from gmi.models import SourceReview
    from gmi.validation import revise_source
    r=apply_review(replay('good'),Review(reviewer='Reviewer',decision='Tiếp tục',reason='Reviewed initial supporting evidence'))
    r=revise_source(r,SourceReview(source_id='S1',reviewer='Reviewer',quality='Publisher report; methodology not representative',relevance='unsuitable',reason='Sample population does not match the question'))
    assert r.recommendation=='Tạm giữ' and r.review is None
    assert r.review_history[0].decision=='Tiếp tục'
    assert r.source_reviews[0].source_id=='S1'
    r=revise_source(r,SourceReview(source_id='S1',reviewer='Reviewer',quality='Direct research with reviewed sampling method',relevance='direct',reason='Corrected source assessment after inspecting full scope'))
    assert r.recommendation=='Tiếp tục' and r.review is None


def test_claim_review_removes_unsupported_conclusion_and_can_be_revised():
    from gmi.models import ClaimReview
    from gmi.validation import apply_claim_review
    from gmi.export import result_summary
    r=replay('semantic_failure')
    assert r.extraction.findings
    r=apply_claim_review(r,ClaimReview(claim_id='C1',reviewer='Reviewer',verdict='unsupported',reason='The quote says demand is not strong.'))
    assert not r.extraction.findings
    assert r.extraction.claims[0].status=='rejected'
    assert 'Chưa đủ bằng chứng' in result_summary(r)['answer']
    assert len(r.claim_reviews)==1
    r=apply_claim_review(r,ClaimReview(claim_id='C1',reviewer='Reviewer',verdict='unclear',reason='Needs more evidence for this wording.'))
    assert not r.extraction.findings
    assert len(r.claim_reviews)==2


def test_claim_review_marks_supported_and_blocks_mechanically_rejected():
    from gmi.models import ClaimReview
    from gmi.validation import apply_claim_review
    good=replay('good')
    out=apply_claim_review(good,ClaimReview(claim_id='C1',reviewer='Reviewer',verdict='supported',reason='The quoted fictional source supports this claim.'))
    assert out.extraction.claims[0].status=='human_verified'
    assert out.extraction.findings
    invalid=raw()
    invalid.extraction.claims[0].quote='Fictitious quotation not found in the source.'
    invalid=validate_run(invalid)
    with pytest.raises(ValueError):
        apply_claim_review(invalid,ClaimReview(claim_id='C1',reviewer='Reviewer',verdict='supported',reason='I want to accept it despite missing quote.'))


def test_reviewed_answer_requires_human_checked_citations_and_survives_export():
    from gmi.models import ClaimReview
    from gmi.validation import apply_claim_review
    from gmi.export import result_summary

    run = replay('other_game')
    premature = Review(reviewer='Reviewer', decision='Reviewed research',
                       reason='The source supports a narrower conclusion.',
                       final_answer='The game has a measurable launch signal.', answer_claim_ids=['C1'],
                       answer_basis='supported')
    with pytest.raises(ValueError, match='semantically reviewed'):
        apply_review(run, premature)

    run = apply_claim_review(run, ClaimReview(claim_id='C1', reviewer='Reviewer',
                             verdict='supported', reason='The quoted fictional source states this metric.'))
    reviewed = apply_review(run, premature)
    assert result_summary(reviewed)['answer'] == premature.final_answer
    assert result_summary(reviewed)['claim_ids'] == ['C1']
    assert result_summary(reviewed)['reviewed']
    assert 'Reviewed answer' in brief_markdown(reviewed)
    assert Run.model_validate_json(reviewed.model_dump_json()).review == premature

    with pytest.raises(ValueError, match='reviewed citations'):
        apply_review(run, premature.model_copy(update={'answer_claim_ids': []}))


def test_reviewer_source_change_invalidates_reviewed_answer():
    from gmi.models import ClaimReview, SourceReview
    from gmi.validation import apply_claim_review, revise_source
    from gmi.export import result_summary

    run = replay('other_game')
    run = apply_claim_review(run, ClaimReview(claim_id='C1', reviewer='Reviewer',
                             verdict='supported', reason='Quoted metric supports this fictional claim.'))
    run = apply_review(run, Review(reviewer='Reviewer', decision='Reviewed research',
                       reason='The source supports the narrow answer.',
                       final_answer='The title has this limited metric.', answer_claim_ids=['C1']))
    changed = revise_source(run, SourceReview(source_id='S1', reviewer='Reviewer',
                            quality='Source method is too weak for a conclusion',
                            relevance='unsuitable', reason='Population differs from the study question.'))
    assert changed.review is None and changed.review_history
    assert not result_summary(changed)['reviewed']


def test_stop_candidate_without_predefined_blocker_is_not_used():
    r=raw(); r.extraction.blocker_claim_ids=['C2']
    assert validate_run(r).extraction.blocker_claim_ids==[]


@pytest.mark.parametrize('start,end,eligible', [
    ('2025-04-01', '2025-04-30', True),
    ('2025-03-01', '2025-06-30', True),
    ('2025-02-28', '2025-04-30', False),
    ('2025-06-01', '2025-07-01', False),
    (None, None, False),
])
def test_measurement_window_accepts_only_contained_subperiods(start, end, eligible):
    from datetime import date
    r = raw()
    r.scope.period = 'March–June 2025 launch window'
    r.scope.period_start = date(2025, 3, 1)
    r.scope.period_end = date(2025, 6, 30)
    r.scope.strict_cutoff = False
    c = r.extraction.claims[0]
    c.period = 'April 2025'  # Preserve the actual period, not the scope label.
    c.period_start = date.fromisoformat(start) if start else None
    c.period_end = date.fromisoformat(end) if end else None
    out = validate_run(r)
    assert (out.extraction.claims[0].status == 'mechanically_checked') == eligible
    assert out.extraction.claims[0].period == 'April 2025'
    assert out.extraction.claims[0].status != 'human_verified'


@pytest.mark.parametrize('bounds', [
    {'period_start': '2025-04-01'},
    {'period_start': '2025-05-01', 'period_end': '2025-04-01'},
])
def test_invalid_measurement_bounds_rejected_by_schema(bounds):
    from gmi.models import Scope
    scope = raw().scope.model_dump(mode='json')
    scope.update(bounds)
    with pytest.raises(ValueError):
        Scope.model_validate(scope)
