# IR-001 — Implementation Readiness: EPR-001 Ratification Order
**To:** Chairman / Executive Producer · **From:** Platform Architect · **Date:** 2026-08-24
**Re:** Executive Ratification Order — EPR-001 Integration & Implementation Authorization
**Status:** **CANNOT PROCEED — the ratified order was not transmitted**

---

## 1. The order is missing

The communiqué instructs:

> *"Please treat the following block as the authoritative Executive Ratification Order for
> implementation."*
> **`(Insert the Executive Ratification Order & Ingestion Prompt exactly as written.)`**

**The placeholder arrived in place of the block.** No ratification order text was transmitted.

I could reconstruct a plausible order from the adoption bullets and my own `PR-001` §4 draft. **I am
not going to.** A reconstruction would be the platform authoring Executive policy and then labelling
it ratified — the exact inversion `DOC-CAND-001` names, and the failure mode ER-002 was written to
prevent for prompts. The order's authority comes from its being *yours*, verbatim.

**Nothing is blocked for long.** Resend the block and implementation proceeds the same session.

---

## 2. What I can confirm without it

The adoption list is unambiguous on its own terms. **Ten items map cleanly onto `PR-001`:**

| adopted | maps to | status |
|---|---|---|
| Executive custody of documentary intent | **C1** — the load-bearing condition | ✅ adopted |
| Separation of intent from observational measurement | **C4** + §3.2 | ✅ adopted |
| Segment-based keying | **C6** | ✅ adopted |
| Structural-only validation | **C3** / V-6 | ✅ adopted |
| Observational purity of `EDITORIAL_SYNCHRONIZATION` | **§3.3** — the chain revision | ✅ adopted |
| Registry-version regeneration | **C5** | ✅ adopted |
| Prohibited musical fields | §4 clause 3 | ✅ adopted |
| Deferred responsibility vocabulary | §4 clause 1.3, option 3 | ✅ adopted |
| Interim integration through `CONDUCTOR_SCORE` | §4 clause 5.3 | ✅ adopted |
| Preservation of deterministic custody | ER-004 | ✅ adopted |

**Every substantive recommendation in the review was accepted.** That is a complete answer to review
areas 1–3 and I have no residual objection to any of it.

---

## 3. Four refinements I have never seen defined

These are named as incorporated. **None appears anywhere in the repository.** Two I can infer with
reasonable confidence; two I cannot, and I will not guess at either.

| refinement | assessment |
|---|---|
| **Categorical dramatic intensity** | **Inferable, and it resolves an open question.** `PR-001` §5 flagged that if `dramatic_intensity` were numeric and later aggregated, it would become a composite score under the `DWR-010` prohibition. *Categorical* removes that risk entirely — a category cannot be averaged. **This is a better answer than the one I asked for.** Still needs its term list, and whether that list is closed |
| **Continuation of the Cue Precondition Contract** | **Inferable.** Reads as `PR-001` §4 clause 1.2, first option — `EMOTIONAL_ARC`'s clause *"a cue that cannot name its emotion and responsibility does not generate"* carried forward rather than retired. If so, one thing must be settled with it: after the split, EPR-001 holds the **emotion** and the Behavior layer holds the **responsibility**. **The precondition therefore spans two artifacts and can no longer be checked in one place.** Where it is evaluated needs stating |
| **Clarification of documentary-versus-musical responsibility** | **Partly inferable** — presumably the boundary at which `music_responsibility` leaves EPR-001. Its exact text matters, because it is what a validator would enforce |
| **Executive Non-Interpolation Invariant** | **NOT INFERABLE. Entirely new.** *Interpolation* has at least three distinct readings here, and they are not equivalent — see below |

### 3.1 `Executive Non-Interpolation Invariant` — three readings, materially different

