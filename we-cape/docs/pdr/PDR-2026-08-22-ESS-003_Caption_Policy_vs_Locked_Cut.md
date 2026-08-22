# PDR-2026-08-22-ESS-003 — Caption policy vs the locked cut: rider lower-thirds
## Governance Status
Document Type: Production Decision Record · Status: **OPEN — AWAITING EXECUTIVE DISPOSITION** · Date: 2026-08-22
Authority: Executive Producer · Origin: Final Executive Disposition, Sprint 3A (2026-08-22), item 2
Reference Execution: RE-001 · Conflict ID: **VCONF-03**
Boundary: ADRs govern the platform · PDRs govern productions.

## Question
CAPTION_REGISTRY 0.1.0 carried the policy *"lower-third naming at each rider first-cue (75 candidates
from RIDER_REGISTRY)."* The locked cut contains **zero rider lower-thirds**. Is the policy retired as
never-adopted, deferred to a future product, or is the lock incomplete?

## Evidence
| kind | value |
|---|---|
| Prior policy | `caption_boundaries_policy: "lower-third naming at each rider first-cue (75 candidates from RIDER_REGISTRY); proclamation text NOT captioned over speakers (silence-zone dignity rule)"` (CAPTION_REGISTRY 0.1.0) |
| Full census | **57** title elements in the locked FCPXML: 40 on connected lanes (the Sprint-2 ETC count) + **17 nested inside compound clips**, newly enrolled by RE-001 |
| Actual composition | 27 question cards (22 in gauntlet 1, 5 in gauntlet 2) · 8 civic lower-thirds · 1 venue card · 1 main title · 4 closing question cards + 1 sign-off · 15 kinetic text cards |
| Named persons on screen | **civic speakers only** — Racquel Peebles (Council Member), Mayor Mary Esther Reed, David Santucci (Town Manager), Jerome Dempsey (Council Member) |
| Named riders on screen | **none** |
| Dignity rule | upheld — no caption sits over the proclamation readings |
| Source | `Info.fcpxml` SHA-256 `2bf06853…3858e7`; positions resolved and validated 191/191 against the ETC spine |

## Why this was not auto-resolved
A policy line is an intent, and the absence of an artifact is not proof the intent was abandoned — it
may be unbuilt, deferred, or deliberately dropped. RE-001 marked the line **SUPERSEDED-BY-EVIDENCE** in
the enriched registry, which records *what the lock contains* without deciding *what should have been*.
Deciding that is editorial.

## The consideration that outruns captioning
75 rider lower-thirds is not only a design question, it is a **consent and rights question**. Under
WET-SPEC-DIE-001 §R-5 every person entity carries `consent_status`, `rights_class`,
`anonymization_eligibility` and `research_use_consent`. Naming 75 people on screen is an emission.
Whatever is decided about the caption design, the decision needs the consent ledger beside it — and the
RIDER_REGISTRY entries are largely UNCONFIRMED on canonical naming (R-3: canonical naming requires GT-3
verification or two independent evidence classes). **Captioning a name the registry has not resolved
would put an ASR-derived spelling on a person's chest.** That is the strongest argument the absence in
the lock was correct.

## Options
**A — Retire the policy.** Record that on-screen naming is reserved for civic speakers, by design. The
question-card cadence carries rider identity as *voice*, not as *nameplate*. Lowest risk; matches the
lock; matches the consent posture.

**B — Defer to a downstream product.** Keep rider naming out of the documentary cut, but authorise it
for a PIE-class derivative (chapters, shorts, index) where names can be verified per item. Preserves
the option without touching the lock.

**C — Reopen the lock.** Add rider lower-thirds. Requires 75 name resolutions to GT-3 or two-evidence
standard, a consent pass per person, and a picture change to a locked cut. Not recommended without a
specific product reason.

## Downstream impact
- Regenerates on decision: `CAPTION_REGISTRY.yaml` (policy line), `EDITORIAL_SYNCHRONIZATION.yaml`.
- Option B creates a PIE-class work item; option C reopens picture lock and invalidates RE-001's
  input hash 2 for any future comparison.
- **No effect on music.** This PDR does not gate MIE on musical grounds; it is listed in the gate only
  because the Executive Disposition gated all four together.

## Blocks
Nothing in MIE directly. Gated with the other three by Executive instruction.

## Decision
> _To be recorded by the Executive Producer._

**Selected option:** ☐ A ☐ B ☐ C ☐ Other: ______
**Consent ledger reviewed:** ☐ yes ☐ n/a
**Rationale:** ______
**Dispositioned by / date:** ______
