#!/usr/bin/env bash
# W.E. C.A.P.E. — Footage 3-2-1 backup  (backup_footage.sh)
#
# Verified mirror of priority footage folders → a target drive, + optional offsite
# (rclone crypt), + optional restore drill. Reuses mirror_verify.sh + restore_test.sh.
#
# THE GUARD (why this exists): it REFUSES to write unless the target is a real,
# WRITABLE, MOUNTED volume. It will not write to the boot disk (the unmounted-target
# "stray folder" trap we nearly hit), and it will not write to a read-only volume
# (a Time Machine disk like "Got My BackUP"). A scheduled run when the backup drive
# is absent fails SAFELY and logs — it never fills your system disk.
#
#   backup_footage.sh --target DIR --list sources.txt [--go] [--offsite] [--restore-test]
#   backup_footage.sh --target /Volumes/BACKUP/originals --source "/Volumes/10TB/O-SIX ..." --go
#
# DRY-RUN by default (previews, writes nothing). macOS bash-3.2 safe; handles spaces.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

TARGET=""; REMOTE=""; GO=0; OFFSITE=0; RESTORE=0; LOG="$HOME/wecape_backup.log"
SOURCES=()

# Offsite (rclone) hardening — applied to every offsite push:
#  --drive-stop-on-upload-limit : stop CLEANLY the instant Google's 750 GB/day cap is
#       hit (a clean fatal stop in seconds, not a 9-hour 403 storm). Resume next day.
#  --skip-links                 : don't chase symlinks (e.g. CapCut's Singleton* locks).
#  --exclude ...                : app cruft / OS metadata are NOT footage. Backing them
#       up inflates the file count → more Drive API calls → faster rate-limiting.
RCLONE_EXTRA=(--drive-stop-on-upload-limit --skip-links
  --exclude "**/CapCut/User Data/**"
  --exclude ".DS_Store"
  --exclude "**/.Spotlight-V100/**"
  --exclude "**/.fseventsd/**"
  --exclude "**/.Trashes/**"
  --exclude "**/.TemporaryItems/**")
usage(){ echo "usage: backup_footage.sh --target DIR [--source DIR ...] [--list FILE] [--remote REMOTE:path] [--go] [--offsite] [--restore-test] [--log FILE]"; }
while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET="${2%/}"; shift 2;;
    --source) SOURCES+=("${2%/}"); shift 2;;
    --list) [ -f "$2" ] || { echo "✗ list file not found: $2"; exit 2; }
            while IFS= read -r l; do l="${l%%#*}"; l="$(printf '%s' "$l" | sed 's/[[:space:]]*$//')"
                                     [ -n "$l" ] && SOURCES+=("${l%/}"); done < "$2"; shift 2;;
    --remote) REMOTE="$2"; shift 2;;
    --offsite) OFFSITE=1; shift;;
    --restore-test) RESTORE=1; shift;;
    --go) GO=1; shift;;
    --log) LOG="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "unknown arg: $1"; usage; exit 2;;
  esac
done
[ -n "$TARGET" ] || { echo "need --target"; usage; exit 2; }
[ "${#SOURCES[@]}" -gt 0 ] || { echo "need at least one --source or --list"; exit 2; }
# Footgun guard: --offsite with no --remote silently uploads NOTHING. Fail loudly.
if [ $OFFSITE -eq 1 ] && [ -z "$REMOTE" ]; then
  echo "✗ REFUSING: --offsite was given but no --remote REMOTE:path was set."
  echo "  Offsite would be SILENTLY SKIPPED (nothing uploaded). Add e.g."
  echo "    --remote gcrypt:originals"
  echo "  …or drop --offsite if you only want the local verified copy."
  exit 2
fi

# ── the guard, in two parts ─────────────────────────────────────────────────
# guard_mount: read-only check — resolve the target's mount point and REFUSE if it's
# the boot volume (/), i.e. the backup drive isn't mounted (the stray-folder trap).
guard_mount(){
  local t="$1" probe_dir mp
  probe_dir="$t"
  while [ ! -e "$probe_dir" ] && [ "$probe_dir" != "/" ]; do probe_dir="$(dirname "$probe_dir")"; done
  mp="$(df -P "$probe_dir" 2>/dev/null | awk 'NR==2{print $NF}')"
  [ -n "$mp" ] || { echo "✗ cannot resolve a mounted volume for target: $t"; return 1; }
  if [ "$mp" = "/" ] && [ "${WECAPE_TEST_ALLOW_ROOT:-0}" != "1" ]; then
    echo "✗ REFUSING: target '$t' resolves to the BOOT volume (/)."
    echo "  The backup drive is not mounted — writing here would fill your system disk"
    echo "  or create a stray folder. Mount the target drive and retry."
    return 1
  fi
  return 0
}

