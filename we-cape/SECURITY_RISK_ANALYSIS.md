# SECURITY_RISK_ANALYSIS.md — W.E. C.A.P.E.
## Living security north star · v1.0 · 2026-07-03

This is a governance document, peer to `UI_Dashboard_Design_Guidelines_v2.md` and the
compliance notes: every new feature (dashboard, wizard, Health Report, cloud sync) is
checked against it. It is **grounded in the actual repository and storage map**, not a
generic checklist. Items I could not verify from the code are marked **[VERIFY]** — they
are questions for the operator, not assertions.

Guiding truth, stated plainly: **for a one-person creator studio, the dominant risk is
data *loss*, then *credential* exposure, then remote intrusion — in that order.** Exotic
mitigations (e.g. post-quantum crypto at J3) must not precede the basics (working
backups, key handling, full-disk encryption). This document is ordered by that reality.

---

## 1. Asset & Data-Flow Inventory (what exists today)

### 1.1 Data assets, ranked by *recoverability* (not size)

| Asset | Location | Recoverable? | Sensitivity | Notes |
|-------|----------|--------------|-------------|-------|
| `annotations.db` | `~/.wecape/annotations.db` (internal SSD) | **NO — irreplaceable** | Human notes (may be sensitive) | Deliberately outside the deterministic registry. **Crown jewel for backup.** |
| Original footage | External drives (10TB, WE_CAPE_OUTPUT NVMe, Holder Mac) | Only if a second copy exists | Client/creator content | Two-copy rule enforced at *ingest* by `offload_cards.py`. |
| Registry `wecape.db` | `~/.wecape/registry/wecape.db` (internal SSD) | Yes — re-CAPTURE (~hours) | Metadata + path **hashes** | Reconstructable but expensive; audit/trust anchor (P1/P3). |
| Proxies / FCPXML / output | `WE_CAPE_OUTPUT`, Desktop | Yes — regenerate | Derived | Regenerable from footage + registry. |
| `shoot.yaml`, `_offload_manifest.json`, `_new_shoot_session.jsonl` | Output/shoot folders (external) | Yes — re-run | **PII in plaintext** (names, location, paths) | See Decision D1. |
| Credentials | See 1.3 | — | **Highest confidentiality** | Not in repo (verified by scan). |

### 1.2 Credentials & keys (the real confidentiality crown jewels)

| Secret | Where it lives | Blast radius if leaked |
|--------|----------------|------------------------|
| rclone OAuth token + Google API client secret (`weforge-archive`) | `~/.config/rclone/rclone.conf` **[VERIFY location/permissions]** | Full read/write to the **20 TB Google Drive** (3.3 TB archive) |
| Apple Developer signing cert (future, J3) | Keychain (once purchased) | Ability to ship **signed malicious builds** under your identity |
| GitHub push credential / SSH key | macOS keychain / `~/.ssh` **[VERIFY]** | Write access to the source repo |

A code scan (2026-07-03) found **no hardcoded secrets** in tracked `.py`/`.yaml`/`.sh`.
The secrets above live on the machine, outside the repo — which is correct, and is why
**credential hygiene matters more than encrypting the registry folder.**

### 1.3 Egress points (where data leaves the machine) — there are only two today

1. **`rclone → gdrive:WECAPE_Backup`** via `scripts/backup_holder_mac.sh` (`OFFSITE=1` by
   default). Pushes `~/.wecape` snapshots — **including `annotations.db`** — to Google
   Drive. `RCLONE_REMOTE` is currently a **placeholder** [VERIFY]. See Decision D4.
2. **`git push → GitHub`** (`theworkmanexperience-sketch/Curser`). Source only;
   `.gitignore` excludes `*.fcpxml`, `wecape_dashboard.html`, `.DS_Store`, `__pycache__`.

Everything else is local by design. The **engine makes zero network calls (P2)** — verified
by scan: no `socket`/`urllib`/`requests`/`http` imports anywhere in `wecape/` or `scripts/`.

### 1.4 Single points of failure (from your own storage map)

- **Holder Mac 4.6 TB — zero backup** (production content + legal docs). Partially
  addressed by `backup_holder_mac.sh → Got My BackUP` **[VERIFY it actually runs]**.
