# DOC-002 — Never patch intelligence. Regenerate intelligence.
## Governance Status
Document Type: Doctrine (ratified) · Status: **RATIFIED** · Date: 2026-08-22
Authority: Executive Producer (Executive Assessment, Sprint 3A, 2026-08-22)
Chairman countersignature: ☐ pending
Origin note: **not** among the ten DOC-SRC-001 candidates. It emerged from the disposition exchange
itself, and it **generalises an existing rule** rather than introducing a new one — see §"What this
actually changes".
Scope: PLATFORM.

## The doctrine
> **Never patch intelligence. Regenerate intelligence.**
>
> A derived artifact is corrected by re-running the process that produced it against corrected inputs —
> never by editing the artifact.

## What it requires, operationally
1. Every derived artifact declares its sources by hash and is **regenerate-on-mismatch**.
2. A disposed decision is applied to the **input** (registry, cue sheet, spec), then the artifact is
   regenerated. The decision is never typed into the output.
3. The generating script is committed beside its output. Reproducibility is a property of the
   repository, not of anyone's memory.
4. A correction to a *preserved* record — a Reference Execution, a Doctrine Source, a closed audit log —
   is a **new record with the delta categorized**, not an edit. RE-001 is corrected by RE-002.

## What this actually changes — stated plainly
ADR-009 §2 already established this for `EDITORIAL_SYNCHRONIZATION.yaml`: *"a hash-pinned,
regenerate-on-mismatch, never-hand-edited artifact."* DOC-002 does not invent that rule. It **removes
its exception surface** — it stops being a property of one artifact and becomes a property of the class.

That is the whole change, and it is worth being precise about, because a doctrine that quietly restates
existing law while appearing to make new law is how governance loses its footing.

## Why it matters more than it sounds
A hand-edited derived artifact is indistinguishable from a generated one by inspection. It has the same
shape, the same fields, the same hash-pinned header claiming provenance it no longer has. The header
becomes a lie that nothing in the system can detect.

Regeneration is what makes hash-pinning mean anything. Without it, `sources: {sha256: ...}` is
decoration.

There is a second, less obvious payoff. Because correction requires regeneration, and regeneration
requires the script, **the pipeline stays executable**. Platforms that permit patching lose the ability
to reproduce their own outputs within about two correction cycles — not through any decision, just
through accumulated small edits nobody recorded.

## The cost, honestly
Regeneration is more expensive than editing one field, and there will be moments — usually late,
usually under pressure — when a single typed character would fix something in seconds. This doctrine
says: pay the cost. The alternative is not "one small edit"; the alternative is a class of artifact
that can no longer be trusted without re-deriving it by hand.

## In force now
`intelligence/p2/ess/DOWNSTREAM_AUTHORIZATION_GATE.yaml` `on_all_dispositioned` already carries the
operative form of this doctrine: when the four PDRs are dispositioned, `EDITORIAL_SYNCHRONIZATION.yaml`
and `CONDUCTOR_SCORE.yaml` are **regenerated from the disposed values and archived as RE-002** — not
edited to match.

## Provenance
Executive Assessment, Sprint 3A, 2026-08-22 ("My Favorite Line" — *"That should become permanent
doctrine."*) → **DOC-002**. Generalises ADR-009 §2. Related candidate: `DOC-SRC-001` DC-06
("artifacts are generated, never hand-authored") — the authoring-side statement of the same principle.
