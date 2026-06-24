#!/usr/bin/env bash
#
# W.E. C.A.P.E. — iPhone media organizer + verifier
# Principle #1 helper: turn a flat folder of exported iPhone originals into a
# clean, de-duplicated, date-sorted archive you can trust.
#
#   * Sorts photos + videos into YYYY/MM/ by capture date
#     (exiftool > Spotlight mdls > file mtime — best source available)
#   * De-duplicates by SHA-256 content hash (dupes routed to _duplicates/)
#   * Reports photo vs video counts; writes a CSV manifest
#   * DRY-RUN by default — shows what it would do, touches nothing
#
# macOS (Mac Studio). Safe on bash 3.2 (no associative arrays).
#
# Usage:
#   bash scripts/organize_iphone_backup.sh "<SRC export folder>" "<DST archive folder>"
#   ... --apply     actually copy files (default is dry-run)
#   ... --move      move instead of copy (use only if SRC is itself a copy)
# ---------------------------------------------------------------------------

set -uo pipefail

SRC="${1:-}"; DST="${2:-}"
APPLY=0; MODE="copy"
if [ "$#" -ge 2 ]; then shift 2; else shift "$#"; fi
for a in "$@"; do
  case "$a" in
    --apply) APPLY=1 ;;
    --move)  MODE="move" ;;
    *) echo "Unknown option: $a"; exit 1 ;;
  esac
done

if [ -z "$SRC" ] || [ -z "$DST" ]; then
  echo "Usage: $0 <src export folder> <dst archive folder> [--apply] [--move]"
  exit 1
fi
[ -d "$SRC" ] || { echo "✗ Source folder not found: $SRC"; exit 1; }
mkdir -p "$DST"

PHOTO_EXT="jpg jpeg heic heif png gif tiff tif dng cr2 cr3 arw nef webp bmp"
VIDEO_EXT="mov mp4 m4v avi mkv 3gp"
MANIFEST="$DST/_manifest_$(date +%Y%m%d_%H%M%S).csv"
SEEN="$(mktemp)"; trap 'rm -f "$SEEN"' EXIT
echo "original,capture_date,year_month,kind,sha256,duplicate,dest" > "$MANIFEST"

capture_date() {  # -> YYYY-MM-DD (best available source)
  local f="$1" d=""
  if command -v exiftool >/dev/null 2>&1; then
    d=$(exiftool -d '%Y-%m-%d' -DateTimeOriginal -CreateDate -s3 "$f" 2>/dev/null | head -1)
  fi
  if [ -z "$d" ] && command -v mdls >/dev/null 2>&1; then
    d=$(mdls -name kMDItemContentCreationDate -raw "$f" 2>/dev/null | cut -d' ' -f1)
    [ "$d" = "(null)" ] && d=""
  fi
  [ -z "$d" ] && d=$(stat -f '%Sm' -t '%Y-%m-%d' "$f" 2>/dev/null)   # macOS stat
  # Trust only a clean YYYY-MM-DD; anything else -> unknown (no garbage folders).
  case "$d" in
    [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]) ;;
    *) d="" ;;
  esac
  echo "$d"
}

kind_of() {
  local ext; ext="$(printf '%s' "${1##*.}" | tr '[:upper:]' '[:lower:]')"
  local e
  for e in $PHOTO_EXT; do [ "$e" = "$ext" ] && { echo photo; return; }; done
  for e in $VIDEO_EXT; do [ "$e" = "$ext" ] && { echo video; return; }; done
  echo other
}

photos=0; videos=0; other=0; dups=0; done_n=0
echo "Scanning: $SRC"
echo "Mode: $([ "$APPLY" = 1 ] && echo "$MODE (APPLY)" || echo 'DRY-RUN (nothing written)')"

while IFS= read -r -d '' f; do
  k=$(kind_of "$f")
  if [ "$k" = other ]; then other=$((other+1)); continue; fi

  d=$(capture_date "$f"); [ -z "$d" ] && d="unknown"
  if [ "$d" = "unknown" ]; then ym="unknown"; else ym=$(printf '%s' "$d" | cut -d- -f1,2 | tr '-' '/'); fi

  h=$(shasum -a 256 "$f" 2>/dev/null | cut -d' ' -f1)
  dup=no
  if [ -n "$h" ] && grep -qxF "$h" "$SEEN"; then dup=yes; dups=$((dups+1)); else [ -n "$h" ] && printf '%s\n' "$h" >> "$SEEN"; fi

  if [ "$dup" = yes ]; then destdir="$DST/_duplicates/$ym"; else destdir="$DST/$ym"; fi
  dest="$destdir/$(basename "$f")"
  printf '"%s",%s,%s,%s,%s,%s,"%s"\n' "$f" "$d" "$ym" "$k" "$h" "$dup" "$dest" >> "$MANIFEST"

  [ "$k" = photo ] && photos=$((photos+1))
  [ "$k" = video ] && videos=$((videos+1))

  if [ "$APPLY" = 1 ]; then
    mkdir -p "$destdir"
    if [ "$MODE" = move ]; then mv -n "$f" "$dest"; else cp -n "$f" "$dest"; fi
    done_n=$((done_n+1))
  fi
done < <(find "$SRC" -type f -print0)

echo
echo "── Summary ──────────────────────────────────────────────"
echo "  Photos:        $photos"
echo "  Videos:        $videos"
echo "  Other/skipped: $other"
echo "  Duplicates:    $dups  (routed to _duplicates/)"
echo "  Manifest:      $MANIFEST"
if [ "$APPLY" = 1 ]; then
  echo "  ${MODE}d:        $done_n files into $DST"
else
  echo "  DRY-RUN — review the manifest, then re-run with --apply."
fi
