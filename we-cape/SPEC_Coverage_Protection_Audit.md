# SPEC — Coverage & Protection Audit
## Living doc · v0.1 · 2026-07-08 · owner: T. · extends SECURITY_RISK_ANALYSIS.md + STORAGE_RISK_AND_BACKUP_PLAN.md

> **The one sentence:** a read-only pass that observes the *actual* state of every shoot
> across drives + Google Drive + the registry, and reports — per shoot — whether it is
> **protected** (enough verified copies, offsite, encrypted), **correctly identified**
> (cameras), and **intact** (no case-collision / truncation), then **proposes** fixes it
> never silently performs.

**Why this exists.** Everything W.E. C.A.P.E. builds today detects and corrects *inside* its
own workflow (`new_shoot` → CAPTURE → `backup_footage`). A real novice — validated by the
operator deliberately behaving as one — sidesteps that workflow: manual Google Drive uploads
(unencrypted, unverified), a mislabeled card left mislabeled, footage never CAPTURE-processed.
If the platform only works when the user already did everything right, it has no value. This
audit is the **workflow-independent** safety net: it trusts *observed state*, not that the
process was followed.

---

## 1. Principle: reconcile observed state, don't assume process

The audit **observes** and **reconciles**. It never assumes a shoot went through the sanctioned
path. It answers, for any pile of footage — however it got there — three questions:

1. **Is it protected?** How many copies, on how many devices, offsite? Verified? Encrypted?
2. **Is it correctly identified?** Do the cameras resolve from the footage, and does any label
   contradict the footage (the card-label trap)?
3. **Is it intact & representable?** Any case-collision pairs, size/hash mismatches, or targets
   that can't faithfully hold the source?

It is an **ops tool** (`scripts/`), consistent with the platform's separation of concerns:
read-only, additive, and it never imports or mutates the deterministic engine (P4).

---

## 2. Detect / Note / Correct — the operating contract

For every finding the audit does exactly three things, in order, and **stops at "note" for
anything irreversible**:

- **DETECT** — compute the fact from observed state (registry + filesystem + remote listing +
  metadata), never from a label or an assumption.
- **NOTE** — record it: a per-shoot status, a human-readable reason, and an append-only audit
  line (P3). Notes are always safe.
- **CORRECT** — *propose* an action and, only within the safety tier below, offer to run it.

### 2.1 Correction safety tiers (the guardrail)

The word "correct" is dangerous for a novice: a wrong auto-fix propagates an error faster than
a human could. Corrections are therefore tiered:

| Tier | Examples | Behavior |
|------|----------|----------|
| **AUTO-SAFE** (additive, reversible) | re-run `cryptcheck`, regenerate a report, queue an existing backup job, write an annotation | may run automatically / on one keypress |
| **CONFIRM-GATED** (irreversible or judgment) | relabel a camera, migrate plain→crypt, rename a case-collision file, delete a duplicate, wipe a card | **detect + note + PROPOSE only**; requires explicit human confirmation of a *fact* (never a guess) |
| **NEVER-AUTO** | delete originals, empty Drive Trash, overwrite a source file | the audit will never do these; it only flags |

