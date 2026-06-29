# W.E. C.A.P.E. — UI/Dashboard Design Guidelines v2

**Supersedes:** UI_Dashboard_Design_Guidelines_v1.md (titled "W.E. NEXUS").
**Purpose:** Philosophy, scope, and guardrails for the dashboard, corrected to match the *actual* current build.
**Core principle:** The UI is a **read-only window + light annotation layer**. It must strengthen — never erode — the moat: **Privacy (P2), Determinism (P1), Auditability (P3)**.

> **What changed from v1 (and why):** v1's principles were right, but two of its
> models described a *different, more conventional tool* than what you built.
> This version corrects them against the real engine, registry schema (v3), and
> locked v4.1 spec. Corrections are flagged **[FIX]**; new build-grounded
> material is **[ADD]**. A working reference implementation now exists:
> `scripts/dashboard.py`.

---

## 0. Brand note (resolve before publishing)
v1 is titled **"W.E. NEXUS."** That name is not in the locked brand architecture
(W.E. C.A.P.E. = **C**apture / **A**rchive / **P**ulse / **E**valuate). An
analytics/oversight dashboard maps naturally to **PULSE** ("heartbeat of
production") or **EVALUATE** ("turn content into intelligence"). Either adopt one
of those, or formally add NEXUS to the brand architecture — don't ship a 5th name
by accident.

---

## 1. Overall Philosophy
- Make the product's core strengths **visible and verifiable**.
- **Not** an editor, post tool, or a control panel for overriding deterministic decisions.
- User-generated data (tags, notes, favorites, flags) lives in a **separate annotations store**, never mixed with the immutable registry.
- **100% local by default.** No CDN, no phone-home, no runtime network for core function.
- **Explainability is first-class.**

**Rule:** the dashboard is a **window**, not a mutation layer.

---

## 2. Light UI Approach (v1 scope)
A focused "window + light annotation" UI, not a rich dashboard yet.

**Should:** show high-level processing info; make determinism visible (hashes,
timestamp fallback level/confidence, conflict decisions); light annotations in a
separate store; project overview, search, status; one-click export/delete (P7).

**Must NOT (v1):** allow manual overrides of deterministic decisions; be a video
editor/timeline; mutate the registry/audit trail; require network for core function.

---

## 3. User Expectations by Level
- **Solo creators:** calm, scannable; "what happened to my files?"; media reconciliation; status/time; light tags; trust signals.
- **Small teams (2–5):** project visibility; "who ran what & when"; activity awareness; shared status.
- **Medium studios (6–20+):** oversight/reporting; accountability; performance metrics; exportable audit reports; role-aware (future); storage/growth.

> **[FIX] "Who ran what" has no data behind it today.** The `runs` table records
> *when* (timestamp) but **not who** — there is no operator/user column. (Operator
> is captured in `_preflight.json` + EULA state, not the registry.) The team tier
> requires adding an `operator` column to `runs` (a schema bump) before "who ran
> what" can be built. Treat it as a Phase-2 data prerequisite, not a given.

---

## 4. Key Information to Display

### Disposition — NOT a culling funnel  **[FIX — critical]**
v1 modeled "Original → After ingestion → After dedup/variant grouping → Final
archived count" with statuses incl. **Rejected / Needs Review**. That contradicts
the build:
- §3.x is LOCKED: *"MUST ingest every file… zero silent failures… data loss is a critical failure."* **The engine rejects nothing.**
- Deduplication is **off by default** (`enable_duplicate_content_detection: false`).
- Variants are **preserved and linked, never removed.**

So counts do **not** shrink, and "Rejected"/"Needs Review" are states the engine
never emits. Replace the shrinking funnel with a **disposition view** whose
headline trust signal is **"0 files lost"**:

```
Total ingested  =  [camera | generic | reference | camera-audio]
                 ×  [grouped | ungrouped]
                 ×  [variant | standalone]
                 +  quarantined (archive engine: partial/corrupt downloads)
                 +  low-confidence-timestamp (flagged, NOT dropped)
```

### Processing time & status  **[FIX]**
Show run status (Started / Completed / Failed) and final elapsed/runtime. **But a
read-only-registry UI cannot show live "Running… ETA"** — the registry is written
at run *start* and *finalize* only; there is **no mid-run progress persisted**.
Live progress requires the engine to emit a heartbeat to a pollable location
(new mechanism). v1: show start/finish + historical runtime; defer live ETA.
> Note: "historical averages **per camera family**" aren't computable — the
> registry stores whole-*run* `runtime_sec`, not per-file/per-camera timing.

### Explainability panel (core differentiator)  **[FIX scope]**
On selecting a clip/group, show what the registry actually holds: **content hash
(`content.id` = SHA-256)**, camera family (classification), shoot date, proxy
path, and **derivation lineage** (`source_clip` / `source_clip_sha`, v3).
> **In the DB:** hash, classification(family), shoot_date, proxy, lineage.
> **NOT in the DB — lives in each run's `LOGS/*.json`:** timestamp *fallback level
> & confidence*, grouping *conflict-resolution* decisions, variant *membership*.
> The panel must read those run logs to be complete, or the schema must capture
> them per-content row. **AI fields (quality/highlight/tags/embeddings) are null in v1.**
> "Confidence" = `timestamp_confidence` (high/low) only — never imply AI scoring.

### Light annotations (separate store)  **[FIX]**
Tags/favorites/notes/flags keyed by content hash — stored in a **separate
database file** (e.g. `~/.wecape/annotations.db`), **not** a table inside
`wecape.db`. (A table in the same file would force a writable connection and
break the read-only guarantee on the audit registry.) Consider a `(project, hash)`
compound key so a tag in one project doesn't bleed into every project sharing
that content hash.

---

## 5. Post-Production Workflow Display  **[FIX — make it source-aware]**
Support post-production without becoming it.

The handoff is **conditional, and v1 treated it as unconditional.** Your `CAMERA/`
originals are **symlinks to the source drive**; only `PROXIES/` are self-contained.
So proxy editing is always ready, but full-res conform depends on the source drive
being mounted. The UI must reflect this:

- **Structure (real layout):** `<shoot>/YYYY-MM-DD/CAMERA/<family>/`, `/MULTICAM/MCG_*.json`, `/PROXIES/`, `/LOGS/` — date-first, not camera-first.
- **Edit-media vs originals:** PROXIES = self-contained, always editable; CAMERA = symlinked, **mount-dependent**. The "Ready for Editing" badge must check source-drive presence ("originals on '10TB' — mounted ✓ / NOT MOUNTED ⚠").
- **Relink:** surface proxy path + original path per clip (proxies are named after originals → clean NLE relink).
- **Multicam:** surface MCG group membership (which DJI + Insta360 clips sync) so editors can build multicam sequences — replaces reading JSON by hand.
- **Lineage:** carry select→source into the handoff view.
- **Trust flag:** mark low-confidence/misdated clips (the "2018 folder" case) *before* the cut.
- Workflow flags ("In Review", "Ready for Edit") = annotations only (separate store). **Do not orchestrate NLEs** — that's W.E. EDIT (J4).

---

## 6. Phased Rollout
- **Phase 1 (solo):** project list, disposition (0-lost) numbers, start/finish + historical runtime, basic explainability (hash, classification, shoot_date, lineage), light tags, search/filter.
- **Phase 2 (team awareness):** multi-project, activity feed — **requires the `operator` column [ADD]** — export manifest/audit report.
- **Phase 3 (studio):** oversight, performance trends, storage projections (needs OS-level disk data, see §7), saved views, role-based visibility (future).

---

## 7. Technical & Architectural Guardrails
- **Read-only** access to the core registry — open `wecape.db` with `mode=ro`; never write it.
- **Annotations in a SEPARATE database file** — keep the audit DB untouched by the UI.
- **Indexes** before launch: `camera_family`, `shoot_date`, `run_id`, `source_clip`, content `id`.
- **WAL mode + read-only connections** so the dashboard never locks a running ingest.
- **No network calls** for core UI. **All manual decisions** (when overrides eventually exist, post-v1) logged as a distinct human-decision layer.
- **[ADD] Local-first STACK mandate (this is where P2 silently dies if unspecified):**
  - Vendored/bundled assets only — **zero CDN** (no Google Fonts, no CDN charting/JS).
  - No telemetry SDKs; product analytics (if any) opt-in, local-aggregate, anonymized.
  - **Offline-first updates** — no auto-update over the network.
  - **Platform decision required:** native macOS app in the signed `.dmg`, a bundled local web app, or static generated HTML. (Engine is macOS-only: VideoToolbox, `mdls`, `stat -f`.) The reference prototype below uses the static-generated-HTML path.
- **[ADD] Schema-version aware:** read `schema_version`; detect columns via `PRAGMA table_info` and degrade gracefully (a v2 DB has no `source_clip`; it appears after the next run auto-migrates to v3).
- **[ADD] Storage/safety data is partly OS-level:** footage volume comes from the registry (`file_size_bytes`); drive free-space and backup state do **not** — they need OS disk queries (`shutil.disk_usage`), outside the registry.

---

## 8. Reference Implementation  **[ADD]**
`scripts/dashboard.py` is a working, on-architecture prototype: stdlib-only Python
reads `~/.wecape/registry/wecape.db` **read-only** and emits one **self-contained,
zero-CDN, zero-network** HTML file (inline CSS + hand-built SVG charts). It proves
the local-first mandate is achievable and renders the disposition view, shoots,
camera mix, lineage (v3), and a per-clip record with the honest in-DB-vs-in-LOGS
note. It is a *window* (opens the DB `mode=ro`, never writes), not the packaged
shippable app.

```
python3 scripts/dashboard.py            # -> ./wecape_dashboard.html
open wecape_dashboard.html
```

---

## 9. Success Criteria
A successful dashboard makes privacy/determinism/auditability **visible and
demonstrable**; feels calm, not overwhelming; answers "what happened to my files?"
instantly (with **0 lost** front and center); allows light user value without
touching the immutable record; and serves as both a daily tool and the demo/
marketing asset.

---

**Status:** v2 — corrected against the live build (engine, registry v3, locked v4.1 spec).
**North star** alongside the COMPLIANCE_DELTA set and core architecture principles.
