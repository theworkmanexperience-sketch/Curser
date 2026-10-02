# W.E. C.A.P.E. Build Status and Internal Launch Roadmap

| | |
|---|---|
| **Status** | DRAFT — CHAIRMAN REVIEW |
| **As-of date** | 2026-10-02 |
| **Repository baseline / HEAD** | `origin/main` `106fd837f884aac7b9cabcfc94a427cba5b242fc` |
| **Purpose** | Internal build-status and launch-readiness record |

> **Reading this document.** Sections 1–7 and 10–11 state **historical fact** as recorded in the repository, its
> rulings and committed qualification evidence. Sections 8–9 are a **roadmap**: every forward milestone, effort band
> or T+n marker is a **PLANNING TARGET — NOT GOVERNING DEADLINE**. Commit IDs and hashes in this document were
> filled programmatically from the repository and the recorded evidence files at the baseline above.

---

## 1. Executive summary

W.E. C.A.P.E. can now take a real production — Alpha RoundUp Part 2 — and hold its whole editorial record under
governed, hash-bound custody: source, picture lock, caption stream and timing contract. When the edit changes, it
re-derives the editorial structure mechanically. The 08-24 recut was absorbed this way: every affected beat was
re-derived and individually ruled (R1–R9); the canonical TIMELINE (v1.1.0) and Emotional Progression
Registry (EPR-001 v1.15.0) were ratified on 2026-10-01; and the 08-24 source and context were
ingested on 2026-10-02. On the engineering side, the producers that turn source material into factual
observations are being qualified one at a time against historical known-good output. Three are now **EFFECTIVE**
(timeline resolver, camera-run derivation, semantic anchors), each bound to its exact code and runtime identity.

What remains is gated, not broken. The audio producer is deterministic, but no available decoder reproduces the
historical measurement bit-for-bit, so it was correctly not qualified and no tolerance was invented. The
timing-offset producer depends on that audio decision; the video producer awaits an HDR semantic ruling; observation
generation is fenced by the Decision D gates (S19, BLOCKED classes, G-01–G-09); and both downstream regeneration
holds remain **HELD**. The immediate infrastructure milestone is the **24 TB operational backup drive**: the capacity
analysis sized the in-scope backup set at about 9.55 TB, and the historical audio oracle that audio qualification
depends on currently exists as a **single copy**, with custody **HELD** for want of an established backup target.
The shortest governed path is: drive → oracle custody → audio, offset and video qualification → D4/D5 →
observations → D6 → hold release → regeneration → end-to-end validation → internal launch.

---

## 2. Authoritative baseline

| Item | Current state | Identity (from repository) |
|---|---|---|
| `origin/main` HEAD | Addendum G custody | `106fd837f884aac7b9cabcfc94a427cba5b242fc` |
| TIMELINE_REGISTRY | **v1.1.0 RATIFIED** 2026-10-01 (`096d127`) | file `510697b9bbd1ed01…` |
| EPR-001 | **v1.15.0 RATIFIED** 2026-10-01 (`de0c902`); v1.14.0 and v1.13.0 kept in `superseded/` | file `add0d88ff52b5c65…`; ratified proposal `f0650a04…` (`f8f74eb`) |
| Decision A | **APPROVED** — 08-24 observation source `Alpha RoudUp Part 2.mov` | `ff34278fe1f47f67…` |
| Decision C | **APPROVED as corrected**, ingested | Commit A `41d0ea1` (ingestion) + Commit B `795a847` (provenance closure); successor ETC `declared_lock 01:18:09:11`; `regeneration_scope CANONICAL_EDITORIAL_TIMELINE` |
| Decision B | **Conditionally approved; incomplete** | 3 of 6 designated producers EFFECTIVE (Addenda E/F/G) |
| Decision D | **ADOPTED** as the pre-observation gate; not satisfied | — |
| Regeneration holds | **v1.14.0 and v1.15.0 both HELD** | Addendum D §1; EPR `regeneration_trigger` |
| Storage / custody | Candidate A toolchain and qualification workspaces outside Git on WE_CAPE_OUTPUT; historical RMS oracle custody **HELD** (single copy) | oracle `1af3e65f…` |

