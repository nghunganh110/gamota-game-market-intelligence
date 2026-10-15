# First live run — T01

Status: first user-executed live run returned partial; see [actual result and AI audit](live-T01-review.md). Instructions below describe each invocation, not permission for additional runs.

The second full live run also returned partial because discovery yielded only a navigation shell. See [rerun diagnosis and one-call snapshot extraction](live-T01-rerun-review.md) before spending another full discovery run.

## Scope and expected behavior

Input: `live-T01-scope.json`. Research South Korea launch performance, distinguishing company-reported results, estimates and metric limitations. Do not infer Vietnam fit. No predetermined positive/negative answer.

This is a current retrieval run about a historical measurement period, not a reconstruction of Mission 1's historical cutoff. `strict_cutoff=false` allows reading current documents about that period; it does not prove that those documents existed before the old cutoff. Confirm the retrieval cutoff before execution.

The scope now explicitly includes March 1–June 30, 2025 measurement bounds. Extraction preserves the actual subperiod of each metric; date containment does not prove semantic support or whole-window coverage.

Expected: important claims trace to readable full text and exact quotes; source quality and relevance remain distinct; unsupported metrics remain gaps. A `completed` pipeline status alone is not a quality pass.

## Private configuration

### Project .env (local)

CLI and Streamlit now load the root `.env` automatically. A private template has been created with key/model blank; `.env` is gitignored. Fill `GEMINI_API_KEY` and `GEMINI_MODEL` locally. Never paste the real key into chat. `.env.example` is a public template with empty credentials. Default usage note permits only one T03 research run (up to two API attempts, no retry); it does not grant unlimited runs or enforce an account-wide monetary limit.

The loader supports literal `KEY=value`, optional matching outer quotes, and full-line `#` comments. No `export`, multiline values, interpolation, or shell execution. Existing exported environment variables take precedence. Restart Streamlit to pick up changed file values after they have been loaded into its process; CLI gets a fresh process per invocation. Codex can run the CLI from the project once this file is filled, without receiving the key in chat.

Use a local terminal; never send the key in chat. In the project's zsh terminal, enter the key without storing its value in shell history:

```zsh
read -rs 'GEMINI_API_KEY?Gemini API key (hidden): '
export GEMINI_API_KEY
```

After the model and usage limit have been agreed, configure `GEMINI_MODEL`, `GMI_BUDGET_NOTE`, `GMI_KEY_AUTHORIZED=1`, `GMI_LIVE_ENABLED=1`, and `GMI_MAX_CALLS=2` in that terminal. The script inherits this terminal's environment; exporting a variable does not update another running Codex/Streamlit process.

Two API attempts maximum per invocation: one search and, if sources are readable, one extraction. No automatic retries. This is an attempt limit, not a monetary or account-wide limit. A new invocation resets it. Model-generated search queries may be billed separately; consult the current [Google pricing](https://ai.google.dev/gemini-api/docs/pricing) and [grounding documentation](https://ai.google.dev/gemini-api/docs/google-search/).

## Check then run

Preflight makes no network/API calls and prints boolean configuration flags only:

```sh
.venv/bin/python -m scripts.live_research --scope docs/mission2/live-T01-scope.json
```

Only after preflight is ready, execute once:

```sh
.venv/bin/python -m scripts.live_research --scope docs/mission2/live-T01-scope.json --run
```

Results go into a new ignored `runs/<id>/` directory: `run.json` with source snapshots and usage, `brief.md`, and `audit.md` with pending review fields. Do not publish full source snapshots automatically. A partial/failed run is still retained; inspect before deciding on another invocation. Cost remains unavailable unless independently calculated from applicable billing and usage.

## Review and report

Audit every claim used by findings, including negation, qualifiers, numbers, scope, source provenance and limitations. Record reviewer identity and corrections; an AI review is not a human verification. For each finding, check whether its cited claims support the conclusion. Keep failed artifacts and distinguish technical success from answer quality. Then add Expected → Actual → Pass/Fail → Learned to the test report, with run ID and usage/latency.
