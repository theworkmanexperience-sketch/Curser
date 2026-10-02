#!/usr/bin/env python3
"""produce_audio_rms.py — ECR-GEN-002 · B-3

Producer for the audio RMS observation array (`audio_rms_0p25.npy`).

Until this script existed the array had no producer anywhere in the repository
or on the work volume, and `step0_offset.py` could not be run.  The recipe below
was recovered by conformance against the 08-22 fixture and reproduces it
exactly (max absolute error 0.000000 across all samples).

SPECIFICATION — stated so no future run has to rediscover it
------------------------------------------------------------
  decode      ffmpeg -i <media> -ac 1 -ar 16000 -f s16le -
              (mono, 16 kHz, signed 16-bit little-endian PCM)
  window      0.25 s == 4000 samples, non-overlapping, from t=0
  tail        a trailing partial window is DISCARDED, not zero-padded
  value       rms = sqrt( mean( (x / 32768.0)^2 ) )  over each window
  dtype       float32
  shape       (n_windows,)

The normalisation constant is 32768.0 (2**15), so the array is dimensionless and
bounded by 1.0 for non-clipping material.  No smoothing, windowing function,
pre-emphasis, or dynamic-range compression is applied: the array is an
observation, and any shaping would be an interpretation of it.

USAGE
    produce_audio_rms.py <media> <out.npy> [--window-s 0.25] [--rate 16000]
                         [--verify <reference.npy>]

Exit codes
    0  produced (and, if --verify was given, matched)
    2  STOP - ffmpeg failed, no audio stream, or verification failed

ECR-GEN-003 (path parameterization and reproducibility; no algorithm change):
  - <out> is normalised to end in `.npy` before writing, so the file written is
    exactly the file reported (np.save would otherwise append the suffix silently);
  - a deterministic provenance sidecar `<out>.provenance.json` is written beside the
    array: script SHA-256, input SHA-256, arguments, toolchain identity. No
    wall-clock value is recorded. The ffmpeg used is whichever `ffmpeg` resolves on
    PATH, and its resolved binary path and SHA-256 are recorded.
"""
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys

import numpy as np

RATE_HZ = 16000
WINDOW_S = 0.25
FULL_SCALE = 32768.0
DTYPE = np.float32


def decode_pcm(media, rate_hz):
    """Decode `media` to mono signed-16-bit PCM at `rate_hz`. Raises on failure."""
    proc = subprocess.run(
        ['ffmpeg', '-v', 'error', '-i', media,
         '-ac', '1', '-ar', str(rate_hz), '-f', 's16le', '-'],
        capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError('ffmpeg failed (%d): %s'
                           % (proc.returncode, proc.stderr.decode('utf-8', 'replace')[:400]))
    if not proc.stdout:
        raise RuntimeError('ffmpeg produced no audio samples; the media may carry no audio stream')
    return np.frombuffer(proc.stdout, dtype='<i2')


def rms_windows(pcm_i16, rate_hz=RATE_HZ, window_s=WINDOW_S):
    """Non-overlapping RMS. A trailing partial window is discarded, not padded."""
    n = int(round(rate_hz * window_s))
    if n <= 0:
        raise ValueError('window length resolves to %d samples' % n)
    m = len(pcm_i16) // n
    if m == 0:
        raise RuntimeError('media is shorter than one %.3f s window' % window_s)
    block = pcm_i16[:m * n].astype(np.float32).reshape(m, n) / FULL_SCALE
    return np.sqrt((block ** 2).mean(axis=1)).astype(DTYPE)


def _sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b''):
            h.update(chunk)
    return h.hexdigest()


def _tool_identity(name):
    """Resolved path, SHA-256 and first version line of an external executable."""
    exe = shutil.which(name)
    if not exe:
        return dict(name=name, resolved=None)
    real = os.path.realpath(exe)
    ver = subprocess.run([exe, '-hide_banner', '-version'], capture_output=True)
    first = ver.stdout.decode('utf-8', 'replace').splitlines()[:1]
    return dict(name=name, resolved=real, sha256=_sha256(real), version=first[0] if first else None)


def _numpy_identity():
    ident = dict(version=np.__version__)
    try:
        ident['blas'] = np.show_config(mode='dicts')['Build Dependencies']['blas'].get('name')
    except Exception:                              # noqa: BLE001 - older numpy: not recorded
        ident['blas'] = None
    return ident


def write_provenance(out, arguments, inputs, tools):
    """Deterministic sidecar: sorted keys, no wall-clock value, output named by basename."""
    rec = dict(schema='b3-provenance/1',
               producer=os.path.basename(__file__), producer_sha256=_sha256(__file__),
               arguments=arguments,
               inputs=[dict(role=r, path=p, sha256=_sha256(p), bytes=os.path.getsize(p))
                       for r, p in inputs],
               outputs=[dict(path=os.path.basename(out), sha256=_sha256(out),
                             bytes=os.path.getsize(out))],
               toolchain=dict(python=platform.python_version(),
                              implementation=sys.implementation.name,
                              interpreter=os.path.realpath(sys.executable),
                              machine=platform.machine(),
                              numpy=_numpy_identity(),
                              tools=[_tool_identity(t) for t in tools]))
    with open(out + '.provenance.json', 'w') as fh:
        fh.write(json.dumps(rec, indent=1, sort_keys=True) + '\n')


def main():
    ap = argparse.ArgumentParser(description='Produce the audio RMS observation array.')
    ap.add_argument('media')
    ap.add_argument('out')
    ap.add_argument('--rate', type=int, default=RATE_HZ)
    ap.add_argument('--window-s', type=float, default=WINDOW_S)
    ap.add_argument('--verify', default=None,
                    help='reference .npy to check the produced array against')
    a = ap.parse_args()

    try:
        pcm = decode_pcm(a.media, a.rate)
        arr = rms_windows(pcm, a.rate, a.window_s)
    except Exception as exc:                       # noqa: BLE001 - reported, not absorbed
        print('STOP: %s' % exc, file=sys.stderr)
        return 2

    out = a.out if a.out.endswith('.npy') else a.out + '.npy'
    np.save(out, arr)
    write_provenance(out,
                     dict(rate=a.rate, window_s=a.window_s,
                          verify=os.path.basename(a.verify) if a.verify else None),
                     [('media', a.media)] + ([('verify_reference', a.verify)] if a.verify else []),
                     ['ffmpeg'])
    print('produced %s  shape=%s dtype=%s covered_s=%.3f'
          % (out, arr.shape, arr.dtype, len(arr) * a.window_s))

    if a.verify:
        ref = np.load(a.verify)
        if ref.shape != arr.shape:
            print('VERIFY FAILED: shape %s != reference %s' % (arr.shape, ref.shape),
                  file=sys.stderr)
            return 2
        err = float(np.abs(arr - ref).max())
        exact = bool((arr == ref).all())
        print('verify against %s: max_abs_err=%.8f  bitwise_identical=%s'
              % (a.verify, err, exact))
        if not exact:
            print('VERIFY FAILED: produced array is not bitwise identical to the reference',
                  file=sys.stderr)
            return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