---

## 3. Completed milestones (historical fact)

Dates are commit dates on `origin/main` unless the governing record states an operative date.

| Date | Milestone | Resulting capability | Governing record | Status |
|---|---|---|---|---|
| 2026-08-22 | Sprint 3A run; 08-22 artifacts generated | Historical baseline: inputs pinned, ETC binding 191/191, Step 0 timing closure, DIE-V, ESS, Conductor's Score | `3fe7365`, `8f70dee`, `EXECUTION_LOG.md`, RE-001 (`567d0e5`) | COMPLETE |
| 2026-08-22 | ER-004 Amendment 1: Primary Sources vs Governed Artifacts | Evidence is immutable; products regenerate | `d7ebbc0` | COMPLETE |
| 2026-08-24 | Second cut of Part 2 discovered (157.125 s shorter, diverges at 00:03:27) | Triggered custody alert → rebase, re-derivation, ingestion, B-3 requirements | `7771e44` | COMPLETE |
| 2026-08-26 | EPR-001 ratified and implemented | Canonical emotional-progression registry | `f133d89` | COMPLETE |
| 2026-08-28 | **EPR-07 retired** (Q10 RETIRE adjudicated 2026-08-28; custody `c7b5d3a` recorded 2026-08-29 UTC) | Out-of-scope beat retired, not deleted | Addendum C §1 | COMPLETE |
| 2026-08-29 | ECR-GEN-001 / ECR-GEN-002 | Parameterized generator (v1 == v2 byte-identical); validator and runtime guards; audio RMS recipe reproduced bitwise (E15) | `cfae47d`, `57c9ed1` | COMPLETE |
| 2026-08-31 | ED-003 picture lock; CF-001 canonical caption stream (08-24 lineage) | Designated 08-24 editorial sources | `3bc4f93`, `aaf0117` | COMPLETE |
| 2026-09-29 | **EO-2026-09-29**: B-5 mechanical re-derivation authorized; B-6 STAGED READING 3; B-14 into the decision packet | Governed rebase path | `3d14d5b`; packet `aec3a27` | COMPLETE |
| 2026-09-29 | Addendum A (B-5 tiered; B-14 CLOSED-MOOT); Addendum B (F-2 context repair, G8 structural-only) | Tiered review; context repaired | `31c6e9b`, `28957f8` | COMPLETE |
| 2026-09-29 – 2026-09-30 | F-5 / G-07 declared expectation; B-7 proxy designation | 23 out-of-range elements declared | `ad05e85`, `e966f8a` | COMPLETE |
| 2026-09-30 | R1–R8 PRESERVE; G8 v2 mapping ratified (`5bd4af48…`) | Corrected structural mapping governs | `2b3416f` … `1a80d2a`, `1f806de` | COMPLETE |
| 2026-10-01 | R6 re-ruled REVISE-BOUNDARY: **S14 end 3247.583333s / 00:54:07:14 / frame 77942**; **R9 MOOT** — R1–R9 closed | All nine review cells closed | `2f814a1`, `ee515d1` | COMPLETE |
| 2026-10-01 | **TIMELINE v1.1.0 + EPR-001 v1.14.0 RATIFIED** | Canonical 08-24 temporal authority | `c9fa343` → `096d127` | COMPLETE |
| 2026-10-01 | PBC reconciliation + Addendum C (EPR-07 rationale correction) → **EPR-001 v1.15.0 RATIFIED** | PBC lifecycle reconciled; EPR-07 remains retired | `f8f74eb` → `de0c902` | COMPLETE |
| 2026-10-01 / 2026-10-02 | Addendum D: Decisions A–D (ruling dated 2026-10-01, §4 2026-10-02) | Observation/ingestion authority; producer gates | `41d0ea1` | COMPLETE |
| 2026-10-02 | Decision C ingestion (Commits A/B) | Hash-bound 08-24 context | `41d0ea1`, `795a847` | COMPLETE |
| 2026-10-02 | ECR-GEN-003 (path parameterization, sidecars, harness) | Reproducible, auditable producers | `e0a346a` | COMPLETE |
| 2026-10-02 | Wave 1 → **Addendum E** | `fcpx_resolve.py` | `1def9ea` → `894aff6` | EFFECTIVE |
| 2026-10-02 | ECR-GEN-004 → **Addendum F** | `derive_camera_runs_v2.py` (UNCERTAIN fallback) | `f2c6e2e` → `bc32e85` | EFFECTIVE |
| 2026-10-02 | Candidate A provisioned (outside Git) | Pinned CPython/NumPy runtime | prefix manifest `07f2ce26…` | COMPLETE |
| 2026-10-02 | Wave 2A → **Addendum G** | `step0_anchors.py` under Candidate A | `d491e1d` → `106fd83` | EFFECTIVE |
| 2026-10-02 | Wave 2B (F1/F2 audio) | Neither decoder reproduces the oracle | external workspace only | NOT QUALIFIED |
| 2026-10-02 | Historical RMS-oracle custody | No established writable backup target | — (no repository change) | HELD |
| 2026-10-02 | Backup capacity analysis | 24 TB operational backup sized | analysis only | COMPLETE (purchase OPEN) |

