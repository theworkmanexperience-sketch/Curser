# W.E. C.A.P.E. — Storage Risk & Backup Plan
## Living doc · v0.2 · 2026-07-07 · owner: T. · extends SECURITY_RISK_ANALYSIS.md

> **The one sentence:** the irreplaceable asset this whole platform exists to protect —
> the raw multi-camera originals — currently lives on a **single striped enclosure with
> no real second copy**, and the "Time Machine backup" appears to sit on the **same
> physical device** as the thing it's backing up. That's not a backup; it's an illusion.
> Fix that before anything else.

This doc follows the data-loss-first threat model in `SECURITY_RISK_ANALYSIS.md`:
for a solo creator the dominant risk is **losing footage to hardware failure / human
error**, not intrusion. Everything below is ranked by *blast radius to the footage*.

---

## 0. VERIFIED TOPOLOGY (2026-07-05 — from live diskutil/df/tmutil/du)

Confirmed against the real machine; supersedes the June-22 map. Two earlier assumptions
were WRONG and are corrected here (this is why we verified before automating).

**THE SPOF — CONFIRMED (worse than a partition detail):**
`disk13` is a **single 20 TB USB enclosure** carved into four volumes:
- `10TB` (disk15s1) — **9.3 TB, the originals** — 94% full (642 GB free)
- `Holder Mac` (disk13s4) — **6 TB HFS+, production + LEGAL DOCS** — 84% full
- `timemachine` (disk16s1) — 3.9 TB, an **old** Time Machine — 99% full (dead weight)
- `200MB` (disk14s1) — stub
→ **One device failure loses the originals AND the legal docs AND that TM, simultaneously.**
`SMART Status: Not Supported` on all USB drives → **this disk will fail without warning.**

**CORRECTION 1 — NOT RAID 0.** No stripe; single enclosure, one `/dev/disk13`, no
AppleRAID. The earlier "RAID 0 doubles failure odds" claim (from the stale map) is
withdrawn. SPOF stands regardless (everything on one disk).

**CORRECTION 2 — Time Machine is on a SEPARATE disk but does NOT protect the footage.**
`tmutil` → TM targets **`Got My BackUP`** (disk12, separate 5 TB, 172 GB used, 4.4 TB
free). But TM backs up only the **internal Mac (~340 GB)** — the external 10 TB
originals are **not** in any backup. The originals currently have **zero copies of any
kind.** (The 99%-full `timemachine` volume on disk13 is a defunct TM on the same disk as
the source — useless.)

**Originals footprint ≈ 8.5 TB** (du on `/Volumes/10TB`): June 2024 **2.7 TB**, 2026
Harley Chronicles 1.1 TB, 2025 1.0 TB, O-SIX RYDER 12TH 976 GB, O-SIX RYDERZ 777 GB,
Harley Bagger World Cup 403 GB, O-SIX Community Service 218 GB, + others. `WE_FLOW_OUTPUT`
(150 GB) is regenerable proxies.

**Capacity reality:** **no attached drive can hold a full second copy of 8.5 TB.**
`Got My BackUP` 4.4 TB free (also the TM disk); `G-DRIVE SSD` (disk6) ~3.8 TB free
(nearly empty, SEPARATE disk); `WE_CAPE_OUTPUT` NVMe (disk9, PCIe, SMART Verified)
3.2 TB free. → prioritize now, buy ≥ 12 TB for the rest (§6).

---

## 1. Current state (from documented map — confirm with §0)

| Volume | Size | Free | Role | Backup today | Structural risk |
|--------|------|------|------|--------------|-----------------|
| 10TB My Book Duo (**RAID 0**) | 10 TB | ~0.8 TB | **Active originals** (O-SIX, all shoots) | Time Machine → **same disk? [VERIFY]** | RAID 0 = either drive dies → **total loss**; ~92% full |
| timemachine | 4 TB | ~0.1 TB | Time Machine target | — | **[VERIFY]** same physical disk as 10TB → backup is theater; also 99% full = TM pruning old history |
| Holder Mac (HFS+) | 6 TB | 1.4 TB | Production content + **legal docs** | **weekly** via `backup_holder_mac.sh` → [VERIFY target] | single HFS+ volume; zero-backup if the script's target is unset/offline |
| WE_CAPE_OUTPUT (Samsung 990 PRO NVMe) | 4 TB | ~3.5 TB | Proxies + source copies (regenerable) | — | proxies are **regenerable** from originals → lower priority |
| Got My BackUP (WD 5TB) | 5 TB | ~4.8 TB | *intended* backup dest | backs up **almost nothing** | **4.8 TB of idle capacity** — the obvious near-term target |
| G-DRIVE SSD (4TB) | 4 TB | ? | MG-02 proxies | — | **disconnected** → proxies inaccessible |
| ~/.wecape registry | — | — | SQLite registry | **3-2-1** (internal + rclone crypt offsite + external mirror) | already the best-protected asset |
| Google Drive (20TB plan) | 20 TB | large | offsite (rclone **crypt**) | — | 3.3 TB archive present; **room for footage offsite** |

