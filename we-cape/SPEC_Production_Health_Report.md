# SPEC — Production Health Report (Postmortem)
## Draft v0.1 · 2026-07-01 · status: DESIGN (pre-build)

## 1. Purpose

After every CAPTURE run, give the creator a clear, **honest** postmortem that answers:

- **What happened?** — files in, grouped, ungrouped, nothing lost.
- **Where were the problems?** — which cameras / clips were hard to assemble.
- **Why did they happen?** — root cause, in plain language (usually a camera clock).
- **How do I prevent it next time?** — a specific, actionable cure, with the *projected* gain.

This is what turns CAPTURE from an ingestor into a Production Intelligence tool: it doesn't just
process footage, it **explains the shoot back to the creator** and makes the next one cleaner. No
competitor in the ingest lane (Hedge, PluralEyes, Kyno) does this, because none of them see every
camera together.

---

## 2. Honesty guardrails (the non-negotiables)

The value of this report is trust. If it overclaims once, it's worthless. Rules:

1. **Grouping health, NOT alignment accuracy.** CAPTURE decides *which clips belong together*
   (grouping, ±seconds). It does **not** do frame-accurate audio *alignment* (that's J3 / FCP's
   "Synchronize Clips"). Never print a "% sync accuracy" number. Metrics are about grouping,
   clock health, and window pressure only.
2. **"Cures" are recommendations, not guarantees.** Phrase as "should," "expected," "projected" —
   never "will." A projected improvement is a *simulation*, labelled as such.
3. **Never name a culprit we can't prove.** Without a trusted clock reference, report *relative*
   disagreement and flag the statistical outlier — do not assert which camera is "right."
4. **"0 files lost" is the one absolute** — it is always true (P5/P7) and may be stated plainly.
5. **Report is derived, not asserted.** Every number traces to run data (P3 auditability); the
   report adds no facts the run didn't produce.

---

## 3. Qualifying-information intake (optional shoot manifest)

To move from "these cameras disagree" to "*this* camera is wrong, here's the fix," CAPTURE needs a
**ground-truth clock**. Two independent sources, either sufficient:

- **User-declared** trusted clock (this section), or
- **DJI `.SRT` GPS time** (Phase 2 — an atomic reference; see §8).

### Design constraints
- **Optional and non-blocking.** CAPTURE is headless/deterministic; a required prompt breaks
  automation. The manifest is *context*, read if present, defaulted to "unknown" if absent.
- **Config-level, not engine output.** Qualifying info is human-supplied (like annotations). It
  influences the **report's framing**, never the deterministic pipeline output (P1). Same files +
  config → same groups/proxies, with or without a manifest.
- **Collected at offload, not mid-pipeline.** The human is physically present at offload; that's the
  moment to ask. `offload_cards.py` already takes `--shoot` and `--camera` — extend it to write a
  small manifest that travels with the footage; CAPTURE reads it at pre-flight.

