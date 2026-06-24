# iPhone Photos + Videos → External Drive (full originals)

**Your situation:** "Optimize iPhone Storage" is **ON**, so the full-resolution
originals live in **iCloud** — only smaller copies are on the phone. A plain
Image Capture import would archive *compressed* versions. This workflow gets the
**true originals** onto a drive, then organizes and verifies them.

> Don't use `Got My BackUP` as the target — it's being consumed by the Holder Mac
> backup. Pick a drive with real headroom (exported originals can be 100s of GB).

## Step 1 — Get the originals out of iCloud, onto the drive

The Mac's internal SSD has little free space, so pull originals **straight to the
external drive** via the Photos app (it downloads each original from iCloud as it
exports):

1. On the Mac, open **Photos** (signed into the same Apple ID, good internet).
2. Edit → **Select All** (or pick a date range to do it in batches).
3. **File → Export → Export Unmodified Original…**
4. Set: Subfolder Format = **Moment Name** or **None**, File Naming = **Use Filename**.
5. Choose a folder on your target drive, e.g. `/Volumes/<drive>/T_iPhone_Originals/`.
6. Let it run. Large libraries take a while — each original downloads from iCloud.

*(Alternative if you'd rather have the whole library local first: Photos →
Settings → iCloud → "Download Originals to this Mac" — but only if the library
fits on the destination; relocate the library to the external drive first if it's
large.)*

## Step 2 — Organize + de-duplicate + verify

Run the organizer on the exported folder. Dry-run first (writes nothing):

```bash
cd ~/Curser/we-cape
bash scripts/organize_iphone_backup.sh "/Volumes/<drive>/T_iPhone_Originals" "/Volumes/<drive>/T_iPhone_Archive"
```
Review the printed summary + the `_manifest_*.csv`, then apply:
```bash
bash scripts/organize_iphone_backup.sh "/Volumes/<drive>/T_iPhone_Originals" "/Volumes/<drive>/T_iPhone_Archive" --apply
```
Result: photos + videos sorted into `YYYY/MM/`, duplicates routed to
`_duplicates/`, and a CSV manifest of every file (date, kind, hash, destination).

## Step 3 — Confirm it's complete

On the iPhone: **Settings → General → iPhone Storage → Photos** (or the count at
the bottom of the Photos app) shows how many photos + videos exist. Compare to the
organizer's `Photos:` + `Videos:` totals. Match = full backup.

## Honest caveats

- **iCloud download is the slow part** — gated by your internet and library size,
  not the drive. Do it in date-range batches if it's huge.
- **Live Photos / edits:** "Export Unmodified Original" gives the original capture
  (and a paired `.MOV` for Live Photos) — not your in-Photos edits. Use "Export"
  (not unmodified) if you also want edited versions.
- **Still not offsite.** This is a second copy on a local drive. Your 20 TB Google
  Drive is the natural third, offsite copy once this local archive exists (3-2-1).
- **Don't delete from the phone/iCloud** until Step 3's counts match and you've
  spot-checked a few files open correctly.
