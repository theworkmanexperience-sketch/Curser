#!/usr/bin/env bash
# W.E. C.A.P.E. — Backup restore drill  (restore_test.sh)
#
# A backup you have never restored is a rumor. This restores a CANARY sample from a
# backup target (a local mirror OR an rclone remote) into a SCRATCH area and proves it
# matches the live SOURCE byte-for-byte (SHA-256). It NEVER touches SOURCE or the
# backup, and appends a PASS/FAIL row to RESTORE_TESTS.md (P3 auditability for backups).
#
# For an rclone-crypt remote the drill also proves the passphrase + remote are actually
# usable — i.e. it doubles as a passphrase-recovery rehearsal.
#
#   restore_test.sh --source SRC --backup BACKUP_DIR   --scratch DIR [--sample N] [--log F]
#   restore_test.sh --source SRC --rclone gcrypt:path  --scratch DIR [--sample N] [--log F]
#
# macOS bash-3.2 safe; handles spaces. Falls back sha256sum<->shasum.
set -uo pipefail

SRC=""; BACKUP=""; RCLONE=""; SCRATCH=""; SAMPLE=3; LOG="RESTORE_TESTS.md"
usage(){ echo "usage: restore_test.sh --source SRC (--backup DIR | --rclone REMOTE:path) --scratch DIR [--sample N] [--log F]"; }
while [ $# -gt 0 ]; do
  case "$1" in
    --source)  SRC="${2%/}"; shift 2;;
    --backup)  BACKUP="${2%/}"; shift 2;;
    --rclone)  RCLONE="$2"; shift 2;;
    --scratch) SCRATCH="${2%/}"; shift 2;;
    --sample)  SAMPLE="$2"; shift 2;;
    --log)     LOG="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "unexpected arg: $1"; usage; exit 2;;
  esac
done
[ -n "$SRC" ] && [ -n "$SCRATCH" ] || { echo "need --source and --scratch"; usage; exit 2; }
[ -n "$BACKUP" ] || [ -n "$RCLONE" ] || { echo "need --backup or --rclone"; usage; exit 2; }
[ -d "$SRC" ] || { echo "✗ source not a dir: $SRC"; exit 2; }

hashof(){ if command -v shasum >/dev/null 2>&1; then shasum -a 256 "$1" | awk '{print $1}';
          else sha256sum "$1" | awk '{print $1}'; fi; }

mkdir -p "$SCRATCH"
target="${RCLONE:-$BACKUP}"
echo "════════════════════════════════════════════════════════════"
echo "  W.E. C.A.P.E. — Restore Drill"
echo "  SOURCE : $SRC"
echo "  BACKUP : $target"
echo "  SCRATCH: $SCRATCH   (sample: $SAMPLE file(s))"
echo "════════════════════════════════════════════════════════════"

fail=0; ok=0; bytes=0
# Canary = first N files under SOURCE (relpaths). Loop runs in the current shell
# (process substitution) so counters survive.
while IFS= read -r rel; do
  [ -z "$rel" ] && continue
  rel="${rel#./}"
  mkdir -p "$SCRATCH/$(dirname "$rel")"
  if [ -n "$RCLONE" ]; then
    if ! rclone copyto "$RCLONE/$rel" "$SCRATCH/$rel" >/dev/null 2>&1; then
      echo "  ✗ restore FAILED (rclone): $rel"; fail=$((fail+1)); continue; fi
  else
    if [ ! -f "$BACKUP/$rel" ]; then echo "  ✗ NOT in backup: $rel"; fail=$((fail+1)); continue; fi
    cp "$BACKUP/$rel" "$SCRATCH/$rel"
  fi
  a=$(hashof "$SRC/$rel"); b=$(hashof "$SCRATCH/$rel")
  if [ "$a" != "$b" ]; then echo "  ✗ MISMATCH after restore: $rel"; fail=$((fail+1));
  else ok=$((ok+1)); bytes=$((bytes + $(wc -c < "$SRC/$rel"))); echo "  ✓ $rel"; fi
done < <(cd "$SRC" && find . -type f | head -n "$SAMPLE")

ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if [ $fail -eq 0 ] && [ $ok -gt 0 ]; then result="PASS"; else result="FAIL"; fi
if [ ! -f "$LOG" ]; then
  printf '# Restore Tests — W.E. C.A.P.E.\n\nProof that backups are actually restorable (P3).\n\n' > "$LOG"
  printf '| date | target | files_ok | bytes | result |\n|---|---|---|---|---|\n' >> "$LOG"
fi
printf '| %s | %s | %d | %d | %s |\n' "$ts" "$target" "$ok" "$bytes" "$result" >> "$LOG"

echo "────────────────────────────────────────────────────────────"
echo "  restored_ok=$ok  failed=$fail  →  $result   (logged to $LOG)"
[ "$result" = "PASS" ] || { echo "  ✗ restore drill FAILED — this backup is NOT proven restorable."; exit 1; }
echo "  ✓ backup proven restorable for the sampled files."
exit 0
