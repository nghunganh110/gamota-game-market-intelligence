from pathlib import Path
import pytest
from gmi.models import Run, Review, Finding
from gmi.replay import replay, FIXTURES
from gmi.validation import validate_run, apply_review
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
    r=raw()
    r.scope.blocker_definition='Rights holder confirms territory unavailable'
    r.extraction.blocker_claim_ids=['C2']
    r=validate_run(r)
    assert r.recommendation=='Tạm giữ'
    with pytest.raises(ValueError):
        apply_review(r,Review(reviewer='Test reviewer',decision='Dừng',reason='Confirmed territory blocker',verified_claim_ids=['C2']))
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


def test_stop_candidate_without_predefined_blocker_is_not_used():
    r=raw(); r.extraction.blocker_claim_ids=['C2']
    assert validate_run(r).extraction.blocker_claim_ids==[]
