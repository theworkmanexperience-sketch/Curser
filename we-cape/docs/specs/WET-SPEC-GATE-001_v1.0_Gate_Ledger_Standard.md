# WET-SPEC-GATE-001 v1.0 — Gate Ledger Standard
## Governance Status
Document Type: Specification (named-series) · Status: **RATIFIED** · Date: 2026-08-22
Authority: Executive Producer (Executive Assessment, Sprint 3A, 2026-08-22 — "One Recommendation")
Chairman countersignature: ☐ pending
Numbering: named-series per docs/README, extended from intelligence specifications to governance
instruments. The sequential platform-core series is untouched — WET-SPEC-003 remains available and
deferred per WET-REV-002.
Supersedes: nothing. **Extends** SOP-06 and honours WET-REV-002's standing rule.

## 0. The rule this standard was written to obey
> WET-REV-002: *"PDR approvals join the existing gate ledger, never a parallel system."*

The platform already has gates. SOP-06 defines **GATE 1** (timeline custody audit), **GATE 2**
(claims/content review) and **GATE 3** (Chairman publication approval), ratified from CAPE clauses
17–19, and PDR records already carry `gate:` and `gate_clearance_ref:` fields against them.

A second, unrelated gate mechanism would have been precisely the parallel system WET-REV-002 forbids.
So this standard does not create one. It defines **one ledger with two kinds of gate**, and makes the
existing three the terminal authority within it.

## 1. Scope
Governs the declaration, state, composition and machine-readability of every gate in the platform.
Out of scope: what any individual gate decides. A gate standard says how a gate is *written*, never
what it should *say*.

## 2. The ledger — one register, two kinds
| kind | question answered | instances | authority |
|---|---|---|---|
| `PUBLICATION` | *May this be released?* | GATE 1 · GATE 2 · GATE 3 (SOP-06) | Chairman (GATE 3) |
| `PROGRESSION` | *May the next stage of work begin?* | declared per sprint / production / phase | Executive Producer |

**Precedence, stated once so it is never argued:** a PROGRESSION gate can only ever *further restrict*.
It cannot open what a PUBLICATION gate has closed, cannot substitute for GATE 1/2/3, and confers no
release authority. A production with every progression gate OPEN and GATE 3 unrecorded is unpublished.

## 3. Required fields (normative)
Every gate file SHALL carry:

| field | meaning |
|---|---|
| `gate_class: EXECUTION_GATE` | the ledger marker — see §4 |
| `gate_kind` | `PUBLICATION` \| `PROGRESSION` |
| `gate_id` | stable, unique, never reused |
| `schema_version` | this standard's version the file conforms to |
| `scope` | `SPRINT` \| `PRODUCTION` \| `PHASE` \| `PLATFORM` |
| `subject` | what the gate governs, in one line |
| `state` | `OPEN` \| `CLOSED` \| `SUPERSEDED` |
| `authorized` | boolean — the single field a dashboard reads |
| `unblock_condition` | prose; what must be true to open |
| `blocking_items[]` | each with `id`, `path`, `status`; empty only when `state: OPEN` |
| `authority` | who may change `state` |
| `issued` | ISO date |
| `review_by` | ISO date — see §6 staleness |
| `status_history[]` | append-only; every state change with date, authority, note |
| `composition` | `ADDITIVE` (default) — see §5 |
| `on_open.required_actions[]` | what must happen when it opens |

A gate missing any required field is **non-conforming and SHALL be treated as CLOSED**. Failing shut
is the only safe default for a control artifact.

## 4. Machine-readability — the marker is the index, not the filename
A gate is discovered by its `gate_class: EXECUTION_GATE` marker, not by where it sits or what it is
called. Gates live **beside the work they govern**, because a control that lives far from its subject
is a control that goes stale.

New gate files SHOULD be named `GATE.yaml`. That is a convenience for humans, not the discovery
mechanism: filenames drift, get copied, get renamed during refactors. Enumeration is therefore:

```
grep -rl '^gate_class: EXECUTION_GATE' --include='*.yaml' .
```

`scripts/gate_status.py` implements this and answers the dashboard's only question — *is anything
closed?* — with an exit code, so it can be a CI check rather than a habit.

## 5. Composition — additive, and computed
Gates compose by **AND**. Work proceeds only when every gate in scope reports `authorized: true`.

The aggregate is **computed, never authored**. There is no "master gate" file that a person edits, for
the same reason there is no hand-edited synchronization artifact: a summary someone has to remember to
update is a summary that will eventually lie.

## 6. Staleness — the failure mode this class actually has
The realistic way a gate fails is not that someone ignores it. It is that the blocking items get
resolved and **nobody flips the state**, so a gate sits `CLOSED` long after it should have opened, and
people route around it. That teaches the organisation that gates are advisory. Once learned, the
lesson is expensive to unlearn.

Therefore: every gate carries `review_by`. A gate past `review_by`, or one whose `blocking_items` are
all resolved while `state` is still `CLOSED`, is reported **STALE** by the enumerator. Stale is a
finding, not an error — but it is surfaced, every time, so drift is visible rather than quiet.

## 7. Gate proliferation — the risk this class introduces
ADR-009 named engine proliferation as the platform's top-ranked governance risk and chose a module
over a fifth engine to avoid it. **Gate proliferation is the same risk in a new costume.** If every
sprint, production and phase declares a gate, "is the gate open?" degrades into "which of forty?"

Controls, in order of strength:
1. **A gate needs a blocking item to exist.** No open question, no gate. A gate declared "for
   completeness" is documentation, not control, and shall not be declared.
2. **Gates close over their subject and then become `SUPERSEDED`,** not kept alive for the record. The
   history lives in `status_history` and in the Reference Execution, not in a permanently-open file.
3. **Scope up, not out.** Prefer one PHASE gate with four blocking items over four SPRINT gates with
   one each.
4. The enumerator reports the **total gate count** alongside the open/closed answer. A number that
   climbs every sprint is the early warning.

## 8. Relationship to SOP-06 phases
The Sprint 3A progression gate sits inside **SOP-06 Phase B (the MIE window)**. Phase B already holds
that timeline timing is frozen and MIE work proceeds against the lock XML; the progression gate adds
that *for this production*, MIE work additionally waits on four production PDRs. It narrows Phase B.
It does not reinterpret it, and it expires when its blocking items are dispositioned.

Any picture change during Phase B voids the lock (SOP-06 B2) — which would also invalidate the
Reference Execution's input hashes. Two options in `PDR-2026-08-22-ESS-003` and one in
`PDR-2026-08-22-ESS-004` have exactly that consequence, and both PDRs say so.

## 9. Conformance
| instance | kind | conforms |
|---|---|---|
| `intelligence/p2/ess/DOWNSTREAM_AUTHORIZATION_GATE.yaml` | PROGRESSION | v1.0 (from v1.1.0 of the file) |
| GATE 1 / GATE 2 / GATE 3 | PUBLICATION | **prose-only in SOP-06 — not yet machine-readable** |

That second row is the honest state of things. The publication gates are the ones with real
consequences, and they are the ones a dashboard currently cannot read. Rendering GATE 1/2/3 into
conforming files is the obvious next step and is **deliberately not done here**: SOP-06 is ratified
gate law derived from CAPE clauses 17–19, and re-expressing ratified law is a Chairman act, not an
implementation convenience. Raised as an action item instead.

## 10. Non-goals
No gate may encode a decision. No gate may reference a person as an approver by name without a
consent-checked registry reference. No gate opens itself on a timer.
