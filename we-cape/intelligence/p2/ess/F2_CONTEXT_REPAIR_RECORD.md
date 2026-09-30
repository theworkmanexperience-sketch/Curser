# F-2 — AR2-0824 Context Repair Record

**Executed under:** EO-2026-09-29 Addendum B §F-2 (G2 pinning, against the ED-003 / CF-001 designations only)
**Date:** 2026-09-30 (UTC) · **Custody:** `MACHINE` · **Authority:** NONE
**No generator run** was performed or is implied (Addendum B §F-2).

## Inputs, hash-asserted before reading

| input | sha256 | assertion |
|---|---|---|
| `context/AR2-0824.context.json` (before) | `c8759b00fcfedc9c8597efe7d016b80de8cb517f7aa8b08b000221adc7039535` | disk == HEAD blob (`cfae47d`) |
| designated lock `…/Alpha RoudUp Part 2.fcpxmld/Info.fcpxml` (mounted) | `d82c2c3ec0f788cf47262194d6fbb8aefcd5fc9b7eee899b04bd3487f02e3a80` | == ED-003 §1 == Addendum B |
| designated caption stream `…/Alpha RoudUp Part 2_SRT_English (United States).srt` (mounted) | `d93d86a1b7cd99c9baad2ce8e625f486056a5cb8b6229918d04b3bdcb304ef82` | == CF-001 §1 == Addendum B |

## Changes — three fields, exactly the three the Addendum names

| field | before | after | basis |
|---|---|---|---|
| `sha.fcpxml` | `1ab3d12f0dd150c6…` (PLR-001 candidate, not designated) | `d82c2c3ec0f788cf47262194d6fbb8aefcd5fc9b7eee899b04bd3487f02e3a80` | ED-003, measured |
| `sha.srt` | `2a16dd700148488f…` (not designated) | `d93d86a1b7cd99c9baad2ce8e625f486056a5cb8b6229918d04b3bdcb304ef82` | CF-001, measured |
| `srt.cues` | `2036` | `2034` | measured on the CF-001 stream with `build_context.py`'s own cue regex; index lines 1…2034 contiguous; agrees with CF-001 §1 |

**After:** `context/AR2-0824.context.json` sha256 `b0f432613b5e159d97d9dd41e4255adb1d2d903ff7dedbbd134857fcd75dc048`

## Measured and found already correct — not changed

| field | value | measured on CF-001 stream |
|---|---|---|
| `srt.first_s` | 0.375 | 0.375 |
| `srt.last_s` | 4688.958 | 4688.958 |
| `runtime_s` | 4689.5 | ED-003 sequence duration 4689.500 |

## NOT changed — outside the Addendum's enumeration, reported

| field | current value | condition |
|---|---|---|
| `source_files.fcpxml` | `analysis_cut/Info_analysiscut.fcpxml` | names the `1ab3d12f` file, not the designated lock |
| `source_files.srt` | `analysis_cut/srt_analysiscut.srt` | names the `2a16dd70` stream, not CF-001 |
| `sha.etc` / `etc.spine` / `etc.connected` / `source_files.etc` | `NOT_PRODUCED` / null | the ETC exists (`8c76a8cf…`, packet `aec3a27`) but is not a designation; ETC pinning was not enumerated |
| `sha.mp4`, `proxy.*`, `git_commit` | `NOT_DESIGNATED` / `AWAITING_INGESTION` | unchanged prerequisites (B-7, B-8) |

**Behaviour of the residual is fail-shut, not silent:** `build_context.py` resolves `source_files.*`
and STOPs (exit 2) when a declared `sha.*` disagrees with the file at that path. With the sha fields
now pinned to the designations, the stale paths cannot bind the wrong artifact; they will stop the
build. Repointing `source_files` and pinning the ETC need an explicit authorization.
