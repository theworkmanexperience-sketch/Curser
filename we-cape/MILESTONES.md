# W.E. C.A.P.E. — Engineering Overview & Milestones
## For a software engineer asking: "is this real, or vibe-coding?"
### Living doc · v1.1 · 2026-07-07

An honest, evidence-based read for a developer evaluating this codebase. It links
claims to the **mechanism that enforces them**, because an engineer should trust
specifics, not adjectives. It also states, plainly, where the maturity **isn't** yet
contract-grade. Milestone status is at the bottom.

---

## TL;DR (the honest verdict)

- **On engineering discipline: yes, this is beyond vibe-coding.** It has explicit
  invariants that are *enforced by tests and code*, deterministic behavior validated on
  real data, a clean engine/ops separation, verified data-integrity, honest failure
  modes, and a 384-test suite that includes corruption and equivalence tests — not just
  happy paths.
- **On operational maturity: partially.** It is solo-developed and single-machine. There
  is **no automated CI/CD** (tests are run on demand), **no code signing/notarization**,
  no external security audit, and some tooling is validated in a Linux sandbox rather than
  on the target Mac. Those are the gaps between "engineered like production software" and
  "shipped, audited, contract-deployed."

So: the **practices** are contract-grade; the **release/operational envelope** is still
early. The rest of this doc shows why.

---

## The tells: vibe-coding vs. this

| Vibe-coding tends to… | This codebase… |
|---|---|
| Assert behavior, hope it holds | Encodes invariants (P1–P7) **enforced by tests/guards** |
| Test the happy path only | Tests **corruption, mismatch, conflict, and failure** paths explicitly |
| Trust inputs (labels, filenames, users) | Derives truth from **data/metadata**, treats human/label input as a weak hint |
| Silently "work" on bad input | **Hard-fails / refuses**: hash mismatch, unsafe backup target, ambiguous identity |
| Couple everything | Deterministic **engine** vs. read-only **ops tools**, joined only by defined seams |
| "It ran, ship it" | **Verifies against reality** (production runs, live topology) and records provenance |

---

## Invariants, and how each is *enforced* (not just claimed)

The platform commits to seven principles (P1–P7). What makes them engineering rather
than aspiration is that each has a concrete enforcement mechanism:

- **P1 Determinism** — identical input + config ⇒ identical output.
  *Enforced by:* an **engine-equivalence test** that runs the legacy and re-wired
  pipelines on synthetic multicam footage and asserts identical output; validated again
  on real DJI footage (identical proxy trees).
- **P2 Privacy / zero-network engine** — the core makes no network calls.
  *Enforced by:* `test_no_network.py`, an **AST scan** that fails the build if any
  network-capable import appears in `wecape/`. Not a convention — a test.
- **P3 Auditability** — every run and decision is traceable.
  *Enforced by:* per-run manifests (JSON/HTML/XML), a session audit JSONL, and camera
  identity that records **how** each `camera_id` was derived (metadata vs. label vs.
  human override) — provenance, not just a value.
- **P4 Extensibility without coupling** — new stages never modify existing ones.
  *Enforced by:* `PipelineStage` + `SyncAdapter` ABCs as real seams; ops tools in
  `scripts/` are read-only/additive and never import engine internals.
- **P5 Registry continuity** — enrichment is never overwritten or nulled.
  *Enforced by:* `INSERT … ON CONFLICT DO UPDATE` with `COALESCE` (field-preserving
  upsert) + empty-run pruning; covered by preservation tests.
- **P6 Staged intelligence** — AI is additive, never foundational; v1 ships zero AI.
- **P7 Creator data sovereignty** — local-first; full-fidelity data stays local, PII
  (GPS, filenames) is hashed on egress (`sha256:` path hashing) with tests.

Every one is verifiable by reading the named test or module.

---

## Test posture

- **384 tests, currently green**, run via a pytest-free harness so the gate has no
  external dependency. New features require tests before merge.
- **Failure-path coverage, not just happy path:** SHA-256 mismatch detection, backup
  restore-drill failure on a corrupted copy, identity **conflict-stop** when a card label
  contradicts the footage, a backup **guard that refuses** to write to a boot/read-only
  volume, fail-fast pre-flight checks.
- **Equivalence & invariant tests:** legacy-vs-rewired engine equality; the network AST
  guard; registry field-preservation; schema-migration tests (v1→v2→v3, lossless).
- **Shell tooling is tested too:** the backup primitives are exercised by Python
  subprocess tests (copy, verify, corruption detection, guard refusal).

---

## Architecture: the seams that matter

- **Deterministic core (`wecape/`)** — ingest → classify → group → variants → proxy →
  registry, driven through a `run_stages()` orchestrator over the `PipelineStage` ABC.
