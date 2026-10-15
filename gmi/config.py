"""Load private .env as literal configuration, never shell code."""
import os
from pathlib import Path

PROJECT_ENV = Path(__file__).resolve().parents[1] / '.env'
ALLOWED_KEYS = frozenset({
    'GEMINI_API_KEY', 'GOOGLE_API_KEY', 'GEMINI_MODEL',
    'GMI_LIVE_ENABLED', 'GMI_KEY_AUTHORIZED', 'GMI_BUDGET_NOTE', 'GMI_MAX_CALLS',
})


def load_local_env(path=PROJECT_ENV, environ=None):
    """KEY=value, optional outer quotes and # comment lines; no expansion.

    Process environment takes precedence. Never return secret values.
    """
    env = os.environ if environ is None else environ
    path = Path(path)
    if not path.is_file():
        return
    pending = {}
    for line_number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, separator, value = line.partition('=')
        key, value = key.strip(), value.strip()
        if not separator:
            raise ValueError(f'Invalid .env syntax at line {line_number}; expected KEY=value')
        if key not in ALLOWED_KEYS:
            continue
        if value.startswith(('"', "'")):
            if len(value) < 2 or value[-1] != value[0]:
                raise ValueError(f'Invalid .env quoting at line {line_number}')
            value = value[1:-1]
        pending[key] = value
    for key, value in pending.items():
        env.setdefault(key, value)
