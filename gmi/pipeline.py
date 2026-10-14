import time
from uuid import uuid4
from .models import Run, Scope, Source
from .validation import validate_run


def run_research(scope: Scope, provider, reader) -> Run:
    started = time.monotonic()
    run = Run(id=str(uuid4()), evidence_mode='live', scope=scope)
    try:
        urls = provider.search(scope)
        if not urls:
            run.errors.append('Discovery returned no attributed URLs')
        for index, item in enumerate(urls[:6], 1):
            s = reader.read(item['url'], f'S{index}')
            run.sources.append(s)
            if s.read_status == 'failed':
                run.errors.append(f'{s.id}: {s.error}')
        readable = [s for s in run.sources if s.read_status == 'read' and s.text]
        if readable:
            run.extraction = provider.extract(scope, readable)
            assessments = {a.source_id: a for a in run.extraction.source_assessments}
            for s in readable:
                a = assessments.get(s.id)
                if a:
                    s.quality = a.quality + ' (AI assessment; human review pending)'
                    s.relevance = a.relevance
                    s.relevance_reason = a.relevance_reason
        else:
            run.errors.append('No readable full-text sources; no factual answer generated')
    except Exception as exc:
        run.errors.append(f'Pipeline interrupted ({type(exc).__name__}); no fabricated fallback')
    run.usage = dict(getattr(provider, 'usage', {}))
    run.usage['latency_seconds'] = round(time.monotonic() - started, 3)
    return validate_run(run)
