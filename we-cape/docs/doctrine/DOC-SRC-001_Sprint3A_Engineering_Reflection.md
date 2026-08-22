# DOC-SRC-001 — Doctrine Source: Sprint 3A Engineering Reflection
## Governance Status
Document Type: Doctrine Source (permanent) · Status: PRESERVED — VERBATIM, IMMUTABLE · Date: 2026-08-22
Authority: Executive Producer (Final Executive Disposition, Sprint 3A, 2026-08-22, item 3)
Reference Execution: RE-001 (`WECAPE-AR2-SPRINT3A-20260822-114028`)
Downstream consumers: Production Intelligence Review · LESSONS_LEARNED · V1.0 Platform Retrospective

## What a Doctrine Source is, and what it is not
A Doctrine Source preserves a practitioner's account **at the moment of completion**, before hindsight
tidies it. It is evidence about how the work actually went, held permanently and unedited.

It is **not** doctrine. Nothing in §1 is normative. Doctrine is ratified by the Chairman through the
ordinary route; §2 of this document offers candidate principles distilled from §1 and every one of
them is marked CANDIDATE. A reader who cites §1 as a requirement has misread the class.

Preservation rule: **§1 is verbatim and immutable.** If a later run contradicts it, that is recorded in
a new Doctrine Source, not by editing this one. The value of a reflection is that it was written before
the outcome was known.

---

## §1 — The Engineering Reflection (verbatim, as submitted 2026-08-22 at run completion)

> - **The ETC was less complete than its status implied.** `P2_LOCK_timing.json` publishes
>   `timeline_offset_s: null` for all 404 connected elements and references parents by *non-unique clip
>   name*. The 16 audio elements and 40 titles — the two things Step 0 was chartered to produce — were
>   simply not derivable from it. Re-deriving them from FCPXML nesting became the single most
>   load-bearing piece of work in the sprint.
>
> - **What made that safe was refusing to trust my own resolver.** Reproducing 191/191 ETC spine
>   offsets *first* is what earned the right to believe its connected-element output. Then P3 caught the
>   compound-clip case in rendered picture. Validate-the-instrument-before-the-measurement should be
>   permanent practice.
>
> - **The correlation nearly lied, twice, in exactly the same way.** S08 and S10 returned
>   confident-looking −6.75 s and −3.25 s lags. Both were saturated speech masks — ASR emitting
>   back-to-back cues with a 0.042 s median gap, one frame at 24 fps. Adding a null distribution and
>   edge/sign gates turned two fabricated "shifts" into two categorized INDETERMINATEs. **A correlation
>   peak with no null behind it is not evidence.**
>
> - **Assumption challenged, caught just in time:** I was one step from reading "DJI" in clip names as
>   "drone" and emitting drone-reveal events. DJI-named material includes 24 minutes of handheld
>   interviews. Device family never establishes capture mode — that near-miss is now written into the
>   registry as a warning to downstream consumers.
>
> - **The biggest finding came from the cheapest instrument.** A 64×36 luma series settled S16 in
>   seconds: mean luma 130.7 against a label saying "night". Coarse, quantitative, whole-runtime
>   measurement beat expensive per-frame reasoning, and the two together were stronger than either.
>
> - **Harder than anticipated:** the execution environment, not the analysis. Background processes are
>   killed at the shell-call boundary (the first DIE-V pass died silently), `rm` is blocked so a stale
>   `.git/index.lock` bricked git until I moved it aside, and staging refused the input path because of
>   the space before `/XML`. Roughly a third of the elapsed time went to plumbing.
>
> - **Should become permanent practice:** hash every input before touching it and cite the hash in
>   every artifact; make artifacts machine-generated from a committed script rather than hand-authored;
>   publish the sampling plan and the resolution ceiling *inside* the registry (D-24/D-25) so no reader
>   has to guess what the evidence can bear.
>
> - **Improve before Sprint 4 — the honest one:** supply a real proxy. At 320×180 I can give you
>   day/night, riding/static, crowd bands, ceremony/formation and burned-in text. I cannot give you
>   formation geometry, flag identification, or camera motion separated from subject motion. If Sprint 4
>   wants richer visual events, that needs a better proxy, not a better method.
>
> - **Second improvement:** the cue sheet and TIMELINE_REGISTRY disagree with the picture at two places
>   that matter musically (VCONF-01, VCONF-02) and leave 445.6 s carrying no cue and no silence.
>   Reconciling cue boundaries against observed activity *before* cue generation would prevent writing
>   beds against spans that end 2½ minutes before the action does.
>
> - **What the governance model actually bought:** "registries outrank visual observation" meant three
>   genuine disagreements got recorded rather than argued, and "no silent recovery" meant SLF-01 reached
>   your desk as an open question instead of a quiet judgement call I had no business making.

