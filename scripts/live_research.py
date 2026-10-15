"""Preflight by default; explicit --run executes one bounded live research run."""
import argparse
import json
import os
import hashlib
from pathlib import Path

from gmi.export import brief_markdown
from gmi.gemini import GeminiProvider, LivePolicy
from gmi.models import Scope, Run
from gmi.pipeline import run_research
from gmi.reader import DocumentReader
from gmi.config import load_local_env
from gmi.source_input import parse_source_urls


def preflight(env):
    checks = {
        'key_configured': bool(env.get('GEMINI_API_KEY') or env.get('GOOGLE_API_KEY')),
        'model_configured': bool(env.get('GEMINI_MODEL', '').strip()),
        'live_enabled': env.get('GMI_LIVE_ENABLED') == '1',
        'key_authorized': env.get('GMI_KEY_AUTHORIZED') == '1',
        'usage_limit_documented': bool(env.get('GMI_BUDGET_NOTE', '').strip()),
    }
    try:
        # A full run needs search plus extraction. No retry or extra model call.
        checks['two_call_limit'] = int(env.get('GMI_MAX_CALLS', '2')) == 2
    except ValueError:
        checks['two_call_limit'] = False
    return checks


def audit_markdown(run):
    lines = [f'# Claim audit — {run.id}',
             'Pending reviewer audit. No claim is human-verified by this template.',
             'For each claim: check original source, exact meaning, negation, numbers, '
             'qualifiers, market, period, source independence and effect on findings.']
    sources = {s.id: s for s in run.sources}
    for claim in run.extraction.claims:
        source = sources.get(claim.source_id)
        lines.extend([f'## {claim.id}', claim.text, f'> {claim.quote}',
                      f'Source: {source.url if source else "MISSING"}',
                      f'Current status: {claim.status}',
                      'Reviewer: PENDING',
                      'Verdict (supported / partial / unsupported / unclear): PENDING',
                      'Reason, correction and effect on conclusion: PENDING'])
    lines.extend(['## Findings to check', *[
        f'- {f.text} [{", ".join(f.claim_ids)}] — PENDING'
        for f in run.extraction.findings]])
    return '\n\n'.join(lines) + '\n'


def extract_saved_sources(scope, parent_path, provider):
    """Diagnostic extraction with one API attempt and no new retrieval."""
    from gmi.validation import canonical_url
    parent_bytes = parent_path.read_bytes()
    parent = Run.model_validate_json(parent_bytes)
    # Prevent accidental use of evidence from a different research question.
    if parent.scope.question != scope.question or parent.scope.subject != scope.subject or parent.scope.market != scope.market:
        raise ValueError('Saved sources must belong to the same research question')
    saved, seen_urls, seen_hashes = {}, set(), set()
    for source in parent.sources:
        url = canonical_url(source.url)
        digest = hashlib.sha256(source.text.encode()).hexdigest()
        if source.read_status != 'read' or not source.text or source.relevance == 'unsuitable':
            continue
        if url in seen_urls or digest in seen_hashes:
            continue
        seen_urls.add(url)
        seen_hashes.add(digest)
        saved[source.url] = source.model_copy(deep=True)
    if not saved:
        raise ValueError('No usable saved sources')

    class CachedReader:
        def read(self, url, source_id):
            source = saved[url].model_copy(deep=True)
            source.id = source_id
            source.origin_id = None
            return source

    class ExtractionOnly:
        @property
        def usage(self):
            return provider.usage

        def search(self, unused_scope):
            return [{'url': url} for url in saved]

        def extract(self, current_scope, sources):
            return provider.extract(current_scope, sources)

    run = run_research(scope, ExtractionOnly(), CachedReader())
    run.evidence_mode = 'replay'
    run.usage.update({'retrieval': 'saved snapshots; no new discovery or document reads',
                      'new_model_extraction': True, 'parent_run_id': parent.id,
                      'parent_sha256': hashlib.sha256(parent_bytes).hexdigest()})
    return run


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', required=True, type=Path)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--sources-from', type=Path, help='Diagnostic: reuse snapshots from a prior run of this question, with one new extraction call')
    parser.add_argument('--url-file', type=Path, help='One public source URL per line (1–6); skips Gemini discovery and uses at most one extraction call')
    args = parser.parse_args(argv)
    if args.sources_from and args.url_file:
        parser.error('--sources-from and --url-file cannot be combined')
    load_local_env()
    scope = Scope.model_validate_json(args.scope.read_text())
    checks = preflight(os.environ)
    # Never print environment values, credentials or arbitrary exception bodies.
    print(json.dumps({'checks': checks, 'ready': all(checks.values()),
                      'api_calls': 0}, ensure_ascii=False))
    if not args.run:
        return 0 if all(checks.values()) else 2
    if not all(checks.values()):
        return 2
    source_urls = parse_source_urls(args.url_file.read_text()) if args.url_file else None
    policy = LivePolicy(enabled=True, authorized=True,
                        budget_note=os.environ['GMI_BUDGET_NOTE'], max_calls=2)
    # Reserve a fresh artifact directory before making any API call.
    from uuid import uuid4
    output = Path('runs') / str(uuid4())
    output.mkdir(parents=True, exist_ok=False)
    provider = GeminiProvider(policy)
    if args.sources_from:
        run = extract_saved_sources(scope, args.sources_from, provider)
    else:
        run = run_research(scope, provider, DocumentReader(), source_urls=source_urls)
    (output / 'run.json').write_text(run.model_dump_json(indent=2))
    (output / 'brief.md').write_text(brief_markdown(run))
    (output / 'audit.md').write_text(audit_markdown(run))
    print(json.dumps({'artifact_directory': str(output), 'status': run.status,
                      'evidence_mode': run.evidence_mode,
                      'api_calls': policy.calls, 'claims': len(run.extraction.claims),
                      'human_audit': 'pending'}))
    return 0 if run.status == 'completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
