# WET-EXEC-002 — GRAPHICS GUIDE

> **CANONICAL SOURCE:** `WET_EXEC_MASTER_PRESENTATION.md` (WET-EXEC-005).
> This guide specifies **how** each graphic is drawn. **What it contains comes from the Master** — every figure rendered in a graphic cites an `M-nn` identifier, and no graphic may display a value absent from Master §1. The Master governs any discrepancy.

**Revised under:** EXECUTIVE REVIEW ORDER — WET-EXEC-003
**Companion to:** `WET_EXEC_002_PRESENTATION_OUTLINE.md`
**Targets:** Gamma AI · PowerPoint · Keynote
**Custody:** `EXECUTIVE PRESENTATION PACKAGE ONLY`
**Coverage:** 48 specifications — `G-01`–`G-24` (original) · `G-25`–`G-35` (WET-EXEC-003) · `G-36`–`G-47` + `G-31b` (WET-EXEC-004), with `G-25` amended to seven fields

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

## 1A · GRAPHICS ADDED UNDER WET-EXEC-003

Eleven specifications added by Executive Review Order. `G-25`–`G-27` serve Deck A; `G-28`–`G-34` serve Deck B; `G-35` serves Deck C.

### `G-25` · Moment Card Template  *(Deck A: A7–A12 · Deck B: B14–B15)* — **new hero graphic**
**Form:** one card per moment. Title bar with the moment number, date and commit hash. Five stacked fields beneath, each with a fixed label in small caps and its content in body weight.

```
MOMENT n · <title>
<date> · <commit>
─────────────────────────────────────────
THE POSITION ON RECORD      <what the artifacts stated>
WHAT THE EVIDENCE SHOWED    <the measurement or finding>
DECISION                    <what was done>
GOVERNANCE ARTIFACT         <the instrument produced>
LONG-TERM IMPACT            <what changed permanently>
```

**Rules, and the first one is non-negotiable.**

**The second field is `THE POSITION ON RECORD`, never "What we believed."** `ER-007 §3` prohibits the platform from inferring Executive beliefs, motivations or intent. What a governed artifact *stated* is observable and citable; what a person *believed* is not, and is reserved to `ER-007`'s Executive Reflection column. If the Chairman later authors those reflections, a sixth field may be added and labelled as Executive content — **it may not be inferred to fill the card.**

**`WHAT THE EVIDENCE SHOWED` carries a number or a quotation, never a characterisation.** *"scored 1 of 191"* and *"67 % ungrouped"* are correct; *"the validator was broken"* is not.

**`GOVERNANCE ARTIFACT` cites the instrument by identifier** — `DOC-001`, `CAPE-RAT-20260813`, `GER-001`. This field is what makes the section a bridge to the corpus rather than an anecdote reel.

**Consistency is the whole point.** Ten identical cards read as a system; ten bespoke layouts read as ten stories. Do not vary the treatment for the "important" ones — the uniformity is what lets an engineer, a security lead, a knowledge architect and a board member each read the same card from their own angle.

**Optional accent:** `LONG-TERM IMPACT` in the Evidenced accent; everything else Neutral. One accent per card.

### `G-26` · Why-Now Timing Panel  *(A16)*
**Form:** four horizontal bands, each a force, each with the platform's corresponding capability set opposite it.
**Rule:** the left column is external (regulatory / market), the right is internal (what already exists). The visual argument is **alignment, not prediction** — no arrows implying causation, no dates in the future.
**Do not** draw a market-growth curve. Nothing in this package projects a market.

### `G-27` · Gated Strategic Horizon  *(A18)* — **replaces the vision ladder**
**Form:** a vertical spine of four horizon blocks, each separated by a **gate bar** that spans the full width and names its prerequisites.
**Rule 1:** the gates are visually heavier than the horizons. **The conditions are the content; the destinations are the caption.**
**Rule 2:** the current position marker sits **before Gate A**, drawn explicitly.
**Rule 3:** Healthcare, Government and Education appear in a **separate detached panel**, visually disconnected from the spine — no arrow, no rung, no adjacency. Label it *"separate regulated programmes, not rungs on this ladder."* Each carries its own readiness requirement (HIPAA posture · FedRAMP / ATO pathway · accessibility and privacy programme).
**Why the detachment matters:** an ungated ladder that ends in regulated verticals reads as a pitch and costs the deck its credibility with exactly the audiences it is written for. The detached panel converts ambition into discipline.