# guard_writable: creates the target dir and write-tests it (only in --go, so a
# dry-run writes nothing). Catches a READ-ONLY volume (e.g. a Time Machine disk).
guard_writable(){
  local t="$1" pf
  mkdir -p "$t" 2>/dev/null || { echo "✗ REFUSING: cannot create target dir (read-only volume?): $t"; return 1; }
  pf="$t/.wecape_write_test.$$"
  if ! ( : > "$pf" ) 2>/dev/null; then
    echo "✗ REFUSING: target is READ-ONLY (a Time Machine disk like 'Got My BackUP'?): $t"
    return 1
  fi
  rm -f "$pf" 2>/dev/null
  return 0
}

echo "════════════════════════════════════════════════════════════"
echo "  W.E. C.A.P.E. — Footage 3-2-1 Backup   [$( [ $GO -eq 1 ] && echo EXECUTE || echo DRY-RUN )]"
echo "  Target : $TARGET"
echo "  Offsite: $( [ $OFFSITE -eq 1 ] && echo "$REMOTE" || echo "(off)" )   Restore-test: $( [ $RESTORE -eq 1 ] && echo yes || echo no )"
echo "  Sources: ${#SOURCES[@]}"
echo "════════════════════════════════════════════════════════════"

if ! guard_mount "$TARGET"; then
  if [ $GO -eq 1 ]; then echo "  → refusing to execute. Fix the target and retry."; exit 3
  else echo "  → (dry-run continues; but --go would REFUSE this target)"; fi
fi
if [ $GO -eq 1 ] && ! guard_writable "$TARGET"; then
  echo "  → refusing to execute. Fix the target and retry."; exit 3
fi

fails=0
for src in "${SOURCES[@]}"; do
  if [ ! -d "$src" ]; then echo "⚠ skip (not a directory): $src"; fails=$((fails+1)); continue; fi
  name="$(basename "$src")"
  dest="$TARGET/$name"
  echo; echo ">>> $name"
  if [ $GO -eq 0 ]; then
    bash "$HERE/mirror_verify.sh" "$src" "$dest"                    # dry-run preview
    continue
  fi
  if ! bash "$HERE/mirror_verify.sh" "$src" "$dest" --go --log "$LOG"; then
    echo "  ✗ verify FAILED for '$name' — NOT trustworthy; skipping its offsite push."
    fails=$((fails+1)); continue
  fi
  if [ $RESTORE -eq 1 ]; then
    bash "$HERE/restore_test.sh" --source "$src" --backup "$dest" \
         --scratch "${TMPDIR:-/tmp}/wecape_rt/$name" \
         --log "$(dirname "$LOG")/RESTORE_TESTS.md" || { echo "  ✗ restore drill failed for '$name'"; fails=$((fails+1)); }
  fi
  if [ $OFFSITE -eq 1 ] && [ -n "$REMOTE" ]; then
    if command -v rclone >/dev/null 2>&1; then
      echo "  → offsite: rclone copy → $REMOTE/$name"
      rclone copy "$dest" "$REMOTE/$name" "${RCLONE_EXTRA[@]}" || {
        rc=$?
        if [ $rc -eq 7 ]; then
          echo "  ⏸ offsite HIT Google's daily upload cap (750 GB/day) — stopped cleanly."
          echo "     '$name' is partially uploaded; re-run tomorrow to resume (idempotent)."
        else
          echo "  ✗ offsite copy failed for '$name' (rclone exit $rc)."
        fi
        fails=$((fails+1))
      }
    else echo "  ⚠ rclone not found — offsite skipped for '$name'."; fi
  fi
done

echo; echo "────────────────────────────────────────────────────────────"
if [ $GO -eq 0 ]; then echo "  ✓ dry-run complete — nothing written. Re-run with --go to execute."; exit 0; fi
if [ $fails -eq 0 ]; then echo "  ✓ backup complete — all sources verified$( [ $OFFSITE -eq 1 ] && echo " + pushed offsite" )."; exit 0
else echo "  ✗ $fails issue(s) — see output above and $LOG."; exit 1; fi
