# ECR-GEN-004 — `derive_camera_runs.py` semantic successor: UNCERTAIN fallback

**Status:** PROPOSED — working tree, not committed. Successor **technically qualified**; **NOT
EFFECTIVE**. Activation requires a separate Chairman ruling. Decision B remains incomplete.
**Authority:** CHAIRMAN RULING — derive_camera_runs.py SEMANTIC CORRECTION AND REQUALIFICATION
(2026-10-02); sections 1–3 verbatim in §7.
**Nature:** a **semantic successor change** to the ECR-GEN-003 implementation. It invalidates the
predecessor identity for activation purposes.

## 1 · Identities

| | file | SHA-256 | status |
|---|---|---|---|
| predecessor | `intelligence/p2/ess/scripts/derive_camera_runs.py` | `178ca2b0c8841cd7c5986b8d7787f97e7d800f5b5f5ea8c00183d07c4bc73d2a` | retained unchanged; Wave 1 qualification (`1def9ea`) is historical evidence only; **not activatable** under Decision B / G5 |
| successor | `intelligence/p2/ess/scripts/derive_camera_runs_v2.py` | `ec253c0595f8b325fecd5bd0a2e86299ede9e1c5f34610ace13419b7dddd6873` | qualified here; eligible for a later B-3 activation ruling; NOT EFFECTIVE |

**Why a successor file rather than an in-place edit.** The predecessor's `COMPOUND` label is
embedded in committed 08-22 products (`VISUAL_EVENT_REGISTRY.yaml`
`camera_device_families_from_etc`) and in the ECR-GEN-001/002 byte-for-byte regression proofs on
the 08-22 fixture. The ruling keeps historical 08-22 products unchanged; repository precedent for
an instrument whose output backs committed evidence is to retain it and add a versioned successor
(`rederive_segments.py` / `rederive_segments_v2.py`; `gen_artifacts.py` / `gen_artifacts_v2.py`).
The predecessor therefore keeps reproducing the historical outputs, and no existing caller changes.

## 2 · The change

The successor is the predecessor byte for byte except for one code statement and its documentation:

```diff
 def family(name, known):
     m = NAME_RE.match(name or '')
     if m and m.group(1) in known:
         return m.group(1)
-    return 'COMPOUND'
+    return 'UNCERTAIN'
```

The module docstring states the ECR-GEN-004 semantics and the successor's usage line. Unchanged:
`NAME_RE`, recognized family names and the `X5,DJI,OM1` default, the depth-0 / non-transition
filter, ordering, run segmentation and rounding, the input/output structure, and the ECR-GEN-003
provenance sidecar and `with`-block output. `ecr_gen_004_static_check.py` proves this without
executing either file: **4/4 PASS** (C1 every other top-level statement AST-identical; C2 `family()`
differs only in the fallback constant; C3 no `COMPOUND` constant in the successor's code; C4
predecessor unchanged).

## 3 · Fixtures

| fixture | construction | SHA-256 |
|---|---|---|
| 08-22 resolved timeline (historical, authorized in Wave 1) | `fcpx_resolve.py` E1 output on the 08-22 lock (`ECR_GEN_003_WAVE1_QUALIFICATION_REPORT.md` §2) | `ebf99f84ceb9dcf487b4703f1e377dd55296ff90d10aaac6a1c6bd3eacc791f8` |
| historical expectation | the committed-evidence Wave 1 predecessor output `d3c9fed249d06f07e9690be56acbb79d4cbe20e28c4aedf6880afda624688915`, with every `"camera": "COMPOUND"` replaced by `"camera": "UNCERTAIN"` (the 9 occurrences are all in `camera` fields) | `a51029006b36cafb7dd49ed308ded418df2fc5ca86b4bfd4e1849bad830ff7fc` |
| synthetic classification fixture | `json.dumps({"fixture": "ECR-GEN-004 synthetic camera-family classification fixture", "elements": [four depth-0 elements below]}, indent=1, sort_keys=True) + "\n"` | `b9893a43786bf5a05876a943e2e9d22e3201cd747f1a6beb111b330add85236a` |
| synthetic expectation | `json.dumps([...four rows...], indent=1)`, built independently of the producer | `b5f122c48539bff365750c32b93d92d7906423fd25b7798c971aa1fbda31d62c` |

Synthetic elements (classification only; no 08-24 material; no family inferred): `asset-clip`
`001 · 06-26 10:00:00 · X5 · SYNTH_A.mp4` 0–10 s (recognized family) -> `X5`; `asset-clip`
`002 · 06-26 10:05:00 · ZZ9 · SYNTH_B.mp4` 10–20 s (camera-convention name, unknown family `ZZ9`, a
placeholder token) -> `UNCERTAIN`; `asset-clip` `CONTRIBUTED_SYNTH_C` 20–30 s (contributed /
non-camera, outside the convention) -> `UNCERTAIN`; `gap` `Gap` 30–40 s (structural) -> `UNCERTAIN`.
No repository class defines true compound-camera material, so none is fixtured.

## 4 · Qualification (`b3_qualify.py`, 3 runs per fixture)

Interpreter cpython 3.9.6 `/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9`, SHA-256 `bdea59019a38eb6600cc9e71e984a97fedadc406448431281e7657030f54987e`; environment `PATH=/usr/bin:/bin`,
`LANG=C`, `TZ=UTC`, `PYTHONHASHSEED=0`, `PYTHONDONTWRITEBYTECODE=1`. Expected primary-output hashes were
set in each spec (fail closed).

