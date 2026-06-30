# W.E. C.A.P.E. — Production Dashboard

A **local, read-only** view over your production registry. It turns
`~/.wecape/registry/wecape.db` (plus each shoot's output folder) into a single,
self-contained HTML page you can open offline. It is a **window, never a mutation
layer** — it opens the registry in `mode=ro` and never writes to it.

> Status: **prototype / reference implementation** of `UI_Dashboard_Design_Guidelines_v2.md`.
> It is not the packaged, signed app — that's the future `.dmg` path. It proves the
> "100% local, zero CDN, zero network" mandate is achievable.

## Run it
```bash
cd ~/Curser/we-cape
python3 scripts/dashboard.py                 # reads ~/.wecape/registry/wecape.db -> ./wecape_dashboard.html
python3 scripts/dashboard.py --db /path/to/wecape.db --out /path/to/dash.html
open wecape_dashboard.html
```
Stdlib only — no `pip install`. Works on any Python 3.8+; macOS-native.

## What it shows
- **Overview**: shoots, files (`0 lost`), proxies, footage.
- **Section nav** (sticky): Per-Shoot Reference · Processing Activity · Disposition · Derivation Lineage · Per-clip record.
- **Per-Shoot Reference cards**, in two tiers:
  - **Tier 1 (registry only, always available):** file count, camera mix, proxies, groups/variants, selects, errors, footage, and **processing** (total time + per-stage breakdown + `min/proxy` & `min/GB` rates + an *idempotent re-run* flag when a run transcoded 0).
  - **Tier 2 (when the shoot's `output_path` is reachable):** a **Ready-to-edit / originals-offline** handoff badge (checks the source drive), the **true 4-way classification** (from the run's `index.json`), **multicam membership** (from `MULTICAM/*.json`), and the **explainability panel** (timestamp confidence + fallback level + low-confidence count + conflict-resolved groups, from `LOGS/*.json`).
- **Processing Activity** — pie charts bucketed by processing date, toggling **Monthly / Quarterly / Semi-annual / Annual**, for **shoots / files / proxies / footage**.
- **Disposition** — camera-family breakdown with the *nothing dropped* trust signal.
- **Derivation Lineage** — selects → source clips (schema v3).
- **Per-clip record** — a sample of the registry's per-file rows (hash, camera, shoot date, proxy, source clip).

## Data sources
| View | Source |
|------|--------|
| Shoots, counts, camera mix, lineage, per-clip | the registry (`wecape.db`) |
| Classification breakdown, multicam membership, explainability, handoff | the shoot's output folder — `<run_id>_index.json`, `MULTICAM/*.json`, `LOGS/*.json` (Tier 2, when mounted) |

## Guarantees it honors
- **P2 — privacy:** zero CDN, zero network, no telemetry; the page is fully self-contained.
- **P3 — auditability:** surfaces the determinism (hashes, fallback level/confidence, conflict decisions) and **respects PII path-hashing** — it reports *distributions and counts*, never un-hashes filenames.
- **P4 — read-only, additive:** opens the DB `mode=ro`; never touches the deterministic engine.

## Honest limitations
- **Processing breakdown / rate / re-run flag** populate for runs processed *after* per-stage timing was added; older runs (e.g. the first O-SIX/DJIAction6 runs) show **total runtime only**.
- **Explainability** shows counts/distribution, **not clip names** — the audit logs hash paths by design.
- **Lineage** needs schema **v3**; a v2 registry shows "auto-migrates on the next run" and fills in afterward.
- **AI fields** (quality / highlight / tags / embeddings) are null in v1 by design.
- **Pies** become more meaningful as processing history spans more periods.
- The generated `wecape_dashboard.html` embeds your data and is regenerated each run — it is **gitignored**; don't commit it.
