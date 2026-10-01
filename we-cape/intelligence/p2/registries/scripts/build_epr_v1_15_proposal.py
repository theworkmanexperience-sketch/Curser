#!/usr/bin/env python3
"""
EPR-001 v1.15.0-PROPOSED - PBC lifecycle reconciliation (CHAIRMAN GOVERNANCE RULING - PBC LIFECYCLE
RECONCILIATION, 2026-10-01). Derived from ratified EPR-001 v1.14.0, read from git commit 096d127
(hash-asserted). Writes only EMOTIONAL_PROGRESSION_REGISTRY_v1.15.0-PROPOSED.yaml.

ADDITIVE ONLY. Each PBC record's existing lines (condition, detail, disposition, owner and, for
PBC-4, disposition_token_note) are carried byte-identically; lifecycle fields are appended after
them, using ONLY field names and tokens already present in EPR-001:
  fields  status, resolved, resolution, resolved_by  (undeclared_segments S04/S17, v1.12.0)
          note                                       (undeclared_segments_note; EPR-06 terminal note)
                                                     PBC-1 note added per EPR-07 RETIREMENT INTEGRITY ruling (Option B)
          regeneration_trigger{rule, increment, disposition, authority, reason_verbatim, executed}
                                                     (registry_ratification, v1.14.0)
  tokens  RESOLVED, RESOLVED_BY_RETIREMENT, HELD
PBC-3 receives NO status (two existing tokens could apply; no precedent selects one) - note only.
PBC-5 untouched. No timecode-shaped text is introduced.
"""
import hashlib, os, subprocess, sys

REG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(os.path.join(REG, '..', '..', '..'))
BASE = '096d12762a06aabbf25f0eb3b0c9c019f84053d3'
SRC = 'intelligence/p2/registries/EMOTIONAL_PROGRESSION_REGISTRY.yaml'
SRC_SHA = '4aeb1496bb836aab4fd9153cb750fd671b4f326871b7d4d98362054a566047b9'
TL_SHA = '510697b9bbd1ed01c6c61ab6c6063dd511cfc71abad0ad11629fbeb807db0da3'
OUT = os.path.join(REG, 'EMOTIONAL_PROGRESSION_REGISTRY_v1.15.0-PROPOSED.yaml')
RULING = 'CHAIRMAN GOVERNANCE RULING - PBC LIFECYCLE RECONCILIATION, 2026-10-01'

ADD = {
    'PBC-1': ('    disposition: UNRESOLVED_PENDING_EXECUTIVE\n    owner: EXECUTIVE\n',
              "    status: RESOLVED_BY_RETIREMENT\n"
              "    resolved: '2026-08-28'\n"
              "    resolution: >-\n"
              "      EPR-07 was retired by governing authority and its segment reference is recorded as\n"
              "      RESOLVED_BY_RETIREMENT on the entry. This record therefore no longer requires resolution\n"
              "      because the governed item was retired. This does NOT assert that the original underlying\n"
              "      support question was substantively answered. TIMELINE_REGISTRY v1.1.0 retains S19\n"
              "      unchanged.\n"
              "    resolved_by: >-\n"
              "      EXECUTIVE ORDER - EPR-001 RATIFICATION & RUN_ID LOCK RELEASE, section 1 (Q10 RETIRE);\n"
              f"      lifecycle recorded under {RULING}, ruling 2.\n"
              "    note: >-\n"
              "      EPR-07 REMAINS RETIRED; its operative disposition is unchanged. Its retirement-era\n"
              "      rationale - that S19 exists entirely outside the governed 08-24 production runtime - is\n"
              "      CORRECTED by the G8-ratified re-derivation, which places the measured S19 material inside\n"
              "      the governed runtime, ending before its boundary. The correction does NOT reinstate EPR-07.\n"
              "      Correction record: docs/rulings/EO-2026-09-29_ADDENDUM_C_EPR07_Retirement_Rationale_Correction.md\n"
              "      (CHAIRMAN / EXECUTIVE RULING - EPR-07 RETIREMENT INTEGRITY, Option B, 2026-10-01).\n"
              "      Evidence: DECISION_PACKET_B5_B14 section 4, S19 row; v2/rederivation_v2.json segment S19\n"
              "      (5bd4af48..., G8-ratified). Figures are carried there, not here (timecodes prohibited).\n"),
    'PBC-2': ('    disposition: BOUNDARY_OUT_OF_RANGE_PENDING_REDERIVATION\n    owner: platform, after regeneration is authorized\n',
              "    status: RESOLVED\n"
              "    resolved: '2026-10-01'\n"
              "    resolution: >-\n"
              "      S18 has been re-derived. Its span in the ratified TIMELINE_REGISTRY v1.1.0 lies wholly\n"
              "      inside the governed runtime; the out-of-range and not-re-derived statements above are\n"
              "      historical, not current. Figures are carried by TIMELINE_REGISTRY v1.1.0 S18, not here\n"
              "      (timecodes are a prohibited field of this registry).\n"
              "    resolved_by: >-\n"
              f"      Chairman ratification of TIMELINE_REGISTRY v1.1.0 (sha256 {TL_SHA},\n"
              "      commit 096d127); EO-2026-09-29 Addendum A Tier 1 (S18 PRESERVE + REBASE); G8-ratified v2\n"
              f"      mapping (rederivation_v2.json 5bd4af48...); lifecycle recorded under {RULING}, ruling 3.\n"),
    'PBC-3': ('    disposition: NOT_DERIVABLE_WITHOUT_REGENERATION\n    owner: platform, after regeneration is authorized\n',
              "    note: >-\n"
              "      Recorded under " + RULING + ", ruling 4. Two propositions,\n"
              "      kept separate. (1) HISTORICAL PREMISE, NO LONGER TRUE: segment positions in the 08-24\n"
              "      Parent now exist, in the ratified TIMELINE_REGISTRY v1.1.0. (2) CURRENT CONDITION,\n"
              "      UNCHANGED: no segment-to-episode assignment has been authorized or made; EO-2026-09-29\n"
              "      D-1 charters episode work as a follow-on order. TIMELINE_REGISTRY v1.1.0 establishes\n"
              "      positions but does not authorize the assignment decision. The disposition and owner above\n"
              "      are retained unchanged; this record remains UNRESOLVED. No assignment, straddle, head or\n"
              "      Part-boundary question is decided here.\n"),
    'PBC-4': ('      inflate that census by one without an actual field being empty.\n    owner: EXECUTIVE\n',
              "    status: RESOLVED\n"
              "    resolved: '2026-08-28'\n"
              "    resolution: >-\n"
              "      The ordinality was declared: intensity_scale.ordered is true and scale_class is\n"
              "      ORDERED_CATEGORICAL, transcribed at v1.3.0. The statement above is historical. No\n"
              "      intensity value is changed by this record.\n"
              "    resolved_by: >-\n"
              "      Executive Ruling Q11 - Ordered Categorical Dramatic Intensity Standard (2026-08-28);\n"
              f"      lifecycle recorded under {RULING}, ruling 5.\n"),
}


