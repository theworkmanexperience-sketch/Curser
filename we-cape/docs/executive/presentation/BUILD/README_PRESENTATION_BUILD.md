# PRESENTATION BUILD — README

**Established by** EO-WET-EXEC-012 · Canonical Presentation Architecture & Derived Presentation Build

---

## THE PIPELINE

```
MASTER  ──►  PRESENTATION BUILD  ──►  GAMMA  ──►  + PRESENTER NOTES  ──►  PRESENTATION
```

| stage | artifact | property |
|---|---|---|
| **Master** | `MASTER/WET_EXEC_GAMMA_MASTER_PRESENTATION.md` | **Canonical. Authoritative. Frozen.** |
| **Build** | `BUILD/WET_EXEC_GAMMA_FINAL_PRESENTATION.md` + three companions | **Derived. Disposable. Regeneratable.** |
| **Gamma** | the imported deck | a rendering |
| **Notes** | `BUILD/WET_EXEC_GAMMA_PRESENTER_SCRIPT.md` | never enters Gamma |
| **Presentation** | the room | — |

---

## THE RULE

**The Master is the constitutional source. Everything in `BUILD/` is a rendering of it.**

The Master is never presentation-optimized, never edited for Gamma, never shortened, never simplified. It changes only by Executive Order.

**The Build is disposable.** Delete the entire `BUILD/` directory and nothing authoritative is lost — it can be regenerated from the Master. That property is the point of the architecture, and it is what makes presentation format free to evolve without risking the record.

---

## WHAT THE BUILD MAY AND MAY NOT DO

| the Build **may** | the Build **may never** |
|---|---|
| simplify wording | invent facts |
| split slides | modify figures |
| optimize spacing and rhythm | modify evidence |
| remove author instructions | modify chronology |
| remove governance metadata | change governance |
| reduce text density | change doctrine |
| optimize for Gamma import | alter Executive meaning |

**A regeneration that changes a number has failed, not improved.**

---

## THE FILES

### `MASTER/WET_EXEC_GAMMA_MASTER_PRESENTATION.md`
Canonical source. 41 slides carrying Purpose · Key Message · Speaker Notes · Visual Direction · Callouts · Transition. **Do not edit. Do not optimize. Do not import into Gamma.**

### `BUILD/WET_EXEC_GAMMA_FINAL_PRESENTATION.md`
The audience deck. 42 cards — the Master's 41 plus a title card. Slide text only: titles, hero statements, supporting lines. No authoring metadata, no tables, no ASCII, no code blocks. **This is the only file that enters Gamma.**

### `BUILD/WET_EXEC_GAMMA_DESIGN_BRIEF.md`
Presentation guidance only. Palette with hex values, type scale in points, grid and spacing, animation philosophy, iconography budget, chart rules, prohibited visuals, and the five slides that must not be beautified. Nothing audience-facing.

### `BUILD/WET_EXEC_GAMMA_IMAGE_PROMPTS.md`
One section per slide, 42 sections. Each carries Image Type · Gamma Image Prompt · Diagram Prompt · Infographic Prompt · Background Prompt. **This file holds all diagram geometry.** Since the deck carries no ASCII, this is the only place relationships, proportions, direction and hierarchy are specified — and Gamma must not infer them.

### `BUILD/WET_EXEC_GAMMA_PRESENTER_SCRIPT.md`
Presenter notes only, one section per slide: Opening · Narrative · Timing · Emphasis · Examples and stories · Anticipated questions · Transition. 48-minute target runtime. **Never combined with the deck** — Gamma imports slide text only, so notes are typed into each card's notes panel or read from this file.

---

## HOW TO BUILD THE DECK

1. **Paste** `BUILD/WET_EXEC_GAMMA_FINAL_PRESENTATION.md` into Gamma. Split on `---`. Expect 42 cards.
2. **Theme** — paste the theme prompt from §13 of the Design Brief.
3. **Diagrams** — work slide by slide through `WET_EXEC_GAMMA_IMAGE_PROMPTS.md`. Prepend the global prefix. Roughly 25 slides need a generated diagram; seven explicitly need none.
4. **Notes** — type each section of `WET_EXEC_GAMMA_PRESENTER_SCRIPT.md` into the matching card.
5. **Verify** — walk §10 and §11 of the Design Brief against the rendered deck. Those are the rules Gamma's styling pass is most likely to break.

**Budget an evening for steps 3 and 4.** They are manual because Gamma imports text only.

---

## VERSIONING

**The Master versions independently** and changes only by Executive Order.

**The Build is regenerated whenever required.** A new Build never changes the Master. If a Build and the Master disagree, **the Master governs and the Build is wrong** — regenerate it rather than reconciling by hand.

Every Build file carries a line naming the Master it derives from. If that line is absent, the file is not a governed derivation.

---

## MEASUREMENT CURRENCY

All figures throughout the Build are frozen at a single declared repository snapshot and are true at that commit rather than in general. The repository has advanced past that snapshot — the Build's own commits caused some of the movement.

**That is correct and disclosed, not an error.** A frozen document whose source has moved is honest precisely because it is frozen. A presenter chooses between presenting the frozen figures as of their snapshot or opening a new publication cycle.

---

## ONE OPEN ITEM

**There is no automatic staleness signal.** Nothing computes whether the Build is current against the Master or against the repository. If the Master is amended by a future Order and the Build is not regenerated, the two will drift silently — which is the pattern this repository has already met once, in a committed artifact matching neither its generator nor its successor.

**Recorded, not resolved.** A computed `BUILD CURRENT` / `BUILD SUPERSEDED` state would be a structural addition requiring its own Order.
