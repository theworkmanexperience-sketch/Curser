# Verified Card Offload — the Hedge-style front end

`offload_cards.py` pulls a camera card into the per-camera folder structure CAPTURE
expects, with **checksum-verified** copies and an optional **second destination** — so
*"no asset exists until it exists in two locations"* (Principle #1) is true the moment
offload finishes, **before** CAPTURE runs. This automates the riskiest, most manual step
in the whole pipeline: getting the irreplaceable originals off the card, safely.

## Why this matters

The footage on a card is the one thing nothing can recreate. A plain Finder drag-copy
gives you *no proof the bytes landed intact* and *no second copy*. This tool copies, then
re-reads each file and compares **SHA-256 against the source** — a copy that didn't land
byte-for-byte is a hard failure, not a silent pass — and writes to two places in one pass.

## Usage
```bash
# one destination
python3 scripts/offload_cards.py --source /Volumes/DJIAction6 \
    --camera "DJI ACTION 6" --shoot "O-SIX_2026" --dest "/Volumes/10TB"

# two copies in one pass (Principle #1 satisfied immediately)
python3 scripts/offload_cards.py --source /Volumes/CARD \
    --camera "Insta360 X5" --shoot "O-SIX_2026" \
    --dest "/Volumes/10TB" --dest2 "/Volumes/Got My BackUP/cards"

# see what would happen, write nothing
python3 scripts/offload_cards.py --source /Volumes/CARD --camera "DJI ACTION 5" \
    --shoot O-SIX_2026 --dest /Volumes/10TB --dry-run
```
| Flag | Meaning |
|------|---------|
| `--source` | card mount or folder (read-only — never modified) |
| `--camera` | per-camera label; **use `DJI ACTION 5` / `DJI ACTION 6` / `Insta360 X5`** so CAPTURE resolves the body |
| `--shoot` | top folder under each destination |
| `--dest` | primary destination root (e.g. `/Volumes/10TB`) |
| `--dest2` | optional second destination root (true two-copy) |
| `--ext` | comma-separated extension allowlist (default: copy **everything**) |
| `--dry-run` | list + size, write nothing |

Files land at `<dest>/<shoot>/<camera>/…`, preserving the card's subfolders. The `<camera>`
segment is exactly what lets CAPTURE's `camera_folder_patterns` identify the body downstream.

## What it guarantees

- **Every copy is verified** by SHA-256 against the source (in every destination).
- **Resumable:** a file already present with a matching hash is skipped — re-run after an
  interruption and it picks up where it stopped.
- **Manifest:** `_offload_manifest.json` in each camera folder records every file, its hash,
  and per-destination verification result.
- **It never deletes or modifies the card.** When the summary says *every file verified in
  every destination*, formatting the card is your call — the tool won't touch it.

## The full front-to-back flow
```
offload_cards.py        # card -> 10TB (+2nd copy), verified
        ↓
python -m wecape …      # CAPTURE: classify, group, proxies, registry
        ↓
capture_to_fcp.sh       # (or fcpxml_export.py) -> FCPXML -> open in FCP
```

## Honest caveats

- **SHA-256 is correct but not fast.** Multi-TB cards take a while (it reads every byte twice:
  source + written copy). Hedge uses xxHash for speed; SHA-256 is the safe, always-available
  default here. An `--xxhash` fast mode is a sensible future add if throughput bites.
- **Resume re-hashes the source** to confirm a match (correctness over speed); an interrupted
  multi-TB offload re-reads the card on the next run.
- **It verifies copies; it is not a card-formatter or a delete tool** — by design. Two copies +
  verified is the bar to clear before *you* reformat.
- **Same-machine `--dest2`** (e.g. another drive on the Mac) protects against a drive failure, not
  fire/theft. The registry/notes already go offsite via the backup job; bulk footage offsite (to
  the 20 TB Google Drive) remains a separate, size-bound step.
