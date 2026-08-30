#!/usr/bin/env python3
"""
Editorial Timing Contract (ETC) extractor.

Authorized under EXECUTIVE AUTHORIZATION ED-001A section 2, as completion of an
existing architectural contract rather than a new platform capability: committed
components consume the ETC (fcpx_resolve.py, build_context.py, gen_artifacts*.py)
and no committed producer has ever existed.

CONTRACT (PDR-2026-08-20-ETC-001): the ETC is a machine-readable projection of a
picture-locked FCPXML. Its authority is hash lineage to that FCPXML. It is
DERIVED — regenerate on mismatch, never hand-edit.

ACCEPTANCE (ED-001A section 3, non-negotiable): this extractor may not be pointed
at any lineage until it reproduces the surviving 08-22 ETC BYTE-FOR-BYTE.
Byte equality is the only authorized acceptance criterion.

STRUCTURE, as derived from the surviving reference artifact:
  spine               depth-0 children of the FIRST <spine> element
  connected_elements  their emitted descendants, depth >= 1

  - `transition` is never emitted, at any depth. (This is the same exclusion the
    B-1 remediation put into fcpx_resolve.py: transitions are depth-0 children of
    the spine but are not spine elements for binding purposes.)
  - nested <spine> subtrees (secondary storylines) are NOT traversed. Their
    contents do not appear in the contract at any depth.
  - only timeline-bearing tags are emitted; decoration (conform-rate, timeMap,
    adjust-*, keyword, filter-*, marker, param, data, audio-channel-source) is
    neither emitted nor descended into.

DECLARED, NOT DERIVED: `source` and `sequence.declared_lock` are parameters.
The declared lock timecode does not appear anywhere in the FCPXML; it is a human
declaration reconciled against the parsed duration, and this tool will not
invent one. Absent a declared value the field is emitted as null.

stdlib only · read-only on its input · deterministic.
"""

import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET

# Tags that carry timeline position and therefore appear in the contract.
EMIT = {'asset-clip', 'clip', 'gap', 'title', 'audio', 'video'}

# Never emitted, never descended.
EXCLUDE = {'transition'}

# Traversed as a container in FCP, but its contents are outside the contract.
OPAQUE = {'spine'}

ROUND = 3


def parse_time(v):
    """FCPXML rational or integer seconds -> float, rounded to the contract's precision.

    Accepts '0s', '1s', '59028890/2400s'. Returns None for a missing attribute.
    Raises on anything else rather than guessing.
    """
    if v is None:
        return None
    if not v.endswith('s'):
        raise ValueError(f'unrecognised time value: {v!r}')
    body = v[:-1]
    if '/' in body:
        num, den = body.split('/', 1)
        return round(int(num) / int(den), ROUND)
    return round(float(body), ROUND)


def element(tag, name, lane, depth, parent, offset, duration, start):
    """One contract row. Key order is part of the artifact and is fixed here."""
    return {
        'tag': tag,
        'name': name,
        'lane': lane,
        'depth': depth,
        'parent': parent,
        'timeline_offset_s': parse_time(offset) if depth == 0 else None,
        'rel_offset_s': None if depth == 0 else parse_time(offset),
        'duration_s': parse_time(duration),
        'source_start_s': parse_time(start),
    }


def extract(fcpxml_path, source_declared=None, declared_lock=None):
    root = ET.parse(fcpxml_path).getroot()

    sequences = root.findall('.//sequence')
    if len(sequences) != 1:
        raise SystemExit(f'STOP: expected exactly 1 <sequence>, found {len(sequences)}. '
                         'A multi-sequence project is not a single picture lock.')
    seq = sequences[0]

    spines = root.findall('.//spine')
    if not spines:
        raise SystemExit('STOP: no <spine> element found.')
    spine = spines[0]

    spine_rows, connected_rows = [], []

    def descend(node, depth, parent_name):
        for child in node:
            if child.tag in EXCLUDE or child.tag in OPAQUE:
                continue
            if child.tag not in EMIT:
                continue
            row = element(child.tag, child.get('name', ''), child.get('lane'),
                          depth, parent_name, child.get('offset'),
                          child.get('duration'), child.get('start'))
            connected_rows.append(row)
            descend(child, depth + 1, child.get('name', ''))

    for child in spine:
        if child.tag in EXCLUDE or child.tag in OPAQUE:
            continue
        if child.tag not in EMIT:
            continue
        row = element(child.tag, child.get('name', ''), child.get('lane'),
                      0, 'SPINE', child.get('offset'),
                      child.get('duration'), child.get('start'))
        spine_rows.append(row)
        descend(child, 1, child.get('name', ''))

    with open(fcpxml_path, 'rb') as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()

    return {
        'source': source_declared if source_declared is not None else str(fcpxml_path),
        'source_sha256': sha,
        'sequence': {
            'duration_s': parse_time(seq.get('duration')),
            'format_ref': seq.get('format'),
            'declared_lock': declared_lock,
        },
        'spine': spine_rows,
        'connected_elements': connected_rows,
    }


def write(etc, out_path):
    """Serialisation is part of the artifact and is reproduced exactly:
    indent=1, ASCII-escaped, and NO trailing newline. The reference artifact ends
    at its closing brace; adding a newline is an 11-byte failure of the gate."""
    with open(out_path, 'w', encoding='utf-8') as fh:
        json.dump(etc, fh, indent=1, ensure_ascii=True)


def main():
    ap = argparse.ArgumentParser(description='Extract an Editorial Timing Contract from a picture-locked FCPXML.')
    ap.add_argument('fcpxml')
    ap.add_argument('out')
    ap.add_argument('--source', default=None,
                    help='the source path to record in the contract; defaults to the input path')
    ap.add_argument('--declared-lock', default=None,
                    help='the human-declared lock timecode. Not derivable from the FCPXML. '
                         'Omitted means null; this tool will not invent one.')
    ap.add_argument('--expect-sha256', default=None,
                    help='refuse to run unless the input FCPXML has this sha256')
    a = ap.parse_args()

    etc = extract(a.fcpxml, a.source, a.declared_lock)

    if a.expect_sha256 and etc['source_sha256'] != a.expect_sha256:
        print(f'STOP FAILED_SOURCE_IDENTITY\n  expected {a.expect_sha256}\n  measured {etc["source_sha256"]}',
              file=sys.stderr)
        sys.exit(2)

    write(etc, a.out)
    print(f'{a.out}  spine={len(etc["spine"])}  connected={len(etc["connected_elements"])}  '
          f'duration_s={etc["sequence"]["duration_s"]}  source_sha256={etc["source_sha256"][:16]}…')


if __name__ == '__main__':
    main()