**What's actually a backup vs. theater:**
- ✅ **Registry** — genuinely 3-2-1 (the work we already did).
- ⚠️ **Holder Mac** — a weekly script exists, but its **target must be verified** (and restore-tested — §4).
- ❌ **The raw originals (10TB)** — *this is the gap.* No confirmed independent second copy. Time Machine to the same enclosure (if §0 confirms) protects against nothing that matters (drive death, enclosure death, theft, fire).
- ❌ **G-DRIVE** — disconnected; whatever's only there is at risk of being forgotten.

---

## 2. Single points of failure, ranked by blast radius

1. **The disk13 20 TB enclosure (originals + legal docs + old TM on ONE device).**
   `10TB` (8.5 TB originals), `Holder Mac` (legal docs), and the defunct `timemachine`
   all live on this single physical disk. One enclosure/controller/drive failure loses
   **all three at once**, and with **no SMART** there's no early warning. The originals
   have **zero backup today**. **This is the top risk. Full stop.**
2. **Holder Mac (legal docs + production content).** On the SPOF disk (disk13), single
   HFS+ volume. Loss includes *legal documents* — not re-shootable. Legal docs are small
   and irreplaceable → **fastest highest-value win is to back these up first** (they fit
   anywhere, offsite immediately).
3. **Capacity crisis compounding risk.** 10TB at ~0.8 TB free means the *next* shoot may
   not fit → footage gets parked in ad-hoc places (a laptop, a random drive) → falls
   outside any backup. A full disk is a data-loss risk, not just an inconvenience.
4. **G-DRIVE disconnected.** Anything unique to it (MG-02 proxies) is inaccessible and
   silently rotting out of awareness.

---

## 3. Remediation — prioritized, mapped to hardware you already own

Principle: **3-2-1 for the originals** — **3** copies, on **2** different media/devices,
**1** offsite. We can start today with owned hardware; a purchase closes the last gap.

### Phase A — This week, no purchase (stop the bleeding). Targets are now grounded.
Time Machine already lives on a separate disk (`Got My BackUP`) — no change needed there.
Use **`G-DRIVE SSD` (disk6, ~3.8 TB free, nearly empty, SEPARATE physical disk)** as the
local second-copy target; keep `Got My BackUP` for Time Machine.

1. **Legal docs + Holder Mac essentials FIRST** (small, irreplaceable, on the SPOF disk):
   `mirror_verify.sh "/Volumes/Holder Mac/<legal>" "/Volumes/G-DRIVE SSD/backup/Holder_legal" --go`
   then `rclone crypt` the same offsite. Minutes of work, removes the scariest exposure.
2. **Verified second copy of priority originals → G-DRIVE** (fits the active + recent
   shoots, e.g. O-SIX Community Service 218 GB, O-SIX 12TH 976 GB, recent Harley):
   `mirror_verify.sh "/Volumes/10TB/O-SIX RYDERZ MC Community Service" \
      "/Volumes/G-DRIVE SSD/originals/O-SIX_Community_Service" --go --log ~/backup.log`
   then `restore_test.sh` to prove it. (Big masters like *June 2024* 2.7 TB exceed
   G-DRIVE — those wait for the purchased drive in §6.)
3. **Push priority originals + legal offsite (encrypted).** rclone **crypt** (`gcrypt:`)
   to Google Drive (16 TB headroom) — the "1 offsite" in 3-2-1; survives fire/theft.