### `G-28` · System Component Diagram  *(B1)*
**Form:** left-to-right data flow with real module groups, not conceptual layers.
```
sources → wecape/capture → wecape/registry → derived intermediates
        → intelligence/ pipeline → 7 governed artifacts → gates → publication
```
**Rule:** annotate each block with its measured size — `39 modules · 5,802 LOC` and `31 scripts · 6,122 LOC`. **Mark the pipeline block with the testing gap** (`0 unit tests`) in the Open accent. This is the diagram where the disclosure becomes visible rather than verbal.
**Distinguish** the deterministic engine from the read-only ops layer, and draw the seam between them — that seam is the architectural claim.

### `G-29` · Repository Topology  *(B2)*
**Form:** treemap or nested-rectangle map of the repository, area = file count, one level of nesting.
**Rule:** `docs/` and `wecape/` should be visually comparable in weight — that comparability *is* the 2.3 : 1 finding, rendered spatially rather than as a bar.
**Label** each region with its count and its definition, not just its name.

### `G-30` · Production Workflow  *(B3)*
**Form:** a horizontal swimlane — Capture · Offload · Organise · Conform · Edit · Observe · Generate · Gate · Publish.
**Rule:** run a **governance rail** beneath the whole lane, and mark the three publication gates as vertical stops that the flow must pass through. Mark where human decision is required with a distinct glyph — there should be more of those than a reader expects, and that is the point.

### `G-31` · Testing Hierarchy  *(B4)*
**Form:** four separate blocks, **deliberately not stacked and not summed.**
`engine unit 384` · `acceptance 99/99` · `ECR conformance 22` · `negatives 6`
**Rule:** each block carries *what it does not cover* in smaller type beneath it. **Never draw a total.** Four numbers with a map are an asset; four numbers implying 511 tests are a misrepresentation.
**Pair with** a two-bar comparison: engine 5,802 LOC / 5,823 test LOC against pipeline 6,122 LOC / 0 test LOC. The inversion should be immediately visible.

### `G-32` · Runtime Guard Lifecycle  *(B6)*
**Form:** a horizontal run showing the fourteen guards as sequential checkpoints, with the first-write stage drawn **beyond** the last guard and rendered as void when a guard fires.
**Rule:** show both paths — pass (all 14 clear, write proceeds) and fail (guard n fires, exit 2, write stage never reached and drawn as outline only).
**Annotate** each of the six negative tests at the guard it stops on.

### `G-33` · Local-First Security Architecture  *(B11)*
**Form:** a boundary diagram — the operator's machine as an enclosing boundary, with the engine path inside it and a **struck-through egress arrow** at the boundary.
**Rule:** label the boundary `enforced network invariant — engine path has no egress`. Show the three deliberate crossings (encrypted offsite backup, path-redacted logs, published artifacts) as explicitly gated, each with its control named.
**Do not** draw a cloud. The absence of one is the architecture.

### `G-34` · Risk & Debt Register  *(B16, C10, C11)*
**Form:** a table rendered as a graphic — one row per item, columns for **likelihood · impact · owner · mitigation · status**.
**Rule:** **do not** plot it as a heat map or a 2×2 matrix. A heat map is a composite score with a colour instead of a number, and this platform prohibits composites. A table with an **owner column** is what a board actually needs.
**Rows must include** the governance succession risk, the ADR custody gap, `B-13`, `T11`, `B-3`, `B-16`, the absent dependency manifest, and the soundtrack rights posture.
**An empty owner cell is a finding, not a formatting problem** — leave it visibly empty rather than filling it.

### `G-35` · Governance Authority Boundaries  *(C1)*
**Form:** a responsibility grid — actors down the side (Chairman · Engineering channel · Runtime · Registry), actions across the top (**propose · ratify · implement · refuse · decide**).
**Rule:** the `decide` column has **exactly one mark**, on the Chairman row. Every other cell in that column is empty, and the emptiness is the entire diagram.
**Second rule:** the `refuse` column has marks on both the Engineering channel and the Runtime rows — **the ability to refuse is distributed; the ability to decide is not.** That asymmetry is the governance model in one picture.
**Annotate** the Chairman row with the open condition: *"single authority — no quorum, no delegation, no succession instrument."* The diagram should show the risk, not hide it.

---

## 1B · GRAPHICS ADDED UNDER WET-EXEC-004