### Manifest (`shoot.yaml`, dropped in the source root or passed via `--shoot-manifest`)
```yaml
shoot_name:   O-SIX Community Service
shoot_date:   2026-03-14           # the true date, if the creator knows it
location:     Kansas City, MO      # free text (GPS auto-filled from .SRT later)
event:        Community Service
cameras:      [DJI Osmo Action 5, DJI Osmo Action 6, Insta360 X5, iPhone]
trusted_clock: DJI Osmo Action 6   # the camera/source whose clock is authoritative
                                    #   (or "GPS" / "phone" / "unknown")
notes:        Insta360 clock was not reset this shoot
```
All fields optional. `trusted_clock` is the single highest-value input — it lets §5 name the culprit
definitively. In INTERACTIVE mode only, CAPTURE may *offer* to create one ("No shoot manifest found —
create one? [y/N]", default N); non-interactive runs skip silently.

---

## 4. Report sections

### 4.1 Summary
- Total files processed: **X**
- Grouped: **Y** (Z%) · Ungrouped: **A** · Quarantined: **Q**
- Grouping success rate: **Z%**
- **0 files lost** (always).

### 4.2 Camera Health
- Per-camera **clock skew** relative to the group consensus (median of group-mate timestamps).
  - e.g. "Insta360 X5 runs **~8 years behind** the DJI cameras."
- Worst offender(s) flagged.
- If a `trusted_clock` (manifest) or GPS time (Phase 2) exists: skew is stated **against ground
  truth** and the culprit is named. Otherwise: "relative — one of these clocks is off" + the outlier
  flagged, no accusation.

### 4.3 Grouping Analysis
- Window the run needed (±15s) vs. the RFQ spec (±5s).
- Groups formed; group sizes.
- Low-confidence groupings (fell back to file-clock timestamps) flagged with counts.

### 4.4 Recommendations (The Cure)
- Specific, e.g. "Set the Insta360 X5 clock to current date/time before the next shoot."
- General, e.g. "Sync all cameras to one accurate source (a phone) before rolling."
- **Projected improvement** (a labelled *simulation* — see §6): "with synced clocks: window tightens
  to ±2s, A→0 ungrouped, high-confidence grouping on 100% of files."

### 4.5 Technical Details (power users)
- Link to the dashboard explainability panel.
- Raw diagnostics: timestamp fallback levels, confidence distribution, conflict-resolved groups.

---

## 5. Metrics — precise definitions

| Metric | Definition | Source |
|--------|-----------|--------|
| Grouping success % | grouped camera files ÷ total camera files | registry / index |
| Clock skew (per camera) | median( camera clip time − consensus time ) across the groups it appears in | new analysis |
| Window pressure | max clip-to-anchor delta observed vs. the configured window | grouping metadata |
| Confidence mix | count of files by timestamp confidence (high / low) and fallback level (filename / metadata / file-clock) | LOGS classification |
| Ungrouped count | camera files that formed no group | index `ungrouped_camera_files` |

No "alignment accuracy" metric exists — by design (§2.1).

---

## 6. "Projected improvement" methodology (and its honesty caveat)

1. Measure each camera's skew (§4.2).
2. **Re-simulate grouping** with the measured skew removed from the off cameras (a dry, in-memory
   re-group — no re-processing, no file writes).
3. Report the *simulated* result: window that would have sufficed, ungrouped that would have grouped,
   confidence that would have risen.

**Caveat printed with the number:** this is a projection assuming the *only* problem was clock skew
and that the skew is constant across the shoot. It is a planning estimate, not a promise. It never
implies frame-accurate sync.

---

## 7. Delivery locations

- **Run `summary.md`** — a "Production Health" block appended to the existing per-run summary.
- **Dashboard per-shoot card** — a prominent Health section (extends the existing explainability panel).
- **Optional one-click export** — a standalone `<run_id>_health.md` / `.html` the creator can keep or
  send to a client ("here's why the edit took extra time").

---

## 8. Phasing

- **v1 (no `.SRT`):** cross-camera **relative** skew + outlier flag; if a `trusted_clock` manifest is
  present, name the culprit. Grouping-health metrics, cure text, projected-improvement simulation.
  Rendered in `summary.md` + dashboard.
- **v2 (with DJI `.SRT`):** GPS time as an **authoritative** clock → skew stated against true time,
  culprit named without a manifest, and optional **auto-correction** (apply the measured offset so
  the wrong-clock camera's clips re-group correctly). This is why Health and the `.SRT` telemetry item
  are one feature — GPS is the ground truth the postmortem wants.

---

## 9. Determinism & privacy

- **P1:** the report is a pure function of run data (deterministic). Qualifying info changes *framing*,
  not pipeline output.
- **P2:** generation is local, zero-network (GPS comes from the on-card `.SRT`, not a lookup).
- **P3:** every number is auditable to a source; nothing is invented.
- **P7:** the creator owns the report; the optional export is theirs to share or not.

---

## 10. Open decisions (for review before build)

1. **Health score?** A single 0–100 "shoot health" number is catchy but risks over-summarizing —
   include it, or keep it to the component metrics? (Lean: component metrics + a plain-English verdict,
   no single score, to avoid a misleading headline number.)
2. **Manifest location/name** — `shoot.yaml` in the source root vs. `--shoot-manifest PATH` vs. both.
3. **Offload capture** — add `--trusted-clock` / `--shoot-date` / `--location` to `offload_cards.py`
   and have it write the manifest? (Lean: yes — front-of-pipeline is the right moment.)
4. **v1 without any ground truth** — is "relative skew + outlier flag" useful enough to ship before
   `.SRT`, or wait and ship v1+v2 together? (Lean: ship v1 — the outlier flag + cure text already
   helps; `.SRT` upgrades it from "likely" to "certain.")
