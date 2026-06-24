#!/usr/bin/env bash
#
# W.E. C.A.P.E. — Asset Protection Backup
# Principle #1: No asset exists until it exists in two locations.
#
# Mirrors the currently-UNPROTECTED "Holder Mac" volume (production content +
# legal docs, 4.6 TB, zero backup) onto the underused "Got My BackUP" drive.
#
# Safe by design: read-only on the source (never writes to it); additive by
# default (never deletes on the destination until you opt into MIRROR).
#
# Run on the Mac Studio:  bash scripts/backup_holder_mac.sh
# ---------------------------------------------------------------------------

# ── CONFIRM THESE against `ls /Volumes` before the first run ───────────────
SRC="/Volumes/Holder Mac"                               # source (verify exact name!)
DST="/Volumes/Got My BackUP/HolderMac_Backup"           # destination subfolder
MIRROR=0   # 0 = additive (safe, never deletes). 1 = true mirror (--delete).
# ---------------------------------------------------------------------------

LOG="$HOME/wecape_holdermac_backup_$(date +%Y%m%d_%H%M%S).log"
RSYNC="/usr/bin/rsync"   # Apple's stock rsync: -E preserves HFS+ metadata/forks

echo "============================================================"
echo "  W.E. C.A.P.E. Asset Backup — $(date)"
echo "  Source: $SRC"
echo "  Dest:   $DST"
echo "  Log:    $LOG"
echo "============================================================"

# ── Pre-flight: both volumes mounted? ──────────────────────────────────────
if [ ! -d "$SRC" ]; then
  echo "✗ Source not mounted: $SRC"
  echo "  Run 'ls /Volumes' and set SRC to the exact Holder Mac name (watch for spaces)."
  exit 1
fi
DST_VOL="$(dirname "$DST")"
if [ ! -d "$DST_VOL" ]; then
  echo "✗ Destination drive not mounted: $DST_VOL"
  exit 1
fi
mkdir -p "$DST"

# ── Pre-flight: space check (df -g = GB; instant, no full tree walk) ────────
SRC_USED_GB="$(df -g "$SRC" | awk 'NR==2{print $3}')"
DST_FREE_GB="$(df -g "$DST_VOL" | awk 'NR==2{print $4}')"
echo "  Source used: ${SRC_USED_GB} GB   |   Dest free: ${DST_FREE_GB} GB"
if [ "${SRC_USED_GB:-0}" -gt "${DST_FREE_GB:-0}" ]; then
  echo "✗ Not enough space: need ~${SRC_USED_GB} GB, only ${DST_FREE_GB} GB free."
  echo "  Free space on Got My BackUP (it currently holds ~184 GB of other data),"
  echo "  or add folder excludes below, then retry."
  exit 1
fi
# Headroom warning — this fit is tight (4.6 TB into ~4.8 TB).
HEADROOM=$(( DST_FREE_GB - SRC_USED_GB ))
if [ "$HEADROOM" -lt 300 ]; then
  echo "  ⚠  Only ${HEADROOM} GB headroom after backup — consider a larger destination soon."
fi

# ── Build rsync flags ──────────────────────────────────────────────────────
RSYNC_FLAGS=(-aE --human-readable --progress --stats)
# Skip macOS volume cruft that shouldn't be backed up
RSYNC_FLAGS+=(--exclude ".Spotlight-V100" --exclude ".Trashes" \
             --exclude ".fseventsd" --exclude ".DocumentRevisions-V100" \
             --exclude ".TemporaryItems")
if [ "$MIRROR" = "1" ]; then
  RSYNC_FLAGS+=(--delete)
  echo "  Mode: MIRROR (--delete — destination will exactly match source)"
else
  echo "  Mode: additive (safe — nothing on the destination is ever deleted)"
fi

echo "  Starting rsync — first run copies all 4.6 TB and will take hours."
echo "  (Later runs are incremental and fast.) Keep the Mac awake & drives mounted."
echo

# ── Run (tolerate rsync exit 24 = 'source files vanished mid-copy') ─────────
set +e
"$RSYNC" "${RSYNC_FLAGS[@]}" "$SRC/" "$DST/" 2>&1 | tee "$LOG"
RC=${PIPESTATUS[0]}
set -e
if [ "$RC" -ne 0 ] && [ "$RC" -ne 24 ]; then
  echo "✗ rsync failed (exit $RC) — see $LOG"
  exit "$RC"
fi

echo
echo "✓ Backup complete — $(date)"
echo "  Verify (dry-run; empty output below = byte-for-byte identical):"
echo "      $RSYNC -avEn --delete \"$SRC/\" \"$DST/\""
echo "  Two locations now exist. Principle #1 satisfied."
