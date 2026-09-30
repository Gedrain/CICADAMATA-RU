#!/bin/sh
# Builds dist/CICADAMATA_RU_Installer-x86_64.AppImage from the exported Linux installer.
# Usage: ./build_appimage.sh [--export]   (--export re-exports the Godot project first)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
KIT="$(dirname "$HERE")"
DIST="$KIT/dist"
BIN="$KIT/work/export/CICADAMATA_RU_Installer_Linux.x86_64"
TOOL="$KIT/tools/bin/appimagetool-x86_64.AppImage"
APPDIR="$KIT/work/AppDir"
NAME=cicadamata-ru-installer

mkdir -p "$KIT/work/export"
if [ "$1" = "--export" ] || [ ! -x "$BIN" ]; then
	godot --headless --path "$HERE" --export-release "Linux" "$BIN"
fi
[ -x "$BIN" ] || { echo "no exported binary: $BIN"; exit 1; }
if [ ! -x "$TOOL" ]; then
	mkdir -p "$(dirname "$TOOL")"
	curl -L -o "$TOOL" https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage
	chmod +x "$TOOL"
fi

rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/share/icons/hicolor/256x256/apps" "$APPDIR/usr/share/applications"
cp "$BIN" "$APPDIR/usr/bin/$NAME"
chmod +x "$APPDIR/usr/bin/$NAME"
cp "$HERE/assets/icon.png" "$APPDIR/$NAME.png"
cp "$HERE/assets/icon.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/$NAME.png"
ln -s "$NAME.png" "$APPDIR/.DirIcon"

cat > "$APPDIR/$NAME.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=CICADAMATA RU Installer
Name[ru]=CICADAMATA — русская локализация
Comment=Russian localization installer for CICADAMATA by NOTFOUNDVPN
Comment[ru]=Установщик русской локализации CICADAMATA от NOTFOUNDVPN
Exec=$NAME
Icon=$NAME
Categories=Game;
Terminal=false
X-AppImage-Version=2.0
EOF
cp "$APPDIR/$NAME.desktop" "$APPDIR/usr/share/applications/"

cat > "$APPDIR/AppRun" <<'EOF'
#!/bin/sh
HERE="$(dirname "$(readlink -f "$0")")"
exec "$HERE/usr/bin/cicadamata-ru-installer" "$@"
EOF
chmod +x "$APPDIR/AppRun"

OUT="$DIST/CICADAMATA_RU_Installer-x86_64.AppImage"
ARCH=x86_64 APPIMAGE_EXTRACT_AND_RUN=1 "$TOOL" --no-appstream "$APPDIR" "$OUT"
echo "built $OUT"
