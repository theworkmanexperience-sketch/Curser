# G3-ESS-001 Rev A — Final Executive Disposition, Sprint 3A
## Governance Status
Document Type: Executive Disposition · Status: **ISSUED AND EXECUTED** · Date: 2026-08-22
Authority: Executive Producer · Subject: Sprint 3A (G3-ESS-001 Rev A), run `WECAPE-AR2-SPRINT3A-20260822-114028`
Verdict: **PASS WITH MODIFICATIONS**

## Disposition as issued
1. Archive Sprint 3A as **Reference Execution 001 (RE-001)**.
2. Create **four Executive PDRs** for the production discrepancies identified.
3. Preserve the **Engineering Reflection** as a permanent doctrine source.
4. **Authorize downstream MIE work only after** the identified production PDRs are reviewed and
   dispositioned.

## Execution record
| # | action | artifact | state |
|---|---|---|---|
| 1 | Archive as RE-001 | `docs/reference_executions/RE-001_WECAPE-AR2-SPRINT3A.md` | COMPLETE — 4 input + 13 artifact hashes pinned |
| 2 | Four Executive PDRs | `docs/pdr/PDR-2026-08-22-ESS-001…004` | COMPLETE — all four OPEN, awaiting disposition |
| 3 | Preserve reflection | `docs/doctrine/DOC-SRC-001_Sprint3A_Engineering_Reflection.md` | COMPLETE — verbatim, immutable; 10 candidate principles offered non-normatively |
| 4 | Gate downstream MIE | `intelligence/p2/ess/DOWNSTREAM_AUTHORIZATION_GATE.yaml` | COMPLETE — gate CLOSED, machine-readable |

Two new document classes were declared in `docs/README.md` (the authoritative conventions document):
**Reference Execution** and **Doctrine Source**.

## Item 2 — how "the four" were identified
The disposition specifies four PDRs without naming them. They were taken from the conflict ledger in
`ESS_VALIDATION_REPORT.md` §5, which carries five rows: four in a state requiring disposition
(three CONFLICTED, one UNCERTAIN) and one recorded as an OBSERVATION requiring none.

| PDR | conflict id | subject |
|---|---|---|
| `PDR-2026-08-22-ESS-001` | VCONF-01 | S16 segment label vs observed illumination |
| `PDR-2026-08-22-ESS-002` | VCONF-02 | Escort ride duration vs CUE-03 span |
| `PDR-2026-08-22-ESS-003` | VCONF-03 | Caption policy vs the locked cut's lower-thirds |
| `PDR-2026-08-22-ESS-004` | SLF-01 / D-18 | Audio element inside SIL-01 |

**Candidates deliberately excluded, with reasons** — so the selection is auditable rather than assumed:

- **SLF-02** (SIL-01 opens over ride footage, not speech) — recorded as an OBSERVATION with no registry
  change required. It is not an open question; it is context the conductor needs, and it is already
  carried inside `PDR-2026-08-22-ESS-002`.
- **D-14** (CUE-01 span 00:00–01:13 vs `KICKSTANDS UP v1` out-point 00:01:16.417, Δ +3.417 s) — a real
  production discrepancy, but one the **existing per-cue PDR mechanism already covers**: CUE-02A_SPEC
  establishes that each cue's PDR records "in/out vs closed ETC · reconciliation verdict". D-14 belongs
  to `PDR-<date>-CUE-01`, not to a fifth Executive PDR.
- **D-24** (320×180 watermarked proxy supplied as visual ground truth) — an **input-supply** matter, not
  a production decision about the film. Carried instead as action item **AI-01** in DOC-SRC-001 §3.

If the Executive Team intended a different four — most plausibly substituting D-14 for VCONF-03, which
has no musical consequence — say so and the set will be re-issued. Nothing downstream has moved.

## Item 4 — the gate
Downstream MIE work is **BLOCKED** until all four PDRs above are reviewed and dispositioned. The gate
is recorded in machine-readable form at `intelligence/p2/ess/DOWNSTREAM_AUTHORIZATION_GATE.yaml` so MIE
tooling can read it rather than rely on a human remembering.

Note the pre-existing gate is unaffected and still applies: CUE_SHEET v1.1 records generation as
"gated on MIE-PROD-001", and PDR-2026-08-21-MIE-001 Rev A gates each pass behind cue PDRs with the
Conversation family required before Pass 2 unlocks. **This disposition adds a gate; it removes none.**

### Recommended disposition order
`ESS-004` and `ESS-002` should be taken **together** — both concern SIL-01, one its interior and one its
left boundary, and ESS-004 additionally settles whether MANDATORY_SILENCE means *no score* or *no sound*
for the platform. `ESS-001` follows (it reaches CUE-08). `ESS-003` is independent of music and can be
taken at any point, though it carries a consent dimension that deserves its own attention.

`ESS-004` is blocked on a **62-second human listen** to 00:33:37.708–00:34:39.667 of the locked cut.
That single action unblocks the highest-consequence decision of the four.

## Artifacts unchanged by this disposition
No Sprint 3A artifact was modified. RE-001's §4 hashes were computed from the committed bytes and still
verify. The seven ESS artifacts, the enriched CAPTION_REGISTRY and the five analysis scripts remain
exactly as delivered — regenerate-on-mismatch, never hand-edited (ADR-009 §2).

## Provenance
`COMMUNIQUE_G3-ESS-001_SPRINT3A_EXECUTION.md` → Sprint 3A execution (`3fe7365`, `8f70dee`, `b197e74`)
→ Sprint 3A completion summary → **this disposition** → RE-001 · PDR-2026-08-22-ESS-001…004 ·
DOC-SRC-001 · DOWNSTREAM_AUTHORIZATION_GATE.
