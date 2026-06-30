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
# Run on the Mac Studio:
#   bash scripts/backup_holder_mac.sh                  # ~/.wecape (+offsite) THEN the 4.6 TB Holder Mac
#   bash scripts/backup_holder_mac.sh --registry-only  # ONLY ~/.wecape snapshot + offsite (fast; for hourly/daily)
# ---------------------------------------------------------------------------

# ── CONFIRM THESE against `ls /Volumes` before the first run ───────────────
SRC="/Volumes/Holder Mac"                               # source (verify exact name!)
DST="/Volumes/Got My BackUP/HolderMac_Backup"           # destination subfolder
MIRROR=0   # 0 = additive (safe, never deletes). 1 = true mirror (--delete).

# ── Offsite (3-2-1) for the tiny registry+notes — opt-in, best-effort ──────
# Only ~/.wecape snapshots go offsite (a few MB); the 4.6 TB footage stays local.
# Set RCLONE_REMOTE to YOUR rclone target — run `rclone listremotes` to get the
# exact remote name. The value below is a PLACEHOLDER; verify before relying on it.
OFFSITE=1                                               # 1 = push offsite, 0 = local-only
RCLONE_REMOTE="gdrive:WECAPE_Backup"                    # <remote>:<path> — VERIFY the remote name!
# ---------------------------------------------------------------------------

# Mode: --registry-only does just the ~/.wecape snapshot (+offsite), skipping the 4.6 TB job.
REG_ONLY=0
[ "${1:-}" = "--registry-only" ] && REG_ONLY=1

LOG="$HOME/wecape_holdermac_backup_$(date +%Y%m%d_%H%M%S).log"
RSYNC="/usr/bin/rsync"   # Apple's stock rsync: -E preserves HFS+ metadata/forks

# ── ~/.wecape protection (registry + annotations) ───────────────────────────
# wecape.db (production history) and annotations.db (your human notes — NOT
# regenerable) live in ~/.wecape: tiny but critical. We snapshot them to the
# same backup drive on EVERY run, before the big 4.6 TB job, so they're safe
# even when Holder Mac isn't mounted. SQLite is snapshotted via the online
# .backup API — consistent even if a CAPTURE run is writing right now; a plain
# cp/rsync of a live .db can capture a torn write and back up a corrupt file.
WECAPE_DIR="$HOME/.wecape"
REG_DST_SUB="wecape_Backup"          # destination subfolder (registry + annotations)
REG_KEEP=14                          # retain this many timestamped snapshots (tiny files)

backup_wecape() {
  local base="$1" snap stamp rel out sqlite chk
  [ -d "$WECAPE_DIR" ] || { echo "  (no $WECAPE_DIR yet — nothing to snapshot)"; return 0; }
  stamp="$(date +%Y%m%d_%H%M%S)"
  snap="$base/$stamp"
  mkdir -p "$snap"
  sqlite="$(command -v sqlite3 || true)"
  echo "  ~/.wecape snapshot -> $snap"
  # 1) SQLite databases via the consistent online .backup API + integrity check.
  while IFS= read -r db; do
    rel="${db#"$WECAPE_DIR"/}"; out="$snap/$rel"; mkdir -p "$(dirname "$out")"
    if [ -n "$sqlite" ] && "$sqlite" "$db" ".backup '$out'" 2>/dev/null; then
      chk="$("$sqlite" "$out" 'PRAGMA integrity_check;' 2>/dev/null | head -1)"
      echo "    ✓ $rel  (integrity: ${chk:-?})"
    else
      cp -p "$db" "$out"
      echo "    ⚠ $rel copied as-is (${sqlite:+.backup failed}${sqlite:-sqlite3 not found}) — may be inconsistent if a run is active"
    fi
  done < <(find "$WECAPE_DIR" -type f -name '*.db')
  # 2) Any non-db files (profiles, logs) via rsync.
  "$RSYNC" -a --exclude '*.db' --exclude '*.db-wal' --exclude '*.db-shm' \
           "$WECAPE_DIR/" "$snap/" >/dev/null 2>&1 || true
  ln -sfn "$snap" "$base/latest" 2>/dev/null || true
  # 3) Prune — keep the most recent REG_KEEP timestamped snapshots.
  ls -1dt "$base"/20*/ 2>/dev/null | tail -n +$((REG_KEEP+1)) \
    | while IFS= read -r old; do rm -rf "$old"; done
  echo "    kept $(ls -1d "$base"/20*/ 2>/dev/null | wc -l | tr -d ' ') snapshot(s); restore from $base/latest"
}

