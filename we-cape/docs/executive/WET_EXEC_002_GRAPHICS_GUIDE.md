# WET-EXEC-002 — GRAPHICS GUIDE

**Companion to:** `WET_EXEC_002_PRESENTATION_OUTLINE.md`
**Targets:** Gamma AI · PowerPoint · Keynote
**Custody:** `DOCUMENTATION ONLY`

---

## 0 · DESIGN LAW FOR THIS DECK

Six rules. They are derived from the platform's own reporting standard, not from taste.

**1 · No composite scores, ever.** `WET-SPEC-REPORT-001` prohibits readiness/health/quality/maturity scores. That means **no gauge dials, no traffic-light health rings, no 0–100 "platform score," no radar charts with a filled area implying an aggregate.** If a graphic implies one number summarising many, it violates the platform it depicts.

**2 · Every percentage carries its numerator, denominator and source.** On the slide, not in a footnote. A bare "74.3 %" is prohibited; "74.3 % — 38,056 of 51,237 emitted characters, `traceability_scan.py`" is correct.

**3 · Absence must be drawn as absence.** The eleven silent days are the most important datum in the deck. Rendered as a short bar they disappear; rendered as a void with the axis continuing through it, they land. **Never let a zero look like a small number.**

**4 · Verbs over nouns in architecture diagrams.** Label the six layers with what they *do* — decides, constrains, proposes, refuses, produces, distributes — at equal or greater weight than what they *are*.

**5 · Monospace is a truth signal.** Anything quoted from the repository — commit messages, clause text, guard names, exit codes — is set in monospace. It reads as evidence rather than as copy, and this audience knows the difference.

**6 · Two colours carry meaning; everything else is neutral.** One accent for *evidenced*, one for *open/unresolved*. Never use colour decoratively in this deck — if a thing is coloured, the colour means something.

### Palette

| role | usage | note |
|---|---|---|
| **Ground** | near-black or near-white background | pick one and hold it; theme-consistent throughout |
| **Neutral** | structure, boxes, rules, body copy | carries no meaning |
| **Accent — Evidenced** | verified figures, `[E]` claims, passing states | one hue only |
| **Accent — Open** | `[O]` items, refusals, gaps, unresolved questions | one hue only, clearly distinct |
| **Void** | absence, silence, missing evidence | absence of ink, not a colour |

Keep contrast at 4.5:1 minimum for all text. Assume the deck will be shown on a projector in a lit room, and that at least one viewer will read it on a phone.

---

## 1 · GRAPHIC SPECIFICATIONS

### `G-01` · Rider Wall  *(Slide 1)*
**Form:** 75 uniform tiles in a grid, roughly 10 × 8.
**Rule:** 50 tiles filled (Neutral). **25 tiles drawn as outline only** — no fill, same size, same position in the grid.
**Do not** shade the 25 differently, cluster them, or move them to one side. They are distributed as the data is.
**Caption, below:** `75 riders · 25 marked UNCONF · RIDER_REGISTRY.yaml`
**Why it works:** the eye finds the hollow tiles before the caption is read. The absence *is* the message.

### `G-02` · Split Panel  *(Slide 2)*
**Form:** vertical 50/50 split. Left: unstructured scatter of media-card shapes, no alignment, no labels. Right: a single horizontal pipeline with a continuous rail beneath it.
**Rule:** the rail on the right runs unbroken beneath every stage. That continuity is the point.
**Label the rail:** `governance`.

### `G-03` · Authority Pyramid  *(Slide 3)*
**Form:** four stacked bands, narrowing upward.
**Bands, bottom to top:** Custody · Evidence · Intelligence · **Human Decision**.
**Rule:** the top band is visually heaviest, not lightest — invert the usual pyramid weighting so the apex reads as *authority*, not as *summit*.

### `G-04` · Authority Diagram  *(Slide 4)*
**Form:** three nodes, two double-headed arrows.
`Chairman` ⇄ `Engineering channel (AI)` ⇄ `git custody`
**Rule:** annotate the arrows, not the nodes. Chairman→Engineering: *"orders, ratification."* Engineering→Chairman: *"proposals, exceptions, refusals."* The return arrow is the interesting one — weight it equally.

### `G-05` · Production Stat Band  *(Slide 5)*
**Form:** single horizontal band, six figures, generous letter-spacing, no icons.
`4 cameras · ~170 source files · 139 curated exports · 75 interviews · 3-part series · 8-track album`
**Rule:** no icons. Icons make measured figures look like marketing.

### `G-06` · Commit Density Strip  *(Slide 6)* — **hero graphic**
**Form:** horizontal timeline, 20 May → 29 August, one vertical bar per active day, height = commit count.
**Rule:** the 27 July – 7 August window renders as **void** — the baseline axis continues, the bars stop. Bracket it above with a thin rule and the label `zero commits · Part 1 edited and published`.
**Do not** fill the gap, shade it, or place an icon in it. Emptiness drawn as emptiness.
**Recommended:** this graphic reappears at Slide 11 with the 22 August spike highlighted — same chart, different emphasis. Reuse builds trust in the data.