Thirteen specifications for the elevated architecture narrative. `G-25` is amended.

### `G-25` **AMENDED** · Moment Card Template — now seven fields
The card gains an `ENGINEERING` field between `GOVERNANCE ARTIFACT` and the closing field, and the closing field is renamed to `LONG-TERM PRINCIPLE`.

```
MOMENT n · <title> · <date> · <commit>
─────────────────────────────────────────
THE POSITION ON RECORD    what the artifacts stated
WHAT THE EVIDENCE SHOWED  a number or a quotation, never a characterisation
DECISION                  what was done
GOVERNANCE ARTIFACT       the instrument produced, by identifier
ENGINEERING               what was built or changed in code
LONG-TERM PRINCIPLE       what became permanently true
```

**The prohibition is unchanged and is the reason the card exists in this shape.** The second field is **never** *"What we believed."* `ER-007 §3` forbids the platform inferring Executive beliefs, motivations or intent. Belief and reflection are `ER-007` Executive Reflection content, currently `AWAITING_EXECUTIVE_DECLARATION`. A seventh field may be added when the Chairman authors those stages — **labelled as Executive content, never inferred.**

**Why `ENGINEERING` was added:** without it the card jumps from governance to principle and the reader never sees what was actually built. The full arc is *position → evidence → decision → governance → engineering → principle*, and the engineering row is what makes it a platform architecture review rather than a governance anecdote.

### `G-36` · Five-Layer Platform Stack  *(A3)* — **new hero graphic**
**Form:** five full-width bands. Knowledge (bottom) · Intelligence · Governance · Engineering · Production (top).
**Rule 1 — build it bottom-up.** If the deck animates, Knowledge appears first. The stack's argument is that knowledge is the *foundation*, not the output, and a top-down build inverts it.
**Rule 2:** each band carries **what it holds** and **one measured figure** — Knowledge `14 registries · 75 riders · 25 UNCONF` · Intelligence `4 engines, 4 questions` · Governance `90 documents · 20 clauses` · Engineering `39 modules · 14 guards` · Production `3-part series · 8-track album`.
**Rule 3:** do not draw arrows between bands. They are strata, not a pipeline; the pipeline is `G-30`.

### `G-37` · Governance-First Comparison  *(A5, C4)* — **new hero graphic**
**Form:** two vertical flows side by side, sharing a baseline.
Left, four steps: `PROMPT → OUTPUT → REVIEW → FIX`. Right, six steps: `GOVERNANCE → EVIDENCE → EXECUTIVE REVIEW → ENGINEERING → TESTING → PRODUCTION`.
**Rule 1:** annotate the left flow at the `REVIEW` step — *"governance arrives here: a filter on output that already exists. It can reject. It cannot prevent."*
**Rule 2:** annotate the right flow at the top — *"governance as precondition: ungoverned output cannot be produced."*
**Rule 3:** the left column must not be caricatured. It is what most competent teams do, and the slide is stronger if the audience recognises their own process without feeling mocked. **The argument is sequence, not sophistication.**

### `G-38` · Collaborative AI Model  *(A6, C5)* — **new hero graphic**
**Form:** a vertical spine that **begins and ends at a human**, with the two AI channels as parallel boxes in the middle.
`EXECUTIVE AUTHORITY → EXECUTIVE ORDERS → [ Creative Direction (ChatGPT) ‖ Engineering Channel (Claude) ] → VERIFICATION → GOVERNANCE → EXECUTIVE APPROVAL → PRODUCTION`
**Rule 1:** both channel boxes carry `authority: NONE` in the same weight as their names. **That label is the diagram.**
**Rule 2:** the human blocks — top and bottom — are visually heaviest.
**Rule 3:** name the roles first and the vendors second (parenthetical, smaller). Vendors date a deck; roles do not, and the evidence supports the roles.
**Rule 4:** the two channels are **parallel, not sequential.** Do not draw one feeding the other — they hold different custody and report to the same authority.

### `G-39` · Repository Authority Chain  *(A15)*
**Form:** nine stacked levels with a single descending spine — Executive · Governance · Specifications · Registries · Intelligence · Generators · Runtime · Testing · Commercial.
**Rule 1:** annotate each level with **what it constrains**, not what it contains.
**Rule 2:** draw a **return arrow** on the left running upward, labelled *"regenerate, never patch — any artifact can be rebuilt from the level above."* The chain is not one-directional and the return path is `DOC-002`.
**Rule 3:** mark the currently broken link — `CONDUCTOR_SCORE.yaml`, three dispositions un-materialised — in the Open accent. **A chain diagram that hides its broken link is a marketing diagram.**

