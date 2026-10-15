# T01 — First live run and AI audit

Status: **partial; research-quality acceptance not passed; human audit pending**.

A [Vietnamese corrected brief](live-T01-corrected-brief.md) is now available, with a separate AI-corrected replay artifact. It narrows claims and removes unsupported causal conclusions. It does not replace the failed original or demonstrate a successful new live run.

## Observed run

- User executed the CLI once. Artifact directory: `runs/9e512f9c-3771-472a-9cba-3e1a5a87ae10/` (ignored, local only).
- Internal run ID: `fb2fa171-ae9f-4d9e-96e0-e365c469d67c`. The directory identifier and run ID are separate identifiers.
- Configured model recorded by the adapter: `gemini-3.8-flash`; this records configuration, not independently verified server model identity.
- Two API attempts; seven reported search queries; 67.636 seconds. Search response total tokens: 2,377; extraction: 11,322. Money cost and billable search units remain unavailable.
- Six documents returned text; only four unique URL/content documents. S3 duplicates S2, S5 duplicates S4. S1 is navigation/boilerplate, not usable launch evidence, despite `read_status=read` and an automatically extracted date.
- Five claims extracted; all rejected with `Period mismatch; context only`. Two findings excluded; final findings empty. Recommendation absent because this is Research mode.

## Expected → Actual → Result → Learned

**Expected:** answer the Korea launch question using readable original evidence, separate company reports from estimates, preserve source limitations and identify missing coverage without assuming Vietnam demand.

**Actual:** discovery, document reading and structured extraction executed, with relevant evidence from analytics publishers and a company interview reported by a news agency. However, literal period equality rejected April and March–May subperiods within a March–June window. Proposed output also contained semantic overclaims.

**Result:** technical integration executed; end-to-end research acceptance **not passed**. This is a genuine live product failure, separate from the earlier synthetic O08. It must not be described as a successful research brief just because API calls completed.

**Learned:** time scope needs measurement bounds, not string equality. Mechanical citation validation and semantic support are separate acceptance criteria. A readable page can contain no relevant article content. Retrieval duplicates consume source slots even though later validation marks them.

## AI review of proposed claims (not human verification)

| Claim | AI assessment | Required correction/check |
|---|---|---|
| C1 | Main download and launch-date statements supported by S2; quote omits the approximate 50-day qualifier present elsewhere in the document. | Broaden citation coverage or split the claim; retain estimate label and approximate period. |
| C2 | Revenue statement supported; rankings are elsewhere in S2, absent from its attached quote. | Split revenue from ranking and attach the corresponding evidence. |
| C3 | S4 supports April user count and fifth place. | Prefer the source's monthly user wording until MAU definition/methodology is confirmed; do not assert an unverified sampling method. |
| C4 | April revenue and fourth place supported by S4. | Storefront gross-billing and PC-exclusion methodology in limitations is not established in the captured article; label those details unknown. |
| C5 | S6 reports an executive's retrospective May revenue milestone. | Attribute to Newsis reporting an executive, not a primary Nexon filing. The May figure's PC/mobile breakdown is not explicit. |

Source checks: [Sensor Tower](https://sensortower.com/ko/blog/Mabinogi-Mobile-achieves-cumulative-revenue-of-30-million), [Mobile Index](https://www.mobileindex.com/home/blog/post/mobilegame_chart_2504), [Newsis interview reporting](https://mobile.newsis.com/view/NISX20251020_0003369797). Captured text was inspected and the three public pages opened separately; current web reads do not replace the saved snapshots.

### Findings and other generated text

- F1 is a synthesis; `inference=false` is inappropriate for a combined launch-strength conclusion. Ranking scope and period must remain visible; available evidence does not cover all of June.
- F2 attributes revenue differences to PC/non-monitored channels without a supported revenue decomposition. Remove the causal assertion. A cautious replacement is: figures have different periods/coverage and cannot be reconciled from the available evidence; the contribution of each cause is unknown.
- The conflict explanation uses a recent PC user share as if it explained launch-period revenue. Population share is not revenue share, and the observation period differs. Do not use it to reconcile the figures.
- The model populated Screening dimensions despite Research mode. App-store availability/downloads do not establish business accessibility for Gamota. Prompt now explicitly asks for empty dimensions in Research; next live run must verify compliance.
- Generated gap owners and revisit dates are AI proposals, not assignments or deadlines agreed by the user.

## Implemented fix and offline check

Scope and Claim now accept paired `period_start` / `period_end`. With an explicit scope window, a claim is mechanically eligible only when its known bounds are fully contained; missing, overlapping or outside bounds remain ineligible. Original period text is preserved. Legacy scopes without bounds keep exact-string behavior; no fuzzy date guessing was added.

The extraction prompt asks for source-supported measurement bounds, distinct from publication dates, conservative month bounds when imprecise, and gaps for uncovered portions. It also clarifies Research/Screening and warns against unsupported channel causality. These prompt changes are **not yet live-validated**.

Offline derivative: `runs/9e512f9c-3771-472a-9cba-3e1a5a87ae10/period-replay/`. Codex added conservative date bounds to the saved proposed claims (March 27–May 31 for approximate launch-to-May claims, April 1–30 for April claims) without changing claim text. Provenance records parent SHA-256, annotations and **zero new API calls**. Original run is unchanged.

The derivative is labeled replay. Five claims become mechanically checked and pipeline status becomes completed. Semantic overclaims remain in that derivative deliberately for audit; **this is not a new successful live run, an automatically corrected answer or human verification**.

Regression suite: **47 passed**, including contained subperiod, outside/overlapping bounds, unknown bounds and invalid date pairs. No fresh clean-environment run was performed for this update.

## Next acceptance step

User reviews the corrections above; no claim is currently human-verified. After review, run T01 again with structured dates to verify the revised extraction behavior, then T02/T03 and the harder cases. Each new invocation uses a fresh two-attempt allowance and needs to stay within the agreed usage limit; the original one-run allowance has already been consumed. Do not silently rerun Gemini.
