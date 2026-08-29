# WET-EXEC-010 / 011 — GAMMA DESIGN BRIEF
## Visual language for `WET_EXEC_GAMMA_FINAL_PRESENTATION.md`

**42 cards.** This file is never pasted into Gamma. It governs how the deck is rendered.

---

# 1 · THE ONE RULE ABOVE THE OTHERS

**This deck argues by structure, evidence and typography. It never argues by illustration.**

Its subject is a platform that refused to fabricate. A decorative image of a "governance professional" would be the deck contradicting its own thesis in the one channel the audience processes fastest. Every visual is either a diagram of something real, a number that was measured, or nothing at all.

**Empty space is a permitted design outcome.** Several cards are stronger with no graphic.

---

# 2 · VISUAL REFERENCE

Apple Keynote · OpenAI · Stripe Sessions · AWS re:Invent · Linear · Vercel.

Minimal. Architectural. Premium. Clean. Confident enough to leave half a card empty.

---

# 3 · COLOR SYSTEM

## 3.1 · Ground and neutrals

| role | value | use |
|---|---|---|
| Ground | `#0B0F14` near-black | default card ground |
| Ground alt | `#FFFFFF` | statement cards and the disclosure card |
| Deep navy | `#131C2B` | panel fills, diagram containers |
| Slate | `#5A6675` | secondary type, connector lines, axis rules |
| Light slate | `#A9B4C0` | supporting text on dark ground |

## 3.2 · The two accents — semantic, never decorative

| accent | value | meaning |
|---|---|---|
| **Blue** | `#3D7DFF` | **evidenced** — supported by the repository record |
| **Gold** | `#C9A227` | **open** — a gap, an unknown, or a claim not yet proven |

**These two colors carry meaning and may not be used for emphasis, rhythm, or variety.** A gold element on a card means something on that card is unproven. If nothing is unproven, no gold appears. An audience that learns this in the first five cards reads the rest of the deck faster — and an accent used decoratively destroys that.

**No third accent. No rainbow. No gradient except a single subtle vertical ground wash.**

---

# 4 · TYPOGRAPHY

| element | size | weight | notes |
|---|---|---|---|
| Card title | 56–72 pt | Semibold | Sentence case. One line wherever possible |
| Hero number | 72–120 pt | Bold, tight tracking | Tabular figures. Never wraps |
| Hero label | 20–24 pt | Medium, letterspaced +0.08em | All caps. Sits directly beneath its number |
| Supporting text | 24–32 pt | Regular | Maximum two lines |
| Quotation | 40–56 pt | Medium italic or regular | Set on its own card, no attribution block |
| Data type | 20–24 pt | Monospace, medium | Only for literal record content |

