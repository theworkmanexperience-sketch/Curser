# Asset Protection Backup — Holder Mac → Got My BackUP

**W.E. C.A.P.E. Principle #1: No asset exists until it exists in two locations.**

Closes the highest-risk gap in the ecosystem: the `Holder Mac` volume (4.6 TB of
production content + legal docs) currently has **zero backup**, and shares a
failure domain (`disk12`) with the 10TB and Time Machine volumes. The footage is
the one irreplaceable asset — this puts a second copy on the idle `Got My BackUP`
drive (4.8 TB free).

It **also** snapshots `~/.wecape/` — your production registry (`wecape.db`) and your
notes (`annotations.db`) — to the same drive on every run, *before* the big job, so the
small-but-critical data is protected even when Holder Mac isn't mounted. See
**Registry + annotations** below.

## One-time setup

1. **Confirm the source name.** Volume names vary; the Holder Mac volume may show
   as `Holder Mac`, `Untitled`, etc.
   ```bash
   ls /Volumes
   ```
   Open `scripts/backup_holder_mac.sh` and set `SRC` to the exact name.

2. **First run (manual, foreground).** This copies all 4.6 TB — it takes hours.
   Keep the Mac awake and both drives mounted.
   ```bash
   cd ~/Curser/we-cape
   bash scripts/backup_holder_mac.sh
   ```
   It is read-only on the source and additive on the destination (deletes nothing).

3. **Verify** when it finishes (the script prints this command; empty output = identical):
   ```bash
   /usr/bin/rsync -avEn --delete "/Volumes/Holder Mac/" "/Volumes/Got My BackUP/HolderMac_Backup/"
   ```

## Automatic weekly backup (optional, recommended)

Runs on **your Mac** via `launchd` (this can't be scheduled from Cowork — that
environment has no access to your `/Volumes` drives).

```bash
cp scripts/com.wecape.holdermacbackup.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.wecape.holdermacbackup.plist
launchctl list | grep wecape           # confirm it's registered
```
Default: Sunday 03:00 (incremental runs are fast). Edit the plist to change the
time, or delete the `<Weekday>` key for a daily backup. Logs land in
`~/Library/Logs/wecape_holdermac_backup.*.log`.

To stop automation:
```bash
launchctl unload ~/Library/LaunchAgents/com.wecape.holdermacbackup.plist
```

## Registry + annotations (`~/.wecape`)

The registry (`wecape.db`) and your notes (`annotations.db`) are tiny but critical, so they back up
on a **separate, frequent** schedule from the 4.6 TB footage — to three places:

1. **Internal staging** (`~/.wecape_snapshots/<timestamp>/`) — always available, so the backup never
   depends on an external drive being plugged in.
2. **Offsite** (cloud, via `rclone`) — reachable regardless of which drives are mounted.
3. **Got My BackUP** (`wecape_Backup/`) — mirrored as a bonus *when that drive is present*.

The last **14** snapshots are kept at each tier (a few MB each). Run standalone anytime:
```bash
bash scripts/backup_holder_mac.sh --registry-only     # snapshot + offsite; skips the 4.6 TB job
```

- **SQLite is snapshotted with the online `.backup` API**, not a file copy — it produces a
  *consistent* database even if a CAPTURE run is writing at that moment (a plain `cp`/`rsync` of a
  live `.db` can capture a torn write). Each snapshot is verified with `PRAGMA integrity_check`; the
  first real run should print `(integrity: ok)`. If `sqlite3` is missing it falls back to a copy and says so.
- **`annotations.db` is the one truly irreplaceable file** — nothing can regenerate your notes.
  (`wecape.db` is valuable history; re-CAPTURE can't reproduce timestamps/runtimes.)

### Offsite (3-2-1) — one-time setup
With `OFFSITE=1` (default) each run `rclone copy`s new snapshots to `RCLONE_REMOTE`. It uses **copy,
not sync** — additive, so it *never deletes* on the remote (safe even if the path holds other data;
offsite copies accumulate but are only MBs). Confirm your remote name once and set it atop the script:
```bash
rclone listremotes        # e.g. prints "gdrive:" — then set RCLONE_REMOTE="gdrive:WECAPE_Backup"
```
Point it at a **dedicated** path (the default `…:WECAPE_Backup` is its own folder). Missing
rclone/remote → it skips with a warning; internal + external copies still succeed. `OFFSITE=0` disables.

### Automatic daily registry backup (recommended)
```bash
cp scripts/com.wecape.registrybackup.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.wecape.registrybackup.plist
launchctl list | grep registrybackup
```
Runs `--registry-only` **daily at 12:30** (and once at load). For **hourly**, delete the `<Hour>` key
in the plist — but then raise `REG_KEEP` in the script (default 14 ≈ 14 hours hourly / ≈ 2 weeks daily).
Logs: `~/Library/Logs/wecape_registry_backup.*.log`.

- **Restore** (point-in-time): `latest` points at the newest snapshot at any tier.
  ```bash
  cp -a ~/.wecape_snapshots/latest/.  ~/.wecape/                       # from internal staging
  cp -a "/Volumes/Got My BackUP/wecape_Backup/latest/."  ~/.wecape/    # or the external mirror
  ```
  Or pull a specific `<timestamp>/` to roll back a bad edit.

## Honest caveats

- **Tight fit:** 4.6 TB into ~4.8 TB free leaves little headroom. The script warns
  if under 300 GB remains — plan a larger destination before the gap closes.
- **`Got My BackUP` already holds ~184 GB** of other data; the backup goes into a
  dedicated `HolderMac_Backup/` subfolder so nothing collides.
- **The 4.6 TB footage is still same-machine only.** The Holder Mac → Got My BackUP copy protects
  against a single *drive* failure, not theft/fire/flood — both drives hang off the Mac Studio. The
  **registry + notes now go offsite** (above), so the small critical data is 3-2-1; the footage's
  offsite copy (to the 20 TB Google Drive) remains a future step given its size.
- HFS+ metadata/resource forks are preserved via Apple's stock `/usr/bin/rsync -aE`.
  For a bulletproof GUI alternative, Carbon Copy Cloner does the same job.
