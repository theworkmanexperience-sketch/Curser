# CAR-003 — Platform Hygiene Review: Findings
## Governance Status
Document Type: Collaborative Architecture Review — Findings · Status: **FOR EXECUTIVE REVIEW**
Date: 2026-08-22 · Initiative: PHI-001 · Review request: CAR-003
Authority: Executive Office (PHI-001, effective immediately)
**Recommendations only. No implementation was performed. No architecture was proposed.**
Independence disclosure (CAR-001 A4): reviewer is the same party that executed Sprint 3A. Findings
that concern Sprint 3A's own output are marked **[SELF]** and warrant independent confirmation.

---

## 0. Scope of evidence — read this before the findings
This review searched **the repository and this working session**. It did not have access to prior
conversations, the W.E.I.C.P. corpus, engineering-channel history, or any material outside
`~/Curser/we-cape`.

That boundary matters more than usual here, because CAR-003 asks what was *discussed*. This review can
say with confidence what is **in governed documentation**. Where it reports NOT FOUND, that means *no
trace in governed sources* — never *never discussed*. Ten of the twenty named topics fall in that
category, and that finding is the strongest possible validation of PHI-001's premise: the initiative
exists because memory is currently load-bearing, and this review can measure the load but not read it.

**Corpus surveyed:** 191 commits (2026-05-20 → 2026-08-22) · 123 governed markdown/YAML documents ·
12 registries · 4 governance trees.

---

## 1. Headline findings
| # | finding | evidence |
|---|---|---|
| F1 | **10 of 20 named topics have no governed trace** | §2 topic table |
| F2 | **5 of those 10 exist in substance under a different name.** The platform's problem is naming, not absence | §2, §4 |
| F3 | **The entire forward review roadmap lives in one table cell** — `CAR_INDEX.md` row 3, eight planned reviews, unnumbered | `docs/reports/CAR_INDEX.md` |
| F4 | **Four referenced ADRs have no document in this repository**: ADR-001 (8 refs), ADR-003 (16 refs), ADR-006, ADR-010 | grep census vs `find` |
| F5 | **Two parallel governance trees** — `docs/` and `records/` — with two PDR numbering schemes, two spec spellings, and ADRs split across both | §4 |
| F6 | **Registry identifiers drift from filenames**, and one spec-required registry does not exist | §4.2 |
| F7 | **A ratified amendment references a document that was never created** (`CAR_ROADMAP.md`, CAR-001 A1) | CAR-001 Rev A |
| F8 | **A publication-blocking rights gap is currently unowned** — the single score asset in the Part 2 lock | DWR-026 |
| F9 | **[SELF]** Sprint 3A's ESS artifact silently omitted a fusion input its own communiqué named | §6.1 |

---

## 2. Special review request — topic-by-topic disposition
`IMPLEMENTED` = exists and is governed · `PARTIAL` = exists, incompletely governed ·
`DIFFERENT NAME` = the substance exists under another label · `NOT FOUND` = no trace in governed sources

