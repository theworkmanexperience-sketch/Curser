# Camera Probe — `probe_camera.py`

Discovery/onboarding tool for **unknown** cameras. Point it at a file, folder, or
mounted card; it fingerprints the footage and tells you exactly what to add so the
platform recognizes it — turning per-camera detective work into one command.

```bash
python3 scripts/probe_camera.py /Volumes/SOMECARD          # human report
python3 scripts/probe_camera.py /Volumes/SOMECARD --json   # structured
python3 scripts/probe_camera.py /Volumes/SOMECARD --add    # opt-in: append cameras.yaml stub
python3 scripts/probe_camera.py CLIP.MP4 --add --interactive
```

## What it reports
- **Recommended next step** (first line) — the action to take.
- **Structure** — extensions, card markers (DCIM/…), sidecars, a ready-to-use filename regex.
- **Identity** — brand (from filenames, or the exif Make tag), serial, model, DJI model code.
- **Time** — datetime tags split into **drift-free (GPS)** vs **camera-clock**.
- **Streams** — video codec/res/fps, and any **telemetry stream flagged** (djmd/gpmf/gps).
- **Coverage** — does `identify()` resolve it today? Is it in `cameras.yaml`? What are the gaps?
- **Paste-ready stubs** — a `cameras.yaml` entry and a `camera_folder_patterns` / `FAMILY_PATTERNS` line.

## Boundaries (by design)
- **Not a telemetry decoder** — it *flags* a `djmd`/`gpmf` stream and hands off to vendor
  tools (Telemetry Extractor, Gyroflow). It does not parse IMU/GPS binary.
- **Not a transcode tester** — codec/container is a proxy hint only.
- **Read-only by default** — `--add` is the only writer, and it never guesses: a
  brand-only camera lands at `Unknown <Brand> - TODO confirm model`, and identity still
  defers unverified cameras to a human confirm.

## Onboarding checklist (what the probe helps you answer)
1. Identity — can we name the body from the footage? 2. Time — drift-free or camera-clock?
3. Telemetry — GPS/IMU, and where? 4. Structure — filename pattern / sidecars.
5. Grouping — fits the ±window? 6. Proxy — will ffmpeg transcode the codec/container?
7. Privacy — GPS → `telemetry.db`, hashed on egress.

Requires `exiftool` (+ `ffprobe` for streams); degrades gracefully and says so if absent.
stdlib only · zero network · read-only except `--add`.
