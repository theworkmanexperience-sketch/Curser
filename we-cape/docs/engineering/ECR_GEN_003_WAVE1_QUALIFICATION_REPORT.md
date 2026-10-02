# ECR-GEN-003 — B-3 Qualification, Wave 1: `fcpx_resolve.py`, `derive_camera_runs.py`

**Status:** technical qualification PASSED on the authorized historical (08-22) fixture set.
**This is not a B-3 activation.** Decision B is NOT EFFECTIVE; neither identity is activated or
authorized against the governed 08-24 package. Both regeneration holds remain HELD.
**Authority:** CHAIRMAN AUTHORIZATION — B-3 QUALIFICATION WAVE 1; CHAIRMAN ACCEPTANCE — WAVE 1
TECHNICAL QUALIFICATION / EVIDENCE CUSTODY (2026-10-02).
**Code under test:** ECR-GEN-003 engineering custody commit
`e0a346a16abf77db4a6abe5d59a2b31dadcf4464`. Machine-readable results:
`docs/engineering/ECR_GEN_003_wave1_test_results.json` (7 passed, 0 failed).

## 1 · Identities

| producer | qualified identity (current, `e0a346a`) | behavioural oracle (pre-ECR, `795a847`) |
|---|---|---|
| `fcpx_resolve.py` | `faacec8bd67b9be70cda79014953127cffeffd6e134da035d1bfe296ba866038` | `5fd6373d29dd2e8c26d0f2babfeaa2ec4d14b1da603b08e626b704eab6558423` |
| `derive_camera_runs.py` | `178ca2b0c8841cd7c5986b8d7787f97e7d800f5b5f5ea8c00183d07c4bc73d2a` | `15115bdabcd65080b2db3a2567baf07a3a8082279cbc58d0acbd445e38bd42b4` |
| harness `b3_qualify.py` | `8019565de14775c215efddccbfeda7381003f453c0523eb55db99875f48e0ded` | — |

Oracles were materialized from `795a847` into the external workspace (read-only) and were not
restored into the repository.

**Interpreter:** `/usr/bin/python3` -> `/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9`,
CPython 3.9.6, arm64, macOS 26.6.2, SHA-256 `bdea59019a38eb6600cc9e71e984a97fedadc406448431281e7657030f54987e`.
Environment fixed by the harness: `PATH=/usr/bin:/bin`, `LANG=C`, `TZ=UTC`, `PYTHONHASHSEED=0`,
`PYTHONDONTWRITEBYTECODE=1`. Standard library only: no numpy, no ffmpeg; nothing installed (D2 HELD).

## 2 · Fixture manifest

| fixture | origin / construction | SHA-256 |
|---|---|---|
| 08-22 lock FCPXML | `WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK/inputs/Info.fcpxml` (existing, read-only) | `2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7` |
| 08-22 ETC | `…/SPRINT3A_WORK/inputs/P2_LOCK_timing.json` (existing, read-only) | `e91318a6719c81e448e6c57267dff7a807076cb9aded822a459fb6353e80010d` |
| E2 truncated ETC | `e = json.load(ETC); tr = dict(e); tr['spine'] = e['spine'][:-1]; json.dump(tr, f)` — the construction in `ecr_gen_002_suite.py` | `d610aa905f54ba38039e0b9293799b26d6812dd85706e7de3adfce2412a21751` |
| E4 drift ETC | `pe = json.loads(json.dumps(e)); pe['spine'][100]['timeline_offset_s'] += 0.002; json.dump(pe, f)` — the construction in `ecr_gen_002_suite.py` | `db28b9c96f10c428fda14110d073d3be48aee2a2b566286f4a771216d0ce6c58` |
| E3 source-identity variant | the 08-22 lock FCPXML bytes + `b'\n<!-- b3 wave1 E3 source-identity variant -->\n'` (see §3) | `fc45ca24dcb1882d5b2c6d6706b99c3ed29a2434f0fd7ae7cef7a00ad4b4181d` |
| 08-22 resolved timeline (input to `derive_camera_runs.py`) | the E1 primary output, identical from oracle and current resolver | `ebf99f84ceb9dcf487b4703f1e377dd55296ff90d10aaac6a1c6bd3eacc791f8` |