| # | topic requested | disposition | where it actually is | DWR |
|---|---|---|---|---|
| 1 | DJI camera naming convention | **PARTIAL** | Ratified as CAPE-RAT clause 10 — namespaced keywords `CAM_X5`, `CAM_OM1`, `CAM_DJI5`, `CAM_DJI6`. DJI model-code offsets resolved in `cameras.yaml` (AC003=Action 4, AC004=Action 5 Pro, AC006=Action 6). The *full* identity system remains open | 015 |
| 2 | Capture Device Registry | **DIFFERENT NAME** | `cameras.yaml` at repo root — self-described *"Camera Identity Registry … the SOURCE OF TRUTH for which physical body recorded a card"*, keyed by serial. Ungoverned: no `registry_id`, no version, outside every governance tree | 016 |
| 3 | Capture Intelligence | **NOT FOUND** | No trace. Adjacent substance exists (probe-before-label, camera identity provenance) but never under this name | — |
| 4 | Asset Library | **NOT FOUND** | No trace | — |
| 5 | Asset Reconciliation | **PARTIAL** | Commit `a465527` ships a *"reconcile audit"* in the FCPXML path. No governed artifact, no specification | — |
| 6 | Production Readiness Assessment | **PARTIAL** | Named once, in the Sprint 3A communiqué. No standard, no instance | — |
| 7 | Production Intelligence Dashboard | **DIFFERENT NAME** | A working local read-only dashboard exists: `scripts/dashboard.py` → `wecape_dashboard.html`, governed by `UI_Dashboard_Design_Guidelines_v2.md`. Covers the **capture** registry only | 021 |
| 8 | Production Intelligence Score | **LIKELY ALREADY DECIDED** | GAP-03 locks *"No single 0–100 health score; component metrics + plain-English verdict only."* Whether that ruling extends to a *Production Intelligence* score has never been stated | 010 |
| 9 | Executive Dashboard | **PARTIAL** | Planned CAR (index row 3, *"Executive Dashboard & Analytics"*). Named as a downstream consumer in `PRODUCTION_INTELLIGENCE_SEED.yaml`. Prototype exists (item 7) | 021, 027 |
| 10 | File Utilization Metrics | **PARTIAL** | Exercised in Part 1 (*"the Part-1 1.9% instrument"*); SOP-06 A3 requires a utilization report at lock. No governed artifact class | — |
| 11 | Documentation Efficiency | **NOT FOUND** | No trace | — |
| 12 | Engineering Doctrine | **NEWLY IMPLEMENTED** | `docs/doctrine/` created 2026-08-22: DOC-001, DOC-002, DOC-SRC-001. Did not exist before this week | 009 |
| 13 | PBOM | **PLANNED, UNDEFINED** | Appears exactly once, as a planned CAR title in `CAR_INDEX.md`. No expansion of the acronym anywhere in the corpus | 027 |
| 14 | DPAL | **DIFFERENT NAME** | The abbreviation appears **nowhere**. The expansion — *"Digital Provenance & Asset Lineage"* — is a planned CAR in index row 3. A pure abbreviation-only artifact | 027 |
| 15 | Post Production Intelligence | **NOT FOUND** | No trace under this name | — |
| 16 | Camera Metadata | **IMPLEMENTED** | `WEFORGE_Architecture_v1.0.md` schema: `camera_id`, `camera_family`, `camera_confidence` (J1: detected, not assumed). Exercised in the probe path | — |
| 17 | GPS Metadata | **IMPLEMENTED (deliberately constrained)** | 35 references. GAP-02: GPS **deliberately excluded** from the pipeline path — privacy separation via a separate `telemetry.db`. CAPE-RAT clause 12: corroborating evidence, not mandatory | — |
| 18 | Telemetry | **PARTIAL** | 31 references. SRT sidecar telemetry BUILT and config-gated (default `false`); promotion to VALIDATED blocked on four unit tests | 017 |
| 19 | Capture Device Profiles | **PARTIAL** | `brand_profiles/twe.yaml`; Phase 1 Pillar 3 *"Config / Profile-Based Workflows (COMPLETE)"*; WEFORGE extension layer names custom camera metadata parsers | — |
| 20 | Reference Executions | **IMPLEMENTED** | RE-001 + scorecard + index + document class, created 2026-08-22 | 033 |

**Read F2 from this table.** Items 2, 7, 8, 12 and 14 are not missing work — they are existing work the
organisation cannot find by the name it remembers. That is a naming failure wearing the costume of a
capability gap, and it is much cheaper to fix.

---

## 3. Deliverable 2 — Deferred Work Register
Delivered as `records/dwr/DEFERRED_WORK_REGISTER.yaml`, conforming to DWR-001 with all fourteen
required fields present on all **36** entries (validated programmatically).

**13 Deferred Decisions · 23 Deferred Implementations · P1: 14 · P2: 11 · P3: 7 · P4: 4**

### 3.1 Deferred Decisions vs Deferred Implementations *(Executive enhancement, adopted)*
The distinction the Executive Team requested is now a first-class field (`class`) on every entry, and it
turned out to be more than a filing convenience — it changes what you can *do* with a row.

| | Deferred **Decision** | Deferred **Implementation** |
|---|---|---|
| What it is | A question still needing a ruling | A decision made, work postponed |
| Blocked on | **Authority** | **Capacity** |
| Can be scheduled? | No — scheduling it produces guesses | Yes |
| Who unblocks it | Executive Producer / Chairman | Engineering |
| Failure if mixed | An unanswered question enters a sprint as a task, and gets answered by whoever writes the code | A ready task sits in a governance queue waiting for a ruling nobody owes |

