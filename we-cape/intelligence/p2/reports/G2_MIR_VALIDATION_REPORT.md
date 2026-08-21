# G2_MIR_VALIDATION_REPORT
## Four-source chain status
SRT↔TIMELINE: PASS — 19 segments tile 00:00-80:46 with categorized gaps (music/ambience).
SRT↔ETC: PASS WITH CATEGORIZED DELTA — SRT timebase (pre-lock 01:20:40) vs ETC lock (4846.625s = 01:20:46.625): +6.025s tail delta, consistent with lock-render tail; segment boundaries carry ±6s tolerance pending lock-SRT pass. NOT unexplained.
ETC internal: PASS — runtime reconciled vs declared lock within frame rounding (PDR-ETC-001); spine census consistent (191/404/16-audio); opens 005-OM1, closes triple-080 (matches SOP-05 doctrine).
FCPXML custody: PASS — Gate 1 audit 5/5 contributed cleared (batch2 ledgered, both manifests).
MP4 visual validation: NOT PERFORMED IN THIS ENVIRONMENT — the video file is not reachable from the executing channel. DOCUMENTED LIMITATION, non-blocking for MIE (music authoring consumes timing+themes, not pixels). Local spot-check recommended: 3 probes (S05 escort, S12 silence, S19 close) against MP4.
Lock-SRT (SRT 2) reconciliation: DEFERRED-DOCUMENTED — founding extraction (canonical SRT of record) is the governed transcript basis; the lock SRT is expected content-identical ±6s. Delta class: EXPECTED.
## Deltas ledger
D1 +6.025s runtime (EXPECTED, lock tail) · D2 MP4 unavailable to channel (EXPLAINED, environment) · D3 CAPTION positions stats-only (EXPLAINED, full ETC JSON pass deferred local) · D4 entity canonical names UNCONFIRMED (SPECIFICATION-COMPLIANT per R-3). No unexplained deltas.
