# RE-001 — Reference Execution 001: WECAPE-AR2-SPRINT3A
## Governance Status
Document Type: Reference Execution (archival) · Status: ARCHIVED — IMMUTABLE · Date: 2026-08-22
Authority: Executive Producer (Final Executive Disposition, Sprint 3A, 2026-08-22)
Class boundary: ADRs govern the platform · PDRs govern productions · **Reference Executions govern
comparison** — they are the frozen evidence a later run is measured against, and they are normative
about nothing else.

## 1. What a Reference Execution is
A Reference Execution is a complete, hash-pinned record of one governed run that the Executive Team
has elected to preserve as the comparison baseline for future runs. It is not a specification, not a
requirement, and not a target. It answers exactly one question: *what did the platform actually do,
on what inputs, at what commit, producing what bytes.*

The distinction matters. WET-SPEC-DIE-001 Appendix A already carries a **reference fixture** — observed
values that validate but never define. RE-001 extends that discipline from a single extraction to a
whole sprint: the fixture principle applied at execution scale.

## 2. Frozen coordinates
| field | value |
|---|---|
| RUN_ID | `WECAPE-AR2-SPRINT3A-20260822-114028` |
| Sprint | G3-ESS-001 Rev A (Sprint 3A) |
| Production | Alpha RoundUp Part 2 |
| Executed | 2026-08-22T11:40:28Z → 2026-08-22T12:14Z (~33.5 min wall clock) |
| Commit at launch | `ff0c45f77b2fb612606e1d5b8ef86641822e5e4a` |
| Commits produced | `3fe7365382118c71dcdf43d013c321f58dddb81a` · `8f70dee88b6d281ec01ca4edafeb9a523c40bf61` · `b197e74` |
| Branch | `main` |
| Governing spec | WET-SPEC-DIE-001 v0.2 (frozen, tag `wet-spec-die-001-v0.2-frozen`) |
| Governing architecture | ADR-009 (ACCEPTED, Chairman 2026-08-21) |
| Constitution | AIS-001 v1.0 (`51d31e2`, certified) |
| Executive verdict | PASS WITH MODIFICATIONS |

## 3. Input hashes (the four authoritative production artifacts)
| # | input | SHA-256 |
|---|---|---|
| 1 | `Filmage_Editor.mp4` (visual ground truth — see §7) | `a53655fc673945a0d99dde3d5b60c9a126d8b41e4e44a7c7eedeb058ba0f47e8` |
| 2 | `Alpha RoudUp Part 2.fcpxmld/Info.fcpxml` (editorial ground truth) | `2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7` |
| 3 | `…_SRT__SRT 2_English (United States).srt` (canonical SRT, GT-2) | `89d61f965aa17e4d3dade14173869b34efb0c09d689b1c347d3c9c8f6eca1c6b` |
| 4 | `P2_LOCK_timing.json` (Editorial Timing Contract) | `e91318a6719c81e448e6c57267dff7a807076cb9aded822a459fb6353e80010d` |

The ETC's own `source_sha256` field equals input 2's hash. The four-source chain is closed at the hash
level in both directions, not asserted.

## 4. Artifact hashes (the bytes this reference preserves)
| artifact | SHA-256 |
|---|---|
| `intelligence/p2/ess/STEP0_TIMING_CLOSURE.md` | `de3ae56b791674737c59d917fb2cc6db800d3fd6307d3ccce353def4b05ebec8` |
| `intelligence/p2/ess/VISUAL_EVENT_REGISTRY.yaml` | `bb699bc7b093e6b150455dc3b8cd5ac3b93135d6c645e7a24948afae26893161` |
| `intelligence/p2/ess/EDITORIAL_SYNCHRONIZATION.yaml` | `505d5c0953887c55f5d91eaa9dc520f8144a3fac327d78d770ba8d121e28d49b` |
| `intelligence/p2/ess/CONDUCTOR_SCORE.yaml` | `12c97e69a0285c2c9c37905e9d521b1d6ef247401cd994b0669ac9156c3109e7` |
| `intelligence/p2/ess/ESS_VALIDATION_REPORT.md` | `3d010a9578c58767dab940e65127baf54f603eb7ae188bc8a4a4a5a987586814` |
| `intelligence/p2/ess/PRODUCTION_INTELLIGENCE_SEED.yaml` | `f58004548a1b2c0f15a71c9d16879304f49151c1b2d14e315a60044155904fab` |
| `intelligence/p2/ess/EXECUTION_LOG.md` | `cfc0530dda90c3fe92f222c6a46b73b923ea59f05aa63f0b7e6831dd86bfa825` |
| `intelligence/p2/registries/CAPTION_REGISTRY.yaml` (0.2.0) | `89e1db10cacff43f8b15db51e3d80c66095718df6db9abaf96132d9c7632d5d3` |
| `…/ess/scripts/fcpx_resolve.py` | `79dd908cfe2ff0fc84067425421d68c774163ebbb5920be44f2e6fb695d4102b` |
| `…/ess/scripts/step0_offset.py` | `47b7d760bd1145fcb2e98fc9e240e69006d70b80b1625dbfdcbce9afd6215997` |
| `…/ess/scripts/step0_anchors.py` | `f3825ca3d878fe1f96320aa45157c9bcd198047877993eecd8c7c543d5cf66d0` |
| `…/ess/scripts/die_v_observables.py` | `a11c9d4f54fc6c5698268dbc59a01af87d934d1bed5b6623f24f99c63bd12e9f` |
| `…/ess/scripts/gen_artifacts.py` | `33434869d0e72951d9b0a0962f2519a4ab77c16dd06cc99f9ea3007625b47b8a` |

