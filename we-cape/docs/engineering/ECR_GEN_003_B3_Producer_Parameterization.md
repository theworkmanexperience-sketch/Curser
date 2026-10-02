# ECR-GEN-003 — B-3 Producer Path Parameterization and Reproducibility

**Status:** PROPOSED — working-tree implementation, **UNQUALIFIED**, not committed.
**Authority:** CHAIRMAN RULING — B-3 PRODUCER ECR SCOPE / D2 TOOLCHAIN HOLD (scope approved in
principle); CHAIRMAN AUTHORIZATION — ECR-GEN-003 IMPLEMENTATION PROPOSAL; CHAIRMAN RULING —
ECR-GEN-003 RESOLVER COMPATIBILITY: OPTION (a); all 2026-10-02.
**Base:** `origin/main` = `795a847d5ccbe7373d0da86babe8df1d5edc70f1` (Decision C provenance closure).
**Decision B:** NOT EFFECTIVE. No producer is qualified, activated, or authorized to operate on
the governed 08-24 sources. Both regeneration holds remain HELD.

## 1 · Scope

Covered: `produce_audio_rms.py`, `produce_video_obs.py`, `fcpx_resolve.py`,
`derive_camera_runs.py`, `step0_offset.py`, `step0_anchors.py`; new `b3_qualify.py`; this
document; the validation/diff artifacts `ecr_gen_003_static_check.py` and `ecr_gen_003.diff`.

Excluded: `die_v_observables.py` (threshold-derived classification — not a B-3 producer);
generator code, guards, `build_context.py`, registries, Decision A, Decision C, downstream
artifacts.

Permitted change classes: (A) removal of machine-specific paths, inputs/outputs as explicit
CLI arguments; (B) deterministic serialization, provenance sidecars (script SHA-256, input
SHA-256, arguments, toolchain identity, no wall-clock value), `.npy` path normalization,
bounded/streamed processing proven byte-equivalent. Category C (formulas, thresholds,
coverage/duration rules, score thresholds, lag/trial behaviour, RNG seeds, status vocabulary,
camera-family logic, column meanings, interpretation, segment/beat assignment) is prohibited.

## 2 · Changes per file

| file | change | class |
|---|---|---|
| `produce_audio_rms.py` | `<out>` normalised to end in `.npy` before `np.save`; sidecar `<out>.provenance.json` (media and optional `--verify` reference hashed; `rate`, `window_s`; resolved `ffmpeg` path + SHA-256 + version line; Python, numpy version and BLAS name). `decode_pcm`, `rms_windows`, constants unchanged. | A/B |
| `produce_video_obs.py` | `decode_frames` (whole-decode buffering, ~233 GB for the 08-24 MOV) replaced by `stream_frames` (same ffmpeg command, frames read one at a time, stderr drained concurrently, the same three failure checks in the same order); `observe` replaced by `observe_stream`, whose per-frame statements are the former loop body verbatim. Sidecar names the array and its schema. `probe_geometry`, `COLUMNS`, schema, colour/YUV->RGB/luma handling unchanged. **Byte-equivalence still to be proven on an authorized SDR fixture; 08-24 HDR use NOT AUTHORIZED.** | B |
| `fcpx_resolve.py` | argparse wrapper around the same three positionals; output JSON written in a `with` block (same bytes, flushed before hashing); sidecar written on every exit path (STOP included), with the FCPXML and the ETC recorded as hashed inputs. **Stdout and the output JSON are unchanged** (Option (a)): `etc_file` still echoes the ETC path as invoked, and no `etc_sha256` field is emitted. `rt`, `f2`, `TOL`, `STORY`, `Resolver`, every gate, census and STOP unchanged. | A/B |
| `derive_camera_runs.py` | sidecar only (families argument, timeline hashed); output written in a `with` block so it is flushed before hashing. `NAME_RE`, `family`, `derive`, default `X5,DJI,OM1`, `COMPOUND` fallback unchanged. | B |
| `step0_offset.py` | `--srt --rms --rms-window-s --timeline --segments --out` replace the Sprint 3A `/mnt/...` and `/home/claude/...` literals; the S01–S19 literal becomes the `--segments` input (§4); `--rms-window-s` must equal `H=0.25`, and so must the RMS array's own sidecar `window_s` when present; sidecar. `H`, `RNG=default_rng(20260822)`, every function, every threshold, lag, trial count and status string unchanged; module-level execution order unchanged. | A/B |
| `step0_anchors.py` | `--srt --timeline --out` replace the hard-coded paths; sidecar. Matching rule (score ≥ 0.6, ±25 s, words > 2 chars) and statistics unchanged. | A/B |

No absolute path literal remains in any of the six producers.

## 3 · Script identities