4. **Retire the defunct `timemachine` volume on disk13** (99% full, superseded by
   `Got My BackUP`). It only consumes space on the SPOF disk. (Doesn't reduce SPOF, but
   removes dead weight; do NOT repurpose it as a backup target — it's on the SPOF disk.)
5. **Check `FreeAgent GoFlex`** (95% full, flagged corrupt): `reconcile.py` / a read pass
   to see if anything unique is trapped there before it dies.

### Phase B — Structural (reduce probability, not just add copies)
5. **Get the originals off RAID 0.** RAID 0 is the wrong topology for irreplaceable data.
   Options: reconfigure the My Book Duo to **RAID 1 (mirror)** — halves capacity to ~9 TB
   usable but survives one drive failure — or move originals to a single large drive that
   is then backed up (a mirror you *manage* beats RAID 0 you *trust*). Decision needed
   (§6) because RAID 1 reconfigure **erases the array** — copies in Phase A must exist first.
6. **Capacity headroom.** At 92% full the 10TB is effectively out of room for redundancy.
   A **dedicated backup drive sized ≥ total originals** (see §6 sizing) is the real fix;
   until then, Phase A copies to Got My BackUP + offsite are the stopgap.

### Phase C — Formalize
7. **One backup script for the footage**, mirroring the registry's 3-2-1 pattern:
   local mirror (verified) + offsite rclone crypt, scheduled (launchd plist like the
   registry/Holder Mac ones). I can build `backup_footage.sh` + plist on the same model
   as `backup_holder_mac.sh`.
8. **Backup dashboard signal.** Surface "last verified backup per volume" so a stale/failed
   backup is *visible*, not assumed (extends the dashboard, read-only).

---

## 4. Backup restore testing (a backup you haven't restored is a rumor)

The most common backup failure is discovering at restore time that it never worked.
Procedure to adopt (run quarterly + after any backup-config change):

1. **Pick a canary:** a non-critical file set (e.g. one shoot's proxies, or a tagged
   `RESTORE_TEST/` folder) present in each backup target.
2. **Restore to a scratch location** (never over the original):
   - Local mirror: copy back from `Got My BackUP` → scratch; `shasum` compare to source.
   - Offsite: `rclone copy gcrypt:<path> /tmp/restore_test` → verify checksums (proves the
     crypt passphrase + remote are actually usable — the passphrase is stored **off-machine**;
     a restore test is also a passphrase-recovery drill).
   - Holder Mac: restore a sample from `backup_holder_mac.sh`'s target; checksum compare.
3. **Verify integrity, not just presence:** `shasum -a 256` on restored vs. source; a
   byte-mismatch is a hard fail.
4. **Time it & log it:** record date, target, bytes, pass/fail into a `RESTORE_TESTS.md`
   log (P3 auditability for backups, ISO-9001-style).
5. **Registry restore drill:** `~/.wecape` is 3-2-1; prove it — restore `wecape.db` from the
   offsite copy to scratch and open it read-only (`sqlite3 file:copy?mode=ro`).

I can build `restore_test.sh` that automates the checksum-compare + logs to `RESTORE_TESTS.md`.

---

## 5. External-drive encryption

Status (from the D1–D4 security decisions, already implemented):
- **FileVault: ON** (internal disk encrypted at rest) — verified by `security_check.py`.
- **Offsite is encrypted:** rclone **crypt** (`gcrypt:`) encrypts filenames + contents
  before they touch Google Drive — cloud sees ciphertext only.

Remaining decision — **drives that physically leave the premises** (a portable original
or backup taken offsite, handed to a client, or stored elsewhere):
- **Recommendation:** any drive that leaves = **encrypted at rest** (APFS-encrypted volume
  on macOS, or VeraCrypt for cross-platform). Weigh against: an encrypted drive that loses
  its passphrase is *unrecoverable* — so the passphrase goes in the same **off-machine**
  store as the rclone crypt passphrase (per `CREDENTIAL_INVENTORY.md`), and is part of the
  restore-test drill (§4).
- **Do NOT encrypt the primary on-desk working drives** beyond FileVault — encryption there
  adds passphrase-loss risk without a threat model to justify it (they don't leave).

Decision to confirm: **encrypt-drives-that-leave = yes/no**, and **which drives count as
"leave"** (portable backups, client handoffs).

---

## 6. Open decisions (need your input / a purchase)

1. **RAID 0 → RAID 1, or single-drive + managed mirror?** RAID 1 halves the 10TB to ~9 TB
   usable; reconfigure **erases** the array (Phase-A copies must exist first). Or move to a
   larger single drive + a separate backup drive.
2. **Sizing the dedicated backup drive — now known.** Originals ≈ **8.5 TB** and the SPOF
   disk is nearly full. No attached drive fits a full second copy. The **≥ 12 TB** floor
   fits *today's* backlog only; for an **annual-usage / 2029 horizon** the number is
   **24 TB single (or a 2-bay DAS)** — see **§6a** for the corrected growth rate and the
   projection. Plan **two** (on-desk mirror + rotated offsite). G-DRIVE only covers the
   priority subset in Phase A.
3. **Offsite scope.** All originals to Google Drive, or only "keeper" shoots? (Bandwidth +
   the 20TB plan ceiling — 3.3 TB already used.)
4. **Encryption for drives that leave** (§5) — confirm the policy.

---

## 6a. Capacity projection 2026–2029 (annual-usage sizing · 2026-07-07)

Sizing by *annual footage rate*, from a live `du` of `/Volumes/10TB`. **Correction:** an
earlier read annualized the 8.5 TB backlog over ~10 months (→ 8–10 TB/yr) — WRONG. The
backlog actually spans **2023 → 2026 (~3+ years)**, so the real generation rate is far lower:

| Year | Footage | Basis |
|------|---------|-------|
| 2023 | ~0.08 TB | `2023/` |
| 2024 | ~2.9 TB | `2024/` 200 GB + `June 2024/` **2.7 TB** (verify — a third of the whole backlog; likely dedupe-heavy) |
| 2025 | ~2.2 TB | `2025/` 1.0 TB + `12TH ANNIVERSARY` 976 GB + `2025_EARLY_2026` 201 GB |
| 2026 (to Jul) | ~1.4 TB | `2026 HD Chronicles` 1.1 TB + `Community Service` 218 GB + `Sat_3-14` 58 GB |
| undated | ~1.2 TB | `O-SIX RYDERZ` 777 GB + `Harley Bagger` 403 GB |

**Corrected annual rate ≈ 2.5–3.5 TB/yr, trending up** (2026 pacing ~2.6 TB annualized).

**New footage per year (TB):**

| Year | Flat (3 TB) | Base (+15%/yr) | Aggressive (+30%/yr) |
|------|-------------|----------------|----------------------|
| 2026 | 3.0 | 3.0 | 3.0 |
| 2027 | 3.0 | 3.5 | 3.9 |
| 2028 | 3.0 | 4.0 | 5.1 |
| 2029 | 3.0 | 4.6 | 6.6 |
| **2026–29 total** | **12.0** | **15.1** | **18.6** |

**Cumulative archive size (backlog ~6.4 TB through 2025 + new, TB):**

| End of | Flat | Base | Aggressive |
|--------|------|------|------------|
| 2026 | 9.4 | 9.4 | 9.4 |
| 2027 | 12.4 | 12.9 | 13.3 |
| 2028 | 15.4 | 16.9 | 18.4 |
| **2029** | **18.4** | **21.5** | **25.0** |

**Purchase sizing (never fill past ~80%, per copy):**
- The **≥12 TB** floor fits *today's* backlog only — full within ~1 year of growth.
- **For a 2029 horizon: a 24 TB single drive** (base case ~21.5 TB → ~88% full by 2029),
  or a **2-bay/4-bay DAS** (2× 20–24 TB) so the backup tier is itself redundant + expandable.
- If resolution / camera count climbs (Insta360 X5 8K, the new **OM System OM-1**), plan for
  the **aggressive** column (~25 TB by 2029) and buy the 2-bay now rather than re-buy in 2028.

**⚠ FORMAT THE BACKUP DRIVE CASE-SENSITIVE APFS.** The originals on `/Volumes/10TB` are on
**Case-sensitive APFS** and contain real files that differ only by case (verified: the
Harley shoot has both `IMG_7893.MOV` 90.9 MB and `IMG_7893.mov` 86.2 MB — two distinct
clips). A **case-insensitive** target (like the current `WE_CAPE_OUTPUT` NVMe) can hold only
one of each such pair — the other is **silently lost** from the backup, and the byte-for-byte
verify will (correctly) refuse to certify it. The dedicated backup drive **must** be
formatted **APFS (Case-sensitive)** to faithfully mirror the source. Interim note: offsite
(rclone crypt → Drive) is unaffected — encrypted names keep both — so the cloud copy is more
complete than the case-insensitive NVMe for these pairs. Scan scope before buying:
`find "/Volumes/10TB" -type f | tr '[:upper:]' '[:lower:]' | sort | uniq -d`.
**Scan result (2026-07-08):** only two collisions — the `IMG_7893.MOV`/`.mov` footage pair
(real) and a `.DS_Store` (junk). The `.DS_Store` hit reveals **two case-variant directories**,
`Holder/` (16 GB) and `HOLDER/` (450 GB), which a case-insensitive target would MERGE.
→ case-sensitive APFS is **confirmed mandatory**; and separately, **investigate whether
`HOLDER/` (450 GB) is an accidental/partial duplicate of `Holder/`** (potential reclaim +
data-hygiene) before copying 8.5 TB.

**3-2-1 multiplier:** the *logical* archive ≈ 21 TB by 2029, but 3-2-1 = **2 local copies +
1 offsite**, so budget **~2× 24 TB** drives + Drive offsite.

**Offsite is quota-bound, not just bandwidth-bound:** Google Drive caps uploads at
**750 GB/day** (confirmed live — the priority run hit it and `--drive-stop-on-upload-limit`
now stops cleanly). One-time ~8 TB backlog ≈ **~11 upload-days**; steady-state incremental is
only ~3–5 TB/yr ≈ **under a week/year**. So Drive can stay current *after* the backlog clears,
but can never be the primary for the bulk — the **local 24 TB drive is the real backup**;
offsite is the crown-jewel + incremental layer.

**Shrink the number before buying:** run `reconcile.py --hash` on `/Volumes/10TB` (esp.
`June 2024/` 2.7 TB) to reclaim byte-identical duplicates, and exclude regenerable output
(`WE_FLOW_OUTPUT` 150 GB, `Variations` 102 GB) from the archive footprint — either could cut
the backlog by a TB or more and lower the drive size you need.

---

## 7. Immediate action checklist (once §0 is verified)

- [ ] Confirm physical topology (§0) — is TM on the 10TB enclosure? Is it RAID 0?
- [ ] Repoint Time Machine to a *different* physical drive (Got My BackUP).
- [ ] Verified second copy of current production originals → Got My BackUP (and/or NVMe).
- [ ] Offsite: rclone crypt the current production originals → Google Drive.
- [ ] Reconnect + inventory G-DRIVE; fold unique data into the backup set.
- [ ] Restore-test one canary from each target; log to RESTORE_TESTS.md.
- [ ] Decide RAID 1 vs. dedicated backup drive; size it (§6).
- [ ] Confirm encrypt-drives-that-leave policy.

Tooling status:
- ✅ **`mirror_verify.sh`** — BUILT (2026-07-05). Verified folder→folder copy (SHA-256,
  additive/never-deletes, dry-run default, `--verify-only` bit-rot check). Tested incl.
  corruption detection. **Ready to make the first verified second copy of the originals.**
- ✅ **`restore_test.sh`** — BUILT. Canary restore from a local mirror or rclone remote →
  scratch → checksum vs. live source; logs PASS/FAIL to `RESTORE_TESTS.md`. Tested incl.
  bad-backup failure.
- ✅ **`backup_footage.sh` + `com.wecape.footagebackup.plist`** — BUILT (2026-07-05).
  Verified mirror of a priority-folder list (`backup_sources.txt`) → target drive +
  offsite (rclone crypt) + restore drill, reusing the primitives. **GUARD:** refuses to
  write unless the target is a real, writable, mounted volume — never the boot disk
  (the unmounted-target stray trap), never a read-only TM disk. Dry-run default. plist
  is a scheduled template (weekly), safe when the drive is absent (guard refuses + logs).
  Repoint `--target` from WE_CAPE_OUTPUT (interim) to the ≥12 TB drive when it lands.

Both primitives are topology-agnostic (path args), so you can start the verified copy to
`Got My BackUP` today:
```bash
chmod +x scripts/mirror_verify.sh scripts/restore_test.sh   # one-time
# preview first (writes nothing):
scripts/mirror_verify.sh "/Volumes/10TB/O-SIX RYDERZ MC Community Service" \
    "/Volumes/Got My BackUP/originals/O-SIX_Community_Service"
# then execute + verify:
scripts/mirror_verify.sh "/Volumes/10TB/O-SIX RYDERZ MC Community Service" \
    "/Volumes/Got My BackUP/originals/O-SIX_Community_Service" --go --log ~/backup.log
# prove it restores:
scripts/restore_test.sh --source "/Volumes/10TB/O-SIX RYDERZ MC Community Service" \
    --backup "/Volumes/Got My BackUP/originals/O-SIX_Community_Service" --scratch /tmp/rt
```