**Continuing role of 08-22.** The 08-22 package is the **qualification oracle** (known outputs for every producer
qualification), **historical producer evidence** (pre-ECR behaviour), the **regression fixture** (byte-identity) and the
**comparison basis** for 08-24 re-derivation. It is immutable under ER-004.

---

## 4. Testing and operational phases

| Phase | Purpose | Capability proven | Key tests / evidence | Governance alignment | Current status | Remaining exit condition |
|---|---|---|---|---|---|---|
| **0 — Historical evidence baseline** | Known-good fixtures and oracles | Reproducible fixtures, known-output oracles, regression comparison, source/measurement provenance | `EXECUTION_LOG.md` input hashes; RE-001; ECR-GEN-001 (7/7 byte-identical); ECR-GEN-002 (22 pass) | ER-004 immutability | COMPLETE | Oracle custody (B2) |
| **1 — Temporal/editorial rebase** | Map 08-22 structure onto the 08-24 lock | G8 v2 mapping; R1–R8 PRESERVE; S14 boundary corrected; R9 MOOT; TIMELINE/EPR regenerated and ratified | v2 validation 19/19 PASS (`0db0821`); `096d127` | Per-row Chairman disposition, verbatim | COMPLETE | — |
| **2 — Registry governance** | Proposal → validation → remote custody → ratification | Superseded versions kept byte-identical; canonical TIMELINE/EPR; PBC lifecycle reconciled; EPR-07 rationale corrected | `superseded/` copies; `f8f74eb` → `de0c902` | Proposal before ratification | COMPLETE | — |
| **3 — Source ingestion (Decision A + C)** | Hash-bound 08-24 sources | Observation source designated; successor ETC (lock 01:18:09:11); manifest repaired; provenance-closure commit; no proxy generated | `41d0ea1`, `795a847`; context `git_commit` = Commit A | Hash-bound identity; incumbent ETC kept | COMPLETE | — |
| **4 — Producer engineering** | Reproducible, auditable producers | Path parameterization; deterministic sidecars (`b3-provenance/1`); hidden-write detection (`b3_qualify.py`); semantics preserved (AST checks); versioned successor for semantic change | `ecr_gen_003_static_check.py`, `ecr_gen_004_static_check.py` | Semantic change ⇒ new identity + requalification | COMPLETE (ECR-GEN-003, ECR-GEN-004) | Per-producer requalification |
| **5 — Producer qualification and activation** | Per-producer authority | 3 producers EFFECTIVE | Wave 1, ECR-GEN-004, Wave 2A evidence; Addenda E/F/G | Qualification ≠ activation | PARTIAL | See §5 producer table |
| **6 — Numeric/media toolchain** | Pinned runtime | Candidate A frozen and deterministic; F1/F2 deterministic but not historical | Wave 2A; Wave 2B (external workspace) | Runtime-bound activation; no silent tolerance | PARTIAL | Decoder lineage (B3) |
| **7 — Observation pipeline** | Factual 08-24 observations | Measurement separated from adjudication (by design) | — | Decision D | OPEN | D2 (producers), D4, D5, D6 |
| **8 — Guard/generator readiness** | Safe generation on 08-24 | Guards exist (ECR-GEN-002) | G-07 expectation declared (23) and present in the 08-24 context | Fail-closed | OPEN | D6 dry-run and known defects |
| **9 — Downstream regeneration** | Regenerate governed artifacts | — | — | Regeneration holds | HELD | Hold release |
| **10 — Internal operational launch** | Controlled internal production use | — | — | — | OPEN | B14–B16 |

