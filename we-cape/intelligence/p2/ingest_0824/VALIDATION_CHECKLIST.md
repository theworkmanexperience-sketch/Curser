# INGESTION VALIDATION CHECKLIST — 08-24 Production Lineage

**State:** `PREPARED_NOT_EXECUTED` · **Prepared:** 2026-08-28 · **Custody:** `MACHINE`
**Authority:** `EXECUTIVE ORDER — CUSTODY_ALERT_001 FINAL DISPOSITION & WORKBOOK GENERATION` §2.5

**Every box below is unchecked. Nothing on this list has been performed.** The Order authorizes
preparing the checklist, not working it.

---

## 0 · Live conditions that exist right now

**These are not future steps. They are true today, while the suspension runs.**

| # | condition | why it matters now |
|---|---|---|
| **LC-1** | **`APPROVED_VIEWING_MASTER` names an APPROVED master for a superseded assembly.** `89e911b1…` at 4846.625 s is conformant to the 08-22 lock, which is now `SUPERSEDED_ASSEMBLY` | Any Executive Viewing Session held today would be held against the wrong film. Re-designation is **not authorized** and is barred by §4 |
| **LC-2** | **No conformant viewing master of the governed production exists or is designated** | No timecoded Executive judgement is possible on the production at all |
| **LC-3** | **`V-2` cannot detect `EPR-07`'s broken reference** | The validator's segment authority is the superseded assembly's. See `EPR-001_VALIDATION_REPORT_PATH_B.md` §3 |
| **LC-4** | **`EPR-001` v1.2.0 arms the §4.5 regeneration trigger, which §4 holds shut** | Documented, not worked around. Anyone reading the version increment alone would conclude regeneration is due |
| **LC-5** | **`RE-001` still reads `reference_status: ACTIVE`** | Under Path B it describes a superseded assembly. Changing it is **not authorized by any Order to date** |
| **LC-6** | **`TIMELINE_REGISTRY` v1.0.0 still carries its stale ±6 s tolerance note** | Superseded by Step 0 at offset 0.000 s, and now doubly stale under Path B |

---

## 1 · Instrument validation — before any measurement (`DOC-001`)

- [ ] **IP-1** · Editorial Timing Contract produced for the 08-24 lineage
- [ ] **IP-2** · `fcpx_resolve.py` re-validated against that ETC, element-for-element
- [ ] Resolver agreement recorded as a **number**, not an adjective (`DOC-001` rule 2)
- [ ] Second independent check taken where cheap (`DOC-001` rule 4)
- [ ] **Instrument declared conformant before any measurement is trusted**

## 2 · Source custody

- [ ] `SOP-06` Phase A re-export performed
- [ ] **`GATE-1`** timeline custody audit recorded (`SOP-06` A4)
- [ ] Four input hashes computed and pinned: FCPXML · SRT · MP4 · ETC
- [ ] The `Music/` directory inside `Final Data Source Files` inspected and classified
- [ ] The two `Sunday August 23` `_segment_*.mov` files classified
- [ ] Every asset in `observed_unclassified` assigned a class **by the Executive**

## 3 · Viewing master

- [ ] Conformant master exported for the governed production
- [ ] Conformance measured as **equality to the millisecond** against the governed lock
- [ ] **`APPROVED_VIEWING_MASTER` re-designation authorized by Executive Order** — *not authorized today*
- [ ] Previous APPROVED entry moved to `reference_only` with its reason recorded
- [ ] The quarantined `a94569ce…` candidate adjudicated — **duration equality is not source identity**

## 4 · Caption ingestion

- [ ] **IP-4** · Collapse rule declared for the Parent SRT's doubled cues (`A-D1`)
- [ ] 29 non-positive-duration cues (`A-D2`) dispositioned
- [ ] Per-episode SRTs reconciled against the Parent SRT by **text**, not timestamp
- [ ] The three Parts' 73.800 s prepended heads and 15–20 s tails accounted for in any per-episode caption index

## 5 · Segment authority

- [ ] Segment set re-derived against the governed production
- [ ] **Segment ID set ratified by the Executive** — additions, splits and retirements are Executive acts
- [ ] `S18`'s boundary re-derived (`PBC-2`)
- [ ] `S19`'s disposition ruled (`PBC-1`) — **survive · migrate · retire**
- [ ] `TIMELINE_REGISTRY` stale `delta_note` corrected (`LC-6`)
- [ ] **IP-7** · Episode boundaries assigned to segments — **not derivable before IP-1** (`PBC-3`)

## 6 · Cue-index integrity — the silent-failure surface

- [ ] All **91** `#NNNN` SRT cue-index citations re-pointed or retired
      — `RIDER_REGISTRY` 80 · `MOTORCYCLE_REGISTRY` 6 · `ORGANIZATION_REGISTRY` 3 · `PROMPT_REGISTRY` 2
- [ ] Re-pointing **method recorded**, not just the result
- [ ] **A cue index always resolves. It never errors. Nothing detects a wrong one but a human reading the line.**

## 7 · Executive intent

- [ ] **IP-5** · `EPR_EXECUTIVE_AUTHORING_WORKBOOK.md` completed by the Executive
- [ ] Intensity-scale ordinality declared (`PBC-4`)
- [ ] `EPR-05`'s two-state `audience_state` reviewed
- [ ] `S04` and `S17` — declare intent or confirm they carry none
- [ ] `EPR-001` reviewed and **formally ratified**

## 8 · Regeneration — gated

**None of this may begin until §7 is complete. `gen_artifacts.py` is under RUN_ID lock.**

- [ ] Regeneration authorized by Executive Order
- [ ] One atomic `gen_artifacts.py` run under one `RUN_ID` — **all seven artifacts, not four**
- [ ] `VOICE_PRIORITY_MAP` · `MUSIC_OVERLAY_TIMELINE` · `BEHAVIORAL_FINGERPRINT` re-derived
- [ ] `CUE_SHEET` · `CUE_SHEET_v1.1` · `MIE_INPUT_PACKAGE` re-derived
- [ ] Hand-authored registries re-derived — `VOICE_OVER` · `DOCUMENTARY_PROGRESSION` · `QUOTE_LIBRARY` · `ENERGY_CURVE` · `WHY_I_RIDE`
- [ ] `RE-002` archived with the `RE-001` delta categorized
- [ ] `RE-ARCHIVE-01` remedied — RE-001 holds no copy of the artifacts its scorecard describes
- [ ] `D-26` fix carried into `RE-002`
- [ ] `RE-001` set `reference_status: SUPERSEDED` — **requires Executive authorization**
- [ ] `ESS-001` · `ESS-002` · `ESS-003` re-scoped · `EVS-001` re-prepared

## 9 · Governance closure

- [ ] `EXECUTIVE_RULINGS.yaml` amended to record the final disposition — **not authorized today**
- [ ] Governance class assigned to the two 2026-08-26 Executive Orders (neither is `CAR/ADR/SPEC/PDR/ER`)
- [ ] `ER-005` Editorial Lineage Classification considered — registered as a future ruling, not drafted
- [ ] `DEFERRED_WORK_REGISTER` updated with everything deferred by this checklist

---

**Nothing above has been performed, and nothing above may be performed under the authority of the
Order that created this file.** The Order authorizes preparation only.