The second failure mode is the quiet one, and this register contains live examples of both. **DWR-020**
(grouping intelligence never used in an edit) is a fully built capability sitting in a governance
context — pure capacity. **DWR-010** (is the Production Intelligence Score already decided?) looks like
a feature request and is actually a one-sentence ruling.

Recommendation: carry `class` on every future DWR entry, and **never allow a DECISION row into a sprint
plan.** Decisions are dispositioned; implementations are scheduled.

---

## 4. Deliverable 3 — Naming Consistency Report
### 4.1 Structural: two parallel governance trees
| class | `docs/` | `records/` |
|---|---|---|
| ADR | `docs/adr/ADR-009` | `records/governance/ADR-007` |
| PDR | `docs/pdr/PDR-2026-08-20-ETC-001` (date-typed, markdown) | `records/pdr/PDR-000003` (sequential, YAML) |
| SPEC | `docs/specs/WET-SPEC-002_v0.1`, `v0.2` | `records/specs/WETSPEC002_v0.3` |

Three record classes, each split across two trees, with **two PDR numbering schemes**, **two spec
spellings** (`WET-SPEC-002` vs `WETSPEC002`), and the newest version of WET-SPEC-002 living in the tree
that does not hold its predecessors. `PDR-2026-08-20-ETC-001` flags the numbering collision in its own
header and routes reconciliation to `docs/README` — where it never arrived (**DWR-005**).

### 4.2 Registry identifiers vs filenames — DIE spec F-1
F-1: *"Immutable identifiers name every registry (schema, storage, APIs, documentation)."*

| file | `registry_id` inside | status |
|---|---|---|
| `QUOTE_LIBRARY.yaml` | `QUOTE_REGISTRY` | **MISMATCH** |
| `WHY_I_RIDE_REGISTRY.yaml` | `WHY_RIDE_REGISTRY` | **MISMATCH** |
| `DOCUMENTARY_PROGRESSION.yaml` | *(none — uses `document_id`)* | **NO IDENTIFIER** |
| `INTERVIEW_REGISTRY` | — | **DOES NOT EXIST** (spec §7 names it; V-5 requires it be populated *or* reported empty with reason — neither was done) |
| other 9 | match | OK |

Two of nine spec-named registries are unreachable by their immutable identifier. Sprint 2's action-item
list (`G2-MIR-005`) uses the *filenames*, which is how the drift entered.

### 4.3 Abbreviations with no governed expansion
`DPAL` (→ Digital Provenance & Asset Lineage) · `PBOM` (no expansion anywhere in the corpus).
Both are load-bearing in conversation and absent from documentation — the exact PHI-001 failure mode.

### 4.4 Version collisions and superseded artifacts kept live
`EXECUTIVE_SUMMARY_v4.6.md` **and** `v4.7.md` at root · `CUE_SHEET.yaml` **and** `CUE_SHEET_v1.1.yaml`
with no SUPERSEDED marker on the former · `WE_FLOW_*_v6` at root while v4.1 sits in `archive/` ·
`CAR-001` exists as *…_Standard.md* in `docs/reports/` and as *…_Package.md* in the production media
folder — same ID, two titles, two locations.

### 4.5 Class-vs-location drift
`docs/reports/` holds reports, communiqués, work orders, **standards** (CAR-001), memoranda and briefs.
`docs/reviews/` holds reviews — but `WET-REV-DIE-001` and `WET-REV-AIS001` live in `reports/`.
**CAR-002 has no document at all** — it exists only as a row in the index.

### 4.6 Repository root
**28 loose files** at `we-cape/` root, including four `SPEC_*.md` specifications, three `.fcpxml`
production files, a credential inventory, a security risk analysis, a generated dashboard HTML and
`run_tests.py`. `CLAUDE.md`, `MILESTONES.md` and `ENGINEERING_OVERVIEW.md` are genuinely root-level;
most of the rest are misfiled.

---

