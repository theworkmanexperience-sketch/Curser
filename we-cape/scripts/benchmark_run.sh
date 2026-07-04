#!/usr/bin/env bash
#
# W.E. C.A.P.E. — Benchmark / confirmation run
#
# Times a real CAPTURE + proxy run end-to-end and prints a paste-ready benchmark
# row for the CLAUDE.md table, plus proxy count / errors / rate / gate result.
#
#   bash scripts/benchmark_run.sh <source> <output> [extra wecape args…]
#
# ⚠ IMPORTANT — point <output> at a FRESH/EMPTY folder. Re-running onto an
#   already-processed output is idempotent (SHA-skip) and finishes in seconds:
#   that is NOT a transcode benchmark. This script refuses a non-empty output
#   unless you pass --force.
# ---------------------------------------------------------------------------

set -uo pipefail

FORCE=0; args=()
for a in "$@"; do if [ "$a" = "--force" ]; then FORCE=1; else args+=("$a"); fi; done
set -- "${args[@]}"

[ "$#" -ge 2 ] || { echo "usage: bash scripts/benchmark_run.sh <source> <output> [extra wecape args…]"; exit 2; }
SRC="$1"; OUT="$2"; shift 2
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; REPO="$(dirname "$SCRIPT_DIR")"

command -v ffmpeg  >/dev/null 2>&1 || { echo "✗ ffmpeg not on PATH";  exit 1; }
command -v ffprobe >/dev/null 2>&1 || { echo "✗ ffprobe not on PATH"; exit 1; }
[ -d "$SRC" ] || { echo "✗ source not found: $SRC  (check /Volumes; watch for spaces)"; exit 1; }

if [ -d "$OUT" ] && [ -n "$(ls -A "$OUT" 2>/dev/null)" ] && [ "$FORCE" -ne 1 ]; then
  echo "✗ output '$OUT' is not empty."
  echo "  A re-run here will SHA-skip existing proxies (seconds, not a real transcode)."
  echo "  Point --output at a fresh folder, or pass --force to benchmark anyway."
  exit 1
fi
mkdir -p "$OUT" || { echo "✗ cannot create output: $OUT"; exit 1; }

LOG="$(mktemp -t wecape_bench.XXXXXX)"; trap 'rm -f "$LOG"' EXIT
echo "════════════════════════════════════════════════════════════"
echo "  W.E. C.A.P.E. — benchmark run   $(date)"
echo "  source: $SRC"
echo "  output: $OUT"
echo "════════════════════════════════════════════════════════════"

START=$(date +%s)
( cd "$REPO" && WECAPE_NONINTERACTIVE=1 python3 -m wecape --input "$SRC" --output "$OUT" --proxy "$@" ) 2>&1 | tee "$LOG"
rc=${PIPESTATUS[0]}
END=$(date +%s); ELAPSED=$((END - START))

PROX=$(grep -oiE '[0-9]+ (proxies )?transcoded' "$LOG" | grep -oE '^[0-9]+' | tail -1)
ERRS=$(grep -oiE '[0-9]+ errors?' "$LOG" | grep -oE '^[0-9]+' | tail -1)
RUNID=$(grep -oE 'WEF_[0-9]{8}_[0-9]{6}_[0-9A-Fa-f]{6}' "$LOG" | tail -1)
MIN=$(awk "BEGIN{printf \"%.1f\", $ELAPSED/60}")
RATE="n/a"; [ -n "${PROX:-}" ] && [ "${PROX:-0}" -gt 0 ] && RATE=$(awk "BEGIN{printf \"%.2f\", ($ELAPSED/60)/$PROX}")
GATE="PASS"; awk "BEGIN{exit !($ELAPSED/60 < 90)}" || GATE="FAIL"

echo
echo "──────── RESULT — paste into CLAUDE.md 'Benchmark Results' table ────────"
echo "| NVMe-confirm | NVMe TB4 | 4 | VTB hwaccel | ${MIN} min | ${RATE} min/proxy | ${GATE} |"
echo "  run_id: ${RUNID:-?} · proxies: ${PROX:-?} · errors: ${ERRS:-0} · exit: $rc · wall: ${ELAPSED}s"
if [ "$GATE" = "PASS" ]; then
  echo "  ✓ under the 90-min gate — workers=4 + hwaccel effective on the NVMe."
else
  echo "  ⚠ over 90 min. Likely software decode (not VTB hwaccel) or workers!=4 —"
  echo "    check config.yaml proxy_generation.workers and that VideoToolbox is active."
fi
exit "$rc"
