#!/bin/sh
# Publishes the sources and the v2.0 release (installers) to GitHub.
#   ./release.sh                 -> github.com/<you>/CICADAMATA-RU (public)
#   ./release.sh owner/name      -> custom repository (e.g. an organisation)
#   ./release.sh owner/name --private
# Needs: git, GitHub CLI (gh) logged in (`gh auth login`), built files in dist/.
set -e
cd "$(dirname "$0")"

REPO="${1:-CICADAMATA-RU}"
VIS="--public"
[ "$2" = "--private" ] && VIS="--private"
TAG="v2.0"
TITLE="CICADAMATA — русская локализация v2.0"
DESC="Полный фанатский перевод CICADAMATA на русский язык от NOTFOUNDVPN — установщики для Windows и Linux"
ASSETS="dist/CICADAMATA_RU_Installer-x86_64.AppImage dist/CICADAMATA_RU_v2.0_Windows.zip"

command -v gh >/dev/null 2>&1 || { echo "Нужен GitHub CLI: sudo pacman -S github-cli (или https://cli.github.com)"; exit 1; }
gh auth status >/dev/null 2>&1 || gh auth login
for f in $ASSETS; do [ -f "$f" ] || { echo "Нет файла $f — собери установщики: python3 tools/build_all.py --installers"; exit 1; }; done
git rev-parse HEAD >/dev/null 2>&1 || { echo "В репозитории нет коммитов"; exit 1; }

echo "== контрольные суммы"
(cd dist && sha256sum "$(basename dist/CICADAMATA_RU_Installer-x86_64.AppImage)" CICADAMATA_RU_v2.0_Windows.zip > SHA256SUMS.txt && cat SHA256SUMS.txt)

echo "== исходники -> GitHub"
if git remote get-url origin >/dev/null 2>&1; then
	git push -u origin HEAD
else
	gh repo create "$REPO" $VIS --source=. --remote=origin --description "$DESC" --push
fi
FULL="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
gh repo edit "$FULL" --add-topic cicadamata --add-topic russian-translation --add-topic localization --add-topic godot >/dev/null 2>&1 || true

echo "== релиз $TAG"
if gh release view "$TAG" -R "$FULL" >/dev/null 2>&1; then
	gh release upload "$TAG" $ASSETS dist/SHA256SUMS.txt -R "$FULL" --clobber
	gh release edit "$TAG" -R "$FULL" --title "$TITLE" --notes-file RELEASE_NOTES.md
else
	gh release create "$TAG" $ASSETS dist/SHA256SUMS.txt -R "$FULL" --title "$TITLE" --notes-file RELEASE_NOTES.md --target "$(git rev-parse --abbrev-ref HEAD)" --latest
fi
echo
echo "Готово: https://github.com/$FULL/releases/tag/$TAG"
