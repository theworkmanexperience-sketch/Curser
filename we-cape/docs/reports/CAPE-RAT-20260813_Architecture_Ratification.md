# CAPE-RAT-20260813 — Architecture Ratification (20 Clauses)
## Governance Status
Document Type: Ratification Record · Ratified in principle by Chairman 2026-08-13
Normative Authority: Binding on implementation; formal ADR to be minted from git tree at dev session
Title of resulting ADR: "Asset Identity, Temporal Authority, Evidence Resolution & Editorial Emission"
Basis: Chairman's Ratification Brief + Engineering review (16→20 clauses) + AlphaRoundUp production evidence
Invariant groups: Preamble(3) · Custody(1,2,4,19) · Evidence(5,6,7,14,15,20) · Correlation(11,12,13) · Emission(8,9,10,16,17,18 + Emission Contract)

## The Twenty Clauses (Chairman's final wording, confirmed by Engineering)
1. Original media is immutable — never renamed, rewritten, or modified for organizational convenience.
2. Original camera filenames are immutable identifiers of source provenance; presentation/derivative names never replace them.
3. The CAPE registry is the authoritative organizational/catalog layer; NLE metadata, filenames, folders, and artifacts are projections of registry truth.
4. Every asset has stable content identity (content.id SHA-256); no redundant asset_id/content_hash concepts.
5. Camera body identity is an asset property, never a removable-card property.
6. Camera identity records conclusion AND provenance (body code, unit serial where available, source, confidence); conflicts never silently resolved.
7. Canonical event time is derived by CAPE from evidence; corrected_timestamp evolves into the canonical representation with raw/source/tz/confidence/offset support.
8. FCP Content Created is not CAPE's authoritative chronological signal (diagnostic/secondary only).
9. CAPE-normalized FCP clip names carry sortable chronology + camera identity without renaming sources.
10. Namespaced camera keywords (CAM_X5, CAM_OM1, CAM_DJI5, CAM_DJI6) are the primary FCP camera-organization mechanism; Camera Name optional where reliable.
11. Temporal overlap generates candidate SET/scene relationships; it does not prove membership.
12. GPS is corroborating evidence, not mandatory; correlation must work without it.
13. Inferred SET/scene relationships carry evidence + confidence; reversible, human-confirmable.
14. Camera clock synchronization is a formal pre-shoot procedure (tz/DST verify, common reference, filmed clock, sync event → SOP-04).
15. Clock corrections stored as offsets/normalization metadata; original timestamps never rewritten.
16. Final Cut Pro is CAPE's editorial interface, not CAPE's metadata authority.
17. Gate-1 filtering occurs at emission: consent-pending/disallowed media never enters CAPE-emitted artifacts. Rights enforcement is a system responsibility.
18. Every stage boundary obeys No-Unexplained-Deltas: in/out counts + categorized deltas; unexplained change = defect.
19. Archive and working media are operationally separated; archive volumes are never load-bearing for active edits.
20. Evidence conflicts produce an explicit unresolved state (UNKNOWN/conflicted, flagged for review); CAPE never picks a silent winner.

## Sub-tier: Emission Contract (beneath clause 17)
CAPE-emitted FCPXML contains only media formats the target NLE imports successfully (F3 remediation; generator requirement, not top-tier architecture unless multi-NLE support is declared).

## Dispositions incorporated
Schema: extend, don't parallel — content.id stays sole identity; corrected_timestamp evolves; add capture_ts_raw, ts_source, ts_confidence, tz_offset, per_camera_clock_offset, camera_body_code, camera_unit_serial, camera_id_source, camera_id_confidence; lineage/offload-job/card fields migrate only where traceability materially improves.
F1 confirmed/remediation ratified (closes when schema+normalization ship) · F2 same (columns must exist AND populate) · F3 mitigated→Emission Contract · F4 open, engine · F5 confirmed/remediation ratified (closes when body resolution ships with evidence).
Implementation boundary: docs now · registry migration at dev session · engine channel (identity chain, normalization, conflict handling, scene/set stage, F3/F4) · generator at Part 3 (Gate-1 + importability filters, CAM_ namespace, body codes, singles) · Part 2 edit untouched (body keywords only, after custody tally proves the DJI5/DJI6 split) · Part 3 = first full deployment.
Outstanding evidence (not ratified): DJI5/DJI6 split · DJI serial availability · FCP Camera Name XML writability · SET window values · OM-1 body designation.