### `G-40` · Four Levels of Reuse  *(A16, B18)* — **new hero graphic**
**Form:** four ascending tiers, each wider than the one below, with four columns: *what is reused · persists across · who owns it · status*.
```
4  INTELLIGENCE REUSE   the apparatus itself      every future domain      [E] exists · [O] unproven
3  REGISTRY REUSE       governed cited records    every future production  [E] exists · [O] unproven
2  KNOWLEDGE REUSE      facts extracted once      a project                common · fragile
1  PROMPT REUSE         the words you type        a session                universal · no advantage
```
**Rule 1:** levels 3 and 4 carry the Evidenced accent for *exists* and the Open accent for *compounding unproven*. **Both states on the same tier.** This is the slide where the package's honesty is most load-bearing — the economic argument and its unproven status must appear together.
**Rule 2:** the tiers are **different in kind, not degrees of the same thing.** Use a visual break between 2 and 3 — a rule, a gap, a change of treatment — because that boundary is where most organisations stop.

### `G-41` · Repository Scale Panel  *(A17)*
**Form:** a definition-bearing metrics grid. Three groups — Governance instruments · Code and testing · Knowledge.
**Rule 1:** **every cell carries its definition in smaller type beneath the number.** A number without a definition does not go on this slide.
**Rule 2:** the `ADR` row shows **2 in custody** with the note *"`ADR-001`–`008` cited, not in git"* in the Open accent. The census must show its own gap.
**Rule 3:** the `Executive Orders` row shows *"1 filed standalone · 8 documents record one's terms"* — the ambiguity is real and stating it is more credible than picking a number.
**Rule 4:** no total. The instruments are not commensurable and summing them would be a composite.

### `G-42` · Engineering Practice Matrix  *(A18)*
**Form:** a table graphic — *practice · how implemented · evidence* — with a final block styled differently: **the honest gaps column.**
**Rule:** the gaps block (`no CI · no dependency manifest · no release version since May · no code signing · no independent audit · pipeline has no unit tests`) is drawn at **equal visual weight** to the practices. A matrix that renders strengths large and gaps small is a scorecard, and this platform prohibits scorecards.

### `G-43` · Human Judgment Chain vs Prompt Chain  *(A19)* — **the essential graphic**
**Form:** two vertical chains, left and right, sharing a baseline. **Left, seven links:** Human Judgment · Executive Authority · Governance · Evidence · Engineering · AI Collaboration · Repeatable Production. **Right, three links:** Prompt · LLM · Output.
**Rule 1:** **draw both at true scale.** The right chain must be conspicuously short. Do not stretch it to fill the column — the asymmetry is the argument.
**Rule 2:** the left chain's links are connected by a continuous spine; the right chain's are connected by plain arrows. Different connective tissue, different claim.
**Rule 3:** annotate the right chain, beneath it, in Neutral: *"No custody boundary. No refusal path. No record of what was declined. Nothing here can say 'I will not do that, and here is why.'"*
**Rule 4 — the closing lines are the slide.** Set them as three separate lines with generous leading, in the Evidenced accent:
> **AI accelerated the work.**
> **Governance made it trustworthy.**
> **Human judgment made it valuable.**

**Rule 5:** resist illustration. No robot, no brain, no handshake, no human-and-machine silhouette. **This slide's power is its restraint** — two chains and three sentences.

### `G-44` · Ecosystem Reuse Map  *(A20)*
**Form:** a hub-and-spoke. **Capture** at the top, **Knowledge Repository** as the hub, six outputs beneath, **Enterprise Assets** at the base.
**Rule 1:** every spoke originates at the **hub**, never at Capture. That routing *is* Progressive Intelligence — engines consume governed outputs, never raw media. A diagram where a channel draws directly from footage depicts a different architecture.
**Rule 2:** **every node carries its grade** — `[E]` for YouTube and Music/streaming; `[P]` for Instagram, Community, Education, Future Products, Enterprise Assets.
**Rule 3:** the six reuse mechanisms run as a legend beneath: Content · Knowledge · Registry · Intelligence · Brand · Commercial, each with its own grade.

