#!/bin/bash
# v2 re-derivation (corrections C1, C2 - see rederive_segments_v2.py). Read-only on all
# inputs. v1 (run.sh / rederivation.json 5d6994b3) is untouched and still reproduces.
set -euo pipefail
W=/Volumes/WE_CAPE_OUTPUT/AlphaRoundUp_2026
F24="$W/Alpha RoundUp Part 2 /ALPHA ROUNDUP DAY 2 ANALYSIS/Corrected Video Analysis Files/Alpha RoudUp Part 2.fcpxmld/Info.fcpxml"
S24="$W/Alpha RoundUp Part 2 /ALPHA ROUNDUP DAY 2 ANALYSIS/Corrected Video Analysis Files/Alpha RoudUp Part 2_SRT_English (United States).srt"
F22="$W/SPRINT3A_WORK/inputs/Info.fcpxml"
S22="$W/SPRINT3A_WORK/inputs/lock_srt2.srt"
H=$(cd "$(dirname "$0")" && pwd); ESS="$H/.."; OUT="${1:-$H/v2}"
mkdir -p "$OUT"
python3 "$H/rederive_segments_v2.py" --fcpxml-0822 "$F22" --fcpxml-0824 "$F24" \
  --srt-0822 "$S22" --srt-0824 "$S24" --observations-0822 "$ESS/context/AR2-0822.observations.json" \
  --expect 2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7 \
           d82c2c3ec0f788cf47262194d6fbb8aefcd5fc9b7eee899b04bd3487f02e3a80 \
           89d61f965aa17e4d3dade14173869b34efb0c09d689b1c347d3c9c8f6eca1c6b \
           d93d86a1b7cd99c9baad2ce8e625f486056a5cb8b6229918d04b3bdcb304ef82 \
  --out "$OUT/rederivation_v2.json"
python3 "$H/build_tables.py" "$OUT/rederivation_v2.json" "$OUT"