**Phase 1 note.** With the temporal authority stable, S01–S18 are fixed in 08-24 seconds, EPR beats reference
ratified segment spans, and observation producers and generators have a single canonical timebase. S16: R8 PRESERVE
(bike_night_arrivals, 08-24 temporal rebase only). No separate S16 correction transaction beyond R8 and the rebase is
recorded; the 08-22 VCONF-01 finding remains historical.

**Phase 3 note.** Any B-3 producer may now read the exact designated sources, re-verifying SHA-256 before every
read, against a hash-bound context.

**Phase 7 note.** `AR2-0824.observations.json` does not exist. Decision D prohibits its generation until Decision B
is fully effective (D2), an S19 disposition exists (D4), every BLOCKED class is re-derived or explicitly declared
NOT_OBSERVED (D5), and G-01–G-09 pass (D6). No placeholder values are permitted, and absence of authority is not
NOT_OBSERVED.

**Phase 8 note (only what the repository shows).** G-07's expectation is declared (`ad05e85`) and
`expected_out_of_range_n = 23` is in the 08-24 context; **no 08-24 dry-run of G-01–G-09 is recorded.**
`gen_artifacts_v2.py` still carries hard-coded 08-22 narrative values and references `TIMELINE_REGISTRY version 1.0.0`
(canonical is v1.1.0). The generator and guards were last changed 2026-08-29. EPR
`segment_ref`/timecode safety and downstream regeneration correctness are not shown as corrected.

**Phase 9 (future).** Regenerate governed downstream artifacts (CONDUCTOR_SCORE, EDITORIAL_SYNCHRONIZATION and
others) under canonical registry and source authority; stale R75/R68–R75 lineage references are reconciled only where
separately authorized.

**Phase 10 definition.** Internal launch = stable governed ingestion; required B-3 producers EFFECTIVE; executable
observation pipeline; guards passing; reproducible downstream generation; verified backup and custody; complete
runbook; launch validation passed. It is **not** external commercialization.

---

## 5. Producer status (Phase 5)

