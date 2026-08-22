#!/usr/bin/env python3
"""Generate the Deferred Work Register from a review table.
Guarantees every DWR-001 required field is present on every entry."""
import yaml, sys

REQ = ["dwr_id","title","category","class","origin","discussion_reference","date_identified",
       "reason_deferred","executive_context","dependencies","trigger_event","estimated_value",
       "estimated_complexity","recommended_priority","current_status"]

D = "DECISION"; I = "IMPLEMENTATION"
# id, title, cat, class, origin, ref, date, reason, exec_ctx, deps, trigger, value, cx, prio, status
ROWS = [
# ---------------- DEFERRED DECISIONS ----------------
("DWR-001","Define MANDATORY_SILENCE scope: no score vs no sound","D — Governance Debt",D,
 "Sprint 3A / RE-001 finding SLF-01","PDR-2026-08-22-ESS-004; CONDUCTOR_SCORE.yaml silence_law_integrity_findings","2026-08-22",
 "Content of the audio element inside SIL-01 was never inspected; source media offline (delta D-22). Classified UNCERTAIN and escalated rather than judged.",
 "Executive Team named this the highest-consequence of the four PDRs: it defines a platform rule, not only a production fact.",
 "62-second human listen to 00:33:37.708-00:34:39.667 of the locked cut","Audio inspection completed and content classified",
 "HIGH — resolves years of ambiguity in one ruling","LOW (one listen + one ruling)","P1","Deferred"),
("DWR-002","S16 segment label vs observed illumination","D — Production","DECISION",
 "Sprint 3A conflict VCONF-01","PDR-2026-08-22-ESS-001","2026-08-22",
 "Registries outrank visual observation; DIE-V recorded CONFLICTED and stopped.",
 "Reaches CUE-08 (Pass 4 CELEBRATION). Boundary is correct to 0.5s; only the label disagrees.",
 "None","Executive disposition of the four Sprint 3A PDRs",
 "MEDIUM","LOW","P2","Deferred"),
("DWR-003","Escort ride duration vs CUE-03 span","D — Production",D,
 "Sprint 3A conflict VCONF-02","PDR-2026-08-22-ESS-002","2026-08-22",
 "Cue sheet is ARCHITECTURE APPROVED; extending a cue is musical intent, not measurement.",
 "~150s of escort ride carries no cue; SIL-01 opens over moving ride footage.",
 "DWR-001 (same silence zone)","Executive disposition; should be taken with DWR-001",
 "MEDIUM-HIGH","LOW-MEDIUM","P1","Deferred"),
("DWR-004","Caption policy vs zero rider lower-thirds (consent dimension)","D — Production",D,
 "Sprint 3A conflict VCONF-03","PDR-2026-08-22-ESS-003","2026-08-22",
 "Absence of an artifact is not proof the intent was abandoned; deciding is editorial.",
 "Carries a consent and rights dimension: RIDER_REGISTRY names are largely UNCONFIRMED under R-3.",
 "RIDER_REGISTRY resolution status; consent ledger","Executive disposition",
 "MEDIUM","LOW (option A) to HIGH (option C reopens picture lock)","P3","Deferred"),
("DWR-005","Reconcile the two PDR numbering schemes","D — Governance Debt",D,
 "PDR-2026-08-20-ETC-001 header, self-flagged","PDR-2026-08-20-ETC-001 'Numbering: date-typed scheme, as-issued (reconcile w/ pilot sequence in docs/README)'","2026-08-20",
 "Recorded as-issued to avoid blocking the ETC ruling; reconciliation explicitly postponed to docs/README.",
 "Two live schemes and two storage trees: docs/pdr/PDR-YYYY-MM-DD-TYPE-NNN (markdown) and records/pdr/PDR-00000N (YAML). Never reconciled.",
 "docs/README numbering policy","Next PDR issued, or PHI-001 disposition",
 "HIGH — ambiguity in the platform's most-used record class","LOW (a ruling + a migration note)","P1","Deferred"),
("DWR-006","Separate 'Workman Experience Technologies LLC' formation","D — Business/Entity",D,
 "WET-WF-001 Gap Register GAP-01 (AMENDED, Ruling 3)","docs/reports/WET-WF-001_Gap_Register_Addendum_v1.1.md GAP-01","2026-08-11",
 "DBA-instead decision: DBA filed under Workman Experience, LLC (TX 804929409, 2026-07-21).",
 "Explicitly recorded as deliberately deferred. Resume claims referencing only the DBA are accurate; claims implying a standalone WET LLC remain inaccurate until formed.",
 "None","Business need for a standalone entity",
 "LOW (platform) / MEDIUM (positioning)","MEDIUM (legal, external)","P4","Deferred"),
("DWR-007","Cue-boundary reconciliation as a pre-generation gate","D — Architecture",D,
 "Sprint 3A engineering reflection; carried as AI-02","DOC-SRC-001 section 1 bullet 9; G3-ESS-001_EXECUTIVE_CONFIRMATION AI-02","2026-08-22",
 "Raised at run completion; no authority to change the MIE pipeline during Sprint 3A.",
 "Would prevent writing beds against spans that end 2.5 minutes before the action does (VCONF-02 class of error).",
 "DWR-003 outcome","Next MIE pass planning",
 "HIGH — prevents a whole error class","LOW-MEDIUM","P2","Deferred"),
("DWR-008","Chairman countersignature on platform-scope artifacts","D — Governance Debt",D,
 "PHI-001 predecessor work; carried as AI-06","G3-ESS-001_EXECUTIVE_CONFIRMATION section 4.7","2026-08-22",
 "Ratified on Executive Producer authority; every prior platform-scope artifact carries Chairman acceptance.",
 "Affects WET-SPEC-GATE-001, DOC-001, DOC-002. Flagged rather than assumed.",
 "None","Chairman review session",
 "MEDIUM — authority consistency","LOW","P2","Deferred"),
("DWR-009","Ratify remaining doctrine candidates DC-02 through DC-10","D — Governance",D,
 "DOC-SRC-001 section 2; carried as AI-03","docs/doctrine/DOC-SRC-001 section 3 AI-03","2026-08-22",
 "Ratification is a separate act from preservation; only DC-01 was promoted.",
 "Nine candidates remain explicitly NON-NORMATIVE.",
 "None","Chairman review session",
 "MEDIUM","LOW","P3","Deferred"),
("DWR-010","Confirm whether 'Production Intelligence Score' is already decided","D — Governance Debt",D,
 "PHI-001 special review request vs WET-WF-001 GAP-03","GAP-03 locked design decision: 'No single 0-100 health score; component metrics + plain-English verdict only'","2026-08-11",
 "A locked design decision already rejects a single composite score for the Production Health Report. Whether that ruling extends to a 'Production Intelligence Score' has never been stated.",
 "The Executive Team listed Production Intelligence Score as a topic of interest; the governed record may already answer it.",
 "None","PHI-001 disposition",
 "HIGH — prevents re-litigating a settled decision","VERY LOW (one clarifying ruling)","P1","Completed"),
("DWR-011","CURATED as a ratification candidate in the provenance vocabulary","D — Governance",D,
 "Part 1 governance pilot vocabulary rulings","docs/reports/PMR-001_Pilot_Metrics_Report.md 'CURATED admitted as ratification candidate (human-authorship/copyright rationale)'","2026-08-08",
 "Admitted as a candidate, never ratified. APPROVED was rejected as a provenance class twice.",
 "Touches ADR-003 harmonization and the OBSERVED/DERIVED/INTERPOLATED/ENRICHED/GENERATED vocabulary.",
 "ADR-003 (referenced, absent from this repository)","Provenance vocabulary revision",
 "MEDIUM","LOW","P3","Deferred"),
("DWR-012","WET-SPEC-002 v0.3 consolidations: rights-ledger primacy and timeline.format","D — Governance Debt",D,
 "WET-REV-002 required consolidations","docs/reviews/WET-REV-002_PDR_Disposition.md items 2 and 4; PMR-001 '2 outstanding for v0.3'","2026-08-07",
 "Two of four consolidations landed in v0.2; two were carried to v0.3.",
 "records/specs/WETSPEC002_v0.3 exists in the other governance tree - conformance to the two outstanding items is unverified by this review.",
 "PDR numbering reconciliation (DWR-005)","v0.3 ratification",
 "MEDIUM-HIGH","LOW-MEDIUM","P2","Under Review"),
("DWR-013","Independence disclosure for WET-SPEC-002 v0.3","D — Governance Debt",D,
 "WET-GAP-001 finding adopted under Ruling 2","WET-WF-001 Gap Register: 'v0.2 author = v0.1 reviewer -> v0.3 needs a different reviewer'","2026-08-11",
 "Single-operator condition; CAR-001 A4 later formalised independence disclosure.",
 "PDR-000003 already records the single-operator condition explicitly (section 7 Rule 6).",
 "CAR-001 Rev A independence disclosure form","v0.3 review",
 "MEDIUM","LOW","P3","Deferred"),
# ---------------- DEFERRED IMPLEMENTATIONS ----------------
("DWR-014","DJI / Insta360 telemetry parser (Pillar 2)","G — Future Capability",I,
 "we_capture Phase 1 planning","we_capture/PHASE1_PLANNING.md Pillar 2 (DEFERRED - evidence-driven)","2026-07 (approx)",
 "Evidence-driven deferral: on 103 real files the 9 timestamp fallbacks were .crdownload partials and a PDF, not DJI files. DJI_YYYYMMDDHHMMSS names already parse at fallback_level=0.",
 "Explicit trigger recorded in the source document. PI-04 compliance remains open; GPS redaction not required until GPS is actually extracted.",
 "None","A production run shows DJI files at fallback_level=2",
 "LOW until triggered","MEDIUM","P4","Deferred"),
("DWR-015","Camera Identity Robustness - full multi-layer system","C — Architectural Debt",I,
 "WET-WF-001 Gap Register GAP-04","GAP-04 'Elevated to foundational priority in engineering channel; not a polish item'","2026-08-11",
 "Content-based correction of mislabeled cards is proven in production; the full layered system was not built.",
 "Target: metadata/serial -> cameras.yaml mapping -> structure-based brand -> label as weakest hint -> conflict stop -> confirmation prompts. THIS IS THE SUBSTANCE OF THE 'CAPTURE DEVICE REGISTRY' TOPIC.",
 "cameras.yaml governance (DWR-016)","Next capture-side development cycle",
 "HIGH — novice-safety and identity correctness","MEDIUM-HIGH","P2","Deferred"),
("DWR-016","Bring cameras.yaml under governance as a named registry","B — Naming Hygiene",I,
 "PHI-001 review finding","cameras.yaml at repository root; self-described 'Camera Identity Registry ... SOURCE OF TRUTH'","2026-08-22",
 "Grew organically as a config file alongside the capture engine; never enrolled as a governed registry.",
 "It is the substance of the 'Capture Device Registry' the Executive Team remembers. It carries no registry_id, no registry_version, no schema version, and sits at repository root outside every governance tree.",
 "DIE spec registry framework F-1..F-5","PHI-001 disposition",
 "HIGH — closes a memory-only topic with an artifact that already exists","LOW","P1","Deferred"),
("DWR-017","SRT telemetry unit tests before promotion to VALIDATED","E — Technical Debt",I,
 "WET-WF-001 Gap Register GAP-02","GAP-02 'Unit tests for present / absent / malformed / gate-off required before promotion to VALIDATED'","2026-08-11",
 "Integration complete and config-gated (default false); promotion criteria stated but not met.",
 "Status is BUILT, not VALIDATED. GPS deliberately excluded from the pipeline path (privacy separation via telemetry.db).",
 "None","Before enabling timestamp.enable_srt_telemetry in production",
 "MEDIUM","LOW","P2","Deferred"),
("DWR-018","Production Health Report - full feature","F — Platform Opportunity",I,
 "WET-WF-001 Gap Register GAP-03","GAP-03 status: EXERCISED (basic clock audit) / DESIGN-COMPLETE (full feature); SPEC_Production_Health_Report.md","2026-08-11",
 "Design locked; only the basic clock audit was exercised in production.",
 "Design decisions already locked, including the rejection of a single 0-100 score. This is the nearest governed relative of the 'Production Intelligence Dashboard' topic.",
 "DWR-010 (score decision clarity)","Next production cycle",
 "HIGH","MEDIUM","P2","Deferred"),
("DWR-019","Full external-drive encryption execution","E — Technical Debt",I,
 "WET-WF-001 Gap Register GAP-06","GAP-06 status: ADOPTED (decisions) / OPEN (full external-drive encryption execution); SECURITY_RISK_ANALYSIS.md","2026-08-11",
 "Decisions D1-D4 adopted; execution across drives that leave the building not completed.",
 "FileVault on internal is in place. The gap is selective encryption for travelling drives.",
 "None","Before media leaves the building at scale",
 "HIGH (risk reduction)","MEDIUM","P2","Deferred"),
("DWR-020","STAGING_P2 closure path - grouping intelligence into edit usage","C — Architectural Debt",I,
 "WET-WF-001 Gap Register GAP-05","GAP-05 'Grouping engine is ready; edit usage of that intelligence was bypassed. Closure remains via STAGING_P2 path.'","2026-08-11",
 "Suite-validated engine; never production-used for the Part 1 edit.",
 "A built capability that has never delivered production value - the highest-leverage kind of deferred work.",
 "None","Part 3 edit planning",
 "HIGH — value already built, not yet realised","LOW-MEDIUM","P1","Deferred"),
("DWR-021","Packaged, signed dashboard application (.dmg path)","F — Platform Opportunity",I,
 "Dashboard prototype under custody","scripts/README_dashboard.md 'prototype / reference implementation ... not the packaged, signed app - that is the future .dmg path'","2026-06-30",
 "Prototype proves the 100% local, zero-CDN, zero-network mandate is achievable; packaging deferred.",
 "A working local read-only dashboard ALREADY EXISTS over the capture registry. This is the nearest governed relative of the 'Executive Dashboard' topic.",
 "Code signing / notarization (DWR-030)","Operational deployment need",
 "MEDIUM-HIGH","MEDIUM-HIGH","P3","Deferred"),
("DWR-022","CAR_ROADMAP.md - the CAR pipeline document","D — Governance Debt",I,
 "CAR-001 Rev A engineering amendment A1","CAR-001 A1 'CAR numbers identify review EVENTS ... never pre-allocated (pipeline: CAR_ROADMAP.md)'","2026-08-21",
 "The amendment was ratified referencing a pipeline document that was never created.",
 "A ratified governance instrument points at a file that does not exist. The eight planned reviews currently live in a single table cell in CAR_INDEX.md.",
 "None","PHI-001 disposition",
 "HIGH — a ratified reference must resolve","VERY LOW","P1","Deferred"),
("DWR-023","INTERVIEW_REGISTRY - spec-required, absent from disk","D — Governance Debt",I,
 "WET-SPEC-DIE-001 v0.2 section 7","Spec names nine registries; INTERVIEW_REGISTRY exists only in the specification text","2026-08-20",
 "Not created during Sprint 2 registry population; no empty-registry report was filed either.",
 "DIE spec V-5 requires populating all nine registries OR reporting each empty registry with a reason. Neither was done. The Sprint 3A communique named 'Interview Registry' as an ESS fusion input.",
 "DIE spec V-5","PHI-001 disposition",
 "HIGH — a frozen spec requirement is silently unmet","LOW (create, or file the empty-registry report)","P1","Deferred"),
("DWR-024","Cue custody rows in the registry","E — Technical Debt",I,
 "WET-GAP-001 finding adopted under Ruling 2","WET-WF-001 Gap Register: 'Registry = 726 camera rows, ZERO cue rows. Ungoverned-intelligence-layer risk is proven.'","2026-08-11",
 "The registry models the capture domain; the intelligence/cue domain was never given custody rows.",
 "Two BLACKTOP versions exist on disk without custody of which was accepted. The risk is described in the record as proven, not theoretical.",
 "PRS-001 (deferred)","Next intelligence-layer development cycle",
 "HIGH","MEDIUM","P2","Deferred"),
("DWR-025","ER-2 full session export, ER-4 manifest rights line, ER-5 license basis","D — Governance Debt",I,
 "WET-GAP-001 / Ruling 2 evidence requests","WET-WF-001 Gap Register ER list; PDR-000003 shows restrictions 'PENDING (ER-5)' and empty gate_clearance_ref","2026-08-11",
 "ER-1 (fresh FCPXML) was the convergent next action and is now satisfied for Part 2; ER-2/4/5 were not tracked to closure.",
 "ER-4 had a ready-to-run fix script in the Gap Register. Current status of all three is unverified by this review.",
 "None","Before GATE 2/3 on any release",
 "HIGH (publication-blocking)","LOW","P1","Under Review"),
("DWR-026","Rights-line coverage for KICKSTANDS UP v1 and other placed cues","D — Governance Debt",I,
 "PHI-001 predecessor finding; carried as AI-05","PDR-000003 coverage note: 'at least four additional placed cues (SLAB TALK, KICKSTANDS UP v1, Yo KICKSTANDS UP, The Piney Woods Transition) with no PDRs and no manifest rights lines'; 'record coverage is 2 of >=6 cue decisions'","2026-08-22",
 "Raised during the Sprint 3A confirmation but not created as a fifth PDR - the Executive Team had accepted a set of four.",
 "KICKSTANDS UP v1 is the single score asset in the Part 2 lock (00:00:00.000-00:01:16.417). GATE 2/3 require rights lines for ALL placed cues. Does not block MIE; blocks publication.",
 "DWR-025","Before GATE 2 on Part 2",
 "VERY HIGH — publication-blocking and currently unowned","LOW-MEDIUM","P1","Deferred"),
("DWR-027","Eight planned Collaborative Architecture Reviews","G — Future Capability",I,
 "CAR_INDEX row 3","CAR_INDEX.md: Production Intelligence Review · Digital Provenance & Asset Lineage · PBOM · Executive Dashboard & Analytics · Road Soul Lexicon · Conductor's Score Evolution · Platform Metrics · AI Governance Evolution","2026-08-21",
 "Listed as Planned (unnumbered per A1) - CAR numbers are assigned when a review convenes.",
 "This single table cell is the platform's entire forward review pipeline and holds five of the topics the Executive Team asked this review to find, including DPAL spelled out in full.",
 "DWR-022 (CAR_ROADMAP.md)","Each review convening",
 "VERY HIGH — this cell IS the institutional memory of the roadmap","LOW to expand into a roadmap document","P1","Deferred"),
("DWR-028","Retroactive Part 1 PDRs (8-10 records)","D — Governance Debt",I,
 "WET-REV-002 exercise-first order","WET-REV-002: 'Populate 8-10 retroactive PDRs from Part 1 decisions ... BEFORE v0.2 refinement'","2026-08-07",
 "Two pilots were authored (PDR-000003, PDR-000004); the remaining 6+ were not.",
 "PMR-001 records 'PDRs piloted: 2; pending: 6+'. The exercise-first order also gated PRS-001 and WET-SPEC-003.",
 "DWR-005 (numbering)","v0.3 refinement, or Part 1 archival",
 "MEDIUM-HIGH","MEDIUM","P2","Deferred"),
("DWR-029","Complete the two PDR pilots (BLACKTOP HYPNOSIS, OUT HERE)","D — Governance Debt",I,
 "WET-GAP-001 finding","Both recorded EXERCISED-INCOMPLETE (Draft); validator fails timeline.in/out because the Jul 29 FCPXML predates both cue decisions","2026-08-11",
 "Blocked on evidence (fresh FCPXML), which ER-1 has since produced for Part 2 but not for Part 1.",
 "PDR-000003 status is 'Draft', advancement gated on ER-2, ER-4, ER-5.",
 "DWR-025","Part 1 FCPXML re-export",
 "MEDIUM","LOW-MEDIUM","P3","Deferred"),
("DWR-030","Automated CI/CD, code signing/notarization, external security audit","E — Technical Debt",I,
 "MILESTONES.md honest verdict","MILESTONES.md: 'no automated CI/CD (tests are run on demand), no code signing/notarization, no external security audit'","2026-07-07",
 "Solo-developed, single-machine operating envelope; explicitly named as the gap between engineered-like-production and shipped-audited-deployed.",
 "The document is unusually candid about this and treats it as a known envelope, not an oversight.",
 "None","Contract deployment or external distribution",
 "HIGH for external deployment; LOW while single-operator","HIGH","P3","Deferred"),
("DWR-031","Machine-readable GATE 1/2/3","D — Governance Debt",I,
 "Gate Ledger Standard conformance table; carried as AI-04","WET-SPEC-GATE-001 section 9: publication gates are 'prose-only in SOP-06 - not yet machine-readable'","2026-08-22",
 "Re-expressing ratified gate law (CAPE clauses 17-19) is a Chairman act, not an implementation convenience.",
 "The gates with real consequences are the ones a dashboard currently cannot read.",
 "DWR-008 (Chairman session)","Chairman review session",
 "HIGH — observability of release authority","LOW-MEDIUM","P2","Deferred"),
("DWR-032","Full-resolution unwatermarked proxy for DIE-V","F — Platform Opportunity",I,
 "Sprint 3A delta D-24; carried as AI-01","RE-001 section 7; DOC-SRC-001 section 1 bullet 8","2026-08-22",
 "Sprint 3A was supplied a 320x180 watermarked proxy as visual ground truth.",
 "Caps every visual observation. Formation geometry, flag identification and camera-motion separation are unavailable at this resolution - a better proxy, not a better method.",
 "None","Before Sprint 4 DIE-V work",
 "HIGH","LOW (supply an export)","P1","Deferred"),
("DWR-033","RE-002 - regeneration after PDR disposition","F — Platform Opportunity",I,
 "Gate on_open.required_actions","intelligence/p2/ess/DOWNSTREAM_AUTHORIZATION_GATE.yaml on_open","2026-08-22",
 "Cannot occur until the four Sprint 3A PDRs are dispositioned.",
 "Closes Level 7 (Continuous Improvement): a scorecard index with one row is a baseline, not a trend.",
 "DWR-001..DWR-004","All four Sprint 3A PDRs dispositioned",
 "HIGH — makes platform evolution measurable","LOW (mechanism already armed)","P1","Deferred"),
("DWR-034","PRS-001 storage internals specification","G — Future Capability",I,
 "WET-REV-002 deferral","WET-REV-002: 'PRS-001 and WET-SPEC-003 remain deferred until then' (after retroactive PDRs)","2026-08-07",
 "Deferred behind the exercise-first order.",
 "PMR-001 owes 'exact registry count: TBD (A2/PRS-001)' to this specification.",
 "DWR-028","Retroactive PDR exercise complete",
 "MEDIUM","MEDIUM-HIGH","P4","Deferred"),
("DWR-035","WET-SPEC-003 (platform-core, number reserved)","G — Future Capability",I,
 "WET-REV-002 deferral","WET-REV-002; docs/README sequential platform-core series","2026-08-07",
 "Deferred behind the exercise-first order; the number remains unallocated.",
 "Relevant to numbering hygiene: WET-SPEC-GATE-001 deliberately used the named series to avoid taking this reserved number.",
 "DWR-028","Exercise-first order satisfied",
 "LOW until scoped","UNKNOWN","P4","Deferred"),
("DWR-036","Transmit 5 local commits to origin/main","E — Technical Debt",I,
 "Sprint 3A / PHI-001 execution environment; carried as AI-07","G3-ESS-001_EXECUTIVE_CONFIRMATION AI-07","2026-08-22",
 "The execution sandbox has no network egress and no SSH credentials; push fails host key verification.",
 "Environmental, not architectural. The commits exist and are complete; they need transmitting.",
 "Operator with repository credentials","Next operator session at the machine",
 "HIGH — unpushed governance is unshared governance","VERY LOW (one command)","P1","Completed"),
("DWR-037","Reference Executions archive no artifact snapshot; their scorecards derive from mutable live paths","F — Governance Debt",I,
 "ESS-004 regeneration, 2026-08-22","PDR-2026-08-22-ESS-004 section D.6; scripts/re_scorecard.py argv[1]","2026-08-22",
 "Discovered while regenerating under the ESS-004 ruling. RE-001 is declared immutable, but docs/reference_executions/ holds only META, SCORECARD and the narrative - no copy of the artifacts the scorecard describes. re_scorecard.py takes the seed path as an argument and was run against the LIVE intelligence/p2/ess/PRODUCTION_INTELLIGENCE_SEED.yaml. That path has now been overwritten by the ESS-004 regeneration, so re-running the generator for RE-001 today would stamp post-ruling numbers onto a pre-ruling archive.",
 "The archive is currently recoverable but not self-contained: RE-001's artifacts survive only in git history (commit b197e74 / 8033dc5). An archive whose immutability depends on nobody re-running its own generator is not immutable, it is merely undisturbed. Two candidate remedies: copy the artifact set into docs/reference_executions/RE-001_artifacts/ and repoint the generator at the copies, or have re_scorecard.py resolve its inputs through a git ref recorded in META. NOT implemented - flagged, because RE-002 will inherit the same defect on the same day it is created.",
 "Executive authorization; RE-002 archival is the natural moment","RE-002 archival (gate on_open action)",
 "HIGH — this is the archive's load-bearing property","LOW (a copy step plus a generator argument)","P1","Deferred"),
("DWR-038","No YAML load-and-assert-types lint gate on generated artifacts","E — Technical Debt",I,
 "D-26, found during the ESS-004 regeneration","PDR-2026-08-22-ESS-004 section D.6; STEP0_TIMING_CLOSURE delta D-26","2026-08-22",
 "Every YAML artifact of the RE-001 baseline serialized timecodes bare. Under YAML 1.1 a bare 00:31:43.000 loads as the float 1903.0, not the string. The defect survived a full validation pass because validation checked that the files PARSE, never that the loaded values have the types the schema intends.",
 "The write side is fixed (all timecodes are quoted at write time). The class of defect is not: any future field whose text happens to look like a YAML 1.1 scalar - sexagesimals, y/n/on/off, leading-zero integers, unquoted version strings - will fail the same way and pass the same validation. A round-trip assertion (load the artifact, assert every *_tc is a str and matches the timecode pattern) belongs in the generator's own validation step. Parsing is not validation.",
 "None — engineering capacity only","Next artifact-generating sprint",
 "MEDIUM — prevents a silent data-type corruption class","LOW (a dozen assertions in gen_artifacts.py)","P2","Deferred"),
("DWR-039","Road Soul behaviour vocabulary is undeclared, undefined and unenforced","F — Governance Debt",I,
 "RSB-AUDIT-001, prompted by the Executive Observation of 2026-08-22","docs/reviews/RSB-AUDIT-001_Road_Soul_Behavior_Vocabulary.md sections 3-4","2026-08-22",
 "CONDUCTOR_SCORE v1.1.0 already contains a closed 10-state behaviour vocabulary and a family-determined grammar holding across all 15 cues with zero exceptions. None of it is declared in any document. No validator enforces it. 39 action values compress to 14 distinct behaviours, which is language-like compression, but nothing states the set is closed and nothing would flag a 16th cue introducing an 11th state.",
 "This is the gap between a house style and a specification. Items 1-3 of the recommended WET-SPEC-RSB-001 are transcription of what the artifact already contains - the audit carries most of the content. Deliberately NOT started immediately: writing the MOTION grammar before CUE-03 and CUE-07 are realized would freeze it on two unrealized cues (DWR-041). Recommended order: ESS-002 boundary, CUE-03, CUE-07, then the spec.",
 "ESS-002 disposition; CUE-03 and CUE-07 realization","CUE-07 selection PDR",
 "VERY HIGH — Chairman ER-002-N2, 2026-08-22: the behavioural specification must OUTLIVE Suno, Udio and whatever comes next. Engine independence is now a stated Executive REQUIREMENT on this spec, not a desirable property. The durable asset is not the music and not the prompts - it is this specification.","LOW-MEDIUM (sections 1-3 are transcription; section 4 is real work on four states)","P1","Deferred"),
("DWR-040","Four of ten behaviour states carry no pass/fail test - reproducibility is untestable","F — Governance Debt",D,
 "RSB-AUDIT-001 section 5","docs/reviews/RSB-AUDIT-001_Road_Soul_Behavior_Vocabulary.md section 5","2026-08-22",
 "DUCK, REBUILD, BREATHE, APPROACH and RETURN carry numeric criteria and are testable. ENTER, SUSTAIN, LEAD and HANDOFF are prose-only: 'never a downbeat announcement', 'inaudible as an event', 'ambient sound must remain audible' cannot be checked by anyone who did not write them. FLOOR is partly testable. A specification whose satisfaction requires asking its author is a preference with formatting.",
 "Classed DECISION, not IMPLEMENTATION, because it asks the Executive Team a question engineering must not answer alone: how much of the artistry-carrying behaviour is the platform willing to quantify? Evidence so far is encouraging - the five quantified states lost nothing by being quantified - but that evidence comes from the five easiest, and the remaining four are the ones that carry the music. A fabricated threshold would be worse than none; PROVISIONAL tests, explicitly marked, are the honest middle.",
 "Executive ruling on how far to quantify","WET-SPEC-RSB-001 drafting",
 "HIGH — the reproducibility claim rests entirely on this","MEDIUM (four states, each needing a defensible test or an explicit PROVISIONAL marker)","P1","Deferred"),
("DWR-041","MOTION family grammar rests on two cues, neither of them realized","E — Technical Debt",I,
 "RSB-AUDIT-001 section 4.1","docs/reviews/RSB-AUDIT-001_Road_Soul_Behavior_Vocabulary.md section 4.1","2026-08-22",
 "MOTION contains only CUE-03 ESCORT_ANTHEM and CUE-07 RIDE_PASSAGE. Neither has been generated. CUE-03 is the cue currently under dispute in ESS-002. The MOTION grammar therefore has the thinnest evidence of any family while carrying the decision in front of the Executive.",
 "Whatever EVS-001 rules about CUE-03 becomes half the evidence base for how MOTION behaves. CUE-07 is the only independent check and is unscored today. This is why DWR-039 is sequenced after CUE-07 rather than started now: a grammar written from one disputed cue and one absent cue would be a guess with a document number.",
 "MIE Pass 3 (gated behind the Conversation family gate and this gate)","CUE-07 realization",
 "MEDIUM — bounds how much can be claimed about MOTION until Pass 3 runs","NONE (this is a constraint to respect, not work to schedule)","P2","Deferred"),
("DWR-042","Behaviour states carry no transition model - half the proposed Grammar layer is unbindable","F — Governance Debt",I,
 "RSB-AUDIT-001 Amendment 1, Correction 2","docs/reviews/RSB-AUDIT-001_Road_Soul_Behavior_Vocabulary.md Amendment 1","2026-08-22",
 "The Executive proposed four grammar rules. Two are SET constraints and verify clean against the artifact today: 'BREATHE only in CONVERSATION' (0 violations, all 4 CONVERSATION cues carry it, no other cue does) and 'LEAD forbidden during SILENCE' (0 violations; silences carry only APPROACH/FLOOR/RETURN). Two are TRANSITION constraints and cannot be checked at all: 'LEAD never follows LEAD' and 'HANDOFF cannot begin inside DUCK'. behaviour_states is a SET, not a state machine. Every field ever used on a behaviour state is: state, action, target_db, sidechain, budget_s, max_gain_db, permitted_between_answers, window_s. No field expresses time, order, sequence or transition condition anywhere in the artifact.",
 "The list READS chronologically - ENTER, SUSTAIN, DUCK, REBUILD, HANDOFF - but nothing declares that, and DUCK and REBUILD plainly recur through a cue rather than occurring once in sequence. This is not an argument against the rules; both transition rules are musically sound. It is an argument that the Grammar layer costs materially more than the Lexicon layer and that the two must not be scheduled as one job. Lexicon is transcription. Grammar needs a model that does not exist.",
 "A state transition model: entry conditions, exit conditions, legal successors","WET-SPEC-RSB-001 drafting, after CUE-03 and CUE-07",
 "MEDIUM — bounds what the Grammar layer can promise","MEDIUM (a model, not a transcription)","P2","Deferred"),
("DWR-043","Expression content sits inside CONDUCTOR_SCORE, contrary to the governs/performs distinction","F — Governance Debt",D,
 "RSB-AUDIT-001 Amendment 1, Correction 3","docs/reviews/RSB-AUDIT-001_Road_Soul_Behavior_Vocabulary.md Amendment 1","2026-08-22",
 "Executive Observation 2026-08-22: 'Conductor's Score is behavior. Road Soul is expression. One governs. One performs. Those should never be merged.' Applied to the artifact it finds a live violation: CONDUCTOR_SCORE.yaml carries instrumentation_guidance on 13 of 15 cues, with fields colour, instruments, tempo, tonality, prohibited - for example 'fingerpicked or clean electric guitar, pad, brushed kit or no kit, low strings; slow to mid; warm major or dorian'. Each cue also carries road_soul_family. That is expression inside the behaviour artifact.",
 "Classed DECISION because the remedy is not obvious and is not engineering's to pick: split the artifact, keep the field but mark it advisory-and-non-normative, or accept that the Conductor's Score legitimately carries a pointer to expression without owning it. Only 'prohibited' reads as behaviour, and only where phrased as a constraint on function ('no percussion transients that read as an event') rather than on material. Flagged, NOT fixed - splitting CONDUCTOR_SCORE while ESS-002 is still open against it would be restructuring the artifact under an open decision, and the Executive has directed that validation precede further governance work.",
 "Executive ruling on the remedy; ESS-002 closed first","ESS-002 disposition, then WET-SPEC-RSB-001 drafting",
 "MEDIUM-HIGH — the distinction is a candidate architectural principle and the artifact contradicts it","LOW to flag, UNKNOWN to remedy (depends which remedy)","P2","Deferred"),
("DWR-044","Palette ownership is unallocated - it is neither behaviour nor any layer of the Road Soul stack","F — Governance Debt",D,
 "ER-002 engineering note N1","docs/rulings/EXECUTIVE_RULINGS.yaml ER-002-N1","2026-08-22",
 "ER-002 places 'Instrumentation: electric guitar, warm organ, upright bass, brush kit' inside the platform-owned Type A Behavioural Specification. By the ruling's own test - behaviour defines what the music must DO - a named instrument says what the music IS, not what it does. The line runs THROUGH the instrumentation field: constraints are behaviour and are testable ('no lyrics', 'no builds', 'no percussion transients that read as an event'); a palette is expression. The same finding is already open as DWR-043 against CONDUCTOR_SCORE, and it now appears inside the ruling that was meant to separate the two.",
 "Proposed remedy, NOT adopted: the platform may CITE a governed family palette but may not INVENT one. Family palettes are Executive-authored once per family and live with Road Soul, not with the Conductor's Score. A Behavioural Specification then reads 'palette: Road Soul MOTION (see family definition)'. This preserves engine-independence - the spec stays handable to any generation engine - without the platform authoring musical material. Open question underneath: a palette is not Lexicon, not Grammar, not Behaviour and not Composition. It sits outside the four-layer stack entirely. Either the stack needs a fifth element or the palette belongs to Composition as an Executive-owned input.",
 "Executive ruling on palette ownership and on where it sits in the stack","first Road Soul cue PDR, or WET-SPEC-RSB-001 drafting",
 "HIGH — it decides what a Behavioural Specification may contain, and that spec is the platform's durable asset","LOW to specify once ruled","P1","Deferred"),
("DWR-045","EDITORIAL_MECHANICS_REGISTRY - 79.1% of the resolved timeline is collected but never surfaced","G — Future Capability",I,
 "ER-003 (COM-004) founding evidence","docs/rulings/EXECUTIVE_RULINGS.yaml er_003.founding_evidence","2026-08-22",
 "The resolver produced 1025 elements; only 214 (depth-0) were ever presented. 811 - 79.1% - were filtered out at presentation because they were judged not immediately useful. The Executive named a 27:10 map overlay from the picture that the platform had resolved hours earlier and withheld. Not missing data: withheld data.",
 "ER-003 forbids exactly that filtering: 'the platform should not evaluate whether an editorial mechanic is important.' Already extractable TODAY at no new measurement cost, from an artifact the platform holds with a resolver validated 191/191: 180 transitions across 8 kinds (166 Cross Dissolve; mean 0.889 s, median 1.000 s, range 0.125-1.000), 109 connected storylines, 57 titles, 22 distinct lanes in use, 478 asset-clips. The first tranche costs a SCHEMA, not a measurement.",
 "A registry schema and an Executive decision on scope","next ingestion sprint; no dependency on Part 2 completion",
 "HIGH — this is the production-intelligence asset ER-003 exists to accumulate, and it is sitting in a file already parsed","LOW-MEDIUM (extraction is done; the work is schema and emission)","P2","Deferred"),
("DWR-046","Layer 2 (Screen Presentation) has no validated instrument and no observer provenance class","G — Future Capability",D,
 "ER-003-N1","docs/rulings/EXECUTIVE_RULINGS.yaml er_003.engineering_notes ER-003-N1","2026-08-22",
 "Layer 1 has an instrument (FCPXML resolver, 191/191). Layer 3 has an authority (the Executive). Layer 2 has neither. DIE-V observes a 320x180 watermarked proxy at 64x36 / 2 fps and cannot see 'a map graphic dissolves into the upper-left corner' - ER-003's own Layer 2 example is beyond every instrument the platform currently owns.",
 "The sharper point: that example came from a HUMAN watching, not a machine. A human-observed Layer 2 fact and a machine-derived one are different evidence classes - one is reproducible by re-running code, the other only by another human watching. DOC-001 requires an instrument be validated before its output enters custody, and a human observer's validation is a second observer, which is exactly the EIO/IEO distinction already ruled for EVS. Proposed and NOT adopted: Layer 2 records carry an observer field - MACHINE with a named validated instrument, or HUMAN with an observer identity and observation class. Neither superior; conflating them would let an unreproducible observation inherit a machine-derived record's authority.",
 "Executive ruling on Layer 2 schema; a validated Layer 2 instrument if machine observation is wanted","Layer 2 schema design",
 "MEDIUM-HIGH — decides whether Layer 2 is a real layer or an aspiration","MEDIUM (schema is cheap; a validated visual instrument is not)","P2","Deferred"),
("DWR-047","Two proposed production-intelligence KPIs cross ER-003's own boundary; none carry frozen definitions","F — Governance Debt",D,
 "ER-003-N2 and ER-003-N3","docs/rulings/EXECUTIVE_RULINGS.yaml er_003.engineering_notes","2026-08-22",
 "Most listed KPIs are Layer 1 arithmetic and safe. Two are not. RIDE-TO-INFORMATION RATIO requires classifying each shot as ride or information - a judgement about what a shot is FOR, absent from the FCPXML and invisible in a frame. It is a Layer 3 interpretation wearing a Layer 1 name. CORRELATION WITH AUDIENCE RETENTION uses data that is not editorial metadata, does not exist in the platform, arrives from a distribution service and carries its own consent and accuracy questions; published without caveats it invites a causal claim the data cannot support. Separately, NO listed KPI carries a frozen definition: this lock holds 180 transitions of 8 kinds, 166 of them Cross Dissolves, so 'average dissolve duration' differs defensibly between a run counting cross-dissolves and one counting all transitions. 'Transition density by chapter' has no definition of chapter.",
 "Proposed and NOT adopted: a KPI is admissible under ER-003 only if every term is derivable from Layer 1 or an instrumented Layer 2 with no human classification step. Ride-to-information becomes admissible once an Executive-defined shot taxonomy exists - then the classification is Executive-authored and the platform merely counts. Retention correlation is deferred as an external-data-class question, not an editorial-mechanics one. Every KPI carries a frozen definition, a version, and the resolver version that produced it, exactly as registries carry registry_version. This is the measurement-vs-score test applied to production intelligence.",
 "Executive ruling before either KPI is implemented; a shot taxonomy for the first","first KPI implementation",
 "HIGH — an unversioned KPI compared across productions is a composite score by another route","LOW to specify, HIGH to retrofit if skipped","P1","Deferred"),
]

