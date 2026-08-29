#!/usr/bin/env python3
"""produce_video_obs.py — ECR-GEN-002 · B-3

Producer for the visual observation array (`video_obs_2fps.npy`), the input
`die_v_observables.py` needs and which had no producer anywhere in the
repository or on the work volume.

STATUS OF THIS PRODUCER — read before using its output
------------------------------------------------------
This script produces a NEW, SPECIFIED array.  It does **not** reproduce the
legacy 08-22 `video_obs_2fps.npy` and does not claim to.

The legacy array carries nine unlabelled float32 columns and was written by a
script that was never saved (the work volume's own `STATUS.txt` records the run;
no `.py` survives anywhere on it).  Conformance testing against the legacy array
recovered the semantics of six columns exactly enough to name them, and could
not recover three:

    col 0  mean R                    RECOVERED  (agrees to ~0.02 of 255)
    col 1  mean G                    RECOVERED  (~0.02)
    col 2  mean B                    RECOVERED  (~0.08)
    col 3  mean luma, Rec.601        RECOVERED  (~0.03)
    col 4  -                         NOT RECOVERED
    col 5  temporal difference       PARTIAL - zero on the first sample, but no
                                     tested formulation reproduces the values
    col 6  -                         NOT RECOVERED
    col 7  mean luma, top row band   RECOVERED  (~0.06)
    col 8  mean luma, bottom band    RECOVERED  (~0.03)

Even the recovered columns do not match bitwise: no decode path tested here
reproduces the legacy pixel values exactly, and no native frame in the proxy
carries the legacy array's first-sample mean.  Recovering the remaining columns
would require inferring an unrecorded specification from its own output, which
the governing constraints prohibit.  The condition is therefore reported, not
resolved.

CONSEQUENCE, stated so it is not discovered later: every value derived from the
legacy array — the DIE-V cut threshold, the night-luma in/out thresholds, the
motion terciles, and the visual event set built on them — rests on an
observable this producer does not reproduce.  Adopting this producer changes the
observational basis and obliges those values to be re-derived.  Re-derivation is
a regeneration and is NOT authorised by ECR-GEN-002.

SPECIFICATION of what this script does produce
----------------------------------------------
  decode      ffmpeg -i <media> -vf fps=<grid_fps> -pix_fmt rgb24 -f rawvideo -
              Frame geometry is read from the media by ffprobe, never assumed.
  sampling    `grid_fps` frames per second, uniform, from t=0
  dtype       float32
  shape       (n_samples, 9)

  column  name                        definition
  ------  --------------------------  ------------------------------------------
    0     mean_r                      mean of the R plane, 0-255
    1     mean_g                      mean of the G plane
    2     mean_b                      mean of the B plane
    3     mean_luma                   mean of 0.299R + 0.587G + 0.114B
    4     std_luma                    population std of that luma plane
    5     mean_abs_frame_diff_luma    mean |luma(t) - luma(t-1)|; 0.0 at t=0
    6     mean_luma_band_middle       mean luma over the middle horizontal third
    7     mean_luma_band_top          mean luma over the top horizontal third
    8     mean_luma_band_bottom       mean luma over the bottom horizontal third

Columns 4, 5 and 6 are DECLARED here by engineering, not recovered from the
legacy array.  Column order 6/7/8 follows the legacy array's recovered ordering
(top at index 7, bottom at index 8) so a consumer written against the legacy
layout reads the same two bands from the same places.

The schema is written beside the array as `<out>.schema.json` so no consumer has
to rediscover it, which is the failure that produced this script.

USAGE
    produce_video_obs.py <media> <out.npy> [--grid-fps 2] [--compare <legacy.npy>]

Exit codes
    0  produced
    2  STOP - ffprobe/ffmpeg failed, or the decoded byte count is not a whole
       number of frames
"""
import argparse
import json
import subprocess
import sys

import numpy as np

GRID_FPS = 2
DTYPE = np.float32
COLUMNS = [
    ('mean_r', 'mean of the R plane, 0-255'),
    ('mean_g', 'mean of the G plane, 0-255'),
    ('mean_b', 'mean of the B plane, 0-255'),
    ('mean_luma', 'mean of 0.299R + 0.587G + 0.114B'),
    ('std_luma', 'population standard deviation of the luma plane'),
    ('mean_abs_frame_diff_luma', 'mean |luma(t) - luma(t-1)|; 0.0 at the first sample'),
    ('mean_luma_band_middle', 'mean luma over the middle horizontal third'),
    ('mean_luma_band_top', 'mean luma over the top horizontal third'),
    ('mean_luma_band_bottom', 'mean luma over the bottom horizontal third'),
]