### `G-07` · Commit Callout  *(Slide 7)*
**Form:** the raw commit message, monospaced, set large, on Ground, with nothing else on the slide.
```
fix(preflight): sys_free_gb reads Data volume via Path.home() —
was reading OS volume (12GB used) instead of user Data volume
(314GB used), all prior reports incorrect
```
**Rule:** emphasise only `all prior reports incorrect`. One emphasis per slide.
**Attribution, small:** `d402855 · 2026-06-22`

### `G-08` · Before/After Bar  *(Slide 8)*
**Form:** two horizontal bars.
Bar 1 — `±5 s specified`: 67 % of the bar in Open accent, labelled `ungrouped on real footage`.
Bar 2 — `±15 s field-validated`: predominantly Evidenced accent.
**Caption:** `documented as a formal deviation, not a silent change · 3973b19`

### `G-09` · The Ratification Loop  *(Slide 9)*
**Form:** four-node cycle. `Finding → Tool → Doctrine → Hash-pinned record →` (back to Finding).
**Rule:** annotate one traversal with a real example — F1 timestamp → chronological-sets generator → SOP-05 → `19727ef`. An abstract loop persuades nobody; an instantiated one persuades engineers.

### `G-10` · Single-Day Timeline Strip  *(Slide 10)*
**Form:** one horizontal day, seven marked events left to right.
`assess → freeze (SHA) → certify → ratify → specify → 12 modifications → freeze (tag) → sprint launch`
**Rule:** mark the two freezes with a distinct glyph and show the truncated SHA beside each. Add a small annotation at the fifth position: `paste error caught by size reconciliation`.

### `G-11` · Commit Density Chart  *(Slide 11)*
**Form:** `G-06` reused, with 22 August highlighted in Evidenced accent.
**Callout:** `32 commits · the densest day in the repository · all governance`

### `G-12` · Divergence Diagram  *(Slide 12)*
**Form:** two horizontal timeline bars sharing a left origin, splitting at a marked point.
**Annotations:** split at `00:03:27` · lower bar ends `157.125 s` short, with the shortfall drawn as void, not as a shortened bar of the same weight.
**Stamp, over the diagram:** `WORK ORDER: NOT EXECUTED`

### `G-13` · Six-Layer Stack  *(Slide 13)* — **hero graphic**
**Form:** six full-width horizontal bands, stacked.
**Rule:** set the **verb** in display weight and the layer name in small caps beneath it.
```
DECIDES        Executive
CONSTRAINS     Governance
PROPOSES       Engineering
REFUSES        Runtime
PRODUCES       Creative Production
DISTRIBUTES    Commercial
```
**Emphasis:** only `DECIDES` and `REFUSES` carry accent. The other four are Neutral. That asymmetry is the argument.

### `G-14` · Custody vs Authority  *(Slide 14)*
**Form:** two **orthogonal axes** — deliberately not a stack, not a hierarchy, not nested boxes.
Horizontal axis: *custody* — `MACHINE · HUMAN · EXECUTIVE`.
Vertical axis: *authority* — `none · decides`.
Plot the AI channel high on custody breadth and **at zero on authority**.
**Rule:** the whole point is that the two axes are independent. Any layout implying one contains the other defeats the slide.
**Caption:** `custody is not authority, and custody is immutable · ER-003`

### `G-15` · Four-Layer Stack  *(Slide 15)*
**Form:** four bands over a Ground Truth base, capped by `Human Decision`.
**Rule:** label each band with its **question**, engine acronym small and secondary.
`what exists? (DIE)` · `why does it matter? (NIE)` · `how should it feel? (MIE)` · `what products result? (PIE)`

### `G-16` · Ordinal Scale  *(Slide 16)*
**Form:** five discrete, evenly spaced blocks — **not** a gradient bar, **not** connected.
`LOW · MODERATE · HIGH · ELEVATED · CLIMACTIC`
**Rule:** overlay a smooth interpolating curve in Open accent and **strike it through**. The prohibited operation must be visible for the permitted structure to mean anything.
**Caption:** `ordinal · non-numeric · no gradient computable · Invariant B`

### `G-17` · Guard Gate Diagram  *(Slide 17)*
**Form:** a left-to-right run: `inputs → [14 guards] → ✗ → first write (never reached)`.
**Rule:** the write stage is drawn but rendered as void — outline only. Nothing was produced.
**Ledger strip beneath:** four rows, each `fault → guard → exit 2 · 0 files`.

