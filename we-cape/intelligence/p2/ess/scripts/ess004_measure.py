#!/usr/bin/env python3
"""ESS-004 evidence: objective audio MEASUREMENTS for the Executive Listening Session.

This script MEASURES. It does not classify, and it emits no verdict. The question
'is this content musical?' is an Executive ruling (PDR-2026-08-22-ESS-004).
Comparison is three-way so the numbers can be read against known references:
  TARGET         00:33:37.708-00:34:39.667  the element inside SIL-01
  CONTROL-MUSIC  00:00:02.000-00:01:03.958  KICKSTANDS UP v1 - the lock's only score asset
  CONTROL-SPEECH 00:35:20.000-00:36:21.958  inside SIL-01, no audio-lane element present
"""
import wave, numpy as np, json

U = "/mnt/user-data/uploads/WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK/ess004/"
SR = 22050

def load(p):
    with wave.open(p) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float64) / 32768.0
    return a

def frames(x, n=2048, hop=512):
    m = 1 + (len(x) - n) // hop
    idx = np.arange(n)[None, :] + hop * np.arange(m)[:, None]
    return x[idx] * np.hanning(n)[None, :]

def spec(x):
    return np.abs(np.fft.rfft(frames(x), axis=1)) + 1e-12

def measure(x, sr=SR):
    S = spec(x)
    freq = np.fft.rfftfreq(2048, 1/sr)
    p = S**2
    tot = p.sum(axis=1)
    # spectral flatness: geometric/arithmetic mean. Tonal -> low. Noise -> high.
    flat = np.exp(np.log(S).mean(axis=1)) / S.mean(axis=1)
    cent = (freq[None, :] * p).sum(axis=1) / tot
    def band(lo, hi):
        m = (freq >= lo) & (freq < hi)
        return p[:, m].sum(axis=1) / tot
    # onset envelope -> beat periodicity by autocorrelation
    flux = np.maximum(0, np.diff(S, axis=0)).sum(axis=1)
    flux = (flux - flux.mean()) / (flux.std() + 1e-12)
    ac = np.correlate(flux, flux, 'full')[len(flux)-1:]
    ac /= (ac[0] + 1e-12)
    hop_s = 512 / sr
    lo, hi = int(0.30/hop_s), int(1.20/hop_s)       # 50-200 BPM
    seg = ac[lo:hi]
    k = int(np.argmax(seg)) + lo
    beat_str = float(seg.max())
    bpm = 60.0 / (k * hop_s)
    rms = np.sqrt((x**2).reshape(-1, 1).mean())
    env = np.sqrt(frames(x).__pow__(2).mean(axis=1))
    env_db = 20*np.log10(env + 1e-9)
    return dict(
        rms_dbfs             = round(float(20*np.log10(rms + 1e-12)), 2),
        level_range_db       = round(float(np.percentile(env_db, 95) - np.percentile(env_db, 5)), 2),
        quiet_frame_pct      = round(float((env_db < np.percentile(env_db, 95) - 25).mean()*100), 1),
        spectral_flatness    = round(float(np.median(flat)), 4),
        spectral_centroid_hz = round(float(np.median(cent)), 1),
        sub_bass_80_250hz_pct= round(float(np.median(band(80, 250))*100), 2),
        speech_band_1k_4k_pct= round(float(np.median(band(1000, 4000))*100), 2),
        beat_periodicity     = round(beat_str, 4),
        implied_bpm          = round(bpm, 1),
    )

rows = {k: measure(load(U + f + ".wav")) for k, f in
        (("TARGET", "target"), ("CONTROL-MUSIC", "control_music"), ("CONTROL-SPEECH", "control_speech"))}

keys = list(rows["TARGET"])
w = max(len(k) for k in keys)
print(f"{'measure':<{w}}  {'TARGET':>14}  {'CONTROL-MUSIC':>14}  {'CONTROL-SPEECH':>15}")
print("-" * (w + 50))
for k in keys:
    print(f"{k:<{w}}  {rows['TARGET'][k]:>14}  {rows['CONTROL-MUSIC'][k]:>14}  {rows['CONTROL-SPEECH'][k]:>15}")
json.dump(rows, open("/home/claude/work/out/ess004_measurements.json", "w"), indent=1)