---

## §2 — Candidate principles (NON-NORMATIVE — none of these is ratified)

Each is a distillation offered for the Chairman's consideration. Ratification is a separate act.

| id | candidate principle | source bullet | improves (Three Improvements) |
|---|---|---|---|
| DC-01 | **Validate the instrument before the measurement.** A derived tool earns trust by reproducing a known-good set first; only then may its novel output enter custody. | 2 | Platform |
| DC-02 | **A correlation peak with no null behind it is not evidence.** Any statistical alignment claim carries a null distribution, an edge-rejection rule and a significance gate, or it is reported INDETERMINATE. | 3 | Platform |
| DC-03 | **Device family never establishes capture mode.** Metadata that names equipment is not evidence about how the shot was made. Generalises to: naming conventions are not observations. | 4 | Production |
| DC-04 | **Prefer the cheap whole-corpus instrument first.** Coarse quantitative measurement over 100 % of a runtime beats expensive reasoning over a sample, and the two together beat either alone. | 5 | Platform |
| DC-05 | **Declare the ceiling inside the artifact.** Sampling plan and resolution limits belong in the registry itself, not in a covering note, so no downstream reader has to guess what the evidence can bear. | 7 | Platform · People |
| DC-06 | **Artifacts are generated, never hand-authored.** The generating script is committed beside its output; reproducibility is a property of the repository, not of a person's memory. | 7 | Platform |
| DC-07 | **Hash before touch.** Every input is hashed as the first act of a run and the hash is cited in every artifact the run produces. | 7 | Platform |
| DC-08 | **Reconcile cue boundaries against observed activity before cue generation**, not after — a bed written against a span that ends before the action does is expensive to discover late. | 9 | Production |
| DC-09 | **An escalation is a deliverable.** Reaching the decision-maker as an open question with the evidence assembled is a successful outcome, not an incomplete one. | 10 | People |
| DC-10 | **Budget for the environment.** Roughly a third of a governed run's elapsed time went to execution plumbing rather than analysis; sprint estimates that assume otherwise will be wrong. | 6 | People |

## §3 — Standing action items raised by this source
| id | item | owner | status |
|---|---|---|---|
| AI-01 | Supply a full-resolution (or substantially higher-resolution) unwatermarked proxy as visual ground truth before Sprint 4 | Production | OPEN |
| AI-02 | Decide whether cue-boundary reconciliation against observed activity becomes a pre-generation gate | MIE / Executive | OPEN |
| AI-03 | Consider ratifying DC-01…DC-10, in whole or part | Chairman | OPEN |

## §4 — Provenance
Reflection submitted at completion of RE-001 (`WECAPE-AR2-SPRINT3A-20260822-114028`), 2026-08-22,
before Executive review. Preserved unedited by Final Executive Disposition, Sprint 3A, item 3.
Source of record: `intelligence/p2/ess/ESS_VALIDATION_REPORT.md` §9 and the Sprint 3A completion
summary. Related: `docs/reference_executions/RE-001_WECAPE-AR2-SPRINT3A.md`.