### `G-18` · Authoring Boundary  *(Slide 18)*
**Form:** a four-column table rendering, one column visibly reserved and empty.
`Stage | Repository Record | Executive Reflection | Resulting Principle`
**Rule:** the Reflection column shows `AWAITING_EXECUTIVE_DECLARATION` in monospace, in Open accent. It must read as *reserved*, never as *unfinished*.

### `G-19` · Refusal Ledger  *(Slide 19)* — **hero graphic**
**Form:** four rows, two columns: `authorised action` | `refused because`.
**Rule:** all four "authorised" cells in Neutral; all four "refused" cells in Open accent. No icons, no checkmarks, no crosses — **this is a ledger, not a scorecard.**
**Footer:** `four refusals · four vindications · a control that has never fired is not a control`

### `G-20` · Validator Comparison  *(Slide 20)*
**Form:** two bars — `1 / 191` and `191 / 191`.
**Rule:** the first bar is nearly invisible at true scale. **Keep it at true scale.** Do not apply a minimum bar height; the near-invisibility is the finding.
**Annotation between them:** `the published figure was a hard-coded string · no committed code had ever produced it`

### `G-21` · Ratio Bar  *(Slide 21)*
**Form:** a single stacked horizontal bar, two segments: `92 governance documents` / `85 engine modules`.
**Rule:** near-parity is the message. Do not round, do not idealise to 50/50.
**Caption:** `nobody planned this ratio`

### `G-22` · Four-Quadrant Audience Map  *(Slide 22)*
**Form:** 2 × 2. Engineering · Security · Information Architecture · Governance.
**Rule:** one sentence per quadrant, taken verbatim from the briefing's §13. Do not paraphrase into marketing copy — the specificity is what makes each reader feel addressed.

### `G-23` · Disclosure Panel  *(Slide 23)*
**Form:** plain list, Ground background, Neutral text, no accent, no frame, no icons.
**Rule:** **deliberately undesigned.** Any styling reads as spin. Five lines, generous leading, nothing else on the slide.

### `G-24` · Improvement Loop  *(Slide 24)*
**Form:** six-node cycle. `Produce → Measure → Find → Ratify → Tool → Produce`.
**Rule:** thicken the `Find → Ratify` arc relative to the others. That is the segment most organisations skip, and it is the one this platform is built around.

---

## 2 · GRAPHICS THAT MUST NOT APPEAR

Listed because they are the default output of every AI deck tool, and each one contradicts the platform being presented.

| prohibited | why |
|---|---|
| Gauge dials, speedometers, health rings | composite scores — prohibited by `WET-SPEC-REPORT-001` |
| Radar/spider charts with filled area | the filled area *is* an aggregate score |
| Traffic-light overall status | the reporting standard requires Processing Status to **name its unmet precondition** |
| Maturity ladders with a single platform position | maturity is assessed per domain, with blocking conditions |
| Bare percentages | every percentage carries numerator, denominator and source |
| Stock photography of motorcycles, code, or "AI" | this deck's credibility is its specificity |
| Any chart of the 85 % utilization figure | **no producing computation exists** |
| Upward-and-to-the-right projections | nothing in this package projects revenue |

---

## 3 · TOOL-SPECIFIC NOTES

**Gamma AI.** Gamma defaults to decorative iconography and gradient fills; both work against this deck. Prompt it with the *rule* rather than the picture — e.g. *"a horizontal timeline where an eleven-day gap is rendered as empty space with the axis continuing through it, no fill, no icon."* Regenerate rather than accept a near-miss on `G-06`, `G-13`, `G-19` and `G-20`; those four carry the argument. Strip auto-added icons from `G-05` and `G-19`.

**PowerPoint.** Build `G-06`/`G-11` as a native chart with the gap as genuinely missing data points, not zero-height bars — zero-height bars still draw an axis tick and read as "small," which is the exact misreading to avoid. Use a monospace theme font for the evidence callouts and keep it out of the body styles.

**Keynote.** Magic Move is well suited to the `G-06` → `G-11` transition (same chart, emphasis shifts to 22 August) and to `G-20` (the 1/191 bar growing to 191/191). Use it twice at most; a deck about restraint should demonstrate it.

**All three.** Export a static PDF as the artifact of record. A deck whose meaning depends on animation cannot be attached to a governance record.

---

## 4 · ACCESSIBILITY AND INTEGRITY

- Never encode meaning in colour alone. `G-01`'s outline tiles, `G-17`'s void write-stage and `G-06`'s gap must all survive greyscale.
- Provide alt text for every graphic; for `G-06` the alt text must state the gap explicitly: *"commit activity by day, 20 May to 29 August 2026; no commits between 27 July and 7 August."*
- Every figure appearing in a graphic must trace to a citation in `WET_EXEC_002_EXECUTIVE_BRIEFING.md`. **If a number cannot be cited, it does not go on a slide** — that is the standard this platform holds its own artifacts to, and a deck about it cannot hold itself to less.
