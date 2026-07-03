#!/usr/bin/env bash
#
# W.E. C.A.P.E. — New Shoot (double-click launcher for the PyWebView skin).
# One-time:  chmod +x scripts/new_shoot_gui.command
#
cd "$(dirname "$0")/.." || exit 1

# PyWebView is the only extra dependency; offer to install it if missing.
if ! python3 -c "import webview" >/dev/null 2>&1; then
  echo "PyWebView isn't installed (the New Shoot window needs it)."
  printf "Install it now with pip3? [y/N] "
  read -r ans
  case "$ans" in
    y|Y) pip3 install pywebview || { echo "install failed — try: pip3 install --user pywebview"; }
         ;;
    *) echo "Skipped. You can still use the CLI: python3 scripts/new_shoot.py detect"
       read -n 1 -s -r -p "Press any key to close…"; exit 0 ;;
  esac
fi

python3 scripts/new_shoot_gui.py
echo
read -n 1 -s -r -p "Press any key to close…"
