from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, model_validator

class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)

class MeasurementPeriod(StrictModel):
    period: str = Field(min_length=2, max_length=200)
    period_start: date | None = Field(default=None, description='Inclusive measurement start, only when supported by the source. Not publication date.')
    period_end: date | None = Field(default=None, description='Inclusive measurement end. For an imprecise month use conservative full-month bounds, never invent an exact day.')

    @model_validator(mode='after')
    def ordered_period(self):
        if (self.period_start is None) != (self.period_end is None):
            raise ValueError('Measurement bounds must both be provided or both omitted')
        if self.period_start and self.period_start > self.period_end:
            raise ValueError('Measurement start must not follow end')
        return self


class Scope(MeasurementPeriod):
    question: str = Field(min_length=10, max_length=2000)
    criteria: str = Field(default='', max_length=500, description='User-defined criteria for evaluative questions; never silently replaced by a model metric.')
    subject: str = Field(min_length=2, max_length=200)
    market: str = Field(min_length=2, max_length=100)
    cutoff: date
    mode: Literal['research', 'screening'] = 'research'
    strict_cutoff: bool = True
    blocker_definition: str = Field(default='', max_length=1000)

class Source(StrictModel):
    id: str
    url: str
    title: str
    publisher: str = 'unknown'
    published: date | None = None
    accessed: datetime | None = None
    text: str = ''
    sha256: str = ''
    read_status: Literal['read', 'failed'] = 'read'
    quality: str = 'AI assessment pending; publisher/methodology not verified'
    relevance: Literal['direct', 'indirect', 'unsuitable'] = 'indirect'
    relevance_reason: str = 'Needs review'
    origin_id: str | None = None
    historical_snapshot: bool = False
    error: str | None = None

class Claim(MeasurementPeriod):
    id: str
    text: str = Field(min_length=1)
    source_id: str
    quote: str = Field(min_length=10, max_length=1200)
    kind: Literal['reported', 'estimate', 'qualitative', 'observed']
    subject: str
    market: str
    metric: str
    limitations: str
    status: Literal['ai_extracted', 'mechanically_checked', 'human_verified', 'rejected'] = 'ai_extracted'
    issues: list[str] = Field(default_factory=list)

class Dimension(StrictModel):
    name: Literal['market_potential', 'business_accessibility', 'feasibility']
    state: Literal['supported', 'concern', 'unknown'] = 'unknown'
    claim_ids: list[str] = Field(default_factory=list)
    reason: str

class Conflict(StrictModel):
    claim_ids: list[str] = Field(min_length=2)
    relation: Literal['conflict', 'different_scope', 'unresolved']
    explanation: str
    next_action: str
    material: bool = True

class Finding(StrictModel):
    text: str
    claim_ids: list[str] = Field(min_length=1)
    inference: bool = True

class Gap(StrictModel):
    missing: str
    impact: str
    action: str
    owner: str = 'Publishing/Strategy reviewer'
    revisit: str = 'After requested evidence is available'

class SourceAssessment(StrictModel):
    source_id: str
    quality: str
    relevance: Literal['direct', 'indirect', 'unsuitable']
    relevance_reason: str

class Extraction(StrictModel):
    source_assessments: list[SourceAssessment] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    dimensions: list[Dimension] = Field(default_factory=list)
    conflicts: list[Conflict] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    gaps: list[Gap] = Field(default_factory=list)
    blocker_claim_ids: list[str] = Field(default_factory=list)

    @model_validator(mode='after')
    def unique_ids(self):
        for items, attr in [(self.claims, 'id'), (self.dimensions, 'name')]:
            ids = [getattr(x, attr) for x in items]
            if len(ids) != len(set(ids)):
                raise ValueError('Duplicate IDs or dimensions')
        return self

class Review(StrictModel):
    reviewer: str = Field(min_length=1)
    decision: Literal['Tiếp tục', 'Tạm giữ', 'Dừng', 'Reviewed research']
    reason: str = Field(min_length=10)
    verified_claim_ids: list[str] = Field(default_factory=list)
    blocker_confirmed: bool = False
    final_answer: str = ''
    answer_claim_ids: list[str] = Field(default_factory=list)
    answer_basis: Literal['supported', 'insufficient'] = 'insufficient'

class SourceReview(StrictModel):
    source_id: str
    reviewer: str = Field(min_length=1)
    quality: str = Field(min_length=10)
    relevance: Literal['direct', 'indirect', 'unsuitable']
    reason: str = Field(min_length=10)

class ClaimReview(StrictModel):
    claim_id: str
    reviewer: str = Field(min_length=1)
    verdict: Literal['supported', 'unsupported', 'unclear']
    reason: str = Field(min_length=10)
    corrected_text: str | None = Field(default=None, min_length=10)
    corrected_metric: str | None = Field(default=None, min_length=3)

    @model_validator(mode='after')
    def correction_requires_support(self):
        if self.verdict != 'supported' and (self.corrected_text or self.corrected_metric):
            raise ValueError('Only a supported claim may carry reviewer corrections')
        return self

class Run(StrictModel):
    id: str
    evidence_mode: Literal['live', 'synthetic', 'replay']
    scope: Scope
    sources: list[Source] = Field(default_factory=list)
    extraction: Extraction = Field(default_factory=Extraction)
    status: Literal['completed', 'partial', 'failed'] = 'failed'
    recommendation: Literal['Tiếp tục', 'Tạm giữ', 'Dừng'] | None = None
    errors: list[str] = Field(default_factory=list)
    usage: dict = Field(default_factory=dict)
    review: Review | None = None
    proposed_extraction: Extraction | None = None
    source_reviews: list[SourceReview] = Field(default_factory=list)
    claim_reviews: list[ClaimReview] = Field(default_factory=list)
    review_history: list[Review] = Field(default_factory=list)