| | reading | consequence for implementation |
|---|---|---|
| **R1** | **No value-filling.** The platform shall not interpolate a missing EPR field from neighbouring entries — an absent `audience_state` stays absent | a validator rule. Strengthens C1. Cheap |
| **R2** | **No temporal interpolation.** Intent applies to its declared segments only and shall not be spread, ramped, or smoothed across the spans between them | a *consumer* rule binding `CONDUCTOR_SCORE`. Materially harder, and it forbids a thing the Behavior layer might otherwise reasonably do |
| **R3** | **No inference of intent between declarations.** Nothing downstream may derive what the Executive *would have* declared for an undeclared segment | the strongest. Would make undeclared segments permanently `UNSPECIFIED` rather than defaulted |

**All three are defensible and consistent with the platform's direction. They require different code.**
R1 is a schema check; R2 binds a consumer; R3 binds every future consumer forever. I have implemented
none of them.

---

## 4. Requested action 5 — what must await `CUSTODY_ALERT_001`

Answerable now, and the segment-keying decision does most of the work.

### Does **not** await the cut ruling

| task | why |
|---|---|
| Author EPR-001 content | segment-keyed; derives nothing; consumes no evidence |
| Ratify supersession of `EMOTIONAL_ARC` | a governance act on two governed artifacts |
| Define the schema and prohibited-field list | structural |
| Build the V-1…V-6 structural validator | tests shape, not timecode |
| Update dependency documentation | describes topology, not spans |
| Record the four refinements once defined | governance |

### **Must** await it

| task | why |
|---|---|
| **Any timecode resolution of a `segment_ref`** | segment→timecode mapping differs between the two cuts. `TIMELINE_REGISTRY` segments are pinned to the 08-22 lock |
| **The regeneration sequence** (`PR-001` §4 clause 9) | every downstream artifact is cut-dependent |
| `VISUAL_EVENT_REGISTRY` · `EDITORIAL_SYNCHRONIZATION` · `CONDUCTOR_SCORE` · `ESS_VALIDATION_REPORT` regeneration | same |
| Any EPR-001 consumer emitting a span | same |
| `ESS-002` / `EVS-001` | already held |

**The consequence is favourable and worth stating plainly: segment keying decoupled EPR-001 authoring
from the cut question entirely.** Content can be written today. Only its *resolution to time* waits.

### 4.1 One dependency the ratification should name

`TIMELINE_REGISTRY` is the segment authority — `S01…S19`, and the identifiers `EMOTIONAL_ARC` already
uses. **It is pinned to the 08-22 lock.** If the 08-24 cut governs, the segment boundaries move, and
possibly the segment *set* does too — the analysis cut carries 10 more primary elements and 8 more
titles.

**EPR-001 keyed on segment IDs is safe only while the ID set is stable.** If a re-edit adds or splits
a segment, intent declared against the old set needs remapping. **The order should state which
registry is the segment authority and what happens to EPR entries whose `segment_ref` no longer
resolves** — V-2 catches it, but V-2 only reports; it does not say what to do.

---

## 5. What I need to proceed

**One thing:** the ratification order text.

With it I will, in a single pass:

1. ratify the supersession of `EMOTIONAL_ARC.yaml` v1.0.0 on the order's stated terms;
2. write the EPR-001 schema and its structural validator (V-1…V-6);
3. update `docs/README.md` and the dependency documentation to the ratified topology;
4. stage the post-cut regeneration sequence as an executable run, **not run it**;
5. record the four refinements verbatim, with the `Non-Interpolation Invariant` implemented per
   whichever reading the order states.

**And I will not fill `EPR-001` with a single value.** Authoring its content is Executive work, per
the condition the order adopts.

---

## 6. Governance conflicts found in the ratified position

**None.** The adoption list contains no contradiction with `DOC-001`, `DOC-002`, `ER-003`, `ER-004`,
`ESS-002`, or the custody model — and *categorical* dramatic intensity closes a hazard I had left
open rather than opening a new one.

The only items outstanding are **definitional, not structural**: four named refinements without text,
and one order that did not arrive.

---

*Prepared 2026-08-24. Blocked on input, not on disagreement. Nine commits await `git push origin main`.*
