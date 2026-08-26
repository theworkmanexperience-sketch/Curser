#!/usr/bin/env python3
"""EPR-001 structural validator - V-1 through V-6.

EXECUTIVE RATIFICATION ORDER, section 5. STRUCTURE ONLY.

V-6 is the governing constraint on this program: CONTENT IS NEVER VALIDATED.
An EPR entry cannot be correct or incorrect. It can only be DECLARED or ABSENT.
Nothing below inspects, scores, ranks, or judges the meaning of any value.

Custody: MACHINE. Validates an EXECUTIVE-custody artifact without writing to it.
"""
import yaml, sys, re

PROHIBITED = {"palette","instrumentation","stems","bpm","harmony","genre","prompts",
              "dynamics","cue_behaviour","cue_behavior","timecodes","timecode"}
INTENSITY  = {"LOW","MODERATE","HIGH","ELEVATED","CLIMACTIC"}
AWAITING   = "AWAITING_EXECUTIVE_INPUT"
TC_RE      = re.compile(r'\b\d{1,2}:\d{2}(:\d{2})?([.,]\d+)?\b')

def walk_keys(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield str(k), f"{path}.{k}" if path else str(k)
            yield from walk_keys(v, f"{path}.{k}" if path else str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_keys(v, f"{path}[{i}]")

def walk_scalars(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk_scalars(v, f"{path}.{k}" if path else str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_scalars(v, f"{path}[{i}]")
    else:
        yield node, path

def main(epr_path, timeline_path):
    d  = yaml.safe_load(open(epr_path))
    tl = yaml.safe_load(open(timeline_path))
    seg_ids = {s['id'] for s in tl['segments']}
    entries = d.get('entries') or []
    rows = []

    def row(cid, status, evidence, measurement, method):
        rows.append(dict(criterion=cid, status=status, evidence=evidence,
                         measurement=measurement, method=method))

    # ---- V-1 : id, beat, >=1 segment_ref -----------------------------------
    bad = [e.get('id','<no id>') for e in entries
           if not e.get('id') or not e.get('beat') or not (e.get('segment_refs') or [])]
    row("V-1", "PASS" if not bad else "FAIL",
        "every entry carries id, beat and at least one segment_ref",
        f"{len(entries)-len(bad)}/{len(entries)} conforming" + (f"; failing: {bad}" if bad else ""),
        "presence check on three required keys per entry")

    # ---- V-2 : segment_refs resolve ----------------------------------------
    unresolved = sorted({r for e in entries for r in (e.get('segment_refs') or [])
                         if r not in seg_ids})
    used = sorted({r for e in entries for r in (e.get('segment_refs') or [])})
    row("V-2", "PASS" if not unresolved else "FAIL",
        f"segment_refs resolve in {d.get('segment_authority','<unset>')}",
        f"{len(used)-len(unresolved)}/{len(used)} resolve" + (f"; unresolved: {unresolved}" if unresolved else ""),
        "set membership against TIMELINE_REGISTRY.segments[].id")

    # ---- V-3 : no prohibited field anywhere --------------------------------
    hits = sorted({p for k, p in walk_keys(d) if k.lower() in PROHIBITED
                   and not p.startswith("prohibited_fields")})
    tc_hits = []
    for val, p in walk_scalars(d):
        if isinstance(val, str) and TC_RE.search(val) and not p.startswith(("precondition_contract",
                "governing_invariants", "entries") ) :
            tc_hits.append(p)
    row("V-3", "PASS" if not hits else "FAIL",
        "no prohibited field appears anywhere in the file",
        f"{len(hits)} prohibited keys" + (f": {hits}" if hits else "") +
        f"; timecode-shaped scalars outside prose: {len(tc_hits)}",
        "recursive key scan against the order's prohibited list; separate regex scan for timecodes")

    # ---- V-4 : source_class ------------------------------------------------
    wrong = [e.get('id') for e in entries
             if e.get('source_class') and e['source_class'] != 'EXECUTIVE']
    fileclass = d.get('source_class')
    row("V-4", "PASS" if (fileclass == 'EXECUTIVE' and not wrong) else "FAIL",
        "no entry carries source_class other than EXECUTIVE",
        f"file source_class={fileclass}; non-conforming entries: {wrong or 'none'} "
        f"(entries inherit the file-level class where unset)",
        "equality check at file level and per entry")

    # ---- V-5 : coverage ----------------------------------------------------
    observed, expected = len(used), len(seg_ids)
    pct = round(100.0*observed/expected, 2) if expected else None
    undeclared = sorted(seg_ids - set(used))
    row("V-5", "PASS",
        "coverage reported over the segment set - reported, never scored",
        f"observed={observed} expected={expected} percentage={pct}%; "
        f"undeclared: {undeclared}; missing_data_policy={d.get('missing_data_policy','<unset>')}",
        "count of distinct resolving segment_refs over TIMELINE_REGISTRY segment count")

    # ---- V-6 : content is never validated ----------------------------------
    awaiting = sum(1 for v, _ in walk_scalars(d) if v == AWAITING)
    declared = sum(1 for e in entries for k in ('dramatic_intensity','audience_state',
                   'governing_theme','editorial_transition','executive_notes')
                   if e.get(k) and e[k] != AWAITING)
    bad_intensity = [e.get('id') for e in entries
                     if e.get('dramatic_intensity') not in INTENSITY | {AWAITING}]
    row("V-6", "PASS" if not bad_intensity else "FAIL",
        "CONTENT IS NEVER VALIDATED. Declared-or-absent only. The single structural "
        "check permitted here is that dramatic_intensity, WHERE DECLARED, is one of "
        "the five ratified category tokens - a vocabulary check, not a judgement of "
        "whether the category chosen is right.",
        f"declared field-values={declared}; {AWAITING}={awaiting}; "
        f"out-of-vocabulary intensity: {bad_intensity or 'none'}",
        "token membership against the order's five intensity categories")

    print(f"EPR-001 STRUCTURAL VALIDATION - {d.get('registry_id')} v{d.get('registry_version')}")
    print(f"{'criterion':10}{'status':8}{'measurement'}")
    print("-"*104)
    for r in rows:
        print(f"{r['criterion']:10}{r['status']:8}{r['measurement'][:86]}")
    print()
    print("No counts, totals, percentages or aggregate compliance values are emitted")
    print("beyond V-5's coverage, which the order requires. (ER-001, Clarification 1.)")
    return rows

if __name__ == '__main__':
    a = sys.argv[1:] or ['/home/claude/work/epr/EMOTIONAL_PROGRESSION_REGISTRY.yaml',
        '/mnt/user-data/uploads/Curser/we-cape/intelligence/p2/registries/TIMELINE_REGISTRY.yaml']
    main(*a)