**Type families.** One grotesque for everything (Inter, Söhne, Helvetica Now or Gamma's nearest equivalent) plus one monospace (JetBrains Mono, IBM Plex Mono). No serif, no display face, no third family.

**Monospace is reserved and meaningful.** It marks text quoted from the record — `exit code 2`, `AWAITING_EXECUTIVE_DECLARATION`, `FAILED_CARDINALITY`, commit hashes, the UPC. It must read as evidence, never as styling. Do not set headlines or labels in monospace.

**Readable from the back of a conference room.** If a line needs to drop below 20 pt to fit, the line is too long — cut it, do not shrink it.

---

# 5 · LAYOUT

## 5.1 · The grid

12 columns, generous gutters, wide outer margins. Content occupies the middle eight columns on most cards; hero diagrams may use ten. **Never full-bleed to the card edge** except the two rider-wall cards.

## 5.2 · The three zones

Every card resolves to: **title** (top), **one visual anchor** (middle, dominant), **one supporting line** (below). Nothing else.

## 5.3 · One anchor, never two

**A card has exactly one visual anchor** — a diagram, or a number, or a timeline, or a matrix, or a quotation. Never a diagram and a chart. Never two number groups. When a card seems to need two, it needs an earlier card to have done more work.

## 5.4 · Whitespace

Minimum 12% clear margin on all sides. At least 40% of a typical card is empty. **Do not fill space with decoration, dividers, corner marks, watermarks, or a repeated logo.**

---

# 6 · ICONOGRAPHY

Clean outline icons, single weight (1.5–2 px at 24 px), single color, drawn from the neutral palette.

**Icon budget: at most eight icons in the entire deck** — the four commercial value pillars, and up to four in the ecosystem diagram. Everywhere else, the number or the diagram is the visual.

**Prohibited:** filled icons, duotone icons, cartoon icons, emoji, 3D or isometric clip art, icons on statistics cards, icons in ledgers or matrices, and any icon that decorates rather than labels.

---

# 7 · ANIMATION PHILOSOPHY

**Motion reveals structure. It never performs.**

| permitted | forbidden |
|---|---|
| Sequential reveal of diagram layers, in the order the argument runs | Fly-ins, bounces, spins, zooms |
| A single build on a number card: label, then figure | Anything with easing that draws attention to itself |
| Cross-fade between cards, ≤ 300 ms | Slide transitions, wipes, cube rotations, parallax |

**Two builds are mandatory:**

- **Card 04 (five-layer stack) builds bottom-up.** Knowledge appears first, production last. That inversion is the architectural claim; a top-down build asserts the opposite.
- **Card 17 builds both chains simultaneously.** If the seven-link chain builds first, the audience reads sequence. The argument is asymmetry, and asymmetry requires them side by side.

---

# 8 · CHARTS AND DATA

1. **Every percentage carries its numerator, denominator and source.** No exceptions.
2. **A zero is drawn as an empty outline at full width, never as a short bar and never as an absence.** An absent bar reads as a layout artifact; an empty one reads as a finding. This governs cards 08 and 21.
3. **True scale always.** No minimum bar heights, no broken axes, no logarithmic rescaling to make a small quantity visible. Cards 12, 17 and 22 argue by proportion and die if the proportion is adjusted.
4. **No totals across incommensurable quantities.** Card 27 sums nothing; summing commits and registries would be a composite.
5. **No composite scores of any kind** — no gauge dial, radar chart, traffic-light ring, health meter, readiness percentage, maturity score, or overall-status graphic, anywhere, including as decoration on an unrelated card. This is a governance prohibition, not a style preference.

---

# 9 · PROHIBITED VISUALS

Absolute, deck-wide:

- **People.** No photographs, illustrations, silhouettes or avatars of executives, engineers, riders, audiences or crowds.
- **Stock photography of any kind**, including offices, studios, workstations, meeting rooms and equipment.
- **Motorcycles, rallies, cameras, film equipment.** The deck is about the platform, not the shoot.
- **Robots, androids, humanoid machines, AI brains, neural-network glow, circuit-board textures, floating servers, cloud-with-lightning, glowing orbs, data-stream tunnels, hexagon grids, blue wireframe globes.**
- **Handshakes, human-and-machine hands touching, silhouettes shaking hands.**
- **Generic AI artwork and decorative cyber graphics.**
- Shields as a metaphor for governance, padlocks as a metaphor for security, gears as a metaphor for process, lightbulbs as a metaphor for insight, rockets as a metaphor for growth, chess pieces as a metaphor for strategy.
- Confetti, glow effects, lens flare, drop shadows on type, bevels, glass morphism.

**When no legitimate diagram exists for a card, the card carries type and space.** That is the correct outcome, not a gap to fill.

---

# 10 · THE FIVE CARDS THAT MUST NOT BE BEAUTIFIED

| card | rule |
|---|---|
| **08** Eleven Days of Silence | The gap renders as void — axis continues, bars stop. Never filled, shaded, iconed, or drawn as zero-height bars |
| **12** The Number That Was Never Computed | `1 / 191` stays almost invisible. No minimum bar height |
| **21** The Testing Inversion | The zero test bar is an empty outline at the exact width it would occupy |
| **31** Who May Decide | Empty cells stay conspicuously empty. No shading, no dashes, no "N/A" |
| **35** What This Presentation Does Not Claim | **Deliberately undesigned.** White ground, neutral text, no accent, no frame, no icon, no illustration, no graphic. Exempt from the 35-word rule. Any styling here reads as spin |

---

# 11 · THE TWO RIDER WALLS

Cards **02** and **41** are the same image, and that is the point.

- Exactly 75 tiles. 50 filled, 25 outline. Identical grid, identical tile positions on both cards.
- The 25 outlined tiles are **distributed as the data is** — never clustered, never shaded differently, never moved to one side, never sorted.
- **No faces, no photographs, no icons, no motorcycle imagery.**
- On card 41 the outlines take the blue accent. **Nothing is filled in.** The grid is unchanged because nothing was resolved — it was honoured.

---

# 12 · THE FINAL CARD

Five links in a single vertical descent, generous spacing, centred.

Links one through four: solid connectors, blue accent. **The fifth link — *The Future will determine the legacy* — is outline rather than fill, reached by a dashed connector,** because it is the only line in the deck written in the future tense.

**No ascending arrow, no upward curve, no growth motif.** A descent that ends in something not yet earned is the correct shape. Nothing else on the card, and nothing after it.

---

# 13 · GAMMA IMPORT SEQUENCE

**Step 1.** Paste the full contents of `WET_EXEC_GAMMA_FINAL_PRESENTATION.md`. Split on `---`. Expect 42 cards.

**Step 2.** Paste this as the theme prompt:

> Premium executive keynote in the register of Apple Keynote, OpenAI, Stripe Sessions and Linear. Near-black ground, deep navy panels, slate neutrals, one blue accent and one gold accent — no other colors, no rainbow, no gradients beyond a single subtle ground wash. Very large display titles and very large numerals, minimal body text, wide margins, generous white space, high contrast. One dominant idea per card. Clean single-weight outline icons, used sparingly. Absolutely no photography, no images of people, no robots, no AI brains, no circuit boards, no floating servers, no handshakes, no stock imagery, no decorative cyber artwork. Communicate through structure, evidence and typography only.

**Step 3.** Generate diagrams card by card using `WET_EXEC_GAMMA_IMAGE_PROMPTS.md`. Do not let Gamma infer a diagram for any card listed there — the geometry carries the argument.

**Step 4.** Type speaker notes from `WET_EXEC_GAMMA_PRESENTER_SCRIPT.md` into each card's notes panel. Gamma does not import notes.

**Step 5.** Walk §10 and §11 against the rendered deck before presenting. Those are the rules Gamma's styling pass is most likely to break.