RESOLUTIONS = {
 "DWR-044": {
   "resolution": ("PARTIALLY RULED, 2026-08-22, Executive Clarification 2. PALETTE is recognised as a "
                  "DISTINCT ARCHITECTURAL LAYER - the fifth - sitting between BEHAVIOR and COMPOSITION. "
                  "Palette constrains permissible expressive space but does not prescribe musical "
                  "realization. OWNERSHIP RULED: Executive. The platform may REFERENCE an "
                  "Executive-defined palette and test candidates against it; it shall NOT author, "
                  "extend, add terms to, or infer one. Revised stack: LEXICON -> GRAMMAR -> BEHAVIOR "
                  "(platform) -> PALETTE (Executive) -> COMPOSITION (composer). "
                  "The three questions: behaviour asks what must the music ACCOMPLISH; palette asks "
                  "what universe may it INHABIT; composition asks what shall this cue BECOME. "
                  "STILL OPEN: (a) no palette has been authored for any family, so nothing can yet be "
                  "referenced; (b) EC-N1 - a palette is only testable if its term vocabulary is closed. "
                  "Palette conformity is one of ER-001's eight criteria and must therefore report a "
                  "measurement and a method, but 'discouraged' has no method. Proposed and NOT adopted: "
                  "PERMITTED->PASS, RESTRICTED->UNCERTAIN-escalate, FORBIDDEN->FAIL, plus a declared "
                  "list_closure of CLOSED or OPEN. That makes palette conformity machine-testable "
                  "without the platform authoring a single term."),
   "resolution_artifact": "docs/rulings/EXECUTIVE_RULINGS.yaml executive_clarification_2026_08_22.clarification_2; notes EC-N1",
   "resolution_date": "2026-08-22",
   "resolution_authority": "Executive Producer / Chairman"},
 "DWR-043": {
   "resolution": ("ESCALATED 2026-08-22 and now BLOCKING. Executive Clarification 2 makes the finding "
                  "sharper than when it was raised: instrumentation_guidance on 13 of 15 cues of "
                  "CONDUCTOR_SCORE is PALETTE content, which the platform may reference but not author. "
                  "The clarification is prospective, so the current artifact and RE-001 are NOT "
                  "retroactively non-conforming. BUT CONDUCTOR_SCORE regenerates on the ESS-002 "
                  "disposition, and gen_artifacts.py would re-author that content at that moment - "
                  "knowingly emitting a non-conforming artifact. Three options recorded at EC-N2: "
                  "(A) retain, marked ADVISORY and NON-NORMATIVE, awaiting palette ratification; "
                  "(B) strip and replace with a palette reference - BLOCKED, no palette exists; "
                  "(C) freeze the field and emit it verbatim as inherited content rather than "
                  "re-deriving it. NO RECOMMENDATION - this is the palette-ownership decision and it "
                  "is Executive. "
                  "RULED 2026-08-22: OPTION C. 'Until Executive-approved Road Soul Palettes exist, "
                  "instrumentation guidance inherited from previously governed artifacts shall be "
                  "preserved verbatim and explicitly identified as inherited content. The platform "
                  "shall neither author nor extend expressive guidance during regeneration.' "
                  "IMPLEMENTED in intelligence/p2/ess/scripts/gen_artifacts.py the same day: the field "
                  "is renamed inherited_expressive_guidance and now emits governance_class, "
                  "normative: false, authored_by: NOT_THE_PLATFORM, status "
                  "AWAITING_EXECUTIVE_PALETTE_RATIFICATION, its ruling_ref, its provenance chain, and "
                  "an on_palette_approval instruction to DELETE the block and replace it with a palette "
                  "reference by governed regeneration. Values are carried forward verbatim, never "
                  "re-derived. A SHA-256 digest guard over the frozen table stops generation with a "
                  "NOTICE if any value is edited - the ruling is checkable rather than merely intended "
                  "(NO SILENT RECOVERY). Guard verified in both directions: silent when frozen, fires "
                  "on mutation. 13 of 15 cues carry the block; the two conducted silences correctly do "
                  "not. NO LONGER BLOCKING. The artifact itself is NOT regenerated here - regeneration "
                  "belongs to the ESS-002 disposition, and regenerating outside a governed trigger "
                  "would be the defect this entry exists to prevent."),
   "resolution_artifact": "docs/rulings/EXECUTIVE_RULINGS.yaml EC-N2; intelligence/p2/ess/scripts/gen_artifacts.py",
   "resolution_date": "2026-08-22",
   "resolution_authority": "Executive Producer / Chairman"},
 "DWR-040": {
   "resolution": ("PARTIALLY RULED, 2026-08-22, Executive Producer. The taxonomy is ADOPTED and the "
                  "unit of classification is settled: classify CRITERIA, not states. A single behaviour "
                  "may carry criteria of different classes - ENTER carries '<=2 s' (Type A) and 'never a "
                  "downbeat announcement' (Type C) simultaneously. "
                  "TYPE A machine-measurable. TYPE B observable now, measurable eventually. "
                  "TYPE C Executive judgement. "
                  "TYPE C GUARDRAIL, ruled constitutional in intent: every Type C criterion SHALL record "
                  "(1) why measurement is currently inappropriate, and (2) WHAT EVIDENCE WOULD JUSTIFY "
                  "RECONSIDERING THAT CLASSIFICATION. Requirement (2) strengthens the engineer's proposed "
                  "'re-review trigger': a trigger is a date, whereas named evidence is falsifiable - the "
                  "classification can be overturned by something specific rather than merely revisited on "
                  "a schedule. Type C is therefore PROVISIONAL BY DEFAULT and permanent only by decision. "
                  "STILL OPEN: which criteria land in which class. That is the drafting work, and it "
                  "remains sequenced behind CUE-03 and CUE-07 per DWR-041 and behind a transition model "
                  "per DWR-042."),
   "resolution_artifact": "docs/reviews/RSB-AUDIT-001_Road_Soul_Behavior_Vocabulary.md Amendment 1; Executive Review of commit 47f5268",
   "resolution_date": "2026-08-22",
   "resolution_authority": "Executive Producer"},
 "DWR-010": {
   "resolution": ("EXTEND GAP-03. Executive Ruling, 2026-08-22. The prohibition on composite "
                  "readiness/health scores is extended to Capture Readiness, Acquisition Intelligence "
                  "and all future platform health reporting. Percentages permitted only for directly "
                  "measurable quantities; no opaque aggregation without explicit Executive approval. "
                  "Supersedable only by an ADR that explicitly does so."),
   "resolution_artifact": "docs/specs/WET-SPEC-REPORT-001_Platform_Reporting_Standard.md",
   "resolution_date": "2026-08-22",
   "resolution_authority": "Executive Producer"},
 "DWR-036": {
   "resolution": ("Transmitted 2026-08-22 by the operator: ff0c45f..d0b0f89, 9 commits, 137 objects, "
                  "193.67 KiB. Verified from the session side: local main == origin/main == "
                  "d0b0f893012f965f20ef5d5b4c67248e7eaf7af9, 0 ahead, 0 behind."),
   "resolution_artifact": "git: origin/main @ d0b0f893012f965f20ef5d5b4c67248e7eaf7af9",
   "resolution_date": "2026-08-22",
   "resolution_authority": "Operator",
   "recurring_constraint_note": (
     "This instance is closed; the underlying condition is NOT. The execution sandbox has no network "
     "egress and no SSH credentials, so every future session will accrue local commits requiring an "
     "operator push. Recorded here rather than opened as a standing register entry - raise one if the "
     "Executive Team wants it tracked as a permanent operational constraint rather than a closed item.")},
}