Following repository precedent (the ECR-GEN-001/002 suites build their negative fixtures at run
time and commit none), derived fixture bytes are not committed; their construction and SHA-256
are recorded above. No 08-24 material was used.

## 3 · E3 — qualification fixture adaptation (source-identity STOP only)

The original ECR-GEN-002 E3 case resolved `SPRINT3A_WORK/analysis_cut/Info_analysiscut.fcpxml`
(`1ab3d12f…`), an export of the later 08-24 lineage, against the 08-22 ETC. Wave 1 did not use
it. In its place, the governed 08-22 FCPXML was copied with one appended XML comment — a
non-semantic modification that changes the file's SHA-256 while leaving the parsed editorial
content identical. This file is **not** the original E3 fixture and is **not** 08-24 evidence. Its
only evidentiary purpose is to show that the resolver's source-identity STOP
(`FAILED_SOURCE_IDENTITY`, exit 2) remains operative and unchanged.

## 4 · Results

`fcpx_resolve.py` — oracle 2 runs, current 3 runs per case; the oracle's primary-output hash was
the harness's expected value for the current runs (fail closed on any byte difference).

| case | verdict (both versions) | primary output (all runs) | current sidecar (all runs) | stdout (both versions) |
|---|---|---|---|---|
| E1 | `VALIDATED` 191 / 191, 18 out-of-range, census 1025, exit 0 | `ebf99f84ceb9dcf487b4703f1e377dd55296ff90d10aaac6a1c6bd3eacc791f8` | `de70e5b95e782facc0262c7f3a97bdd51f8be069567c0e07f76d556144e0f417` | `ffd35e9e6a63…` |
| E2 | `FAILED_CARDINALITY`, no partial comparison, exit 2 | `121e8970eb4872ddf1b894b36a98e3846a4ce3458a4645fa62787ee4532ae59f` | `84e83b9d075783645f8c31fe2e49ad43ab3cdd9f7cbbd582a4fde97c78409eff` | `3c80324a75c8…` |
| E3 | `FAILED_SOURCE_IDENTITY`, exit 2 | `d69c849b4f5ff9d35048352b800391de3d489e7f02261e18e77db377bd098898` | `d3086de0b5aad080fad833d0a8881ce6e1004b13103d246dcc1ade82c971a97e` | `ae289217f40d…` |
| E4 | `FAILED_COMPARISON` 190 / 191, exit 2 | `cdf1bcfca3c69bc929c7454969489dcec2767c127f4c0368771a87f493251de7` | `95c3487e518d74b1f196508a8aaa8109c5b3554f03751e404028584771140373` | `42e772b8f62b…` |

In every case the pre-ECR and current primary output, stdout and exit status are identical.
`etc_file` carries the as-invoked path; no `etc_sha256` appears in stdout or resolver JSON. Each
current sidecar records producer `faacec8b…` and the FCPXML and ETC as hashed inputs (the ETC's
SHA-256 appears only there), with no wall-clock value.

`derive_camera_runs.py` — oracle 2 runs, current 3 runs. Primary output
`d3c9fed249d06f07e9690be56acbb79d4cbe20e28c4aedf6880afda624688915` from both versions and every
run (191 runs: X5 120, DJI 57, OM1 5, COMPOUND 9; identical order and segmentation); current
sidecar `9249ff3a256feb07d53f212ab7436796fce77d6a7d0e03f2db7b1a0e90203906` in every run (producer
`178ca2b0…`, `families=X5,DJI,OM1`, timeline `ebf99f84…`); stdout identical.