Confirmation style matches `camera_identity`: the human confirms a fact ("this card holds
Action 5 footage — yes/no"), never picks blindly ("5 or 6?").

---

## 3. Per-shoot Protection Status model

The audit's core output is one record per shoot. A "shoot" is keyed by, in priority order:
registry `run_id` → `shoot.yaml` identity → footage folder path (for un-processed piles).

```
ShootProtection:
  shoot_id            # run_id | folder key
  name                # human name (shoot.yaml / folder basename)
  bytes, file_count   # observed source size
  copies: [ Copy ]    # every located copy
  identity: [ CameraID ]
  integrity: IntegrityFlags
  workflow: WorkflowState
  freshness: FreshnessState
  status              # GREEN | AMBER | RED  (+ reasons[])

Copy:
  location            # e.g. /Volumes/10TB/... | gcrypt:originals/... | My Drive/... (plain)
  media_id            # physical device id (to measure "2 media" diversity)
  kind                # local | offsite
  present             # bool
  verified            # hash | size | none        (how strongly proven)
  encrypted           # bool (offsite: crypt vs plain)
  last_verified       # timestamp | null

CameraID:
  camera_id, identity_status   # verified|conflict|ambiguous|label_only|unknown (from camera_identity)
  identified_by, conflict      # provenance + label-vs-footage contradiction

IntegrityFlags:
  case_collisions: [path]      # from the case-fold scan
  size_or_hash_mismatch: [path]
  target_case_insensitive      # a backup target that can't hold the source faithfully

WorkflowState:
  in_registry, capture_processed, fcpxml_exported, health_reported   # bools

FreshnessState:
  source_changed_since_backup  # bool (mtime/size delta vs newest verified copy)
  new_bytes_unprotected        # bytes added since last verified copy
```

### 3.1 Status rules (Red / Amber / Green)

- **RED (at risk — act now):** fewer than **2 copies**, OR **no offsite**, OR the *only* copy is
  **unverified**, OR an **unresolved identity conflict**, OR a **known size/hash mismatch**.
- **AMBER (protected but degraded):** 3-2-1 exists BUT offsite is **size-verified only** (not
  hash), OR offsite is **unencrypted** (plain Drive), OR **case-collision risk** on a
  case-insensitive target, OR **source changed since last backup** (stale), OR identity is
  **ambiguous / label-only** (not yet confirmed).
- **GREEN (fully protected):** ≥ **2 media** + **hash-verified encrypted offsite** + identity
  **verified/confirmed** + **no** integrity flags + backup **current**.

The status is intentionally conservative: anything unproven degrades the grade. "Same size" is
not "same bytes"; "uploaded" is not "verified"; "card says X" is not "footage is X."

---

## 4. The checks (detectors), mapped to existing tools

| # | Check | Detects | Reuses | Correction (tier) |
|---|-------|---------|--------|-------------------|
| C1 | **Copy census** | how many copies, on how many devices, offsite present? | filesystem scan + `backup_sources.txt` + registry | queue `backup_footage` (auto-safe: enqueue) |
| C2 | **Verification depth** | copy proven by hash / size / not at all | `mirror_verify` (local SHA), `rclone cryptcheck` (offsite) | run cryptcheck (auto-safe); re-copy bad files (confirm) |
| C3 | **Encryption/offsite coverage** | offsite in `gcrypt:` vs plain `My Drive/` (unencrypted) | rclone remote listing (ro) | migrate plain→crypt then delete plain (confirm) |
| C4 | **Camera identity** | footage-first id; label-vs-footage conflict | `camera_identity` / `probe_camera` / `cameras.yaml` | relabel / record provenance (confirm) |
| C5 | **Case-collision & fidelity** | case-variant pairs; target that can't hold them | the case-fold scan; source vs target FS case-sensitivity | rename or route to case-sensitive target (confirm) |
| C6 | **Coverage vs registry** | processed / unprocessed / duplicate | `reconcile.py` (`--hash`) | run CAPTURE (confirm); reclaim dupes (confirm) |
| C7 | **Freshness** | source grew since last verified copy (the "folder changed after backup" gap) | mtime/size delta vs newest verified copy | re-run additive backup (auto-safe: enqueue) |
| C8 | **Clock health** | intra/inter-camera clock disagreement | `health_report.py` | suggest `trusted_clock` (note only) |

Every detector is **injectable** (registry reader, filesystem lister, rclone runner, exiftool
runner) so the logic is unit-tested without hardware, rclone, or network present.

---

## 5. Where it plugs in

- **New module:** `scripts/coverage_audit.py` — pure status/report core + a thin CLI. Mirrors the
  house pattern (`health_report.py`): a `build_protection_data()` that returns the model, and
  renderers on top (CLI table, JSON, markdown).
- **Registry:** read-only (`mode=ro`) — `runs` + `content` for processed shoots and known copies.
- **`shoot.yaml`:** source of `trusted_clock`, declared cameras, and `identified_by` provenance.
- **`reconcile.py`:** invoked for C6 coverage/dedup facts (don't reimplement).
- **`camera_identity` / `probe_camera`:** invoked for C4 identity + conflict status.
- **`rclone cryptcheck` / `mirror_verify`:** invoked (read-only) for C2/C3 verification.
- **`health_report.py`:** reused for C8 (already produces per-shoot clock data).
- **Dashboard (`dashboard.py`):** a new **protection status chip** (🟢/🟡/🔴 + reasons) per shoot
  card, reusing `build_protection_data()` the same way it reuses `build_report_data()`.
- **Audit log:** append-only `~/.wecape/coverage_audit.jsonl` (P3), never in the deterministic
  registry (like `annotations.db` / `telemetry.db`, mutable ops state stays separated from
  engine output).

---

## 6. Principles alignment

- **P1 Determinism** — untouched; the audit only *reads* engine output.
- **P2 zero-network (engine)** — preserved. The audit is an **ops tool**, not the engine; it MAY
  query the offsite remote (read-only) for C2/C3. It ships an **`--offline`** mode that skips all
  network checks so a run can be fully local. It never lives in `wecape/`.
- **P3 Auditability** — every finding is logged append-only with its evidence.
- **P4 Extensibility w/o coupling** — a new observer; imports no engine internals; existing tools
  don't change to support it.
- **P5 Registry continuity** — read-only; writes nothing to the registry.
- **P7 Creator data sovereignty** — proposes, never destroys; NEVER-AUTO tier protects originals.
- **D1 Privacy** — full-fidelity locally; any path/GPS in an *exported* report is hashed on egress
  (`sha256:`), consistent with the dashboard/report rules. Filenames may carry PII → local-only
  detail, hashed in anything that leaves the machine.

---

## 7. Outputs

```
python3 scripts/coverage_audit.py                 # all shoots, table + status
python3 scripts/coverage_audit.py --shoot "O-SIX RYDERZ MC Community Service"
python3 scripts/coverage_audit.py --offline       # skip offsite/network checks
python3 scripts/coverage_audit.py --json           # machine-readable
python3 scripts/coverage_audit.py --propose        # print the CONFIRM-GATED fixes (runs nothing)
```

- **CLI table:** shoot · status · copies (n/media) · offsite(verified?) · identity · flags.
- **Per-shoot markdown** (optional `--out`): the full record + the proposed corrections.
- **Dashboard chip:** 🟢/🟡/🔴 with a one-line reason on each shoot card.
- **JSONL audit line** per run (P3).

---

## 8. Phasing

1. **Phase 1 — Observe & Note (read-only).** `coverage_audit.py` core + CLI report + JSONL. C1,
   C2 (local), C4, C5, C6, C7. No corrections. *This alone would have flagged every gap from the
   2026-07 sessions.*
2. **Phase 2 — Offsite & Dashboard.** C3 + C2-offsite (rclone, opt-in online); dashboard status chip.
3. **Phase 3 — Confirm-gated corrections.** Wire the CONFIRM-GATED actions to the existing tools
   (`backup_footage`, `cryptcheck`, `camera_identity` relabel, case-collision rename).
4. **Phase 4 — Scheduled + staleness.** launchd template; alert when a GREEN shoot goes AMBER/RED
   (e.g. source grew, a drive went missing, a verification aged out).

---

## 9. Test requirements

- Pure `build_protection_data()` over **injected** state → each R/A/G case has a fixture
  (1-copy RED, unverified-offsite AMBER, fully-protected GREEN, identity-conflict RED,
  case-collision AMBER, stale-source AMBER).
- Failure/edge fixtures: plain-Drive-unencrypted copy, size-only-verified offsite, a target
  flagged case-insensitive, a manual upload with no registry entry (the AlphaRoundUp case).
- No network, rclone, exiftool, or hardware required in the suite (all injected).
- Must keep the full suite green (currently 384) and add its own tests before merge.

---

## 10. Open decisions (need input before build)

1. **Offsite discovery of *plain* uploads.** Detecting unencrypted manual uploads (the
   AlphaRoundUp folders) requires listing the raw Drive remote — but only `gcrypt:` is configured
   today. Decision: add a read-only **base Drive remote** to rclone config, or limit C3 to "is it
   in `gcrypt:`? if not, flag as unverified/plain" without enumerating plain content.
2. **Shoot identity for un-processed piles.** How to key a shoot that never entered the registry
   (folder path? a lightweight `shoot.yaml` stub written on first audit?).
3. **Audit state location.** Ephemeral each run, or a small `coverage.db` (like `annotations.db`)
   to track status-over-time and detect GREEN→RED transitions for Phase 4 alerts.
4. **"2 media" definition.** Count distinct physical devices (via `diskutil`/`stat` device id), or
   trust path roots? Physical-device detection is more correct but macOS-specific.
5. **Auto-safe scope.** Is "enqueue a backup job" acceptable as AUTO-SAFE, or should even queuing
   require confirmation for a novice?

---

## 11. Non-goals

- Not a backup/mover — it observes and *proposes*; data movement stays in `backup_footage`/rclone.
- Not the engine, and not coupled to it.
- Not a dedup engine — defers to `reconcile.py`.
- Not a telemetry decoder — reads `telemetry.db` if present, doesn't parse `.SRT`/`gpmf`.
- Does not delete anything, ever.
