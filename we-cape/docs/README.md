
## Constitutional Conventions (ratified 2026-08-20)

### Specification Numbering
Intelligence specifications use named-series numbering:
WET-SPEC-DIE-001, WET-SPEC-NIE-001, WET-SPEC-MIE-001, WET-SPEC-PIE-001.
The sequential series (WET-SPEC-001, -002, -003...) continues to govern
platform-core specifications. This README is the authoritative
numbering policy.

### Document Class: Chairman's Acceptance Memorandum
A first-class governed artifact recording the Chairman's ratification
of an assessed document, including incorporated modifications and a
References provenance chain (assessment commit, frozen-source commit,
source SHA-256, certification date).

### docs/architecture/
Home of architectural vision documents (repository canonical sources,
frozen at certification; e.g. AIS-001).

### The Three Improvements Principle (ratified 2026-08-21)
Every significant improvement to WE CAPE shall improve one of three
things: the Platform, the Production, or the People. Improvements that
strengthen all three are considered enduring platform investments.

### Document Class: Reference Execution (ratified 2026-08-22)
A complete, hash-pinned record of one governed run preserved as the comparison
baseline for future runs. Numbered RE-NNN, held in docs/reference_executions/.
A Reference Execution validates; it never defines. It certifies what the
platform did on stated inputs at a stated commit, and it carries an explicit
statement of what it does NOT certify. Values inside one do not become
normative targets by being cited — promotion to a requirement takes an ordinary
specification change under the Freeze route. Artifacts referenced by a
Reference Execution are immutable: a correction is a new run archived as the
next RE, with the delta categorized, never an edit to the old one.
Class boundary: ADRs govern the platform · PDRs govern productions ·
Reference Executions govern comparison.

### Document Class: Doctrine Source (ratified 2026-08-22)
A practitioner's account preserved verbatim at the moment of completion,
before hindsight edits it. Numbered DOC-SRC-NNN, held in docs/doctrine/.
A Doctrine Source is evidence, not doctrine: nothing in its preserved section
is normative, and candidate principles distilled from it are marked CANDIDATE
until ratified through the ordinary route. The preserved section is immutable —
a later run that contradicts it is recorded in a new Doctrine Source, because
the value of a reflection is that it was written before the outcome was known.
Feeds: Production Intelligence Review · LESSONS_LEARNED · Platform Retrospective.