**Filesystem-write audit:** 15 current-producer runs, zero undeclared writes, exactly the
declared outputs in each. Watch roots: the qualification workspace, both fixture directories, the
oracle directory, the repository scripts directory, the user temp directory and the Python
bytecode cache.

**Discrepancy recorded.** The first oracle E3 report failed on one metadata change of the
macOS-managed temporary directory `…/T/TemporaryItems` during oracle run 2 — a directory the
resolver does not touch. The harness correctly failed closed. A re-run of the oracle case passed
with identical bytes; no current-producer run showed the condition. Both reports are kept.

**Dispositions:** `fcpx_resolve.py` `faacec8b…` — **PASS**. `derive_camera_runs.py` `178ca2b0…` —
**PASS**. Each exact identity is technically qualified on historical fixture data and eligible to be
considered for a later Chairman activation ruling; see §5 for `derive_camera_runs.py`.

## 5 · `derive_camera_runs.py` — designation versus behaviour (read-only check)

The Decision B scope approved in Addendum D describes this producer as: *"mechanical; unknown
camera families are marked UNCERTAIN, not inferred"*; `ENGINEERING_READINESS_REVIEW_ETC_GATE.md`
G5 likewise says *"any element unassignable to a known family -> classify `UNCERTAIN`, do not
infer"*. The qualified implementation (unchanged in behaviour by ECR-GEN-003) labels every
depth-0, non-transition element whose clip name does not match `NAME_RE` with a family in
`X5,DJI,OM1` as **`COMPOUND`**, not `UNCERTAIN`. On the 08-22 fixture the nine `COMPOUND` rows are
three `asset-clip`, three `clip` and three `gap` elements (contributed media such as `HO11YWOOD_GP`,
`NOTOR1OUS_CARAVAN_1_`, `Mark S. Tillman (GP)_CARAVAN`, and timeline gaps) — none is a compound
clip. **The designation language and the implementation differ semantically.** No code or
designation text is changed here; the mismatch is reported for a ruling before any activation.

## 6 · External evidence (not committed)

The raw workspace `/Volumes/WE_CAPE_OUTPUT/_b3_qualification/wave1_20261002/` (≈15 MB: oracle
copies, derived fixtures, specs, run outputs, harness reports) remains outside Git. Harness
reports (SHA-256):
`fcpx_E1_current` `0b3d644317b2107e79e70ff535b67597923c9239b4a8e87f4eef73450880a1db` ·
`fcpx_E1_oracle` `c05b6293557dab65652af01607a494886b60ab27bfad129d2f5f98f08f147527` ·
`fcpx_E2_current` `3c39adf31ba86aa5c14266fd71d8c07ab02c055ce0d85dee955ff283a4156195` ·
`fcpx_E2_oracle` `0c5de7c6890a4068964384ff03c700f999362b0204f42fcc1b6caba03d0a1703` ·
`fcpx_E3_current` `4d434c45cda8aa57d4fc79b267b09d93a8edc9355be16c3e5d5e4a0b9651ae58` ·
`fcpx_E3_oracle` `4dde8289930ad897743f89a04dd05a41419b1c6b17fbb9c32904a427e7bbf96e` ·
`fcpx_E3_oracle_rerun` `f93fe0a3994502887f1cfd375b2b7ffd6d154428cd7d1ebf96226febd062b83d` ·
`fcpx_E4_current` `97e63b654ee043a666af08e774f35183985af7e2b1b7786cf659d9188e1398e7` ·
`fcpx_E4_oracle` `09b23d6bfaf902550434f3106ec23862f7503941a3cc348d4f136403f06c8764` ·
`dcr_current` `3d57d7d1389f439b4c846285e7be370e11802d75ad87d60a51cab968c7f076e7` ·
`dcr_oracle` `6225292c9226f3771123b1e77fd3eb48ffd534ca58eaede2463fd13dc55b1711`.

No producer was run against the governed 08-24 package; no `AR2-0824.observations.json` exists.