| Producer | Role | Engineering | Qualification | Activation | Runtime binding | Permitted capability | Remaining blocker |
|---|---|---|---|---|---|---|---|
| `fcpx_resolve.py` `faacec8b…` | FCPXML → resolved timeline, ETC binding | ECR-GEN-003 | Wave 1 PASS | **EFFECTIVE under B-3 — Addendum E** | CLT CPython 3.9.6 `bdea5901…` | Resolution and ETC validation | — |
| `derive_camera_runs.py` `178ca2b0…` | Historical camera runs (COMPOUND fallback) | ECR-GEN-003 | Wave 1 PASS (historical) | **Preserved / inactive** (historical only) | — | None | Superseded by v2 |
| `derive_camera_runs_v2.py` `ec253c05…` | Camera runs, UNCERTAIN fallback | ECR-GEN-004 | PASS | **EFFECTIVE under B-3 — Addendum F** | CLT CPython 3.9.6 `bdea5901…` | Mechanical family transcription | — |
| `step0_anchors.py` `66079f2a…` | SRT ↔ title anchors | ECR-GEN-003 | Wave 2A PASS (0.784 clarified as non-producer) | **EFFECTIVE under B-3 — Addendum G** | Candidate A, complete prefix manifest `07f2ce26…` | Anchor rows plus provenance sidecar | — |
| `produce_audio_rms.py` `df656716…` | Audio RMS envelope | ECR-GEN-003 | **NOT QUALIFIED** — F1 (475 samples, ≤4 ULP) and F2 (4,169 samples, ≤7 ULP) both miss the historical bitwise oracle | **NOT EFFECTIVE** | — | None | Oracle custody; decoder lineage |
| `step0_offset.py` `64343354…` | Envelope cross-correlation offset | ECR-GEN-003 | Not run | **NOT EFFECTIVE** | — | None | Downstream of the RMS-lineage decision (Branch H/R); NumPy/RNG/BLAS qualification; D4 |
| `produce_video_obs.py` `946941d4…` | Video observables | ECR-GEN-003 | Not run; never fixture-equivalent (ECR-GEN-002: 3 of 9 columns unrecovered) | **NOT EFFECTIVE** | — | None | HDR/BT.2020-PQ 08-24 semantic qualification |
| `die_v_observables.py` | DIE-V thresholds | — | — | **Excluded from B-3 designation** — performs threshold-derived classification (Decision B) | — | — | Not designated |

### Phase 6 — Candidate A and Wave 2B

- **Candidate A:** isolated CPython 3.10.12 (`3a855bd1…`) + NumPy 2.2.6 (wheel `8e41fd67…`;
  scipy-openblas 0.3.29 bundled within the installed-file manifest `36fa915d…`), frozen by a
  3139-file deterministic prefix manifest, deployed on WE_CAPE_OUTPUT outside Git. **Proves:** stable,
  deterministic execution and `step0_anchors.py` behaviour. **Does not prove:** BLAS/RNG fidelity for
  `step0_offset.py`, or anything about ffmpeg.
- **Wave 2B:** F1 (MacPorts 4.4.6) and F2 (Homebrew 8.1.1) are each byte-deterministic with `.npy` headers identical
  to the oracle, but their values differ (475 vs 4,169 differing samples; F2 materially farther).
  Pre-ECR and current producers are byte-identical under each decoder. **Neither decoder qualified; no tolerance was
  introduced.** The historical decoder recorded in `EXECUTION_LOG.md` is ffmpeg `4.4.2-0ubuntu0.22.04.1` (Ubuntu, arm64);
  its packages remain obtainable with verified checksums but it has not been reconstructed.

---

## 6. Aligned Governance

- **Fail-closed operation** — discrepancies stop execution rather than being silently normalized.
- **Immutable historical evidence** — 08-22 outputs, superseded registries and the incumbent ETC are kept byte-identical.
- **Proposal before ratification** — `-PROPOSED` → validation → Chairman ratification.
- **Remote custody before activation/ratification** — evidence commits precede Addenda E/F/G.
- **Hash-bound identity** — sources, producers, runtimes, fixtures and outputs are explicitly identified.
- **Producer-specific authority** — qualification ≠ activation; no inheritance between producers.
- **Runtime-bound activation** — e.g. Addendum G binds the complete Candidate A prefix.
- **Versioned semantic successors** — `derive_camera_runs_v2.py`, not an edit of v1.
- **Measurement ≠ adjudication** — observation producers cannot make editorial/Executive decisions.
- **Scope isolation** — one transaction addresses one authorized objective.
- **No silent tolerance** — historical measurement mismatches are not accepted because they are numerically small.
- **External custody separation** — source, operational backup, archive and testing/toolchain storage have distinct roles.
- **Regeneration holds** — v1.14.0 and v1.15.0 remain HELD until explicit prerequisites pass.

---

## 7. What W.E. C.A.P.E. Can Do Today