- **`disk12` holds `timemachine` + `10TB` + Holder Mac** — one physical disk failure
  loses **three** logical volumes at once.
- **`annotations.db` — single irreplaceable copy** unless offsite/backup is verified.

---

## 2. Threat Model (ordered by probability × impact for *this* setup)

### T1 — Data loss / availability  *(highest probability, highest impact)*
Drive failure, ransomware, accidental deletion, bit rot. **This is the real #1.**
Concrete exposures: Holder Mac zero-backup; `disk12` triple-volume single point of
failure; single-copy `annotations.db`.

### T2 — Credential exposure  *(medium probability, high impact)*
Leak of the rclone token → 20 TB Drive; future signing cert → supply-chain compromise
of your own builds; tokens inadvertently included in an offsite backup.

### T3 — Integrity / determinism tampering  *(low probability, high impact on trust)*
The registry is the P1/P3 trust anchor. `mode=ro` in the dashboard is a **safety control
against bugs, not a security boundary** — anything running as your user can reopen the DB
read-write. Integrity rests on backups + provenance, not on the `ro` flag.

### T4 — Content / PII confidentiality  *(medium probability, variable impact)*
Plaintext footage on external drives (lost/stolen drive = exposure); PII in
`shoot.yaml`/manifests riding to cloud or backup; `annotations.db` egressing to Google
Drive in plaintext today (T2+T4 overlap).

