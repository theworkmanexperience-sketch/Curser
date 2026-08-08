# IAR-001 — Baseline Freeze Checklist
## Governance Status
Document Type: Procedural Checklist (Informational) · Normative Authority: None
Ratification Status: Not Ratified · Routing: Permanent corpus, docs/reviews/

## Required repository state BEFORE review
1. [ ] docs/README.md committed — Governance Status convention +
       git-tree-as-numbering-authority rule
2. [ ] SEM-001 + EA-001 committed to docs/methodology/ (both
       Informational; EA-001.5/.6 marked "Engineering Review Candidate")
3. [ ] ADR stubs 001-007 committed to docs/adr/ (number, title, status)
4. [ ] WET-SPEC-002 state truthful: v0.3 if it closes the two REV-002
       gaps; else v0.2 with gaps noted in its Governance Status
5. [ ] PMR-001 TBDs filled or marked OPEN
6. [ ] Runtime evidence to docs/reviews/IAR-001_baseline/: pytest
       output · repo tree · one full shoot.yaml · LINEAGE_X5 yaml ·
       derivations_X5.json · representative config
7. [ ] Large binaries referenced by path + SHA-256 in an evidence
       index, not committed
8. [x] PDR-000003/000004 under records/ (f2460cc)
9. [ ] Freeze commit "IAR-001 baseline freeze" →
       git tag iar-001-baseline && git push --tags
10.[ ] SHA recorded on the package cover + IAR-REP-001 §0.
       The TAG is what the reviewer reads.
