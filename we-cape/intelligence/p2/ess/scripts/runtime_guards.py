#!/usr/bin/env python3
"""runtime_guards.py — ECR-GEN-002 · B-9

Fail-fast execution validation for the artifact generator.

The condition this closes was reported as R-4 in ECR-GEN-001 and restated as
B-9 in the Engineering Readiness Review: once the generator was parameterised,
nothing checked that its inputs described the same production.  A context for
one lineage paired with observations from another produced seven well-formed,
hash-stamped artifacts describing the wrong film, with no exception, no exit
code and no log line — *wrong film, right format, no error*.

Every check here runs BEFORE the first byte of the first artifact is written.
A failure raises `GuardFailure`, which the generator turns into exit 2.  No
check repairs, defaults, or downgrades anything: a guard either passes or the
run stops.

CHECK REGISTER
  G-01  production_id agreement          context vs observations
  G-02  lineage agreement                context vs observations
  G-03  source hash agreement            context vs observations
  G-04  runtime contract                 declared runtime vs resolved spine end
  G-05  ETC binding verdict              resolver verdict is VALIDATED, or the
                                         context explicitly declares it may be
                                         absent for this lineage
  G-06  ETC census agreement             ETC spine census vs resolved census
  G-07  out-of-range disposition         resolved count vs declared expectation
  G-08  segment registry                 ordered, non-overlapping, in range
  G-09  cue registry                     ordered, non-overlapping, in range
  G-10  derived-set provenance           camera runs vs resolved spine census
  G-11  observation bundle completeness  every class the generator reads exists
  G-12  canonical regeneration scope    ERO-001 §2 - one timeline, one Conductor
                                        Score, one Narrative Progression, no
                                        episode-specific emotional progressions
  G-13  governed narrative boundaries   ERO-001 §1 - the S12/S13 transitional
                                        overlap is PRESERVED, EPR-05 holds through
                                        it, EPR-06 begins at its completion, and no
                                        interpolated or intermediate state exists
"""

OBSERVATION_CLASSES = (
    'segments', 'cues', 'visual_events', 'not_observed', 'delta_ledger',
    'audio_sources', 'progressions', 'energy', 'voice_over', 'offset_model',
    'anchors', 'die_v',
)

TOL_S = 0.0005


class GuardFailure(Exception):
    """Raised when a guard fails. Carries the failing check id and the evidence."""

    def __init__(self, check, detail):
        self.check = check
        self.detail = detail
        super().__init__('%s: %s' % (check, detail))


def _fail(check, detail):
    raise GuardFailure(check, detail)


