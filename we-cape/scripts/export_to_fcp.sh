#!/bin/bash
# One-command chain: CAPTURE run -> FCPXML -> FCP-safe filter -> Final Cut Pro
# Usage: scripts/export_to_fcp.sh WEF_RUN_ID
set -euo pipefail
RUN_ID="$1"
cd "$(dirname "$0")/.."
python3 scripts/fcpxml_export.py --run "$RUN_ID"
XML=$(ls -t *.fcpxml | grep -v _FCP_SAFE | head -1)
python3 scripts/fcpxml_fcp_safe.py "$XML"
SAFE="${XML%.fcpxml}_FCP_SAFE.fcpxml"
echo "Opening in Final Cut Pro: $SAFE"
open -a "Final Cut Pro" "$SAFE"