### T5 — Remote intrusion / supply chain  *(lowest probability today, rising toward J3)*
Mac remote access (SSH / Screen Sharing / iCloud) **[VERIFY what's enabled]**; Python
dependency + `ffmpeg` binary provenance; future Cowork/Claude Code plugins; the J3
CloudSyncAdapter attack surface. This is where the "lock down remote access" advice
becomes relevant — **but only if remote access exists.**

---

## 3. Prioritized Controls

### 3.1 Quick wins (hours–days, mostly verification + config)

| # | Control | Addresses | Status |
|---|---------|-----------|--------|
| Q1 | **Verify backups actually run & restore.** Confirm `backup_holder_mac.sh` + the LaunchAgents are loaded; set real `RCLONE_REMOTE`; do one **test restore** of `annotations.db`. A backup unverified is a backup unowned. | T1 | [VERIFY] |
| Q2 | **Confirm FileVault ON** (protects internal SSD → registry + `annotations.db` at rest). | T4 | [VERIFY] |
| Q3 | **Enforce P2 as a test** — a suite test that fails if a network import appears in `wecape/`. Turns "zero network" from claim to invariant. | T5, P2 | TODO (offered) |
| Q4 | **Lock rclone config** — `chmod 600 ~/.config/rclone/rclone.conf`; confirm it is **not** inside any path that gets pushed offsite. | T2 | [VERIFY] |
| Q5 | **Match the engine's PII discipline in `new_shoot`** — hash paths in `_new_shoot_session.jsonl` as `wecape/capture/audit.py` already does. | T4 | TODO |
| Q6 | **Break the `disk12` SPOF** — relocate `timemachine` *or* Holder Mac backup to a different physical disk (Got My BackUP has 4.8 TB free). | T1 | TODO |
| Q7 | **Git pre-commit guard** — block committing `*.db`, `shoot.yaml`, `*_manifest.json`, `*_session.jsonl`, anything under `.wecape/`. | T2, T4 | TODO |

### 3.2 Medium term (weeks)

| # | Control | Addresses |
|---|---------|-----------|
| M1 | **Encrypt external drives** that hold output/registry-adjacent data or that ever leave the building (APFS encrypted volume). Trade-off: transcode perf + unlock friction — see D2. | T4 |
| M2 | **`annotations.db` 3-2-1, verified** — ≥2 local + 1 offsite, with a tested restore. It is the one irreplaceable asset. | T1 |
| M3 | **Credential inventory + rotation plan** — one page: every token/cert, where it lives, how to rotate. | T2 |
| M4 | **Encrypt the offsite copy** (rclone *crypt* remote) so `annotations.db`/registry are ciphertext in Google Drive. | T4, D4 |

### 3.3 Longer term (J3 / cloud horizon)

| # | Control | Addresses |
|---|---------|-----------|
| L1 | **Signing-cert handling** designed *before* the Apple Developer purchase pays off — keychain/hardware-backed, never in repo or plaintext backup. | T2 |
| L2 | **CloudSyncAdapter threat model** written before any code — authN/authZ, transport, key management. *Then* evaluate CRYSTALS-Kyber. Basics before post-quantum. | T5 |
| L3 | **Remote-access hardening** *iff* the Mac is ever exposed (Tailscale/WireGuard, no port-forwarding). Not needed while the machine is LAN-local. | T5 |
| L4 | **Dependency/supply-chain pinning** — pin `ffmpeg` provenance + Python deps; vet any plugin before install. | T5 |

---

## 4. Decision Register (needs the operator's call)

Each decision has a **recommended default**; record the choice + date so this stays living.

### D1 — `shoot.yaml` / manifest PII handling
`shoot.yaml` stores **name, location, date** in plaintext; the session log stores
**paths + mounts**. These live in the output folder (external drive).
- **Recommended:** keep `shoot.yaml` (needed for keywords + Health Report) but **exclude
  it, `_offload_manifest.json`, and `_session.jsonl` from any cloud/Drive sync**, and
  **hash the paths** in the session JSONL (Q5) to match the engine. Keep name/date/location
  plaintext *locally* — they're needed and stay on the machine.
- **Decision:** ____________  **Date:** ______

### D2 — External-drive encryption
- **Recommended:** encrypt drives that hold **output + registry-adjacent data** and any
  drive that **leaves the premises**; footage-only archive drives that never leave can be
  lower priority. Accept the transcode-perf trade-off on the working NVMe or exempt it.
- **Decision:** ____________  **Date:** ______

### D3 — Backup scope & cadence
- **Recommended:** `annotations.db` + registry → **3-2-1, daily** (already scripted via
  `--registry-only`; verify it's scheduled). Footage → **2 copies minimum** (offload's
  two-dest already gives this at ingest; make Holder Mac's job to Got My BackUP actually
  run). Verify a restore quarterly.
- **Decision:** ____________  **Date:** ______

### D4 — Should `annotations.db` go offsite to Google Drive at all?
Today `OFFSITE=1` pushes it **in plaintext** (unless a crypt remote is used).
- **Recommended:** **yes, but encrypted** — switch the offsite target to an **rclone crypt
  remote** (M4). Offsite protection for the irreplaceable asset without handing plaintext
  human notes to a third party.
- **Decision:** ____________  **Date:** ______

---

## 5. Control Status Snapshot (2026-07-03)

- ✅ **Already true:** engine zero-network (P2, verified); engine audit hashes paths;
  dashboard + annotations open `mode=ro`; no hardcoded secrets in the repo; two-copy rule
  enforced at ingest; backup + offsite tooling *exists*.
- 🟡 **Partial / unverified:** backups scheduled & restore-tested [VERIFY]; FileVault
  [VERIFY]; `RCLONE_REMOTE` still a placeholder; Holder Mac backup actually running.
- 🔴 **Gaps to close:** `disk12` SPOF; `new_shoot` plaintext PII (Q5); network-invariant
  test (Q3); offsite encryption of `annotations.db` (M4); credential inventory (M3);
  git pre-commit guard (Q7).

---

## 6. Living-Doc Mechanics

**Review triggers** — revisit this document when any of these happen:
- A new script or feature introduces a **network call or a new egress point**.
- A new **credential or key** is added (esp. the Apple signing cert).
- The **storage topology** changes (new drive, NAS, cloud sync, remote access).
- Work begins on **J3 CloudSyncAdapter** (rewrite §2/§3 for the cloud threat surface).

**Verification step (per the project's testing discipline):** the security posture is only
as real as its proof. Each control should have a check — a test (Q3), a scripted restore
(Q1), or a documented [VERIFY] resolved to a dated fact. Unverified controls are logged as
🟡, not ✅.

> Honest scope note: this analysis is built from the repository and the CLAUDE.md storage
> map. It cannot see runtime facts — whether FileVault is on, whether LaunchAgents are
> loaded, what remote-access services are enabled, or where `rclone.conf` actually sits.
> Those are the **[VERIFY]** items, and resolving them is the first pass of ownership.