## 5. Execution metrics preserved
Runtime processed **4846.625 s** · offset model **0.000 s, no drift** · DIE-V events **39** ·
synchronization rows **32** (91.0 % of runtime inside a registry segment) · cues + conducted silences
**15 + 3** (90.8 % of runtime covered) · existing audio elements reconciled **16/16** · captions
positioned **57** (40 ETC-census + 17 newly enrolled) · deltas logged **25**, uncategorized **0** ·
probes **3/3 PASS** · conflicts **3** · escalations **2** · music generated **0** · biometric
operations **0** · sentiment inferences **0**.

## 6. What RE-001 certifies — claims that may be cited downstream
1. **The Step 0 offset model.** Lock SRT ≡ ETC timebase, offset 0.000 s, drift 95 % CI
   [−0.541, +1.909] s over the full runtime. Established by three independent methods.
2. **The FCPXML absolute-time resolver.** Reproduces 191/191 ETC spine offsets to within 0.0006 s and
   terminates exactly at 4846.625 s. Any future run may cite this as the validated resolution method
   for connected elements the ETC leaves null.
3. **The resolved positions** of the 16 audio-lane elements and all 57 title elements.
4. **The audio-element provenance split**: 1 score asset, 14 detached production audio, 1
   contributed-video audio — read from FCPXML asset paths, not inferred.
5. **The fixture-probe method** (three windows, validate before custody) as a working instance of
   WET-SPEC-DIE-001 rule X-5.

## 7. What RE-001 does NOT certify — read this before citing it
A reference execution is only as good as its declared ceiling. RE-001's:

- **The visual ground truth was a 320×180 watermarked proxy**, not the 3840×2160p24 master the FCPXML
  describes (delta D-24). RE-001 is *not* evidence that DIE-V can resolve formation geometry, flag
  identification, or camera motion separated from subject motion. It is evidence of what DIE-V can do
  **at proxy resolution**. A future run against a real master is not comparable on those classes.
- **20 of 54 survey contact sheets were read in full** (D-25). Non-gauntlet coverage is complete; the
  two interview gauntlets — 38 % of runtime — carry span-level classification only. RE-001 must not be
  cited as per-event coverage of the gauntlets.
- **12 of 19 registry segments could not yield an independent offset estimate** and are recorded
  INDETERMINATE with reasons (D-10). The zero-offset conclusion rests on the seven that could, plus the
  two non-correlation methods — not on 19 agreeing measurements.
- **The envelope correlation is a weak instrument** (peak r = 0.278). It is convincing because the peak
  sits at exactly zero and beats a proper null, and because two independent methods agree. Cited alone
  it would not close the tolerance.
- **Four production discrepancies remain undecided** (§9). RE-001 preserves the *evidence* for them; it
  does not preserve an answer, and nothing in it should be read as one.

## 8. Permitted uses
- **Regression baseline.** A future run on the same four input hashes should reproduce §4 byte-for-byte
  from the preserved scripts. Divergence is a finding, not a failure — but it must be categorized.
- **Fixture source.** The three probe windows and their expectations may be reused as validator
  fixtures for any model-mediated visual extraction.
- **Method citation.** §6 claims may be cited by later sprints without re-deriving them, provided the
  citing document also carries the §7 boundary.
- **Comparison, and only comparison.** RE-001 never becomes a requirement by being referenced. It
  validates; it does not define. Any attempt to promote a value here into a normative target requires
  a specification change under the ordinary Freeze route.

## 9. Open Production Decision Records attached to this reference
| PDR | subject | status |
|---|---|---|
| `PDR-2026-08-22-ESS-001` | S16 segment label vs observed illumination (VCONF-01) | OPEN |
| `PDR-2026-08-22-ESS-002` | Escort ride duration vs CUE-03 span (VCONF-02) | OPEN |
| `PDR-2026-08-22-ESS-003` | Caption policy vs the locked cut's lower-thirds (VCONF-03) | OPEN |
| `PDR-2026-08-22-ESS-004` | Audio element inside SIL-01 (SLF-01 / D-18) | OPEN |

Downstream MIE work is gated on the disposition of all four — see
`intelligence/p2/ess/DOWNSTREAM_AUTHORIZATION_GATE.yaml`.

## 10. Immutability
The artifacts listed in §4 are frozen at the hashes given. They are **regenerate-on-mismatch, never
hand-edited** (ADR-009 §2). Correcting a finding does not mean editing RE-001: it means executing a new
run and archiving it as RE-002, with the delta between them categorized. RE-001 records what happened,
including the parts that were wrong.

## 11. Provenance chain
Constitution AIS-001 v1.0 (`51d31e2`) → Acceptance Memorandum (`27674d7`) → WET-SPEC-DIE-001 v0.2
(frozen) → ADR-009 (ACCEPTED 2026-08-21) → PDR-2026-08-20-ETC-001 (ETC elevated) →
PDR-2026-08-21-MIE-001 Rev A (Road Soul palette) → COMMUNIQUE_G3-ESS-001_SPRINT3A_EXECUTION →
**RE-001** (this document) → Final Executive Disposition, Sprint 3A, 2026-08-22.