| file | before (`795a847`) | after (working tree) |
|---|---|---|
| `produce_audio_rms.py` | `63f56e5587cfcd6124f39995c9e3da00c0646463dbdee5266e7691cccd0be937` | `df656716a16db8a032e5d79fd4e292d490cb8aeefdd0f6e62c12d2c95b5f50b1` |
| `produce_video_obs.py` | `8228692e49f61d695d8935100ca10f27811238fcf2f713cc7c35fc6c6d7e5d63` | `946941d48db1037dca9e5d179d13b30ec3d87d2c5f60a2e7747d1119d08fc2ea` |
| `fcpx_resolve.py` | `5fd6373d29dd2e8c26d0f2babfeaa2ec4d14b1da603b08e626b704eab6558423` | `faacec8bd67b9be70cda79014953127cffeffd6e134da035d1bfe296ba866038` |
| `derive_camera_runs.py` | `15115bdabcd65080b2db3a2567baf07a3a8082279cbc58d0acbd445e38bd42b4` | `178ca2b0c8841cd7c5986b8d7787f97e7d800f5b5f5ea8c00183d07c4bc73d2a` |
| `step0_offset.py` | `47b7d760bd1145fcb2e98fc9e240e69006d70b80b1625dbfdcbce9afd6215997` | `643433546e15afd90e8aeccc89dc7b6819aa3699342e5622cde053197ddc52d5` |
| `step0_anchors.py` | `f3825ca3d878fe1f96320aa45157c9bcd198047877993eecd8c7c543d5cf66d0` | `66079f2ada0f60c186edc43cf82fe3f02e9e22568b986695445c5e89535d474e` |
| `b3_qualify.py` | — | `8019565de14775c215efddccbfeda7381003f453c0523eb55db99875f48e0ded` |

These are proposal identities. Final identities are recorded only at qualification, per
producer, together with the commit.

## 4 · `step0_offset.py` 08-22 segment table (the former literal, verbatim)

Recorded here, not materialized as a fixture file (fixture creation is not yet authorized).
Canonical serialization (`json.dumps(..., indent=1) + "\n"`) SHA-256
`ed564a0f407384ea147a0d770c4f8eb9ab10c61fa2e879d53cb4fd4178885170`; check `O1` proves it equals
the base literal value for value. This is the **08-22** table; it decides nothing about the
08-24 segment set (D4 / S19).

```json
[["S01", "00:00", "01:13", "cold_open"], ["S02", "01:13", "01:51", "host_day_brief"], ["S03", "01:51", "27:02", "interview_gauntlet_1"], ["S04", "27:02", "27:23", "ride_brief"], ["S05", "27:40", "29:10", "escort_ride"], ["S06", "31:43", "32:33", "librarian_speech"], ["S07", "32:45", "33:50", "council_profile"], ["S08", "33:51", "35:56", "town_proclamation"], ["S09", "36:03", "36:30", "first_ride_moment"], ["S10", "36:59", "38:52", "state_proclamation"], ["S11", "38:55", "52:00", "interview_gauntlet_2"], ["S12", "52:04", "53:56", "honors_and_silence"], ["S13", "53:50", "54:35", "group_photo"], ["S14", "54:36", "55:24", "service_wrap_preview"], ["S15", "56:10", "58:43", "riding_music_passage"], ["S16", "58:43", "66:25", "bike_night_arrivals"], ["S17", "66:25", "66:48", "audience_cta"], ["S18", "69:25", "79:40", "bike_night_ambience"], ["S19", "79:44", "80:46", "friday_wrap_part3_tease"]]
```

## 5 · `b3_qualify.py` — evidence only

Runs one producer (as a subprocess; never imported) against one explicitly supplied fixture
spec, ≥ 2 runs. Asserts every input against its declared SHA-256 before running (STOP
otherwise); runs each pass in a fresh `runN/out`, with `runN/cwd` as working directory and a
fixed environment (`LANG=C`, `TZ=UTC`, `PYTHONHASHSEED=0`, `PYTHONDONTWRITEBYTECODE=1`, PATH from
the spec — the toolchain selector); snapshots the declared watch roots and the work directory
before and after each run and reports every write outside that run's output directory;
requires exactly the declared output files; compares output bytes across runs and, if given,
against expected SHA-256; records producer/input/interpreter/tool identities; writes a sorted-key
report with no wall-clock value and a mechanical PASS/FAIL. It designates nothing, adjudicates
nothing, touches no registry and grants no B-3 authority — the report says so.

## 6 · Validation (non-executing)

