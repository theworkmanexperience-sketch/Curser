# SPEC — `.SRT` Sidecar Telemetry (Phase 1: GPS + drift-free time)
## Design note · v0.1 · 2026-07-03 · companion to SPEC_Production_Health_Report.md

## 1. Problem & value
DJI/Osmo cameras drop a `.SRT` subtitle sidecar next to each clip containing, per
timecode, a **precise datetime** and (when a GPS lock exists) **GPS coordinates** plus
exposure metadata. Two independent payoffs:

- **Drift-free time** — the `.SRT` datetime is the camera's real clock at record time.
  This is the "name the culprit camera" signal the Production Health Report needs, and it
  can shrink the ±15s grouping window. **Works even when GPS is absent.**
- **Location** — GPS lat/lon/alt for future location-based features (maps, geo-search).

## 2. Scope
- **Phase 1 (this note):** parse the `.SRT` *text* sidecar only. Tolerant, read-only.
- **Phase 2 (deferred):** embedded binary telemetry (DJI `CAM meta` / KLV inside the MP4)
  — only if/when per-frame depth is needed or for cameras that don't emit `.SRT`.

## 3. `.SRT` format (tolerant parsing)
Format varies by model/firmware; the parser MUST be regex-tolerant, not positional. A block:

```
1
00:00:00,000 --> 00:00:00,033
<font size="28">FrameCnt: 1, DiffTime: 33ms
2026-03-14 09:30:40.123
[iso: 100] [shutter: 1/500] [latitude: 33.123456] [longitude: -84.123456] [rel_alt: 1.2 abs_alt: 250.5]</font>
```

- **Datetime line:** `YYYY-MM-DD HH:MM:SS(.ms)` → the record-time clock (always present).
- **GPS:** `[latitude: <f>] [longitude: <f>]` (+ optional altitude) → **may be absent** (no lock).
- Parser extracts the **first** and **last** datetime (clip start/end), and a representative
  GPS fix (first valid). It MUST NOT fail a clip that has time but no GPS.

## 4. Data model (per clip)
```
content_sha        # SHA-256 of the video clip (the join key to the registry)
run_id             # run that ingested the clip (context)
srt_path_hash      # sha256 of the .SRT path (never plaintext)
start_time         # ISO — first .SRT datetime (drift-free record time)
end_time           # ISO — last .SRT datetime
gps_lat, gps_lon   # nullable — present only if a fix existed
gps_alt            # nullable
sample_count       # SRT blocks parsed
parser_version
```

## 5. Storage decision (the consequential one) — 🔒
**Telemetry lives OUTSIDE the deterministic registry**, in its own store
`~/.wecape/telemetry.db` (SQLite, stdlib), keyed by **content SHA** (+ `run_id`).

Rationale — identical to why `annotations.db` is separate:
- **P1 determinism:** the deterministic engine's output must not depend on whether a `.SRT`
  happened to be present; telemetry is enrichment, not pipeline truth.
- **PII posture:** GPS is location PII. Governance keeps GPS **hashed in engine logs**. We
  keep **full-fidelity coordinates only in this separate, creator-owned local store** (P7),
  and apply the **D1 rule on egress** — hash/omit GPS + path in any shared/offsite artifact.
- **P4 no coupling:** a separate post-processor can be added, changed, or removed without
  touching the engine.

Joins to the registry read-only by `content_sha`. Telemetry is regenerable from the `.SRT`
files (unlike `annotations.db`), so it is not itself irreplaceable.

## 6. Delivery: post-processor now, integration later
- **Now:** `scripts/srt_telemetry.py` — a read-only ops tool. `scan <run_id|folder>` parses
  `.SRT` sidecars, writes `telemetry.db`; `show <sha>` / `list` query it. Idempotent
  (re-scan updates by content SHA). stdlib-only, zero-network, never mutates footage.
- **Later (opt-in):** once schema is proven, a `TelemetryStage` (PipelineStage) MAY populate
  it during ingest — additive, disabled by default (P6-style staging), behind config.

## 7. Consumers
- **Production Health Report:** uses `start_time` to compute each camera's true clock vs the
  group anchor → names the drifting camera with *real* data, not just relative skew.
- **FCPXML export (future):** could stamp GPS into clip notes/keywords (local only).
- **W.E. ARCHIVE (J5):** geo-search over the telemetry store.

## 8. Open questions
1. Multiple GPS fixes per clip — store first-fix only (v1), or a track? (v1: first + count.)
2. Confidence when `.SRT` time disagrees with filename/ffprobe time — surface as a Health
   Report signal, don't silently override the deterministic timestamp.
3. Model coverage — validate against real Osmo Action 5/6 `.SRT` (reliability run #2 card has them).
