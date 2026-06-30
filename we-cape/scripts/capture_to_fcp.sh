#!/usr/bin/env bash
#
# W.E. C.A.P.E. — capture → FCPXML → Final Cut Pro  (one-command handoff)
#
# Runs CAPTURE on a source, exports the new run's multicam groups to FCPXML, and
# opens it on FCP's import sheet. Stops at the ONE click FCP needs — it never
# UI-scripts the import (no API, and the editor's call: library, proxy vs original).
#
#   bash scripts/capture_to_fcp.sh <source> <output> [extra wecape args…]
#   bash scripts/capture_to_fcp.sh "/Volumes/10TB/O-SIX …" "/Volumes/WE_CAPE_OUTPUT/O-SIX_v2" --proxy
#
# The [extra wecape args] pass straight to `python -m wecape` (e.g. --proxy,
# --profile ryderz, --engine stages). For an editable FCP handoff you usually
# want proxies — either add --proxy here, or rely on proxies already linked by
# SHA from a prior run (P5 preserves them). For an --fps tweak on the export,
# run scripts/fcpxml_export.py directly afterward (see README_fcpxml.md).
# ---------------------------------------------------------------------------

set -uo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: bash scripts/capture_to_fcp.sh <source> <output> [extra wecape args…]" >&2
  exit 2
fi

SRC="$1"; OUT="$2"; shift 2     # remaining args ("$@") pass straight to wecape

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(dirname "$SCRIPT_DIR")"
DB="$HOME/.wecape/registry/wecape.db"

[ -d "$SRC" ] || { echo "✗ source not found: $SRC  (run 'ls /Volumes'; watch for spaces)"; exit 1; }
mkdir -p "$OUT" || { echo "✗ cannot create output: $OUT"; exit 1; }

echo "════════════════════════════════════════════════════════════"
echo "  W.E. C.A.P.E. — capture → FCPXML → FCP"
echo "  Source: $SRC"
echo "  Output: $OUT"
[ "$#" -gt 0 ] && echo "  wecape args: $*"
echo "════════════════════════════════════════════════════════════"

# ── 1) CAPTURE (tee so you see progress; capture stdout to find the run_id) ──
LOG="$(mktemp -t wecape_cap.XXXXXX)"
trap 'rm -f "$LOG"' EXIT
( cd "$REPO" && WECAPE_NONINTERACTIVE=1 python3 -m wecape --input "$SRC" --output "$OUT" "$@" ) 2>&1 | tee "$LOG"
rc=${PIPESTATUS[0]}
[ "$rc" -eq 0 ] || { echo "✗ CAPTURE failed (exit $rc) — not exporting."; exit "$rc"; }

# ── 2) Determine the new run_id: parse the summary line, else newest in registry ──
RUNID="$(grep -oE 'WEF_[0-9]{8}_[0-9]{6}_[0-9A-Fa-f]{6}' "$LOG" | tail -1)"
if [ -z "$RUNID" ] && command -v sqlite3 >/dev/null 2>&1 && [ -f "$DB" ]; then
  RUNID="$(sqlite3 "$DB" "SELECT id FROM runs WHERE file_count>0 ORDER BY timestamp DESC LIMIT 1;" 2>/dev/null)"
fi
[ -n "$RUNID" ] || { echo "✗ could not determine the run_id — export skipped. Run fcpxml_export.py --run <id> manually."; exit 1; }
echo
echo "  run_id: $RUNID"

# ── 3) Export FCPXML for that run (into the shoot's output folder) ──────────
FCPXML="$OUT/$(basename "$OUT")_multicam.fcpxml"
if ! python3 "$SCRIPT_DIR/fcpxml_export.py" --run "$RUNID" --db "$DB" --out "$FCPXML"; then
  echo "✗ FCPXML export failed (see message above). The CAPTURE run is fine; fix and re-export."
  exit 1
fi

# ── 4) Hand off to FCP — opens the import sheet (one confirming click) ──────
if command -v open >/dev/null 2>&1; then
  open "$FCPXML" && echo "  → opened in Final Cut Pro: confirm the import sheet (library / event)."
else
  echo "  Import manually in FCP ▸ File ▸ Import ▸ XML:  $FCPXML"
fi
echo "✓ Done. Then open a multicam clip ▸ Angle Editor; 'Synchronize Clips' to lock audio (see SOP_fcpxml_import.md)."
