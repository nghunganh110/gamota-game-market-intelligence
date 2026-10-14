"""Generate explicitly synthetic regression inputs. No real commercial claims."""
from pathlib import Path
from gmi.models import Scope, Source, Claim, Extraction, Dimension, Finding, Conflict, Gap, Run

root = Path(__file__).resolve().parent.parent / 'fixtures'
root.mkdir(exist_ok=True)
scope = Scope(question='Does fictional Game Alpha justify deeper research in Vietnam?', subject='Fictional Game Alpha', market='Vietnam', period='Q1 2025', cutoff='2025-04-01', mode='screening')
texts = [
    'SYNTHETIC evidence. Fictional Game Alpha has a positive demand signal from the Vietnam concept study in Q1 2025. This is an invented statement for software tests only.',
    'SYNTHETIC evidence. The rights holder states that Vietnam territory is available for Fictional Game Alpha in Q1 2025. This is an invented statement for software tests only.',
    'SYNTHETIC evidence. The internal review indicates feasible operations in Vietnam for Fictional Game Alpha in Q1 2025. This is an invented statement for software tests only.'
]
quotes = [t.split('. ')[1] + '.' for t in texts]
sources = [Source(id=f'S{i+1}', url=f'https://example.org/synthetic/{i+1}', title=f'Synthetic document {i+1}', publisher='Fictional test publisher', published='2025-03-01', text=t, historical_snapshot=True, quality='Synthetic; no factual authority', relevance='direct', relevance_reason='Synthetic scope matches fixture') for i,t in enumerate(texts)]
claims = [Claim(id=f'C{i+1}',text=q, source_id=f'S{i+1}',quote=q,kind='reported',subject=scope.subject,market=scope.market,period=scope.period,metric=m,limitations='Synthetic fixture; not market evidence') for i,(q,m) in enumerate(zip(quotes,['demand','rights','feasibility']))]
ext = Extraction(claims=claims, dimensions=[Dimension(name=n,state='supported',claim_ids=[f'C{i+1}'],reason='Synthetic supporting claim') for i,n in enumerate(['market_potential','business_accessibility','feasibility'])],findings=[Finding(text='Fictional signals justify reviewing the opportunity.',claim_ids=['C1','C2','C3'])])
run = Run(id='synthetic-good',evidence_mode='synthetic',scope=scope,sources=sources,extraction=ext)
def save(name,r):
    (root / f'{name}.json').write_text(r.model_dump_json(indent=2))
save('good',run)
conflict = run.model_copy(deep=True)
conflict.id='synthetic-conflict'
conflict.sources.append(Source(id='S4',url='https://example.org/synthetic/4',title='Synthetic contradictory demand',published='2025-03-01',text='The Vietnam concept study reports a negative demand signal for Fictional Game Alpha in Q1 2025. Synthetic software test data only.',historical_snapshot=True,relevance='direct',quality='Synthetic',relevance_reason='Same metric, market and period'))
conflict.extraction.claims.append(claims[0].model_copy(update={'id':'C4','source_id':'S4','text':'Negative demand','quote':'The Vietnam concept study reports a negative demand signal for Fictional Game Alpha in Q1 2025.'}))
conflict.extraction.conflicts=[Conflict(claim_ids=['C1','C4'],relation='conflict',explanation='Same scope but opposing fictional demand results.',next_action='Review sampling and methods; obtain original study')]
save('conflict',conflict)
missing=run.model_copy(deep=True)
missing.id='synthetic-missing'
missing.scope.mode='research'
missing.scope.question='What is D30 retention by country for Fictional Game Alpha?'
missing.extraction=Extraction(gaps=[Gap(missing='D30 retention by country',impact='Cannot answer requested KPI',action='Request owner cohort dataset')])
save('missing',missing)
failure=run.model_copy(deep=True)
failure.id='synthetic-semantic-failure'
failure.scope.mode='research'
failure.sources[0].text='The Vietnam study says Fictional Game Alpha does not have strong demand in Q1 2025. This is synthetic test data only.'
failure.extraction=Extraction(claims=[claims[0].model_copy(update={'text':'Game Alpha has strong demand in Vietnam.', 'quote':'The Vietnam study says Fictional Game Alpha does not have strong demand in Q1 2025.'})],findings=[Finding(text='Strong Vietnam demand.',claim_ids=['C1'])])
save('semantic_failure',failure)
other=run.model_copy(deep=True)
other.id='synthetic-other-game'
other.scope.subject='Fictional Game Beta'
other.scope.market='China'
other.scope.question='What public signals justify reviewing Fictional Game Beta in China?'
other.scope.mode='research'
for s in other.sources:
    s.text=s.text.replace('Game Alpha','Game Beta').replace('Vietnam','China')
for c in other.extraction.claims:
    c.subject=other.scope.subject; c.market=other.scope.market
    c.quote=c.quote.replace('Game Alpha','Game Beta').replace('Vietnam','China')
    c.text=c.quote
other.extraction.findings=[Finding(text='Signals are scoped to fictional China data; no transfer to Vietnam assumed.',claim_ids=['C1'])]
save('other_game',other)