## 5. Deliverable 4 — Governance Debt Register
| id | debt | severity | DWR |
|---|---|---|---|
| GD-01 | **ADR-001, ADR-003, ADR-006, ADR-010 referenced but absent from this repository.** ADR-003 is cited 16 times, including as the harmonization target for the provenance vocabulary. ADR-001 is described as *"Board-ratified … corpus-committed"* — it may live in the W.E.I.C.P. corpus, which this review cannot see. Either way, **this repository cannot resolve its own governance references** | **HIGH** | — |
| GD-02 | `CAR_ROADMAP.md` required by ratified amendment CAR-001 A1; never created | **HIGH** | 022 |
| GD-03 | CAR-002 retro-designated with no document; only an index row | MEDIUM | — |
| GD-04 | Two PDR numbering schemes, self-flagged and unreconciled since 2026-08-20 | **HIGH** | 005 |
| GD-05 | `INTERVIEW_REGISTRY` spec-required, absent, and no empty-registry report filed (V-5) | **HIGH** | 023 |
| GD-06 | ER-2 / ER-4 / ER-5 evidence requests never tracked to closure; `PDR-000003` still shows `restrictions: PENDING (ER-5)` and an empty `gate_clearance_ref` | **HIGH** | 025 |
| GD-07 | Rights lines missing for ≥4 placed cues incl. `KICKSTANDS UP v1` — the only score asset in the Part 2 lock. GATE 2/3 require them for **all** placed cues | **CRITICAL** (publication-blocking) | 026 |
| GD-08 | 6+ retroactive Part 1 PDRs owed under WET-REV-002's exercise-first order; that order also gates PRS-001 and WET-SPEC-003 | MEDIUM | 028 |
| GD-09 | Both PDR pilots remain `EXERCISED-INCOMPLETE` (Draft) | MEDIUM | 029 |
| GD-10 | GATE 1/2/3 are prose-only; release authority is the one thing a dashboard cannot read | **HIGH** | 031 |
| GD-11 | Platform-scope artifacts ratified without Chairman countersignature | MEDIUM | 008 |
| GD-12 | Cue custody: 726 camera rows, **zero** cue rows; two BLACKTOP versions on disk without custody of which was accepted | **HIGH** | 024 |
| GD-13 | DWR-001's document ID collides with the entry ID space it defines | LOW | see register header |

## 6. Deliverable 5 — Technical Debt Register
| id | debt | severity | DWR |
|---|---|---|---|
| TD-01 | No automated CI/CD; 384-test suite runs on demand | **HIGH** for external deployment | 030 |
| TD-02 | No code signing / notarization; no external security audit | MEDIUM–HIGH | 030 |
| TD-03 | SRT telemetry BUILT but not VALIDATED — four named unit tests outstanding | MEDIUM | 017 |
| TD-04 | Full external-drive encryption not executed (D1–D4 adopted) | **HIGH** | 019 |
| TD-05 | Grouping engine suite-validated, **never production-used**; closure via STAGING_P2 | MEDIUM | 020 |
| TD-06 | Camera identity multi-layer system incomplete; label-trust risk proven in production (the `DJIAction6` card holding Action 5 Pro footage) | **HIGH** (named foundational, not polish) | 015 |
| TD-07 | 11 `TODO` markers in shipped code — all in `probe_camera.py`'s deliberate *"TODO confirm model"* labels. **Intentional**: the code refuses to guess a model. Recorded so a future sweep does not "clean up" a safety feature | INFO | — |
| TD-08 | `wecape_dashboard.html` is a generated artifact committed at root; README says generated HTML is gitignored | LOW | — |
| TD-09 | 5 commits unpushed; no network egress or SSH credentials in the execution sandbox | **HIGH** (unpushed governance is unshared governance) | 036 |

### 6.1 [SELF] Sprint 3A finding — a silent omission in this reviewer's own work
The Sprint 3A communiqué named the ESS fusion inputs explicitly: *"Editorial Timing Contract ·
Documentary Progression · **Interview Registry** · Voice-over Registry · Caption Registry · Energy
Curve · Visual Event Registry."*

`EDITORIAL_SYNCHRONIZATION.yaml` lists eight consumed sources. `INTERVIEW_REGISTRY` is not among them —
because it does not exist — **and its absence was never declared.** Under the sprint's own
no-silent-recovery constraint, a named input that cannot be consumed should have been recorded as
`NOT_CONSUMED` with a reason, exactly as the run did for five `NOT_OBSERVED` visual classes.

