# CAR-003 — Executive Disposition
## Governance Status
Document Type: Collaborative Architecture Review — Disposition · Status: **CLOSED**
Date: 2026-08-22 · Initiative: PHI-001 · Authority: Executive Producer
Decision: **PASS WITH MODIFICATIONS** · Findings: **ACCEPTED**

## Decision
The Executive Team accepts the findings of the Platform Hygiene Review. The review correctly
distinguished documented knowledge, deferred work, naming inconsistencies, governance debt, technical
debt and institutional memory gaps.

The Executive Team concurs with the review's central finding:

> **The primary risk is not missing capability; it is institutional memory and naming consistency.**

## Executive reframe — recorded because it is larger than the finding it came from
> *"The review wasn't really about hygiene. It was about **discoverability**. Your platform has grown
> to the point where capabilities can exist without people realizing they already exist. That's a sign
> of success — but it's also a signal that information architecture is becoming just as important as
> software architecture."*
> — Executive Producer, 2026-08-22

This is a sharper statement of the problem than the review itself reached, and it changes what the
remedy looks like. A hygiene problem is fixed by tidying. A **discoverability** problem is fixed by
making capability *findable by the name people actually use* — which is an information-architecture
discipline, not a cleanup task.

The evidence supports the reframe: five of the ten "missing" topics were present in the repository the
whole time (`cameras.yaml`, the dashboard prototype, GAP-03's score ruling, DPAL's expansion,
`docs/doctrine/`). Nothing had to be built for them to exist. Something had to be *named*.

**Recorded as a doctrine-source candidate** for the next Doctrine Source, not minted as doctrine here:
*a capability nobody can find has the same value as a capability nobody built.*

## Disposition of the eight recommendations
| # | recommendation | disposition |
|---|---|---|
| R1 | Decision/Implementation split as a permanent DWR field | **ACCEPT** |
| R2 | QW-1 (`CAR_ROADMAP.md`) as highest-value action | **ACCEPT** |
| R3 | Rule on rights-line coverage before any Part 2 publication step | **ACCEPT** |
| R4 | Resolve the ADR reference space | **ACCEPT** |
| R5 | Rule on PDR numbering before the next PDR is issued | **ACCEPT** |
| R6 | Extend the existing dashboard; do not build a new one yet | **ACCEPT** |
| R7 | Treat five topics as naming, not capability, gaps | **ACCEPT** |
| R8 | Schedule the next hygiene review by trigger, not calendar | **ACCEPT** |

## Modification
Capture Intelligence shall **not** be appended to CAR-003. It is opened as a dedicated architectural
review, **CAR-004**, and reframed at Executive direction from *Capture Intelligence* to
**Acquisition Intelligence Architecture**, with Capture Intelligence as its first module.

Rationale, as directed: the platform will eventually acquire photographs, audio, drone logs, GPS, GPX,
SRT, FCPXML, social media, documents, call sheets, interview notes, music and releases. Those are all
acquired production assets. *Capture* is one module of *acquisition*.

This preserves the integrity of the CAR process, keeps the hygiene review focused on institutional
memory, and gives the acquisition architecture the depth it deserves before any implementation begins.

## Status of CAR-003 artifacts
| artifact | state |
|---|---|
| `CAR-003_PLATFORM_HYGIENE_REVIEW_FINDINGS.md` | ACCEPTED, closed |
| `records/dwr/DEFERRED_WORK_REGISTER.yaml` (36 entries) | ACCEPTED as the authoritative deferred-work record |
| Ten Quick Wins | ACCEPTED as recommendations; **not yet authorized for implementation** |
| Governance / Technical Debt registers | ACCEPTED |

CAR-003 is **CLOSED**. Its open items live on in the Deferred Work Register, which is where they
belong — closing a review does not close its findings.

## Successor
`CAR-004 — Acquisition Intelligence Architecture Review` (opened 2026-08-22).
