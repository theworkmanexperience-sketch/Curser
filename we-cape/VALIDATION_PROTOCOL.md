# Real-Footage Validation Protocol — run_stages() Rewire
_Run this on your Mac (the drives and real pytest aren't reachable from the Cowork sandbox)._

## Why
The pipeline was rewired so `run()` executes through `core.stage.run_stages()`
(the PipelineStage seam). It was validated two ways already:
- The full 189-test suite passes with `engine: stages` as default.
- On synthetic 1080p multicam footage, `engine: legacy` and `engine: stages`
  produced **identical** output trees, metrics, and audit-log counts.

What synthetic clips can't cover: real codecs/containers, real camera clock
drift, telemetry, large files, and your actual storage. This protocol closes
that gap. Budget ~30 min with a small real shoot.

## 0. Back up first (no git rollback exists yet)
```bash
cp ~/.wecape/registry/wecape.db ~/.wecape/registry/wecape.db.bak-$(date +%Y%m%d)
```
The registry auto-migrates v1→v2 (we_forge_version → we_cape_version) on first
open. It's tested-lossless, but keep the backup.

## 1. Run the real test suite
```bash
cd ~/Curser/we-cape
python3 -m pytest wecape/tests/ -q        # expect: 189 passed
# pytest-free fallback (acceptance subset only):
python3 run_tests.py
```
If pytest disagrees with the 189 figure, send me the failures — my sandbox
emulates pytest fixtures and could differ on an edge case.

## 2. Equivalence on a SMALL real shoot (the key test)
Pick ~10–30 files from one real shoot (e.g. a slice of the DJIAction6 card).
Copy them to a scratch input folder so nothing original is touched.

```bash
SRC=/Volumes/.../small_real_shoot          # your subset
OUTL=/Volumes/WE_CAPE_OUTPUT/_val_legacy
OUTS=/Volumes/WE_CAPE_OUTPUT/_val_stages

# Run the OLD path:
#   set  pipeline.engine: legacy  in wecape/config.yaml
WECAPE_NONINTERACTIVE=1 python3 -m wecape --input "$SRC" --output "$OUTL" --proxy

# Run the NEW path:
#   set  pipeline.engine: stages  in wecape/config.yaml   (this is the default)
WECAPE_NONINTERACTIVE=1 python3 -m wecape --input "$SRC" --output "$OUTS" --proxy
```

Compare (ignore the differing run-id tokens):
```bash
# Structure should match (filenames identical apart from the run-id in LOGS/):
diff <(cd "$OUTL" && find . -type f | sed -E 's/WEF_[0-9_A-F]+/RUNID/g' | sort) \
     <(cd "$OUTS" && find . -type f | sed -E 's/WEF_[0-9_A-F]+/RUNID/g' | sort)

# Summary metrics should match (files, groups, variants, proxies, errors):
grep -E "Files:|Groups:|Variants:|Proxies:|Errors:" "$OUTL"/LOGS/*_summary.md
grep -E "Files:|Groups:|Variants:|Proxies:|Errors:" "$OUTS"/LOGS/*_summary.md
```
**Pass = the diff is empty and the metrics match.**

## 3. Spot-check the new-path output
- `CAMERA/<Family>/…` symlinks/copies resolve and play.
- `MULTICAM/MCG_*.json` groups look right for the shoot.
- `PROXIES/*.mp4` open and are the expected resolution.
- `LOGS/` has all five streams (ingest, classification, grouping, variants,
  proxies) + `manifest.json` + `summary.md`.
- Registry updated: `sqlite3 ~/.wecape/registry/wecape.db "SELECT id,file_count,we_cape_version FROM runs ORDER BY timestamp DESC LIMIT 3;"`

## 4. Full real shoot
Once the small-shoot diff is clean, run a complete shoot through `engine: stages`
and confirm runtime is in line with your benchmarks (NVMe/4w/hwaccel ≈ 0.43 min/proxy).

## 5. Rollback (instant, no code change)
If anything looks wrong, set in `wecape/config.yaml`:
```yaml
pipeline:
  engine: legacy
```
That restores the exact pre-rewire orchestration. Then send me the diff/summary
from step 2 and I'll reconcile.

## 6. After it passes
Commit (there's no git history in the working mount I used, so this is on you):
```bash
cd ~/Curser/we-cape && git add -A && git commit -m "audit remediation + run_stages rewire (189 tests, equivalence-validated)"
```
Then delete the leftovers I couldn't remove on the mount:
```bash
rm -rf .trash_junk we_capture/profiles
sqlite3 ~/.wecape/registry/wecape.db "DELETE FROM runs WHERE file_count=0;"
```
