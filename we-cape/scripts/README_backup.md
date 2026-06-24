# Asset Protection Backup — Holder Mac → Got My BackUP

**W.E. C.A.P.E. Principle #1: No asset exists until it exists in two locations.**

Closes the highest-risk gap in the ecosystem: the `Holder Mac` volume (4.6 TB of
production content + legal docs) currently has **zero backup**, and shares a
failure domain (`disk12`) with the 10TB and Time Machine volumes. The footage is
the one irreplaceable asset — this puts a second copy on the idle `Got My BackUP`
drive (4.8 TB free).

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

## Honest caveats

- **Tight fit:** 4.6 TB into ~4.8 TB free leaves little headroom. The script warns
  if under 300 GB remains — plan a larger destination before the gap closes.
- **`Got My BackUP` already holds ~184 GB** of other data; the backup goes into a
  dedicated `HolderMac_Backup/` subfolder so nothing collides.
- **Same-machine backup ≠ offsite.** This protects against a single *drive* failure,
  not theft/fire/flood. A true 3-2-1 strategy adds an offsite/cloud copy (you have
  the 20 TB Google Drive — a future step once the local second copy exists).
- HFS+ metadata/resource forks are preserved via Apple's stock `/usr/bin/rsync -aE`.
  For a bulletproof GUI alternative, Carbon Copy Cloner does the same job.