`py_compile` of all eight scripts: OK (bytecode to the interpreter's cache prefix, not the repo).
`ecr_gen_003_static_check.py --base origin/main` (AST only; no producer imported or run): **34/34 PASS** —
per file: parses; every base top-level statement not on the file's allow-list is AST-identical;
no numeric constant lost or changed; no string constant lost except the removed machine paths
(and the segment literal, moved per §4); no absolute path literal; plus V1 (the 12 per-frame
statements of `observe_stream` equal the base `observe` loop body; ffmpeg command unchanged) and
O1 (segment table) and R1 (`fcpx_resolve.py`: `main()` equals the base once the single added
sidecar-bookkeeping statement is removed, every `print` in `_emit()` equals the base, no `etc_sha256`
key, the ETC is a hashed sidecar input — so resolver stdout and output JSON are byte-identical to
the pre-ECR resolver for the same invocation). Full diff: `intelligence/p2/ess/scripts/ecr_gen_003.diff`.

## 7 · Resolver compatibility (Option (a)) and recorded consequences

**Pre-existing path dependence (finding, not corrected here).** `fcpx_resolve.py` echoes the ETC
path exactly as invoked (`etc_file`), so its stdout depends on the invocation path. The B-5/B-14
packet's `etc_validation_stdout.txt` (`2edf7916…`) records the canonical invocation
(`.../we-cape/intelligence/p2/ess/decision_packet_b5_b14/AR2-0824_ETC.json`). A run of the
packet's `run.sh` into a second directory, made 2026-09-29, produced `f9fe2939…`, differing from the
committed file in exactly that one line; two further reruns into other directories differ the same
way. The packet's general statement that a second-directory re-run "reproduced every product byte
for byte" is therefore overbroad for this product. That predates ECR-GEN-003. This ECR does not
alter the packet, its `run.sh`, or its committed stdout, and does not claim to correct the
packet's statement.

**What ECR-GEN-003 preserves.** Resolver stdout and output JSON are unchanged (check R1): the
canonical `run.sh` invocation emits its committed stdout as before. The ETC's SHA-256 is recorded
only in the provenance sidecar, as a hashed input; the governed `etc_sha256` declaration key (see
`CAM-001` U-1) is not emitted by the resolver, and no other stdout field carries it. The sidecar is
provenance, not resolver evidence text.

**Future path normalization.** Any repo-relative, basename or hash-bound resolver output requires a
versioned successor resolver introduced beside the current one (repository precedent:
`rederive_segments.py` / `rederive_segments_v2.py` + `run_v2.sh`; `gen_artifacts.py`, "RETAINED,
NOT DELETED … DO NOT EDIT" / `gen_artifacts_v2.py`), not an in-place change of stdout format.

**Sidecars in temporary workflows (known consequence).** Each producer writes
`<output>.provenance.json` beside its output. Callers that delete only their primary temporary
file — `decision_packet_b5_b14/f5_enumerate.py` (`tempfile.mktemp`, then `os.unlink`) — will leave
the sibling sidecar behind; `run.sh` already leaves its temporary timeline and `mktemp` placeholder
behind. This is a caller-cleanup consequence, recorded here; the decision-packet tooling is not
modified by this ECR. `b3_qualify.py` reports any such residual write outside a run's declared
output directory as an undeclared write.

**Other consequences.** The new sidecars are additional files beside each output; no consumer of
the producers' outputs reads anything that changed. `intelligence/p2/ingest_0824/validate_ingest_0824.py`
is a point-in-time validator of the Decision C transaction: its V26 (`fcpx_resolve.py` unchanged
since `de0c902`) and V27 (allowed file set) will not pass on a tree containing this ECR; it remains
valid at `795a847` and is not modified here (Decision C is out of scope).

## 8 · Deferred — not decided by this ECR

1. `produce_video_obs.py` on the governed 08-24 source: HDR (BT.2020 / PQ, 8-bit yuv420p,
   tv range) tone/transfer handling, YUV->RGB interpretation, luma semantics, meaning of
   columns 4–6 — separate semantic ruling. No 08-24-format video fixture without separate authority.
2. The 08-24 segment table for `step0_offset.py` (D4 / S19).
3. Any new camera-family or clip-name rule for `derive_camera_runs.py` (none needed: 190 of
   201 08-24 spine names match the existing pattern; 11 fall to `COMPOUND`).
4. `die_v_observables.py`, observation-class dispositions, G-01..G-09, G-07, Decision B activation.

## 9 · D2 toolchain preflight (no installation)

- Interpreters: `/usr/bin/python3` -> CommandLineTools 3.9.6 (arm64); MacPorts `/opt/local/bin/python3.14` 3.14.5. Neither has numpy.
- Historical: Sprint 3A `EXECUTION_LOG.md` — Python "3.10.12 (media host) / 3.11 (analysis)", numpy **2.2.6**, ffmpeg 4.4.2 (Ubuntu). No 3.11 patch level is recorded. The scripts directory holds `cpython-310` bytecode dated 2026-08-28 for `ecr_gen_002_suite`, `fcpx_resolve`, `gen_artifacts_v2`, `runtime_guards`: the ECR-GEN-002 conformance work ran on this Mac under a Python 3.10 that is no longer installed (provenance otherwise unrecorded).
- numpy 2.2.6 requires Python ≥ 3.10 (PyPI). macOS arm64 cp311 candidates (published SHA-256 verified on download to scratch; not installed):
  `numpy-2.2.6-cp311-cp311-macosx_11_0_arm64.whl` `c820a93b0255bc360f53eca31a0e676fd1101f673dda8da93454a12e23fc5f7a` — bundles **scipy-openblas64** (same BLAS family as the historical Linux wheel);
  `numpy-2.2.6-cp311-cp311-macosx_14_0_arm64.whl` `3d70692235e759f260c3d837193090014aebdf026dfd167834bcba43e30c2a42` — **Apple Accelerate**.
  cp310: `macosx_11_0` `8e41fd67c52b86603a91c1a505ebaef50b3314de0213461c7a6e99c9a3beff90`, `macosx_14_0` `37e990a01ae6ec7fe7fa1c26c55ecb672dd98b19c3d0e1d1f326fa13cb38d163`.
- Project-local interpreter without touching system Python or a package manager: python-build-standalone `install_only` archives unpack into a directory — `cpython-3.10.12+20230726-aarch64-apple-darwin-install_only.tar.gz` (published SHA-256 `bc66c706ea8c5fc891635fda8f9da971a1a901d41342f6798c20ad0b2a25d1d6`, the historical patch level) or current `cpython-3.11.17+20261001` / `3.10.22+20261001`.
- ffmpeg candidates (installed; `-version` only):
  Homebrew 8.1.1 — `ffmpeg` `00d01197255300c02122c783dd0126a9e7f47d6c6a19faafae2e6610efd071d3`, `ffprobe` `daba6e06838d10260602536a676069cef6d756345e1c6d66268ceb7f2d5e7c39`; libavcodec 62.28.101, libswresample 6.3.101, libswscale 9.5.101; formula **unpinned and outdated** (stable 9.0.2).
  MacPorts 4.4.6 (`ffmpeg @4.4.6_4+gpl2`) — `ffmpeg` `18a94e5c7e165ac0c838e21b75fc8e83009de54e4eb3a4923c60618857aff4f0`, `ffprobe` `5aeec8bb74b582435f0798a9f5b108db9dea7ad03fd06ba970301ab781ad1872`; libavcodec 58.134.100, libswresample 3.9.100, libswscale 5.9.100 (the 4.4.2 library generation; a different build).
  Both link shared libav* libraries, so the library files are part of the identity.
- Machine-wide discovery (2026-10-02, read-only; Macintosh HD and every mounted volume): no
  Python 3.10 or 3.11 environment anywhere (including the 2026-07-09 Time Machine copy); no numpy
  2.2.6 installation or cached wheel; no ffmpeg 4.4.2 build. MacPorts ffmpeg 4.4.6 (and its
  retained package archive `ffmpeg-4.4.6_4+gpl2.darwin_25.arm64.tbz2`) remains a candidate only.
- **Storage constraint:** the internal Macintosh HD Data volume is ~97 % full (≈12 GiB free) and is
  unsuitable for D2 environments or fixture work. Any D2 environment or fixture workspace must be
  proposed on WE_CAPE_OUTPUT or another explicitly authorized volume, never placed silently on the
  internal Data volume. D2 remains HELD; nothing has been installed.
- Fixtures that choose empirically: `produce_audio_rms.py` on `Filmage_Editor.mp4` vs reference `1af3e65f` (bitwise) chooses the ffmpeg build (decode + resample); `step0_offset.py` on the 08-22 inputs vs `STEP0_TIMING_CLOSURE.md` chooses numpy/BLAS/RNG fidelity. `fcpx_resolve.py` / `derive_camera_runs.py` are standard-library only.

## 10 · Proposed first-wave fixtures (Wave 1; not created)

| producer | inputs (existing, hash-bound) | expected | needs |
|---|---|---|---|
| `fcpx_resolve.py` | 08-22 lock FCPXML `2bf06853…`, ETC `P2_LOCK_timing.json` `e91318a6…` | `VALIDATED` 191/191, exit 0 (ECR-GEN-002 E1); 2 identical runs; no undeclared writes | fixture-spec authority; negative ETCs (E2–E4) are derived files and need creation authority |
| `derive_camera_runs.py` | the resolver output of the fixture above | deterministic `camera_runs.json`; synthetic clip-name cases | a small synthetic name-list fixture under authority |

Wave 2 (`produce_audio_rms.py`, `step0_anchors.py`) and Wave 3 (`step0_offset.py`) wait on
the D2 selection; `produce_video_obs.py` stays deferred (§8.1).
