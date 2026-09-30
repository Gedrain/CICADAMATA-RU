#!/bin/sh
# Restores the original (English) CICADAMATA.pck from the backup made by the installer.
G="${1:-$HOME/.local/share/Steam/steamapps/common/CICADAMATA}"
[ -f "$G/CICADAMATA.pck.orig" ] && cp -f "$G/CICADAMATA.pck.orig" "$G/CICADAMATA.pck" && rm -f "$G/CICADAMATA.pck.orig" && echo "Original restored." || echo "No backup found."
