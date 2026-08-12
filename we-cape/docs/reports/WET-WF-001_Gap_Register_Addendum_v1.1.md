# WET-WF-001 Gap Register Addendum

**v1.1 · 2026-08-11 · Corrective Deliverable (Rulings Applied)**

**Purpose**  
This addendum records material gaps between sustained engineering-channel work and the claims/status in `WET-WF-001_Validated_Workflow_v1.0`. It incorporates the formal rulings of 2026-08-11:

- **Ruling 1** — Upstream Stages A–F stand unchanged.
- **Ruling 2** — WET-GAP-001 findings on the G/PDR track are accepted (stricter status vocabulary applied).
- **Ruling 3** — This channel’s GAPs 02–07 are adopted; GAP-01 is **amended** to match verified state-filed fact and ratified ADR-001.

**Status Vocabulary (unchanged)**  
`VALIDATED` · `EXERCISED` · `BUILT-UNEXERCISED` · `ADOPTED` · `PLANNED` · `OPEN` · `EXERCISED-INCOMPLETE` · `DESIGN-COMPLETE` · `CLOSED`

---

## GAP-01 — Platform / Product Naming & Entity Framing (AMENDED)

**Original Addendum Claim (v1.0)**  
“LLC formation remains unformed” and “W.E.I.C.P. treated as interim.”

**Verified Record (Ruling 3)**  
- The DBA **“Workman Experience Technologies”** **is filed** — Texas State ID **804929409**, filed **2026-07-21** — under the existing **Workman Experience, LLC**.  
- A *separate* “WET LLC” was deliberately deferred (DBA-instead decision). Entity exists; the stronger “unformed / resume-accuracy risk” claim is overstated and is **not adopted**.  
- **W.E.I.C.P.** is the **governance domain** name (Board-ratified via ADR-001, corpus-committed). It is not interim.  
- **W.E. C.A.P.E.** correctly leads as the **platform / product brand**. The two names are scoped, not in conflict.

**Corrected Language to Apply**  
Add (or replace any conflicting note with) the following scoped naming statement:

> **Naming Scope (ratified)**  
> - **W.E. C.A.P.E.** = Production Intelligence Platform brand; **CAPTURE** = first product.  
> - **W.E.I.C.P.** = Governance domain name (ADR-001).  
> - Operating entity = Workman Experience, LLC with filed DBA “Workman Experience Technologies” (TX State ID 804929409, 2026-07-21).  
> - A separate “Workman Experience Technologies LLC” was deliberately deferred; current resume claims that reference only the DBA are accurate. Claims that imply a standalone WET LLC remain inaccurate until such entity is formed.

**Status to apply:** `ADOPTED` (scoped naming) · `OPEN` only for any future separate-LLC decision

---

## GAP-02 — SRT Datetime Integration & Privacy Separation (ADOPTED)

**Status:** `BUILT` (integration complete; production exercise pending)

**Language to apply (add as C5 or expand C3):**

> **C5. SRT Sidecar Timestamp Source (config-gated)**  
> When `timestamp.enable_srt_telemetry = true`, first datetime from matching `.SRT` sidecar is used as highest-confidence source (`dji_srt_sidecar`). Default remains `false` — zero change to validated grouping behavior. GPS deliberately excluded from pipeline path (privacy separation via separate `telemetry.db`).  
> Evidence: Design + implementation confirmed in channel. Unit tests for present / absent / malformed / gate-off required before promotion to `VALIDATED`.

---

## GAP-03 — Production Health Report Design Depth (ADOPTED)

**Status:** `EXERCISED` (basic clock audit) · `DESIGN-COMPLETE` (full feature)

**Language to apply (expand C3):**

> **C3. Production Health Report**  
> Locked design decisions:  
> - No single 0–100 health score; component metrics + plain-English verdict only  
> - Trusted-clock field in `shoot.yaml` used to name culprit when present; helpful prompt when absent  
> - Intra-camera date-spread detection is primary signal when GPS unavailable  
> - Full filenames shown in standalone report and dashboard; camera + count (or hashed) in `summary.md`  
> Privacy: follows D1 path-hashing discipline on egress.

---

## GAP-04 — Camera Identification / Novice Robustness (ADOPTED)

**Status:** `DESIGNED` · `PARTIALLY EXERCISED` (probe-before-label proven)

**Language to apply (add as B3):**

> **B3. Camera Identity Robustness (Novice-Safe)**  
> Target architecture (foundational): metadata/serial first → `cameras.yaml` mapping → structure-based brand → label as weakest hint only → conflict stop → confirmation-style prompts.  
> Current production strength: content-based correction of mislabeled cards is proven. Full multi-layer system remains open.  
> Note: Elevated to foundational priority in engineering channel; not a polish item.