# Offsite (3-2-1): mirror the local registry/notes snapshots to a cloud remote.
# Best-effort and non-fatal — the local snapshot already succeeded before this runs.
push_offsite() {
  local src="$1"
  [ "$OFFSITE" = 1 ] || { echo "  (offsite disabled — OFFSITE=0)"; return 0; }
  command -v rclone >/dev/null 2>&1 || { echo "  (rclone not found — skipping offsite; install rclone or set OFFSITE=0)"; return 0; }
  [ -n "$RCLONE_REMOTE" ] || { echo "  (RCLONE_REMOTE unset — skipping offsite)"; return 0; }
  echo "  Offsite push -> $RCLONE_REMOTE  (rclone copy; additive — never deletes, symlinks skipped)"
  if rclone copy "$src" "$RCLONE_REMOTE" --skip-links --transfers 4 --checkers 8 --quiet; then
    echo "    ✓ offsite copy updated"
  else
    echo "    ⚠ offsite push failed — local snapshot is still safe. Check 'rclone listremotes', the RCLONE_REMOTE name, and network."
  fi
}

echo "============================================================"
echo "  W.E. C.A.P.E. Asset Backup — $(date)"
echo "  Source: $SRC"
echo "  Dest:   $DST"
echo "  Log:    $LOG"
echo "============================================================"

# ── Critical-small backup FIRST: registry + annotations ─────────────────────
# Snapshot to an always-available INTERNAL staging dir so the frequent job never
# depends on an external drive; push that offsite (cloud, reachable regardless);
# then mirror to Got My BackUP when it's mounted. Internal + offsite means the
# registry/notes are protected even if the external drive is unplugged.
STAGE="$HOME/.wecape_snapshots"
backup_wecape "$STAGE"
push_offsite "$STAGE"

DST_VOL="$(dirname "$DST")"
if [ -d "$DST_VOL" ]; then
  mkdir -p "$DST_VOL/$REG_DST_SUB"
  if "$RSYNC" -a --delete "$STAGE/" "$DST_VOL/$REG_DST_SUB/" >/dev/null 2>&1; then
    echo "  ✓ mirrored snapshots to $DST_VOL/$REG_DST_SUB"
  else
    echo "  ⚠ external mirror to $DST_VOL failed (internal + offsite copies still made)"
  fi
else
  echo "  (Got My BackUP not mounted — internal + offsite copies made; external mirror skipped)"
fi

if [ "$REG_ONLY" = 1 ]; then
  echo
  echo "✓ Registry-only backup complete — $(date)"
  exit 0
fi

# ── Full mode: the 4.6 TB Holder Mac job needs the external destination ─────
if [ ! -d "$DST_VOL" ]; then
  echo "✗ Destination drive not mounted: $DST_VOL (required for the Holder Mac backup)"
  exit 1
fi

# ── Pre-flight: Holder Mac source mounted? ──────────────────────────────────
if [ ! -d "$SRC" ]; then
  echo
  echo "✓ Registry safe (internal + offsite + external). Holder Mac source not mounted ($SRC)"
  echo "  — skipping the 4.6 TB volume backup. Mount it and re-run to protect the footage."
  echo "  (If the name is wrong, run 'ls /Volumes' and fix SRC — watch for spaces.)"
  exit 0
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
