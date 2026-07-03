# CREDENTIAL_INVENTORY.md — W.E. C.A.P.E.
## Living credential map · v1.0 · 2026-07-03 · companion to SECURITY_RISK_ANALYSIS.md (M3)

**GOLDEN RULE — this file contains NO secret values.** It records *where* each secret
lives, *what it protects*, and *how to rotate it* — never the token, passphrase, key, or
recovery code itself. Do not paste a secret into this document. If you ever do, treat it
as compromised and rotate immediately. (This file is safe to commit *because* it holds
only locations and procedures.)

Ordered by blast radius — what an attacker gains if it leaks.

---

## 1. Credential Register

| # | Credential | Where it lives | Blast radius if leaked | Backed up off-machine? |
|---|------------|----------------|------------------------|------------------------|
| C1 | **rclone crypt passphrase** (`gcrypt`) | Password manager **+ sealed printed copy** — NOT only on the Mac | Decrypts **all offsite backups** (annotations.db + registry) on Google Drive | **REQUIRED** — it is the only recovery key. Lose it = encrypted backups unrecoverable. |
| C2 | **rclone Drive OAuth token** | `~/.config/rclone/rclone.conf` (perms `0600`, verified) | Full read/write to **My Drive (20 TB)**, incl. 3.3 TB archive | No — regenerable via reconnect (C2 rotation). |
| C3 | **Google API client secret** (project `weforge-archive`) | Google Cloud Console; also referenced in `rclone.conf` | Ability to mint new Drive API tokens | No — recreate in Cloud Console if leaked. |
| C4 | **GitHub auth** (SSH key or PAT) | `~/.ssh/` or macOS Keychain | Push access to `theworkmanexperience-sketch/Curser` | Key regenerable; no backup needed. |
| C5 | **FileVault recovery key** | Apple-ID escrow **or** a local recovery key | Unlocks the internal disk (registry + annotations.db at rest) | **REQUIRED** if using a local key — store off-machine. |
| C6 | **Apple Developer signing cert** *(FUTURE — J3)* | macOS login Keychain (once purchased) | Sign **malicious builds** under your identity | Keychain export, encrypted, off-machine — **never** in repo or plaintext backup. |

---

## 2. Rotation Procedures

- **C1 crypt passphrase** — effectively permanent (rotating means re-encrypting every
  offsite object). Treat as a long-lived key: choose a strong one once, store it in two
  off-machine places. Rotate only on suspected compromise (then re-push a fresh encrypted set).
- **C2 Drive token** — expires periodically (`invalid_grant`). Refresh with
  `rclone config reconnect gdrive:` → browser → Allow. No data impact. *(Last refreshed
  2026-07-03 — see log.)*
- **C3 API client secret** — regenerate in Google Cloud Console ▸ APIs & Services ▸
  Credentials, then `rclone config reconnect gdrive:`.
- **C4 GitHub** — regenerate the SSH key or PAT in GitHub ▸ Settings ▸ Developer settings;
  remove the old one.
- **C5 FileVault key** — reissue via `sudo fdesetup changerecovery -personal`; re-escrow.
- **C6 signing cert** — revoke/reissue in the Apple Developer portal; never share the `.p12`.

---

## 3. Rotation & Event Log

| Date | Credential | Action |
|------|------------|--------|
| 2026-07-03 | C2 | Drive OAuth token expired (`invalid_grant`) → refreshed via `rclone config reconnect gdrive:`. |
| 2026-07-03 | C1 | Crypt remote `gcrypt` created; passphrase stored off-machine. **[VERIFY: printed copy filed]** |

---

## 4. Review Triggers

Revisit this document when: a new service/credential is added; a secret is suspected
leaked; the Apple Developer cert (C6) is purchased; or a machine is retired (rotate C2/C4,
confirm C1/C5 exist off-machine before wiping). Verify the environment side any time with
`python3 scripts/security_check.py`.