---

## GAP-05 — Grouping Intelligence vs. Edit Usage (ADOPTED)

**Status:** Suite-validated · NEVER production-used for the Part-1 edit (named gap) — clarification only

**Language to apply (clarify C2):**

> **C2. Scene/Time Grouping (MCG)**  
> Additional channel work: FCPXML export path designed to surface groups as Multicam clips + remaining singles in chronological order, with per-camera Keyword Collections and model+clip angle labels.  
> Distinction: Grouping *engine* is ready; *edit usage* of that intelligence was bypassed. Closure remains via STAGING_P2 path.

---

## GAP-06 — Security & Privacy Decision Register (ADOPTED)

**Status:** `ADOPTED` (decisions) · `OPEN` (full external-drive encryption execution)

**Language to apply (Governance Rail or new subsection):**

> **Security & Privacy Controls (channel decisions)**  
> - D1: Paths hashed on egress; human-readable names remain local  
> - D2: `annotations.db` → encrypted offsite (rclone crypt); local full fidelity  
> - D3: rclone token hardened (permissions + exclusion from normal backups)  
> - D4: FileVault on internal + selective encryption for drives that leave the building  
> - Network-invariant test: zero network imports in core engine (enforced)  
> - Separate stores: annotations.db and telemetry.db never pollute deterministic registry  
> Full analysis lives in SECURITY_RISK_ANALYSIS.md (or successor).

---

## GAP-07 — RFQ / Test 6 Closure (ADOPTED)

**Status:** `CLOSED` (criteria) · `OPEN` only if specific evidence runs remain

**Language to apply:**

> RFQ acceptance criteria (including self-defined quantitative thresholds for Test 6) are now locked. Final RFQ deliverable status = complete pending any remaining production evidence runs.

---

## G/PDR Track Findings Adopted from WET-GAP-001 (Ruling 2)

These items are now part of the formal record and must be reflected in any v1.1 of WET-WF-001:

| Finding | Corrected Status / Action |
|---------|---------------------------|
| PDR pilots (BLACKTOP HYPNOSIS, OUT HERE) | `EXERCISED-INCOMPLETE` (Draft). Validator correctly fails timeline.in/out because the Jul 29 FCPXML predates both cue decisions. |
| Cue custody | Registry = 726 camera rows, **ZERO cue rows**. Ungoverned-intelligence-layer risk is proven. Two BLACKTOP versions exist on disk without custody of which was accepted. |
| `music_rights` contradiction | Real. `shoot.yaml` still said “OPEN — no music placed yet” beside a released album. **ER-4 fix required immediately** (see below). |
| CR-1 session_record custody | Outstanding. |
| Independence disclosure | v0.2 author = v0.1 reviewer → v0.3 needs a different reviewer. |
| ER-1 … ER-5 | Adopted. ER-1 (fresh FCPXML) is the convergent next action across channels. |

**Immediate non-document action (ER-4)** — kill the live contradiction on both manifests:

```bash
for Y in "/Volumes/WE_CAPE_OUTPUT/AlphaRoundUp_2026/shoot.yaml" "/Volumes/10TB/AlphaRoundUp_2026/shoot.yaml"; do
python3 -c "
import pathlib; p=pathlib.Path('$Y'); s=p.read_text()
s=s.replace('status: OPEN — no music placed yet; every cue requires a rights line',
'status: PLACED_AND_RELEASED — see soundtrack_release (UPC 882436051388); per-cue rights = PDR track (pdr.rights canonical, this block = index); ER-4 resolved 2026-08-11')
p.write_text(s); print('fixed: $Y')"
done
```

**ER-1 (human action, no document change):** Next FCP open → File → Export XML on the current Part 1 project → place in `XML/` folder. This simultaneously satisfies the PDR validator, refreshes utilization, and baselines A4.

---

## Ingestion Instructions for Claude Code (v1.1)

1. Treat this **v1.1** Gap Register as authoritative.  
2. Apply the corrected GAP-01 language (scoped naming + verified DBA fact).  
3. Apply GAPs 02–07 exactly as stated.  
4. Incorporate the G/PDR findings and status restatements from Ruling 2.  
5. Do not invent validation status higher than the evidence supports.  
6. Preserve the document’s honest status vocabulary.  
7. After updates, patch the affected tables so the register remains single-source-of-truth.  
8. Flag any item that cannot be verified from current repo state as still `OPEN`.

**End of Gap Register Addendum v1.1**