**Operational now**
- Governed custody of production sources, picture lock, captions and ETC, with hash verification.
- Mechanical temporal re-derivation and per-row adjudication when an edit changes.
- Canonical, ratified TIMELINE v1.1.0 and EPR-001 v1.15.0, with superseded-version preservation.
- EFFECTIVE B-3 producers: timeline resolution with ETC validation, camera-run derivation, semantic anchors.
- A qualification harness: determinism, hidden-write audit, provenance sidecars.

**Technically proven but not yet operationally authorized**
- Deterministic audio RMS production under F1 or F2 — not historically faithful, so not authorized.
- Historical Ubuntu decoder reconstruction — feasible on paper, packages verified, not executed.

**Still under development / gated**
- `step0_offset.py`, `produce_video_obs.py`; observation generation (Decision D); D6 guard dry-run and generator
  corrections; downstream regeneration (HELD); backup and recovery procedure; internal-launch runbook.

---

## 8. Backup-drive milestone

- **Operational backup (this milestone):** a verified second copy of the in-scope source and custody set. The
  read-only capacity analysis (2026-10-02) sized the payload at about 9.55 TB → **24 TB** (≈40% initial use;
  case-sensitive APFS per `STORAGE_RISK_AND_BACKUP_PLAN.md`; additive-mirror behaviour of `mirror_verify.sh`).
- **Archive/offload capacity:** the storage plan's multi-year 2× drive / 3-2-1 discussion — a future infrastructure
  note only, outside this build timeline.
- **Test/toolchain workspace:** remains on WE_CAPE_OUTPUT (Candidate A, qualification workspaces).

---

## 9. Roadmap — post-backup-drive path to internal launch

> **PLANNING TARGET — NOT GOVERNING DEADLINE.** T+0 = backup drive received. No calendar dates are committed: no
> delivery date is in the record, and most phases depend on Chairman rulings. Effort bands apply only once each
> prerequisite ruling exists.

| # | Milestone | Scope | Exit | Depends on | Effort band |
|---|---|---|---|---|---|
| **B0** | 24 TB backup drive acquired | — | Drive on hand | Purchase | — |
| **B1** | Backup drive qualification and designation | Identify; format under approved policy (case-sensitive APFS); record serial/UUID/capacity; SMART/health baseline; read/write verification; designate operational-backup role | Backup target is governed and ready | B0; Chairman designation | <1 day |
| **B2** | Historical RMS oracle custody closure | Re-verify oracle; verified second copy; SHA-256 equality; custody record (`docs/engineering/`) | Durable independent custody | B1 | <1 day |
| **B3** | Audio historical-environment decision | Decide whether historical decoder reconstruction is required; if approved, compare it with F1/F2; or govern a successor measurement lineage | `produce_audio_rms.py` qualifies, or receives an explicitly governed alternative disposition | B2; Chairman ruling | Dependent on ruling (2–5 days if reconstruction approved) |
| **B4** | Audio producer evidence custody + activation | Compact evidence; separate activation of the exact producer/runtime/decoder identity | `produce_audio_rms.py` EFFECTIVE under B-3 | B3 PASS | <1 day each |
| **B5** | `step0_offset.py` qualification | RNG/NumPy/BLAS behaviour; historical oracle; deterministic reruns; hidden-write audit | Technically qualified exact identity | B3/B4 (Branch H or R ruled) | 1–2 days |
| **B6** | `step0_offset.py` activation | Separate governance transaction | EFFECTIVE, subject to D4/S19 limits | B5 | <1 day |
| **B7** | Video/HDR producer ruling and qualification | HDR/BT.2020-PQ behaviour; semantics; approved fixture; streaming equivalence; determinism | `produce_video_obs.py` EFFECTIVE or explicitly excluded/deferred | Ruling | Dependent on ruling |
| **B8** | D4 / S19 observation disposition | S19 observation treatment only | Unambiguous segment scope | Ruling | Dependent on ruling |
| **B9** | D5 BLOCKED-class dispositions | Each class re-derived or explicitly declared NOT_OBSERVED | Every required class governed | Rulings | Dependent on ruling |
| **B10** | Observation generation | `AR2-0824.observations.json` from activated producers and approved sources only | Deterministic, hash-bound observation package | B4, B6, B7, B8, B9 | 1–2 days |
| **B11** | D6 guards / generator correction | G-07; G-01–G-09 dry-run; hard-coded 08-22 assumptions; TIMELINE-version references; segment_ref/timecode safety | Full dry-run passes, no unauthorized semantic change | B10 (ECR) | 2–5 days |
| **B12** | Release regeneration holds | — | Explicit Chairman authorization to regenerate | B10, B11 | Dependent on ruling |
| **B13** | Controlled downstream regeneration | Approved artifacts; determinism; provenance; registry authority; no stale mappings; no unauthorized lineage change | Regenerated artifacts in custody | B12 | 1–2 days |
| **B14** | End-to-end validation | source → ingestion → resolution → observation → guarded generation → downstream artifacts; deterministic rerun; hashes; no hidden writes; provenance; backup verification; STOP behaviour tested | E2E PASS | B13, B1 | 2–5 days |
| **B15** | Internal launch readiness | Operator runbook; system status matrix; active-producer registry; backup/recovery; incident/STOP; known limitations; source-ingestion procedure; validation checklist | Package complete | B14 | 2–5 days |
| **B16** | **W.E. C.A.P.E. internal launch** | The governed system is available for controlled internal production use, with an approved source-to-output workflow and reproducible recovery path | Launched (internal; not external commercial launch) | B15 | — |

