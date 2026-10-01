# EO-2026-09-29 — ADDENDUM C: EPR-07 Retirement Rationale Correction
## Governance Status
Instrument: Executive Ruling (Addendum to EO-2026-09-29) · Authority:
Chairman/EP · Date: 2026-10-01 · Ruling: "CHAIRMAN / EXECUTIVE RULING —
EPR-07 RETIREMENT INTEGRITY", **Option B**. Basis: the PBC-1 / EPR-07 /
S19 retirement-integrity audit (read-only, 2026-10-01). Register entry
deferred (per EO). Correction by addendum; the original ruling text is
preserved and is not rewritten.

## 1 — OPERATIVE DISPOSITION: UNCHANGED — EPR-07 REMAINS RETIRED
The governing disposition is the Executive ruling recorded in EPR-001
(EPR-07 `retirement`, transcribed verbatim): EXECUTIVE ORDER - EPR-001
RATIFICATION & RUN_ID LOCK RELEASE, section 1, Q10 — `disposition:
RETIRE`, adjudicated 2026-08-28 by the Executive Producer / Chairman
(repository custody commit `c7b5d3a`, recorded 2026-08-29 UTC).
**It remains in force.** The later G8-ratified evidence below does not
revoke or reinstate EPR-07. EPR-07 is not returned to active status; no
replacement narrative is inferred; its function is not migrated to any
other beat. Its consequences stand as ruled (EPR-06 terminal; no
migration; no inferred replacement content; provenance intact).

## 2 — HISTORICAL RATIONALE: SUPERSEDED AS TO FACT
The ruling's supporting rationale (verbatim, preserved as historical
record and NOT rewritten in EPR-001):
> "Under the ratified Path B (Episodic Production Architecture), S19
> (Ride_Home) exists entirely outside the governed 08-24 production
> runtime."

That factual premise is **contradicted by the later G8-ratified
re-derivation.** The retirement-era figure was the 08-22 assembly span of
S19 (4784–4846 s) compared against the 08-24 runtime (4689.5 s)
(EPR-001_VALIDATION_REPORT_PATH_B.md §2, `87ef710`), which that report
itself stated were not positions in the governed production.

## 3 — CORRECTED EVIDENTIARY STATE
- The authoritative v2 mapping places the measured S19 material **inside**
  the governed runtime: 08-24 4626.875–4688.875 s (62.000 s), both
  boundaries MAPPED at a constant −157.125 s, nothing removed; captions
  CORROBORATED at start (−156.958 s) and end (−156.912 s).
- The mapped S19 material **ends before** the governed-runtime boundary
  (4688.875 s < 4689.5 s).
- **This corrected measurement does not itself rescind the EPR-07
  retirement ruling.**

Durable repository evidence:
- `intelligence/p2/ess/DECISION_PACKET_B5_B14.md` §4, S19 † row
  (packet `aec3a27`; accepted by Addendum A).
- `intelligence/p2/ess/decision_packet_b5_b14/rederivation.json`, segment
  S19 — sha256 `5d6994b3f36de5bc07d3987cdb3bd611f70493390a8f6a8ed50828a79d666117`
  (v1; historical).
- `intelligence/p2/ess/decision_packet_b5_b14/v2/rederivation_v2.json`,
  segment S19 — sha256
  `5bd4af486e9eb745660504b41290154fb5d8c0b511b6bc74cca5102dd4b0a28b`,
  G8-ratified (Addendum B, `1f806de`). S19 is identical in v1 and v2.
- `intelligence/p2/registries/TIMELINE_REGISTRY.yaml` v1.1.0 (sha256
  `510697b9bbd1ed01c6c61ab6c6063dd511cfc71abad0ad11629fbeb807db0da3`,
  ratified `096d127`) carries S19 deliberately **untouched, in 08-22
  seconds** (`changelog.untouched: [S19]`). The registry representation
  therefore differs from the measured evidence by design; this addendum
  does not change it.

## 4 — CONSEQUENCE FOR PBC-1
With this correction recorded, EPR-001 `path_b_consequences` PBC-1 may be
recorded `status: RESOLVED_BY_RETIREMENT` under the existing lifecycle
mechanism, keeping the caveat that the underlying substantive support
question was not itself answered, and noting that EPR-07 remains retired,
that its outside-runtime rationale is corrected by this addendum, and that
the correction does not reinstate EPR-07.

## SCOPE
The EPR-07 entry text is not edited. PBC-2, PBC-3, PBC-4 and PBC-5 are
not reopened. No EPR-001 or TIMELINE value is changed by this addendum.
No regeneration is authorized; regeneration holds are unaffected.