entries = []
for r in ROWS:
    e = dict(zip(REQ, r))
    e.update(RESOLUTIONS.get(e["dwr_id"], {}))
    missing = [k for k in REQ if not e.get(k)]
    if missing:
        sys.exit(f"{r[0]} missing {missing}")
    entries.append(e)

doc = {
 "register_id": "DEFERRED_WORK_REGISTER",
 "conforms_to": "DWR-001 Deferred Work Register Standard v1.0",
 "version": "1.0.0",
 "status": "FOR EXECUTIVE REVIEW — recommendations only, no implementation authorized",
 "produced_by": "CAR-003 Platform Hygiene Review (PHI-001)",
 "date": "2026-08-22",
 "identifier_note": (
   "Entry identifiers DWR-NNN collide with the standard's own document ID (DWR-001). "
   "This review recommends renaming the standard to WET-SPEC-DWR-001, matching the "
   "named-series convention already used by WET-SPEC-DIE-001 and WET-SPEC-GATE-001, "
   "which frees the DWR-NNN space for entries. Flagged rather than silently resolved."),
 "class_definitions": {
   "DECISION": ("A question still requiring an Executive or Chairman ruling. Cannot be "
                "scheduled as engineering work until answered."),
   "IMPLEMENTATION": ("A decision already made and intentionally postponed. Can be "
                      "scheduled; needs capacity, not authority.")},
 "counts": {
   "total": len(entries),
   "deferred_decisions": sum(1 for e in entries if e["class"] == D),
   "deferred_implementations": sum(1 for e in entries if e["class"] == I)},
 "entries": entries,
}
with open("DEFERRED_WORK_REGISTER.yaml", "w") as f:
    f.write("# Deferred Work Register — produced by CAR-003 Platform Hygiene Review (PHI-001)\n")
    f.write("# FOR EXECUTIVE REVIEW. Recommendations only. No implementation authorized.\n")
    yaml.safe_dump(doc, f, sort_keys=False, width=100, allow_unicode=True)
print("entries:", len(entries), "| decisions:", doc["counts"]["deferred_decisions"],
      "| implementations:", doc["counts"]["deferred_implementations"])