- **Read-only / additive ops layer (`scripts/`)** — dashboard, Health Report, FCPXML
  export, verified offload, New-Shoot wizard/GUI, camera identity, backup tooling. These
  **observe and add**; they never mutate engine output or the deterministic path.
- **Typed data layer** — SQLite registry with an explicit schema, versioned migrations,
  and lineage fields (`source_clip` / `source_clip_sha`).
- **Injected dependencies for testability** — registry writer, sync adapter, and external
  tools (exiftool/ffprobe/rsync) are injected, so logic is unit-tested without hardware or
  those binaries present.

---

## Data-integrity engineering (the "don't lose the asset" discipline)

- **Verified copies:** offload and backup re-read written bytes and compare **SHA-256**;
  a copy that didn't land byte-for-byte is a **hard failure**, never a silent pass.
- **Restore-testing:** backups are *proven restorable* (checksum a canary restored from
  the target), logged to `RESTORE_TESTS.md` — a backup you haven't restored is a rumor.
- **Guards that refuse unsafe operations:** the footage backup won't write unless the
  target is a real, writable, mounted volume (prevents the boot-disk "stray folder" trap
  and read-only-volume writes); it also **fails loudly** if `--offsite` is passed without a
  `--remote` (so an offsite push can't silently upload nothing), stops **cleanly** at
  Google's daily upload cap instead of storming 403s, and excludes app cruft from offsite.
- **Footage-first identity:** derived from embedded metadata (serial / DJI model code)
  over filenames over the volume label; a label that contradicts the footage is a
  **conflict that stops and asks**, not a silent mislabel.

---

## Validated against reality (not just against itself)

- **Production runs:** O-SIX RYDERZ MC (95 files, 2 groups, 0 errors), reproduced across
  engine rewrites; NVMe performance gate passed (48.8 min / 100 files).
- **Verifying, not assuming, caught real bugs:** a camera whose clock was wrong (Insta360
  clips dated 2018), DJI's model codes being **offset** from the marketing name
  (AC004 = Action 5 Pro), a SanDisk card whose **label lied** about its contents, and a
  live-topology check that corrected two stale assumptions in the storage plan.
- **Byte-for-byte verify caught a case-collision the backup target couldn't represent:**
  the source (case-sensitive APFS) holds **two distinct files**, `IMG_7893.MOV` (90.9 MB)
  and `IMG_7893.mov` (86.2 MB); the case-**insensitive** backup volume can store only one, so
  one clip was silently absent from the copy. The SHA-256 pass flagged it among **86,645**
  files — a size+mtime sync to a case-insensitive target would have shipped an incomplete
  backup silently. Fix: a backup drive must be formatted **case-sensitive APFS** to faithfully
  mirror a case-sensitive source. (This also corrected an earlier misdiagnosis of the same
  file as a "truncation" — verifying against reality caught the wrong story, too.)
- **Documented deviations with justification:** e.g. the grouping window ±15s vs. the
  spec's ±5s is an empirically-validated field calibration, recorded as an intentional
  deviation — not an accident.

---

## Where it is NOT (yet) contract-grade — stated plainly

- **No automated CI/CD.** The suite is strong but run on demand, not on every push.
- **No signed/notarized distributable.** No Apple Developer signing or packaged `.app`.
- **Solo-developed, single-machine.** No external code review, no multi-user/concurrency
  hardening, no formal SLA.
- **No independent security audit / pen-test.** The threat model
  (`SECURITY_RISK_ANALYSIS.md`) is self-authored (data-loss-first, correct for the use
  case) but not externally reviewed.
- **Some tooling sandbox-validated only.** Shell/GUI tools pass Linux-sandbox tests and
  syntax checks; a few need a visual/live pass on the target Mac.
- **No formal acceptance gate.** A contract-grade *Technical Specification* exists, but
  quantitative acceptance thresholds (e.g. RFQ Test 6 / Appendix B) aren't yet wired into
  automated tests.

None of these contradict the verdict — they're the difference between **disciplined
engineering** and a **hardened, released, audited product.**

---

## Bottom line for an engineer

You are looking at a codebase built with the habits that distinguish real software:
explicit invariants enforced by tests, determinism proven by equivalence checks,
auditable provenance, verified data integrity, honest failure modes, and validation
against production reality — with a clean separation between a deterministic engine and a
read-only ops layer. That is unambiguously **beyond vibe-coding.**

To call it **contract-grade in the full sense**, the remaining work is operational, not
architectural: CI/CD, signing/packaging, external review/audit, and wiring formal
acceptance thresholds into the gate — milestone #5 below.

---

## Milestones (status)

Legend: ✅ done · 🔄 in progress · ⬜ not started

- ✅ **1. Foundational engine (CAPTURE v1)** — deterministic multi-cam ingest → grouping →
  proxies → SQLite registry. Production-validated (O-SIX: 95 files, 0 errors). 384 tests green.
  → *Engineer action items:* wire the suite into CI so the engine-equivalence + no-network
  invariants run on every push (today: on-demand); add the missing real-**multicam** grouping
  test (current grouping validation was single-camera — see the CLAUDE.md caveat).
- ✅ **2. Performance gate** — <90 min / 100 files; 48.8 min on NVMe + hardware decode.
  → *Engineer action items:* gate `benchmark_run.sh` in CI as a perf-regression check (fail
  the build if a 100-file run exceeds the <90 min / rate threshold) so a slowdown is caught
  automatically, not by eye.
- ✅ **3. Creator & ops tooling** — dashboard · Health Report · FCPXML export · verified
  offload · New-Shoot wizard (CLI + GUI) · footage-first identity + registry · camera discovery.
  → *Engineer action items:* run the GUI conflict-badge **visual pass** on the Mac (still
  pending); onboard the **OM System OM-1** (4th camera, found in Harley footage) via
  `probe_camera.py` + `cameras.yaml`; give `mirror_verify.sh` the same junk-exclude list as
  `backup_footage.sh`.
- 🔄 **4. Data resilience (3-2-1 backups)** — registry + legal docs 3-2-1 (restore-proven);
  backup tooling **hardened** (mount/writable guard + offsite-without-`--remote` fail-loud +
  daily-cap clean-stop + junk excludes; 384 tests green).
  **PRIORITY SUBSET DONE (~1.6 of ~8.5 TB — ≈19% by volume):** the three priority shoots
  (O-SIX Community Service, O-SIX 12TH, Harley) have verified LOCAL copies + offsite copies.
  Harley's offsite is **byte-for-byte verified** (`rclone cryptcheck`: 646/646 files, 0
  differences). Caveat: the case-insensitive interim NVMe can't hold case-collision pairs locally
  (e.g. Harley's `IMG_7893.MOV` vs `.mov`) — a case-sensitive backup drive is required for a
  faithful *local* copy; the offsite (rclone-crypt) already holds both.
  **BULK PENDING (~7 TB): the majority of originals still have ZERO second copy** and live only
  on the disk13 SPOF (`June 2024` 2.7 TB, `O-SIX RYDERZ` 777 GB, the `2024`/`2025` folders…).
  One enclosure failure still loses them — the founding risk is only *partially* retired.
  → *Engineer action items:* run the case-collision scan (`find "/Volumes/10TB" -type f |
  tr '[:upper:]' '[:lower:]' | sort | uniq -d`) to size the problem before formatting;
  extend junk excludes to the **local**
  mirror; add a mock-`rclone` test for the stop-on-limit + exclude path; when the drive lands,
  **format it case-sensitive APFS**, repoint `--target`, enable the launchd plist; retire the
  dead `timemachine` volume on disk13.
  **GATING (highest-leverage action left): buy a ≥12–24 TB drive (case-sensitive APFS)** for
  the full ~8.5 TB — see `STORAGE_RISK_AND_BACKUP_PLAN.md` for the growth rate + 2026–2029 sizing.
- ⬜ **5. Commercial readiness** — Apple Developer + code signing · packaged/notarized app ·
  entity/legal · landing page + domain · **CI/CD + external audit + formal acceptance gate.**
  → *Engineer action items:* stand up **CI/CD** (GitHub Actions running `run_tests.py` + the
  pytest-free harness on every push); Apple Developer account → **codesign + notarize**
  pipeline for the `.app`/`.dmg`; commission an **external security review** of
  `SECURITY_RISK_ANALYSIS.md`; obtain RFQ **Appendix B** and wire Test 6 quantitative
  thresholds into automated acceptance tests.
- ⬜ **6. AI intelligence stack (J1→J5)** — camera AI · quality/content tagging · audio
  alignment (PluralEyes-killer) · highlights + rough-cut XML · cross-project registry + API.
  → *Engineer action items:* design the **J1 camera-AI** stage against the existing
  `PipelineStage` seam — additive, P6, zero engine coupling (keep it behind the
  `_NullIntelligenceStage` default); mine the registry for labeled training data before any
  model work.
- ⬜ **7. Platform expansion** — W.E. EDIT (J4) · W.E. ARCHIVE (J5) · W.E. API public (J3).
  → *Engineer action items:* do **not** start until CAPTURE v1 ships + ~18 months of registry
  data (per "What NOT to build yet"); design the **W.E. API** seams now, publish at J3; W.E.
  ARCHIVE (J5) builds on the registry lineage fields (`source_clip`/`source_clip_sha`) already present.

**Current focus:** finish the priority-originals **offsite** leg (local copies are done) →
the **≥12 TB drive** decision → pivot to **#5 commercial readiness** (which is also what
closes the "contract-grade" gap above).