def probe_geometry(media):
    """Read frame width/height from the media. Never assume a proxy geometry."""
    proc = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
         '-show_entries', 'stream=width,height', '-of', 'json', media],
        capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError('ffprobe failed (%d): %s'
                           % (proc.returncode, proc.stderr.decode('utf-8', 'replace')[:400]))
    streams = json.loads(proc.stdout).get('streams') or []
    if not streams:
        raise RuntimeError('no video stream found in %s' % media)
    w, h = int(streams[0]['width']), int(streams[0]['height'])
    if w <= 0 or h <= 0:
        raise RuntimeError('degenerate frame geometry %dx%d' % (w, h))
    return w, h


def decode_frames(media, grid_fps, width, height):
    proc = subprocess.run(
        ['ffmpeg', '-v', 'error', '-i', media,
         '-vf', 'fps=%s' % grid_fps, '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'],
        capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError('ffmpeg failed (%d): %s'
                           % (proc.returncode, proc.stderr.decode('utf-8', 'replace')[:400]))
    per_frame = width * height * 3
    if not proc.stdout:
        raise RuntimeError('ffmpeg produced no frames')
    if len(proc.stdout) % per_frame:
        raise RuntimeError('decoded %d bytes, not a whole number of %dx%d RGB frames'
                           % (len(proc.stdout), width, height))
    return (np.frombuffer(proc.stdout, dtype=np.uint8)
              .reshape(-1, height, width, 3))


def observe(frames):
    n, h, _w, _c = frames.shape
    out = np.zeros((n, len(COLUMNS)), dtype=DTYPE)
    a, b = h // 3, (2 * h) // 3
    prev = None
    for i in range(n):
        f = frames[i].astype(np.float32)
        luma = 0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2]
        out[i, 0] = f[..., 0].mean()
        out[i, 1] = f[..., 1].mean()
        out[i, 2] = f[..., 2].mean()
        out[i, 3] = luma.mean()
        out[i, 4] = luma.std()
        out[i, 5] = 0.0 if prev is None else np.abs(luma - prev).mean()
        out[i, 6] = luma[a:b].mean()
        out[i, 7] = luma[:a].mean()
        out[i, 8] = luma[b:].mean()
        prev = luma
    return out


def main():
    ap = argparse.ArgumentParser(description='Produce the visual observation array.')
    ap.add_argument('media')
    ap.add_argument('out')
    ap.add_argument('--grid-fps', type=float, default=GRID_FPS)
    ap.add_argument('--compare', default=None,
                    help='legacy .npy to report agreement against; never a pass/fail gate, '
                         'because the legacy array has no recorded specification')
    a = ap.parse_args()

    try:
        w, h = probe_geometry(a.media)
        frames = decode_frames(a.media, a.grid_fps, w, h)
        arr = observe(frames)
    except Exception as exc:                       # noqa: BLE001 - reported, not absorbed
        print('STOP: %s' % exc, file=sys.stderr)
        return 2

    np.save(a.out, arr)
    schema = dict(
        produced_by='produce_video_obs.py',
        media=a.media, grid_fps=a.grid_fps, frame_width=w, frame_height=h,
        dtype='float32', shape=list(arr.shape),
        covered_s=round(len(arr) / float(a.grid_fps), 3),
        columns=[dict(index=i, name=nm, definition=df) for i, (nm, df) in enumerate(COLUMNS)],
        reproduces_legacy_video_obs_2fps=False,
        note=('Columns 4, 5 and 6 are declared by engineering. The legacy 08-22 array '
              'has no recorded specification and is not reproduced by this script.'))
    open(a.out + '.schema.json', 'w').write(json.dumps(schema, indent=1) + '\n')
    print('produced %s  shape=%s dtype=%s covered_s=%.3f  geometry=%dx%d'
          % (a.out, arr.shape, arr.dtype, len(arr) / float(a.grid_fps), w, h))
    print('schema written to %s.schema.json' % a.out)

    if a.compare:
        ref = np.load(a.compare)
        print('\ncomparison against %s (REPORTED, NOT A GATE)' % a.compare)
        print('  shape produced=%s legacy=%s' % (arr.shape, ref.shape))
        m = min(len(arr), len(ref))
        for i, (nm, _d) in enumerate(COLUMNS):
            if i >= ref.shape[1]:
                break
            d = np.abs(arr[:m, i] - ref[:m, i])
            print('  col %d %-26s max_abs=%9.4f  mean_abs=%9.4f'
                  % (i, nm, float(d.max()), float(d.mean())))
    return 0


if __name__ == '__main__':
    sys.exit(main())