It is a small hole in a run that was otherwise strict about this, and it is the kind of thing only a
second pass finds. Remedy is cheap (**QW-5**) and does not require regenerating the artifact for
correctness — only for completeness of the declaration.

---

## 7. Deliverable 6 — Architecture Improvement Opportunities
*Observations, not proposals. No architecture is being recommended for construction.*

| id | opportunity | rationale |
|---|---|---|
| AO-1 | **Unify the two governance trees** | `docs/` and `records/` split three record classes. One tree with class subdirectories would make every ID resolvable by path. Blocked on DWR-005 (numbering ruling) — a decision, not a build |
| AO-2 | **One registry framework across capture and intelligence domains** | `intelligence/p2/registries/` is governed (F-1…F-5); `cameras.yaml` and `~/.wecape/registry/wecape.db` are not. The platform has two registry cultures. Unifying the *contract* (id, version, schema version) is cheap; unifying the *storage* is not, and is not recommended |
| AO-3 | **Give the intelligence layer custody rows** | GD-12's proven risk. The capture domain has 726 rows and full lineage; the cue domain has none |
| AO-4 | **Extend the existing dashboard rather than build an Executive Dashboard** | A working, local, zero-network read-only dashboard already exists. It reads the capture registry. Pointing it additionally at the gate ledger and RE scorecards is incremental — see QW-7 |
| AO-5 | **Make the ADR reference space resolvable** | Either import the missing ADRs from the W.E.I.C.P. corpus or add a pointer file per absent ADR recording where it lives. A governance system whose references dangle teaches people not to follow them |

---

## 8. Deliverable 7 — Quick Wins
*Minimal engineering effort, high effect on end-user experience, observability, production
intelligence, asset management and institutional memory — the criteria the Executive Team named.*

| id | quick win | effort | closes | why it pays |
|---|---|---|---|---|
| **QW-1** | Expand `CAR_INDEX` row 3 into `CAR_ROADMAP.md` | ~30 min | GD-02, DWR-022, DWR-027 | **Highest institutional-memory return in this review.** Eight planned reviews and five of the Executive Team's remembered topics currently live in one table cell. It also satisfies a ratified amendment |
| **QW-2** | Enroll `cameras.yaml` as a governed registry (`registry_id`, versions, move under governance) | ~1 h | DWR-016 | Closes the "Capture Device Registry" topic with an artifact that already exists and is already the source of truth |
| **QW-3** | Rename `QUOTE_LIBRARY.yaml` → `QUOTE_REGISTRY.yaml`, `WHY_I_RIDE_REGISTRY.yaml` → `WHY_RIDE_REGISTRY.yaml` | ~15 min | F-1 compliance | Two renames restore immutable-identifier addressability |
| **QW-4** | File the `INTERVIEW_REGISTRY` empty-registry report | ~20 min | GD-05, DWR-023 | Satisfies spec V-5 **without building a registry** — the spec explicitly allows reporting empty with reason |
| **QW-5** | Add a `NOT_CONSUMED` declaration block to the ESS generator | ~20 min | §6.1 | Closes this reviewer's own silent omission and makes the pattern reusable |
| **QW-6** | One-sentence ruling: does GAP-03's "no 0–100 score" extend to a Production Intelligence Score? | ~5 min | DWR-010 | Prevents re-litigating a decision the record may already contain |
| **QW-7** | Point the existing dashboard at `gate_status.py --json` and the RE scorecard index | ~2–3 h | AO-4, observability | Turns *"is the gate open?"* into a screen, using a dashboard that already exists and already honours the zero-network mandate |
| **QW-8** | Push the 5 local commits | ~1 min | TD-09, DWR-036 | Governance that exists only on one machine is not governance |
| **QW-9** | Move misfiled root documents into `docs/` subtrees | ~1 h | §4.6 | 28 → ~5 root files; every document becomes findable by class |
| **QW-10** | Add `SUPERSEDED_BY` headers to `CUE_SHEET.yaml` and `EXECUTIVE_SUMMARY_v4.6.md` | ~10 min | §4.4 | Removes the two live "which one is current?" ambiguities |

Ten quick wins, roughly **one working day in total**, closing two HIGH governance debts, one spec
non-conformance, the largest institutional-memory risk, and the observability gap.

---