def main():
    b = subprocess.run(['git', 'show', f'{BASE}:./{SRC}'], cwd=ROOT, capture_output=True, check=True).stdout
    if hashlib.sha256(b).hexdigest() != SRC_SHA:
        sys.exit('STOP FAILED_SOURCE_IDENTITY v1.14.0')
    t = b.decode()

    def once(a, c):
        nonlocal t
        if t.count(a) != 1:
            sys.exit(f'STOP anchor x{t.count(a)}: {a[:70]!r}')
        t = t.replace(a, c)

    for pid, (anchor, addition) in ADD.items():
        once(anchor, anchor + addition)

    once('registry_version: "1.14.0"\n',
         'registry_version: "1.15.0-PROPOSED"\n'
         'proposal_status: "PROPOSED — AWAITING CHAIRMAN RATIFICATION"\n'
         'regeneration_trigger:\n'
         '  rule: "ratification order section 4.5 - a registry_version increment is the regeneration trigger"\n'
         '  increment: "1.14.0 -> 1.15.0"\n'
         '  disposition: HELD\n'
         f'  authority: "Chairman, {RULING}, ruling 8"\n'
         '  reason_verbatim: "PBC lifecycle reconciliation is being completed before downstream regeneration, and independent regeneration-readiness blockers remain."\n'
         '  executed: "NO - no regeneration was run"\n')
    once('registry_version_note_1_14_0: >-\n',
         'registry_version_note_1_15_0_PROPOSED: >-\n'
         f'  1.14.0 -> 1.15.0-PROPOSED, 2026-10-01. {RULING}. PBC LIFECYCLE RECONCILIATION ONLY,\n'
         '  ADDITIVE: every existing path_b_consequences line is carried byte-identically and lifecycle\n'
         '  fields are appended using field names and tokens already present in this registry. PBC-1\n'
         '  status RESOLVED_BY_RETIREMENT (Q10); PBC-2 status RESOLVED (TIMELINE_REGISTRY v1.1.0 S18);\n'
         '  PBC-3 note only - REMAINS UNRESOLVED, no assignment made, status not set because no\n'
         '  precedent selects between existing unresolved tokens; PBC-4 status RESOLVED (Executive Ruling\n'
         '  Q11); PBC-5 unchanged. NO beat entry, segment_authority field, intensity value or other\n'
         '  record is changed. Regeneration trigger for this increment HELD by Chairman ruling 8 (see\n'
         '  regeneration_trigger). Derived from ratified v1.14.0 (sha256 ' + SRC_SHA[:16] + '..., commit\n'
         '  096d127). No TIMELINE successor.\n'
         'registry_version_note_1_14_0: >-\n')
    t = ('# ============================================================================\n'
         '# STATUS: PROPOSED — AWAITING CHAIRMAN RATIFICATION\n'
         '# EPR-001 v1.15.0-PROPOSED. v1.14.0 (EMOTIONAL_PROGRESSION_REGISTRY.yaml) is\n'
         '# unchanged and remains the RATIFIED registry until the Chairman rules.\n'
         '# ============================================================================\n' + t)
    open(OUT, 'w', encoding='utf-8').write(t)
    print(hashlib.sha256(t.encode()).hexdigest(), os.path.basename(OUT))


if __name__ == '__main__':
    main()