def run_guards(ctx, obs, timeline, cams, verbose=True):
    """Run every guard. Returns the passed-check register; raises on the first failure."""
    passed = []

    def ok(check, detail):
        passed.append((check, detail))
        if verbose:
            print('  guard %-6s PASS  %s' % (check, detail))

    meas = ctx.get('measured') or {}
    res = meas.get('resolver') or {}
    val = (timeline or {}).get('validation') or {}
    cen = (timeline or {}).get('census') or {}

    # -- G-01 production identity -------------------------------------------
    c_pid, o_pid = ctx.get('production_id'), obs.get('production_id')
    if o_pid is None:
        _fail('G-01', 'the observation bundle declares no production_id; it cannot be '
                      'shown to describe the same production as the context')
    if c_pid != o_pid:
        _fail('G-01', 'context production_id %r != observations production_id %r'
              % (c_pid, o_pid))
    ok('G-01', 'production_id %s' % c_pid)

    # -- G-02 lineage --------------------------------------------------------
    c_lin, o_lin = ctx.get('lineage'), obs.get('lineage')
    if o_lin is None:
        _fail('G-02', 'the observation bundle declares no lineage')
    if c_lin != o_lin:
        _fail('G-02', 'context lineage %r != observations lineage %r' % (c_lin, o_lin))
    ok('G-02', 'lineage %s' % c_lin)

    # -- G-03 source hashes --------------------------------------------------
    c_sha = ctx.get('sha') or {}
    o_sha = obs.get('source_sha')
    if o_sha is None:
        _fail('G-03', 'the observation bundle declares no source_sha; the observations '
                      'cannot be tied to the sources the context pins')
    for k in sorted(set(c_sha) | set(o_sha)):
        a, b = c_sha.get(k), o_sha.get(k)
        if a != b:
            _fail('G-03', 'source %s: context sha %r != observations sha %r' % (k, a, b))
    ok('G-03', '%d source hashes agree' % len(o_sha))

    # -- G-04 runtime contract ----------------------------------------------
    lock = ctx.get('runtime_s')
    end = val.get('spine_end_s')
    if lock is None:
        _fail('G-04', 'context declares no runtime_s')
    if end is None:
        _fail('G-04', 'the resolved timeline carries no spine_end_s; the runtime contract '
                      'cannot be checked against the picture')
    if abs(float(lock) - float(end)) > TOL_S:
        _fail('G-04', 'declared runtime_s %s != resolved spine end %s (tolerance %s s)'
              % (lock, end, TOL_S))
    ok('G-04', 'runtime %s s == resolved spine end' % lock)

    # -- G-05 ETC binding verdict -------------------------------------------
    verdict = val.get('etc_validation')
    if verdict == 'VALIDATED':
        ok('G-05', 'ETC binding VALIDATED, %s' % val.get('spine_comparison'))
    elif verdict == 'NOT_VALIDATED':
        if not ctx.get('etc_absence_declared'):
            _fail('G-05', 'the timeline was resolved without an Editorial Timing Contract '
                          '(etc_validation=NOT_VALIDATED) and the context does not declare '
                          'etc_absence_declared. An unvalidated lineage may not be generated '
                          'by default.')
        ok('G-05', 'ETC absent, and the context declares the absence explicitly')
    else:
        _fail('G-05', 'ETC binding verdict is %r; only VALIDATED or an explicitly declared '
                      'NOT_VALIDATED may proceed' % verdict)

    # -- G-06 ETC census -----------------------------------------------------
    if verdict == 'VALIDATED':
        a, b = meas.get('etc_spine_n'), res.get('spine_excl_transitions')
        if a != b:
            _fail('G-06', 'ETC spine census %r != resolved non-transition census %r' % (a, b))
        ok('G-06', 'ETC spine census %s == resolved census' % a)
    else:
        ok('G-06', 'skipped - no ETC to reconcile against (G-05 declared)')

    # -- G-07 out-of-range disposition --------------------------------------
    got = cen.get('out_of_range_n')
    dec = meas.get('expected_out_of_range_n')
    if got is None:
        _fail('G-07', 'the resolved timeline carries no out_of_range_n census')
    if dec is None:
        _fail('G-07', 'the context declares no expected_out_of_range_n; %d out-of-range '
                      'elements were resolved and have no disposition' % got)
    if got != dec:
        _fail('G-07', 'resolved out-of-range count %d != declared expectation %d' % (got, dec))
    ok('G-07', 'out-of-range count %d matches the declared disposition' % got)

    # -- G-08 segment registry: shape, range, ordering -----------------------
    segs = obs.get('segments') or []
    if not segs:
        _fail('G-08', 'the observation bundle carries no segments')
    prev_id = prev_end = None
    overlaps = []
    for s in segs:
        sid, a, b = s[0], float(s[1]), float(s[2])
        if b < a:
            _fail('G-08', 'segment %s ends (%s) before it starts (%s)' % (sid, b, a))
        if a < -TOL_S or b > float(lock) + TOL_S:
            _fail('G-08', 'segment %s span %s-%s falls outside the %s s runtime'
                  % (sid, a, b, lock))
        if prev_end is not None and a + TOL_S < prev_end:
            overlaps.append(dict(previous=prev_id, segment=sid,
                                 overlap_s=round(prev_end - a, 3)))
        prev_end = b
        prev_id = sid
    ok('G-08', '%d segments in range and in start order' % len(segs))

    # -- G-08b segment overlap: declared, or STOP ----------------------------
    declared = ctx.get('declared_segment_overlaps') or []
    dkey = {(d.get('previous'), d.get('segment'), round(float(d.get('overlap_s')), 3))
            for d in declared}
    fkey = {(o['previous'], o['segment'], o['overlap_s']) for o in overlaps}
    undeclared = fkey - dkey
    if undeclared:
        _fail('G-08b', 'segment overlap(s) present and not declared in the context: %s. '
                       'An overlap means two segments claim the same runtime; the platform '
                       'will not choose between them.'
              % '; '.join('%s/%s by %.3f s' % u for u in sorted(undeclared)))
    stale = dkey - fkey
    if stale:
        _fail('G-08b', 'the context declares overlap(s) the observations do not contain: %s. '
                       'A declaration that no longer matches the data is not evidence.'
              % '; '.join('%s/%s by %.3f s' % u for u in sorted(stale)))
    if overlaps:
        ok('G-08b', '%d declared overlap(s): %s'
           % (len(overlaps), '; '.join('%s/%s %.3f s'
                                       % (o['previous'], o['segment'], o['overlap_s'])
                                       for o in overlaps)))
    else:
        ok('G-08b', 'no segment overlaps')

    # -- G-09 cue registry ---------------------------------------------------
    cues = obs.get('cues') or []
    if not cues:
        _fail('G-09', 'the observation bundle carries no cues')
    prev_end = None
    for c in cues:
        cid, a, b = c[0], float(c[1]), float(c[2])
        if b < a:
            _fail('G-09', 'cue %s ends (%s) before it starts (%s)' % (cid, b, a))
        if a < -TOL_S or b > float(lock) + TOL_S:
            _fail('G-09', 'cue %s span %s-%s falls outside the %s s runtime' % (cid, a, b, lock))
        if prev_end is not None and a + TOL_S < prev_end:
            _fail('G-09', 'cue %s starts at %s, before the previous cue ended at %s'
                  % (cid, a, prev_end))
        prev_end = b
    ok('G-09', '%d cues ordered, non-overlapping, within runtime' % len(cues))

    # -- G-10 derived-set provenance ----------------------------------------
    n_cams, n_spine = len(cams or []), res.get('spine_excl_transitions')
    if n_spine is None:
        _fail('G-10', 'the context carries no resolved spine census to check the derived '
                      'camera runs against')
    if n_cams != n_spine:
        _fail('G-10', 'camera_runs carries %d runs but the resolved timeline has %d '
                      'non-transition spine elements; the derived set was not built from '
                      'this timeline' % (n_cams, n_spine))
    ok('G-10', 'camera runs %d == resolved spine census' % n_cams)

    # -- G-12 canonical regeneration scope (ERO-001 §2) ----------------------
    scope = ctx.get('regeneration_scope') or {}
    mode = scope.get('mode')
    if mode != 'CANONICAL_EDITORIAL_TIMELINE':
        _fail('G-12', 'context declares regeneration_scope.mode=%r; ERO-001 §2 requires '
                      'CANONICAL_EDITORIAL_TIMELINE. A run whose scope is undeclared or '
                      'different is not the run the Order authorises.' % mode)
    for key in ('episode_progressions', 'episodes', 'episode_emotional_progressions',
                'per_episode_progressions'):
        if key in obs:
            _fail('G-12', 'the observation bundle carries %r. ERO-001 §2 prohibits '
                          'independent episode-specific emotional progressions; episodes '
                          'derive their scoring exclusively through governed timeline '
                          'slicing.' % key)
    progs = obs.get('progressions') or []
    if not progs:
        _fail('G-12', 'the observation bundle carries no narrative progression')
    prev_end = None
    for p in progs:
        pid, a, b = p[0], float(p[2]), float(p[3])
        if b < a:
            _fail('G-12', 'progression %s ends (%s) before it starts (%s)' % (pid, b, a))
        if b > float(lock) + TOL_S:
            _fail('G-12', 'progression %s ends at %s, beyond the %s s canonical timeline'
                  % (pid, b, lock))
        if prev_end is not None and a + TOL_S < prev_end:
            _fail('G-12', 'progressions %s overlaps its predecessor; ERO-001 §2 requires '
                          'ONE authoritative narrative progression, which cannot contain '
                          'competing spans' % pid)
        prev_end = b
    slices = ctx.get('episode_slices') or []
    for s in slices:
        a, b = float(s.get('start_s')), float(s.get('end_s'))
        if a < -TOL_S or b > float(lock) + TOL_S:
            _fail('G-12', 'episode slice %r spans %s-%s, outside the canonical timeline'
                  % (s.get('id'), a, b))
        for banned in ('progressions', 'emotional_progression', 'epr', 'beats'):
            if banned in s:
                _fail('G-12', 'episode slice %r carries its own %r. Slices derive from the '
                              'canonical timeline; they do not author scoring.'
                      % (s.get('id'), banned))
    ok('G-12', 'canonical timeline scope; %d progression(s), %d derived slice(s)'
       % (len(progs), len(slices)))

    # -- G-13 governed narrative boundaries (ERO-001 §1) ---------------------
    gnb = ctx.get('governed_narrative_boundaries') or []
    seg_by_id = {s[0]: (float(s[1]), float(s[2])) for s in segs}
    declared_pairs = {(d.get('previous'), d.get('segment'))
                      for d in (ctx.get('declared_segment_overlaps') or [])}
    for b in gnb:
        bid = b.get('id')
        prev, seg = b.get('previous'), b.get('segment')
        if (prev, seg) not in declared_pairs:
            _fail('G-13', '%s governs the %s/%s boundary but no matching declared overlap '
                          'exists' % (bid, prev, seg))
        if prev not in seg_by_id or seg not in seg_by_id:
            _fail('G-13', '%s names segment(s) the observation bundle does not carry '
                          '(%s, %s)' % (bid, prev, seg))
        p_start, p_end = seg_by_id[prev]
        s_start, s_end = seg_by_id[seg]
        # PRESERVATION. This is the clause that matters most: an Executive
        # determination can be erased by "fixing" the data it governs.
        if not (s_start + TOL_S < p_end):
            _fail('G-13', '%s governs a transitional overlap between %s and %s, but the '
                          'observation bundle no longer contains one (%s ends %.3f, %s '
                          'starts %.3f). ERO-001 §1 requires engineering to PRESERVE this '
                          'overlap as a governed narrative boundary.'
                  % (bid, prev, seg, prev, p_end, seg, s_start))
        for key, got, want in (('span_start_s', b.get('span_start_s'), s_start),
                               ('span_end_s', b.get('span_end_s'), p_end),
                               ('authority_beat_through_s',
                                b.get('authority_beat_through_s'), p_end),
                               ('successor_authority_begins_s',
                                b.get('successor_authority_begins_s'), p_end)):
            if got is None or abs(float(got) - want) > TOL_S:
                _fail('G-13', '%s %s is %r; the segment registry gives %.3f. The governed '
                              'boundary no longer describes the data it governs.'
                      % (bid, key, got, want))
        if abs(float(b.get('overlap_s', -1)) - (p_end - s_start)) > TOL_S:
            _fail('G-13', '%s overlap_s %r does not equal the registry span %.3f'
                  % (bid, b.get('overlap_s'), p_end - s_start))
        if not b.get('retained'):
            _fail('G-13', '%s is not marked retained; ERO-001 §1 retains the overlap' % bid)
        if b.get('interpolation') != 'PROHIBITED' or b.get('intermediate_state') != 'PROHIBITED':
            _fail('G-13', '%s must carry interpolation=PROHIBITED and '
                          'intermediate_state=PROHIBITED; ERO-001 §1 authorises no '
                          'mathematical interpolation and no intermediate emotional state'
                  % bid)
        # No third segment may reach into the governed span - two beats already
        # contend for it and a third claimant would make the boundary undecidable.
        for sid, (a, c) in seg_by_id.items():
            if sid in (prev, seg):
                continue
            if a < p_end - TOL_S and c > s_start + TOL_S:
                _fail('G-13', '%s: segment %s (%.3f-%.3f) also intersects the governed span '
                              '%.3f-%.3f' % (bid, sid, a, c, s_start, p_end))
    if gnb:
        ok('G-13', '%d governed narrative boundary/boundaries preserved: %s'
           % (len(gnb), '; '.join('%s %s/%s %.3f-%.3f s, %s through %.3f, %s from %.3f'
                                  % (b['id'], b['previous'], b['segment'],
                                     b['span_start_s'], b['span_end_s'],
                                     b['authority_beat_through_span'],
                                     b['authority_beat_through_s'],
                                     b['successor_beat'],
                                     b['successor_authority_begins_s']) for b in gnb)))
    else:
        ok('G-13', 'no governed narrative boundaries declared')

    # -- G-11 observation completeness --------------------------------------
    missing = [k for k in OBSERVATION_CLASSES if k not in obs]
    if missing:
        _fail('G-11', 'the observation bundle is missing %d class(es): %s'
              % (len(missing), ', '.join(missing)))
    ok('G-11', 'all %d observation classes present' % len(OBSERVATION_CLASSES))

    return passed
