from pathlib import Path
from .models import Run
from .validation import validate_run

FIXTURES = Path(__file__).resolve().parent.parent / 'fixtures'

def replay(name: str) -> Run:
    if name not in {'good', 'conflict', 'missing', 'semantic_failure', 'other_game'}:
        raise ValueError('Unknown replay scenario')
    run = Run.model_validate_json((FIXTURES / f'{name}.json').read_text())
    if run.evidence_mode != 'synthetic':
        raise ValueError('Bundled demos must be labeled synthetic')
    return validate_run(run)
