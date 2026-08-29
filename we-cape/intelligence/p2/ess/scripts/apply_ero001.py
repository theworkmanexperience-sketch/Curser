#!/usr/bin/env python3
"""apply_ero001.py — transcribe EXECUTIVE RESOLUTION ORDER ERO-001 into the context.

This script TRANSCRIBES two Executive determinations into engineering-readable
form so the runtime guards can enforce them. It authors nothing. Every value it
writes is either quoted from the Order or derived from the segment registry the
Order refers to, and the derivation is stated beside it.

ERO-001 §3 permits implementation "solely for purposes of generator conformance"
and prohibits altering Executive narrative declarations, emotional progression
values, and ratified themes. Accordingly:

  * EMOTIONAL_PROGRESSION_REGISTRY.yaml is NOT opened for writing by this script
    or by anything downstream of it.
  * The determination is recorded in the CONTEXT, which is an engineering input,
    and enforced by guards G-12 and G-13.
  * It is NOT written into the observation bundle's `progressions`, which are
    DOCUMENTARY progressions (P1..P5). Writing an emotional boundary into that
    axis would breach Invariant A - documentary intent shall never prescribe
    musical implementation, and observational measurement shall never prescribe
    documentary intent. The two axes stay separate.

The context is not the durable home for an Executive determination. It is the
place a guard can read. Recording the determination somewhere with governance
standing is a separate act requiring separate authority, and is reported.
"""
import json
import sys

ERO_1 = ("The Executive determines that the six-second overlap between S12 and S13 "
         "constitutes an intentional narrative transition rather than a segmentation "
         "error. Transitional overlap is retained. EPR-05 (\"Deepening\") maintains "
         "primary narrative and scoring authority through the visual conclusion of "
         "S12. EPR-06 (\"Celebration\") begins at the editorial completion of that "
         "transition. No mathematical interpolation or intermediate emotional state "
         "is authorized. Engineering shall preserve this overlap as a governed "
         "narrative boundary.")

ERO_2 = ("The Executive determines that regeneration shall target a single Canonical "
         "Editorial Timeline representing the governed 08-24 production lineage. One "
         "authoritative Conductor Score shall be generated. One authoritative "
         "Narrative Progression shall govern the production. Public distribution "
         "episodes derive their scoring exclusively through governed timeline "
         "slicing. Independent episode-specific emotional progressions shall not be "
         "generated. This determination does not modify the previously ratified "
         "Path B public distribution architecture.")


def main():
    ctx_path, obs_path = sys.argv[1], sys.argv[2]
    ctx = json.load(open(ctx_path))
    obs = json.load(open(obs_path))

    segs = {s[0]: (float(s[1]), float(s[2])) for s in obs['segments']}

    boundaries = []
    for d in ctx.get('declared_segment_overlaps') or []:
        prev, seg = d['previous'], d['segment']
        if prev not in segs or seg not in segs:
            print('STOP: declared overlap names a segment the bundle does not carry: %s/%s'
                  % (prev, seg), file=sys.stderr)
            return 2
        p_start, p_end = segs[prev]
        s_start, s_end = segs[seg]
        span_start, span_end = s_start, p_end          # derived, not typed
        overlap = round(span_end - span_start, 3)
        if abs(overlap - float(d['overlap_s'])) > 0.0005:
            print('STOP: declared overlap_s %s does not equal the registry-derived '
                  'overlap %s for %s/%s' % (d['overlap_s'], overlap, prev, seg),
                  file=sys.stderr)
            return 2
        boundaries.append({
            'id': 'GNB-001',
            'authority': 'ERO-001 §1',
            'order_date': '2026-08-28',
            'kind': 'TRANSITIONAL_OVERLAP',
            'classification': 'INTENTIONAL_NARRATIVE_TRANSITION',
            'previous': prev,
            'segment': seg,
            'span_start_s': span_start,
            'span_end_s': span_end,
            'overlap_s': overlap,
            'retained': True,
            # "EPR-05 maintains primary narrative and scoring authority through the
            # visual conclusion of S12" -> S12's declared end, 3236.0.
            'authority_beat_through_span': 'EPR-05',
            'authority_beat_through_s': p_end,
            # "EPR-06 begins at the editorial completion of that transition" -> the
            # end of the transition span, which is the same instant.
            'successor_beat': 'EPR-06',
            'successor_authority_begins_s': span_end,
            'interpolation': 'PROHIBITED',
            'intermediate_state': 'PROHIBITED',
            'engineering_obligation': 'PRESERVE',
            'derivation': ('span_start = start of %s; span_end = end of %s; both read '
                           'from the segment registry. The two clauses of the Order - '
                           '"through the visual conclusion of %s" and "at the editorial '
                           'completion of that transition" - resolve to the same '
                           'instant, %.3f s, so the boundary is determinate.'
                           % (seg, prev, prev, span_end)),
            'executive_text': ERO_1,
        })

    ctx['regeneration_scope'] = {
        'mode': 'CANONICAL_EDITORIAL_TIMELINE',
        'authority': 'ERO-001 §2',
        'order_date': '2026-08-28',
        'conductor_scores_per_run': 1,
        'narrative_progressions_per_run': 1,
        'episode_specific_emotional_progressions': 'PROHIBITED',
        'episode_derivation': 'GOVERNED_TIMELINE_SLICING',
        'path_b_architecture': 'UNMODIFIED',
        'executive_text': ERO_2,
    }
    ctx['governed_narrative_boundaries'] = boundaries
    ctx['ero_001_transcription'] = {
        'transcribed_by': 'apply_ero001.py',
        'authors_nothing': True,
        'epr_registry_written': False,
        'note': ('Recorded in the context because that is where the runtime guards can '
                 'read it. The context is an engineering input and is not a governance '
                 'record; giving this determination durable governance standing is a '
                 'separate act requiring separate authority.'),
    }

    json.dump(ctx, open(ctx_path, 'w'), indent=1)
    print('ERO-001 transcribed into %s' % ctx_path)
    print('  regeneration_scope           : %s' % ctx['regeneration_scope']['mode'])
    for b in boundaries:
        print('  %s %s/%s  span %.3f-%.3f s (%.3f s)'
              % (b['id'], b['previous'], b['segment'],
                 b['span_start_s'], b['span_end_s'], b['overlap_s']))
        print('     authority %s through %.3f s; %s begins %.3f s; interpolation %s'
              % (b['authority_beat_through_span'], b['authority_beat_through_s'],
                 b['successor_beat'], b['successor_authority_begins_s'],
                 b['interpolation']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
