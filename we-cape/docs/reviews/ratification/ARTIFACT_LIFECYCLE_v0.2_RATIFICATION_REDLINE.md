# ARTIFACT LIFECYCLE v0.2 — RATIFICATION REDLINE

**Subject:** `ARTIFACT_LIFECYCLE_SPECIFICATION.md` v0.2 → v1.0 on ratification
**Amendments:** 2 · **Applied:** none · **Repository:** READ ONLY · **Commits:** none

> Amendment package only. Current wording is quoted verbatim from the delivered v0.2 draft. **No amendment has been applied.**

---

# B-1 · §1.5 — adopt the Determination's formulation

**Current wording**

> ## 1.5 · Version independence (normative)
>
> **Model only, per `EGS-001 §4A`. No versioning mechanism is designed.**

**Replacement wording**

> ## 1.5 · Version independence (normative)
>
> **Version belongs to provenance. Authority belongs to governance.**
>
> **Model only, per `EGS-001 §4A`. No versioning mechanism is designed.**

**Authority** — EXECUTIVE DETERMINATION, *Canonical Authority Model*, VERSION MODEL section

**Reason** — Transcription of the Determination's formulation of the principle §1.5 already expresses. All existing bullets are retained unchanged beneath it. Matches `EGS-001` amendment `A-2`.

**Traceability** — `CAM-001_IMPACT_RESOLUTION.md` §3 `S-2`

---

# B-2 · §2.3 `P-3` — align with *"not restored implicitly"*

**Current wording**

> **`P-3` · `SUPERSEDED → CANONICAL` SHALL NOT occur.** A superseded artifact is not reinstated; a new promotion of the same bytes is a **new entry** citing the same `sha256`. `DOC-002` applied to status.

**Replacement wording**

> **`P-3` · `SUPERSEDED → CANONICAL` SHALL NOT occur as a transition, and historical authority SHALL NOT be restored implicitly.** A superseded artifact regains canonical authority **only by a new promotion entry** citing the same `sha256` — never by transition, never by mutation of an existing entry, and never implicitly. `DOC-002` applied to status.

**Authority** — EXECUTIVE DETERMINATION, *Canonical Authority Model*, HISTORICAL PRESERVATION section: *"Historical authority SHALL NOT be restored implicitly."*

**Reason** — The Determination forbids implicit restoration, which by implication permits explicit restoration. `P-3` as written reads as an absolute prohibition. The two are compatible — `P-3`'s second sentence already supplies the explicit mechanism — and the replacement makes the equivalence textual so no future reader concludes one forbids what the other permits.

**Traceability** — `CAM-001_IMPACT_RESOLUTION.md` §3 `S-5`

---

```
Amendments in this package    2
Applied                       0
Sections replaced             2   §1.5 heading block · §2.3 P-3
Sections added                0
Specification edited          NO
Commits                       NONE
```