### `G-45` · Four-Tier Future  *(A21)*
**Form:** four horizontal tiers — CURRENT · NEAR TERM · LONG TERM · ASPIRATIONAL — with a **visible boundary rule** between each.
**Rule 1:** **the boundaries must be hard.** The Order requires *"do not blur."* No gradient fills, no fading, no overlapping shapes across tiers.
**Rule 2:** NEAR TERM and LONG TERM carry their gates inline — each goal paired with the gate that must clear first.
**Rule 3:** ASPIRATIONAL is **detached** from the tier stack, matching `G-27`, and labelled *"separate regulated programmes, not rungs."*
**Rule 4:** every tier carries a grade. CURRENT is `[E]`; the rest are `[P]`.

### `G-46` · Deterministic Generation  *(B11)*
**Form:** two runs of the same generator, side by side, with a byte-diff strip beneath.
**Rule:** show the diff at true proportion — **7 changed lines out of 205,679 bytes.** A diff strip that renders the change visibly is a misrepresentation; the point is that it is almost invisible, and the caption carries the number.

### `G-47` · Milestone Timeline with Callouts  *(Timeline document)*
**Form:** a horizontal timeline with **month bands as an axis** and **era blocks as the structure**, with callout boxes above and below.
**Rule 1 — months are a reading aid, not the organising principle.** The timeline is built on eras because a monthly structure misstates two facts (governance emerged in May, not June; intelligence in August, not July) and cannot render a gap. **Month labels sit on the axis; era blocks sit above it.**
**Rule 2 — the eleven-day silence is drawn as a void with the axis continuing through it**, with its own callout: *"Part 1 edited and published without the platform."* This is non-negotiable; it is the pivot of the narrative.
**Rule 3:** callout boxes for: Project Formation · Governance First · Engineering Acceleration · Documentary Production · **Silent Editorial Period** · Constitution Creation · Executive Orders · Engineering Reviews · Runtime Guard Architecture · Conformance Certification · Governance v1.0 · Presentation Architecture.
**Rule 4:** mark the 22 August spike — **32 commits, the densest day, and it is governance.**

### `G-48` · Legacy Chain  *(E-16, C56)* — **added under WET-EXEC-005**
**Form:** five links in a single vertical descent, each with its evidence grade set beside it.
```
The documentary proved the platform.        [E]
The platform produced knowledge.            [E]
The knowledge became the asset.             [E] exists · [O] compounding
The governance became the differentiator.   [E]
The methodology becomes the legacy.         [P]
```
**Rule 1 — the grades are part of the graphic, not a caption.** They sit at the same weight as the text. A legacy chain without its grades is a slogan.
**Rule 2 — the final link is rendered differently from the four above it.** Outline rather than fill, or a dashed connector into it. **It is the only sentence in the package written in the future tense**, and the visual must say so before the speaker does.
**Rule 3 — the third link carries two grades on one line.** `[E]` for *exists*, `[O]` for *compounding*. Do not resolve the tension; it is the honest state.
**Rule 4:** no ascending arrow, no upward curve, no "growth" motif. A descent that ends in a projection is the correct shape.

### `G-31b` · The Testing Inversion  *(B5)*
**Form:** two paired bars.
`ENGINE  5,802 LOC  ·  5,823 test LOC` — near-parity.
`PIPELINE  6,122 LOC  ·  0 test LOC` — one bar absent entirely.
**Rule:** draw the pipeline's test bar as an **empty outline at the position it would occupy**, not as a missing element. An absent bar reads as a layout artifact; an empty one reads as a finding.

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
| **Risk heat maps / 2×2 likelihood-impact grids** | a heat map is a composite score with a colour instead of a number. Use `G-34`'s table with an owner column |
| **A summed test total** | the four harnesses measure different things and are not additive (`G-31`) |
| **An ungated roadmap ladder** | superseded by `G-27`; regulated verticals are detached programmes, not rungs |
| **"What we believed" as a Moment Card field** | `ER-007 §3` prohibits the platform inferring Executive belief — use `THE POSITION ON RECORD` (`G-25`) |
| **A month-structured timeline** | months misstate two facts and cannot render the eleven-day gap — months are an axis, eras are the structure (`G-47`) |
| **Illustration on `G-43`** | no robot, brain, handshake or human-and-machine silhouette. Two chains and three sentences |
| **A summed instrument total on `G-41`** | governance instruments are not commensurable; summing them is a composite |
| **A right-hand chain stretched to match the left on `G-43`** | the asymmetry is the argument; true scale only |

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
