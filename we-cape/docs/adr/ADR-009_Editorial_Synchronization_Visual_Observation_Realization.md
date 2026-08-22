# ADR-009 — Editorial Synchronization & Visual Observation Realization
## Governance Status
Document Type: Architecture Decision Record · Status: ACCEPTED (Chairman, 2026-08-21)
Authority: preserves frozen AIS-001 (51d31e2, certified) · Companion: Engineering review of the G3/ESS communique

## 1. Why DIE-V became a MODULE, not a new engine
The frozen constitution already assigns DIE extraction from
"transcripts, VIDEO, telemetry" — visual events (formations, reveals,
golden hour, flags, crowd density, camera motion) are OBSERVED facts,
and the registry model was already waiting for them (the
MOTORCYCLE_REGISTRY's empty visual_* triplet fields made the gap
measurable). A fifth engine would have duplicated DIE-X's charter for a
different medium three days after freezing a four-engine architecture —
engine proliferation is the platform's top-ranked governance risk, and
a module delivers the capability at module cost. Boundary preserved:
interpretation ("emotional interactions," "visual pacing") is NIE-class
and arrives only via nie.* enrichment namespaces; biometric
identification is prohibited — person linkage is human-confirmable
registry reference only.

## 2. Why ESS became an ARTIFACT, not an engine
Synchronization is fusion of things that already exist under
governance (ETC + registries + progression + energy + visual events) —
correlation, which the 20-clause architecture assigns to invariants
11-13, already DIE's charter. What downstream consumers need is not a
new authority but ONE governed answer they all read identically: a
hash-pinned, regenerate-on-mismatch, never-hand-edited artifact —
EDITORIAL_SYNCHRONIZATION.yaml, the FIFTH authoritative production
artifact (after master video, canonical SRT, locked FCPXML, ETC).
Artifacts-at-hashes couple automation loosely; engines couple it
tightly. Engine chartering remains available to the evidence-triggered
Rev process if production later proves the need — this ADR preserves
the rationale a future charter would inherit.

## 3. Why the Conductor's Score REMAINED under MIE
It is musical intent made executable — cue boundaries, behavior states,
ducking, rebuilds, Road Soul family assignments — which is MIE's
emission tier evolved, exactly as the cue sheet's successor. It follows
the ETC precedent (PDR-2026-08-20-ETC-001): a machine-readable contract
pinned to the editorial ground truth's hash. Moving it out of MIE would
separate musical intent from musical accountability: it stays advisory
until cue PDRs (Human Editorial Authority), and the silence law
(SIL-01, SIL-02, R46 carve-out) is encoded in it as behavior states —
silences are conducted, not omitted.

## 4. Why sync_event became the CANONICAL synchronization schema
DIE-V and ESS must speak one language or every consumer re-derives
alignment differently — the re-analysis drift Progressive Intelligence
prohibits. Canonical schema:
sync_event: {id, span{start_s,end_s}, event_class, source{artifact,sha},
evidence_ref, confidence, enrichment{nie.*, mie.*, pie.*}}
One schema → visual events, sync rows, and score behaviors align by
construction, and the enrichment namespaces let higher engines annotate
without ever writing DIE-owned fields (M8 ruling, generalized).

## Consequences
Four engines stay frozen · new capability = modules + artifact
contracts · "frame-accurate" gated on closing the ±6s SRT/ETC tolerance
· model-mediated video extraction requires fixture validation before
registry custody.