**Schedule.** Completed dates are those in §3 (Git and rulings). Forward: B1–B2 ≈ T+1 day; B3 onward is dependent on
ruling. Any later calendar estimate must carry the label PLANNING TARGET — NOT GOVERNING DEADLINE.

---

## 10. Readiness matrix

| Area | State |
|---|---|
| Governance (EO-2026-09-29, Addenda A–G) | COMPLETE (in force) |
| Source custody (08-22 inputs; Decision A source) | COMPLETE |
| Registries (TIMELINE v1.1.0, EPR-001 v1.15.0) | COMPLETE |
| Ingestion (Decision C) | COMPLETE |
| Resolver (`fcpx_resolve.py`) | EFFECTIVE |
| Camera runs (`derive_camera_runs_v2.py`) | EFFECTIVE |
| Anchors (`step0_anchors.py`) | EFFECTIVE |
| Audio RMS (`produce_audio_rms.py`) | BLOCKED (not qualified; oracle custody HELD) |
| Timing offset (`step0_offset.py`) | BLOCKED (waits on audio lineage) |
| Video observations (`produce_video_obs.py`) | OPEN (HDR ruling) |
| Observation package | BLOCKED (Decision D) |
| Guards (G-01–G-09) | OPEN |
| Generator | OPEN (known 08-22 literals, version references) |
| Downstream regeneration | HELD |
| Operational backup | OPEN (24 TB drive) |
| Recovery | OPEN |
| Internal launch | OPEN |

---

## 11. Risks / dependencies

- Backup drive availability (gates B1, B2).
- Historical RMS oracle custody — single copy, HELD.
- Audio decoder fidelity — neither available decoder reproduces the oracle.
- `step0_offset.py` downstream dependency on the RMS lineage (Branch H vs R).
- HDR/video semantic qualification.
- S19 / D4.
- BLOCKED observation classes / D5.
- D6 guard/generator readiness.
- Regeneration holds (v1.14.0, v1.15.0).

---

## Immediate Next Milestone

Acquire and qualify the approved 24 TB operational backup drive, then close the held RMS-oracle custody transaction.

## Path to Internal Launch

24 TB backup → oracle custody → audio qualification → offset qualification → video/HDR qualification → D4/D5 → observations → D6 guards/generator → release holds → regeneration → E2E validation → internal launch