| fixture | verdict | primary output (all 3 runs) | sidecar (all 3 runs) |
|---|---|---|---|
| 08-22 historical | **PASS** | `a51029006b36cafb7dd49ed308ded418df2fc5ca86b4bfd4e1849bad830ff7fc` (= expectation) | `e4f03286d8c5023a49882cce90d3715f5666be04f6fe9e525dc80d746758b38e` |
| synthetic | **PASS** | `b5f122c48539bff365750c32b93d92d7906423fd25b7798c971aa1fbda31d62c` (= expectation) | `d00326ba0c84fb889db718a0563001f7b0290f14392c9e7259b2e1064182ca29` |

**Historical diff:** 191 rows in both. Exactly rows 25, 26, 67, 86, 87, 88, 125, 138 and 150 differ,
each only in `camera`, `COMPOUND` -> `UNCERTAIN`. Recognized families are unchanged (X5 120, DJI 57,
OM1 5); order, names, tags and run boundaries are identical; the successor emits no `COMPOUND`.
**Synthetic:** `X5`, `UNCERTAIN`, `UNCERTAIN`, `UNCERTAIN` as specified. **Determinism:** outputs,
sidecars and stdout byte-identical across runs. **Write audit:** 6 runs, zero undeclared writes,
declared outputs only. Each sidecar binds `derive_camera_runs_v2.py` `ec253c0595f8b325…`,
`families=X5,DJI,OM1` and the input hash. **Disposition: PASS.** Results:
`docs/engineering/ECR_GEN_004_test_results.json` (5 passed, 0 failed).

External evidence (not committed): `/Volumes/WE_CAPE_OUTPUT/_b3_qualification/ecr004_20261002/` —
`dcr2_hist0822.json` `61cb732304f48861ed5d1f45a6b7ed146b886d24b2b0e76e73c0a09a4ebab30e` · `dcr2_synthetic.json` `3fd06243d552418d684ccbfa063514094b3e7265da10f98b00f4f4edc675808d` · `build_fixtures.py` `ecdc2efbb8e68ec155ad9810e0b4ca12575db9902ab47fe341b30d7e2d834776` · `run_qualification.py` `b818d4739388bc8c6cecf3f91e07428872c7cbf0f1344ea02262c55f1c2f4aed`. No producer ran against the governed 08-24 package.

## 5 · Consequences

- The predecessor identity `178ca2b0c8841cd7…` cannot be activated; its Wave 1 qualification is historical
  evidence only.
- The successor `ec253c0595f8b325…` is eligible for, not granted, B-3 activation. Any later change to it
  needs requalification and a new ruling.
- Callers are unchanged: `ecr_gen_002_suite.py` and the 08-22 regression continue to use the
  predecessor. Pointing future 08-24 generation at the successor is a separate, later decision.
- `fcpx_resolve.py` remains EFFECTIVE under Addendum E (`faacec8b…`), unchanged; Addendum E is not
  modified. Decision B remains incomplete. D2 remains HELD. Both regeneration holds remain HELD.

## 6 · Records this change does not correct

The Wave 1 report §5 and Addendum E describe the nine historical rows as "contributed media and gaps"
(more precisely: five composite elements, one contributed asset, three gaps) and attribute the
UNCERTAIN wording to Addendum D (it is in the Decision B packet that Addendum D incorporates by
reference). A correction notice has not been issued; this ECR does not amend those documents.

## 7 · CHAIRMAN RULING — VERBATIM (sections 1–3)

```text
CHAIRMAN RULING — derive_camera_runs.py SEMANTIC CORRECTION AND REQUALIFICATION
The read-only semantic reconciliation is accepted.
Determination:
BOTH DESIGNATION CLARIFICATION AND CODE CHANGE ARE REQUIRED.
The currently qualified derive_camera_runs.py identity:
178ca2b0c8841cd7c5986b8d7787f97e7d800f5b5f5ea8c00183d07c4bc73d2a
is not authorized for B-3 activation under the existing Decision-B/G5 requirement.
Preserve its Wave-1 qualification as historical evidence only.
1. Clarify the intended Decision-B semantics
Adopt the following scope clarification:
derive_camera_runs.py is a mechanical transcription of the FCPXML clip-name convention.
- A recognized camera-bearing element whose name matches the established camera-family convention retains its recognized family.
- A camera-bearing element whose family cannot be assigned under the established convention is UNCERTAIN; no family may be inferred from other evidence.
- An element outside the camera-family convention, including contributed/non-camera media or structural/gap material, is also UNCERTAIN for this producer's camera-family output.
- COMPOUND is not an authorized fallback camera-family inference under Decision B/G5.
- Historical 08-22 artifacts containing COMPOUND remain unchanged as historical outputs.
Do not rewrite historical Wave-1 evidence or 08-22 products.
2. Authorize the minimum semantic code correction
Create a successor implementation of derive_camera_runs.py.
Change only the fallback behavior required to conform to the ruling:
COMPOUND → UNCERTAIN
for elements that do not resolve to a recognized camera family.
Preserve unchanged:
- recognized-family regex behavior;
- recognized family names;
- clip/run ordering;
- run segmentation;
- input/output structure;
- provenance-sidecar behavior;
- all other ECR-GEN-003 parameterization and reproducibility changes.
If the necessary diff is more than the expected narrowly scoped fallback/status change plus mechanically required test/documentation changes, stop and report before proceeding.
3. Engineering-governance record
Use the repository's next available engineering-change mechanism/identifier; verify the identifier before assigning it.
Record explicitly that this is a semantic successor change to the ECR-GEN-003 implementation and therefore invalidates the old producer identity for activation purposes.
Do not modify Addendum E or the already activated fcpx_resolve.py.
```
