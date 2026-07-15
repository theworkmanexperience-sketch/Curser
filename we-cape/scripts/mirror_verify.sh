#!/usr/bin/env bash
# W.E. C.A.P.E. — Verified folder mirror  (mirror_verify.sh)
#
# Copy SRC -> DEST and PROVE every file landed byte-for-byte (SHA-256). A copy you
# haven't verified is a rumor; this re-reads the written bytes and hashes both sides.
# ADDITIVE by design — it never deletes anything on DEST (a backup that deletes is a
# footgun). DRY-RUN by default; pass --go to actually copy. Exits non-zero if ANY
# file is missing or mismatched, so it's safe to chain before "card is safe to format".
#
#   mirror_verify.sh SRC DEST --go            # copy, then verify byte-for-byte
#   mirror_verify.sh SRC DEST                 # dry-run (preview only, writes nothing)
#   mirror_verify.sh SRC DEST --verify-only   # verify an existing mirror (bit-rot check)
#   mirror_verify.sh SRC DEST --go --log ~/backup.log
#
# Topology-agnostic: SRC/DEST are just paths. macOS bash-3.2 safe; handles spaces and
# trailing-space folder names. Falls back sha256sum<->shasum and rsync<->cp.
set -uo pipefail

GO=0; VERIFY_ONLY=0; LOG=""; SRC=""; DEST=""
usage(){ echo "usage: mirror_verify.sh SRC DEST [--go | --verify-only] [--log FILE]"; }
while [ $# -gt 0 ]; do
  case "$1" in
    --go) GO=1; shift;;
    --verify-only) VERIFY_ONLY=1; shift;;
    --log) LOG="${2:-}"; shift 2;;
    -h|--help) usage; exit 0;;
    -*) echo "unknown option: $1"; usage; exit 2;;
    *) if [ -z "$SRC" ]; then SRC="$1"; elif [ -z "$DEST" ]; then DEST="$1";
       else echo "unexpected arg: $1"; exit 2; fi; shift;;
  esac
done
[ -n "$SRC" ] && [ -n "$DEST" ] || { usage; exit 2; }
SRC="${SRC%/}"; DEST="${DEST%/}"
[ -d "$SRC" ] || { echo "✗ source not a directory: $SRC"; exit 2; }

hashof(){ if command -v shasum >/dev/null 2>&1; then shasum -a 256 "$1" | awk '{print $1}';
          else sha256sum "$1" | awk '{print $1}'; fi; }

echo "════════════════════════════════════════════════════════════"
echo "  W.E. C.A.P.E. — Verified Mirror"
echo "  SRC : $SRC"
echo "  DEST: $DEST"
if   [ $VERIFY_ONLY -eq 1 ]; then echo "  Mode: VERIFY-ONLY (no copy)";
elif [ $GO -eq 1 ];          then echo "  Mode: EXECUTE (copy + verify)";
else                              echo "  Mode: DRY-RUN (preview only)"; fi
echo "════════════════════════════════════════════════════════════"

# DRY-RUN: preview what would change, write nothing.
if [ $GO -eq 0 ] && [ $VERIFY_ONLY -eq 0 ]; then
  if command -v rsync >/dev/null 2>&1; then rsync -an --itemize-changes "$SRC"/ "$DEST"/ || true; fi
  echo "(dry-run) nothing written. Re-run with --go to copy + verify."
  exit 0
fi

# COPY (skipped in --verify-only).
if [ $VERIFY_ONLY -eq 0 ]; then
  mkdir -p "$DEST"
  if command -v rsync >/dev/null 2>&1; then rsync -a --partial "$SRC"/ "$DEST"/;
  else cp -R "$SRC"/. "$DEST"/; fi
fi

# VERIFY every source file against DEST by SHA-256.
fail=0; ok=0; bytes=0
while IFS= read -r -d '' f; do
  rel="${f#"$SRC"/}"
  d="$DEST/$rel"
  if [ ! -f "$d" ]; then echo "  ✗ MISSING   $rel"; fail=$((fail+1)); continue; fi
  a=$(hashof "$f"); b=$(hashof "$d")
  if [ "$a" != "$b" ]; then echo "  ✗ MISMATCH  $rel"; fail=$((fail+1));
  else ok=$((ok+1)); bytes=$((bytes + $(wc -c < "$f"))); fi
done < <(find "$SRC" -type f -print0)

ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
line="[$ts] mirror $SRC -> $DEST : verified=$ok failed=$fail bytes=$bytes"
echo "────────────────────────────────────────────────────────────"
echo "  $line"
[ -n "$LOG" ] && echo "$line" >> "$LOG"
if [ $fail -ne 0 ]; then
  echo "  ✗ $fail file(s) FAILED verification — DEST is NOT a trustworthy copy."
  exit 1
fi
echo "  ✓ every file verified byte-for-byte ($ok files)."
exit 0
