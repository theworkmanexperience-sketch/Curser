#!/bin/bash
#
# W.E. C.A.P.E. — double-click launcher for the Export Wizard.
#
# One-time setup so Finder lets you double-click it:
#     chmod +x "wecape_export.command"
# Then double-click it in Finder — Terminal opens and walks you through the export.
# (You can rename it in Finder to anything friendly, e.g. "Export to Final Cut.command".)
# ---------------------------------------------------------------------------

DIR="$(cd "$(dirname "$0")/.." && pwd)" || exit 1
cd "$DIR" || exit 1
python3 scripts/export_wizard.py
echo
read -n 1 -s -r -p "Done — press any key to close this window."
echo
