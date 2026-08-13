# SOP-05 — Chronological Sets Import (Part 2, LOCKED)
## Governance Status
Document Type: SOP (exercised 2026-08-13) · Normative Authority: None (ratification-candidate)

DOCTRINE (Chairman, 2026-08-13): the Insta360 X5 curated footage, in
chronological order, is the FOUNDATIONAL video — the spine all other
cameras build on. Presentation must interleave all cameras by TRUE
capture time and group paired coverage into SETS so no timestamp
hunting is ever required.

METHOD: scripts/chrono_sets_p2.py → one FCPXML → one import.
- Times: X5 via parent-stem capture time + (N) pull order (lineage);
  DJI via filename; OM-1 via verified local mtime. Machine clock only.
- Names: order-index + time + camera → browser Name-sort = chronology
  (fixes lexicographic camera-prefix clumping).
- Keywords: SET_NN (20-min temporal clusters, tunable) + scene names.
- Reconciliation: script prints per-camera counts + skipped-with-reason;
  NO UNEXPLAINED DELTAS. Locked run: X5=40 DJI=31 OM1=9 TOTAL=80, 14 sets.
- Import-of-record: records/p2/P2_CHRONO_SETS.fcpxml (this exact XML).
FCP: delete superseded events → File>Import>XML → sort by Name.
LESSONS ENCODED: spine never an afterthought · .insv/.orf never as
timeline assets · curated exports ride the XML natively (engine
enhancement filed for generalized scene/set stage).