## 9. Deliverable 8 — Future Roadmap
Sequenced by dependency, not ambition. **Nothing here is authorized.**

**Horizon 0 — before the next sprint (decisions only)**
Disposition the four Sprint 3A PDRs (DWR-001…004) → they unblock RE-002 and close Level 7 · rule on PDR
numbering (DWR-005) → unblocks tree unification · rule on the score question (DWR-010) · Chairman
countersignature (DWR-008).

**Horizon 1 — the quick-win day** — §8 in full.

**Horizon 2 — publication readiness for Part 2**
Rights-line coverage (DWR-026, **critical**) · ER-2/4/5 closure (DWR-025) · machine-readable GATE 1/2/3
(DWR-031) · full-resolution proxy (DWR-032).

**Horizon 3 — the eight planned CARs**, in the order their dependencies suggest: Production
Intelligence Review → Platform Metrics → Executive Dashboard & Analytics → Digital Provenance & Asset
Lineage → PBOM → Conductor's Score Evolution → Road Soul Lexicon → AI Governance Evolution.

**Horizon 4 — operating envelope**
CI/CD, signing, external audit (DWR-030) · PRS-001 · WET-SPEC-003 · camera identity multi-layer
(DWR-015) · STAGING_P2 closure (DWR-020).

---

## 10. Deliverable 9 — Executive Recommendations
**R1. Adopt the Decision/Implementation split as a permanent DWR field.** It is already carried on all
36 entries. The operative rule: **a DECISION row may never enter a sprint plan.** Decisions are
dispositioned; implementations are scheduled.

**R2. Treat QW-1 as the highest-value action in this review.** The forward roadmap of the entire
platform is one table cell. Everything else in PHI-001 is recoverable from documents; that cell is the
closest thing to a single point of institutional-memory failure the review found.

**R3. Rule on GD-07 (rights lines) before any Part 2 publication step.** It is the only **CRITICAL**
item and it is currently unowned. It does not block MIE; it blocks release.

**R4. Resolve the ADR reference space (GD-01).** Sixteen references to a document this repository does
not contain is the single largest resolvability gap. If ADR-001/003/006/010 live in the W.E.I.C.P.
corpus, a pointer file per ADR costs minutes and restores the chain.

**R5. Rule on PDR numbering (GD-04) before the next PDR is issued.** Every PDR issued while it is
unresolved deepens the split. This review issued four into the date-typed scheme, widening it further —
recorded here rather than left implicit.

**R6. Do not build an Executive Dashboard yet.** A working dashboard exists. Extend it (QW-7), see what
the Executive Team actually reaches for, and let CAR "Executive Dashboard & Analytics" convene against
evidence of use rather than against a blank page.

**R7. Accept that five "missing capabilities" are naming problems.** Capture Device Registry, Executive
Dashboard, Production Intelligence Score, DPAL and Engineering Doctrine all have substance in the
repository under other names. Naming them is a day's work; rebuilding them would be months.

**R8. Schedule the next Platform Hygiene Review by trigger, not by calendar.** DWR-001 §"Review
Frequency" already names the triggers. The natural next one is after RE-002.

---

## 11. What this review deliberately did not do
No architecture was proposed · no implementation was performed · no existing artifact was modified
except `CAR_INDEX.md` (adding the CAR-003 row, which is the act of convening this review under CAR-001
A1) · no missing artifact was created to make a register look complete · no topic was marked FOUND on
the strength of an adjacent artifact — five topics are marked DIFFERENT NAME precisely so the Executive
Team can decide whether the substance satisfies the intent.

## 12. Deliverable index
| # | CAR-003 deliverable | location |
|---|---|---|
| 1 | Platform Hygiene Register | this document §2, §4–§6 (consolidated by category A–J) |
| 2 | Deferred Work Register | `records/dwr/DEFERRED_WORK_REGISTER.yaml` (36 entries, DWR-001 conforming) |
| 3 | Naming Consistency Report | §4 |
| 4 | Governance Debt Register | §5 |
| 5 | Technical Debt Register | §6 |
| 6 | Architecture Improvement Opportunities | §7 |
| 7 | Quick Wins | §8 |
| 8 | Future Roadmap | §9 |
| 9 | Executive Recommendations | §10 |
| — | Deferred Decisions vs Deferred Implementations | §3.1 |
