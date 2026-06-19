# W.E. C.A.P.E. CAPTURE — Phase 0 Operator Guide
## Step-by-Step Instructions for Running the Media Ingestion Engine
**The Workman Experience, LLC | May 22, 2026**

---

## Before You Start

You will need:
- A Mac running macOS 14 or later (or Ubuntu 22.04 LTS)
- Python 3.9 or later
- FFmpeg installed (for multicam grouping)
- At least one external drive with enough free space for your project output
- The `we_capture/` codebase from this package

If you are running a shoot larger than 10 GB, **your output must go to an external drive** — not to your Mac's internal drive. The engine will warn you and block the run if it detects this before any files are touched.

---

## Step 1 — Verify Your System Requirements

Open Terminal and run:

```bash
python3 --version
```

You should see `Python 3.9.x` or higher. If not, install Python from [python.org](https://python.org).

```bash
ffprobe -version
```

You should see a version number. If you get `command not found`, install FFmpeg:

```bash
# Homebrew (recommended)
brew install ffmpeg

# MacPorts
sudo port install ffmpeg
```

After installing, run `ffprobe -version` again to confirm it works. You do not need to do anything else with FFmpeg — the engine calls it automatically.

> **Without ffprobe:** Classification and variant detection still work. Multicam grouping will be disabled and a warning will be printed. Install ffprobe before your first production run.

---

## Step 2 — Install the Engine

Navigate to the `we_capture/` directory and install the one required dependency:

```bash
cd /path/to/we_capture
pip install pyyaml
```

Verify everything is working by running the acceptance suite:

```bash
python3 run_tests.py
```

You should see:

```
49/49 tests passed
```

If any tests fail, stop here and contact The Workman Experience, LLC before proceeding.

---

## Step 3 — Know Your Drives

Before every run, open Finder and look at the **Locations** section in the left sidebar. Every drive listed there is an external drive. Your Mac's internal drive is called **Macintosh HD** and should never be used as the output destination for large shoots.

| Drive type | Where to use it |
|---|---|
| External drive (e.g., `10TB`, `Got My BackUP`) | Input media AND output — both are fine here |
| Mac internal drive (`Macintosh HD`) | Never use as output for shoots over 10 GB |

Keep your Mac's internal drive above **20 GB free** at all times. The engine checks this during pre-flight and will warn you if it drops below that threshold.

---

## Step 4 — Your First Run (EULA Acceptance)

The very first time you run the engine interactively, it will display the W.E. C.A.P.E. CAPTURE End User License Agreement (EULA v1.0). This is a one-time requirement.

Run the engine on any folder of media files:

```bash
python3 main.py \
  --input  /Volumes/YOUR_DRIVE/shoot_folder \
  --output /Volumes/YOUR_DRIVE/WE_FLOW_OUTPUT/project_name
```

The terminal will display the full EULA (approximately 15 sections). Read it, then type:

```
YES
```

and press Enter to accept. If you do not accept, the run is cancelled and no files are touched.

Your acceptance is saved to `~/.weflow/eula_acceptance.json`. You will not be prompted again unless the EULA version changes.

> **Non-interactive / CI environments:** If `stdin` is not a terminal (e.g., you are running from a script), the EULA prompt is skipped and the version is recorded automatically. Use `WECAPE_NONINTERACTIVE=1` to force this mode.

---

## Step 5 — The Attestation Prompt

Immediately after EULA acceptance (or on every subsequent run), the engine will print an attestation prompt:

```
  BEFORE YOU CONTINUE — please confirm all of the following:

  [ ] I am authorized to process the media files in the input folder
  [ ] These files comply with all applicable NDAs and client agreements
  [ ] I understand that W.E. C.A.P.E. CAPTURE will read every file in the input folder
  [ ] The output drive meets my organization's encryption requirements

  Type YES and press Enter to confirm, or Ctrl+C to cancel.
  >
```

Review each item. If all apply, type `YES` and press Enter. If any item does not apply, press `Ctrl+C` to cancel and resolve the issue before proceeding.

This confirmation is logged with a hash in `_preflight.json` for chain-of-custody.

---

## Step 6 — Read the Pre-Flight Check

After attestation, the engine prints a pre-flight summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  W.E. C.A.P.E. CAPTURE — Pre-Flight Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Input media:    /Volumes/10TB/shoot
                  141.0 GB · 49,602 files
  Output folder:  /Volumes/10TB/WE_FLOW_OUTPUT/project
                  887.0 GB free  ✓
  File mode:      symlink mode — no files copied
  Space needed:   5.0 GB minimum on output drive
  System drive:   147.0 GB free  ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**What to check:**

| Symbol | Meaning |
|---|---|
| `✓` | This check passed — nothing to do |
| `✗` | This check failed — the run will be blocked |
| `⚠ WARNING` | Read the warning before proceeding |

**If you see a WARNING about the system drive:** Your output folder is pointing to your Mac's internal drive. Change `--output` to a path on an external drive.

**If you see a WARNING about PII:** One or more filenames contain what looks like personal information (a name, phone number, or email). These filenames will be hashed in all log records — they are never stored in plaintext. Confirm you are authorized to process this content in the attestation prompt.

**If pre-flight FAILS:** The engine will print exactly what to fix and stop without touching any files. Fix the issue and re-run.

---

## Step 7 — Running the Engine

### Basic command

```bash
python3 main.py \
  --input  /Volumes/DRIVE/shoot_folder \
  --output /Volumes/DRIVE/WE_FLOW_OUTPUT/project_name
```

### With a custom config

```bash
python3 main.py \
  --input  /Volumes/DRIVE/shoot_folder \
  --output /Volumes/DRIVE/WE_FLOW_OUTPUT/project_name \
  --config /path/to/custom_config.yaml
```

### With more parallel workers (large shoots)

```bash
python3 main.py \
  --input  /Volumes/DRIVE/1TB_shoot \
  --output /Volumes/DRIVE/WE_FLOW_OUTPUT/project_name \
  --workers 16
```

The default is 8 workers. Increase this on multi-core machines for large shoots.

### Progress

The engine prints stage-by-stage progress to the terminal. A typical run on a 150 GB, 178-file shoot takes 12–15 minutes in symlink mode. You will see each stage complete in sequence.

---

## Step 8 — Understand the Output

When the run completes, your output folder will have this structure:

```
project_name/
├── 2026-03-04/                  ← one folder per calendar date in the shoot
│   ├── CAMERA/
│   │   ├── DJI/                 ← all DJI files for this date
│   │   ├── iPhone/
│   │   ├── Insta360/
│   │   ├── GoPro/
│   │   └── Unknown_Camera/      ← files the engine could not identify
│   ├── CAMERA_AUDIO/            ← field recorders (Zoom, Sound Devices, Tascam)
│   ├── GENERIC/                 ← screen recordings, AI-generated files, misc
│   ├── PROXIES/                 ← empty in Phase 0 (Phase 1 feature)
│   ├── MULTICAM/
│   │   └── MCG_4a7f2b1c.json   ← one file per multicam group detected
│   └── OUTPUTS/
├── REFERENCES/                  ← PDFs, EDLs, SRTs, media kit documents
├── LOGS/                        ← all audit logs (see Step 9)
└── WEF_20260304_143022_A1B2C3_index.json   ← machine-readable run summary
```

**In symlink mode (default):** The files in the camera folders are symbolic links pointing back to your original media. Nothing is copied. Your original files are never moved or modified.

**In copy mode:** Full copies of each file are written to the output folder. Use this only when delivering a self-contained project folder.

**Multicam groups:** If the engine finds two or more cameras that were recording at the same time (within ±5 seconds of each other), it creates a group file in `MULTICAM/`. Open the `.json` file to see which clips are in the group and their timestamps.

---

## Step 9 — Read the Logs

Every run writes six files to the `LOGS/` folder. The run ID in the filename (e.g., `WEF_20260304_143022_A1B2C3`) uniquely identifies this run.

| File | What it tells you |
|---|---|
| `{run_id}_preflight.json` | EULA version accepted, attestation hash, input path hash, disk check results |
| `{run_id}_manifest.json` | SHA-256 fingerprints of all five log streams — tamper evidence |
| `{run_id}_ingest.json` | Every file the engine discovered: size, timestamp, content hash |
| `{run_id}_classification.json` | How every file was classified: camera source, detection method |
| `{run_id}_grouping.json` | Multicam groups formed and why; ungrouped camera files and why |
| `{run_id}_variants.json` | Variant files detected (v2, _final, _edit, etc.) and parent selection |
| `{run_id}_errors.json` | Any files the engine could not process, with the reason |
| `{run_id}_summary.md` | Human-readable run summary — start here |

**Start with `_summary.md`** — it has total file counts, throughput, and a plain-English summary of what the engine found.

**Check `_errors.json`** — if any files failed to process, they are listed here with the reason. This does not mean the run failed; the engine continues past individual file errors.

> All filenames in logs are stored as SHA-256 hashes, not plaintext paths. This is a privacy control. If you need to trace a hash back to a filename, use the `_ingest.json` cross-reference alongside the source file list.

---

## Step 10 — Re-Running on the Same Input

You can re-run the engine on the same input folder with the same output folder at any time. The engine detects existing output files and skips them — it will not create duplicate entries or `_1` suffix artifacts.

```bash
# Second run on the same input — safe to run, identical result
python3 main.py \
  --input  /Volumes/DRIVE/shoot_folder \
  --output /Volumes/DRIVE/WE_FLOW_OUTPUT/project_name
```

The index JSON from both runs will be byte-for-byte identical. This is by design.

---

## Step 11 — Configuration

All behavior is controlled by `config.yaml`. You can edit this file or point to a custom copy with `--config`. Key settings:

| Setting | Default | When to change |
|---|---|---|
| `pipeline.file_operation` | `symlink` | Change to `copy` when delivering a self-contained project |
| `grouping.window_seconds` | `5` | Widen to `10` if your cameras start within 10 seconds of each other |
| `grouping.camera_offsets` | all `0` | Set a per-camera offset (seconds) if one camera has a clock that runs fast or slow |
| `variant_detection.parent_selection` | `largest_file` | Change to `earliest_timestamp` if you want the original clip as the parent, not the largest |
| `performance.max_workers` | `8` | Increase on multi-core machines; minimum 8 for large shoots |

**Do not change:**
- `proxies.generate_proxies` — must remain `false` in Phase 0
- `compliance.eula.version` — do not edit; set by The Workman Experience, LLC
- `grouping.window_seconds` below `5` — the ±5s LOCKED default is the compliance standard

---

## Common Issues

### "ffprobe not found — multicam grouping disabled"

FFmpeg is not installed or not on your PATH. Install it:

```bash
brew install ffmpeg      # Homebrew
sudo port install ffmpeg # MacPorts
```

Then run `ffprobe -version` to confirm it is found.

### Pre-flight fails: "Not enough space on output drive"

Your output drive does not have 5 GB free (symlink mode) or 110% of input size free (copy mode). Free up space on the output drive, or point `--output` to a different drive.

### Pre-flight fails: "Output folder is on your Mac's internal drive"

Change `--output` to a path on an external drive. Open Finder → Locations to see your external drives and their names.

### "EULA not accepted"

You must type `YES` (uppercase) exactly. Any other response cancels the run. The EULA prompt only appears on your first interactive run.

### Unknown_Camera files in output

Files in `CAMERA/Unknown_Camera/` are media files the engine could not match to a known camera source by filename or folder. This does not affect the rest of the run. To resolve: check whether the filenames follow a pattern, and if so, add a new pattern to `classification.camera_sources` in `config.yaml`.

### Run seems slow

Check `performance.max_workers` in `config.yaml`. The default is 8. On a 16-core machine, setting this to 16 will roughly double throughput. On a 150 GB shoot, expect 10–15 minutes in symlink mode.

---

## Quick Reference

```bash
# Full run on a shoot (symlink mode — recommended)
python3 main.py --input /Volumes/DRIVE/shoot --output /Volumes/DRIVE/WE_FLOW_OUTPUT/project

# Custom config
python3 main.py --input ./raw --output ./project --config ./custom.yaml

# More workers for large shoots
python3 main.py --input /Volumes/DRIVE/1TB_shoot --output /Volumes/DRIVE/project --workers 16

# Run acceptance tests
python3 run_tests.py

# Verify ffprobe
ffprobe -version

# Check EULA acceptance status
cat ~/.weflow/eula_acceptance.json
```

---

## Support

For questions about W.E. C.A.P.E. CAPTURE or this guide, contact:

**The Workman Experience, LLC**  
For legal or licensing questions: Valerie Workman, Esq. — valerieworkmanesq@gmail.com

---

*W.E. C.A.P.E. CAPTURE Phase 0 Operator Guide | v4.6 | May 22, 2026*  
*Compliance: 26/28 | Gate: CONDITIONALLY GREEN | Engine: 49/49 tests passing*
