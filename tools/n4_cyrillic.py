# Adds Cyrillic code points to the N4NOOSE cipher fonts by pointing them at the Latin glyph
# of the transliterated letter (the font is an abstract cipher, so no new drawing is needed).
import sys
from fontTools.ttLib import TTFont
MAP = dict(zip('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
               'ABVGDEEJZIYKLMNOPRSTUFHCQWWXYXEUA'))
def patch(src, dst):
    f = TTFont(src, recalcTimestamp=False); n = 0
    for t in f['cmap'].tables:
        if not t.isUnicode(): continue
        cm = t.cmap
        for cy, la in MAP.items():
            for a, b in ((cy, la), (cy.lower(), la.lower())):
                g = cm.get(ord(b))
                if g and ord(a) not in cm: cm[ord(a)] = g; n += 1
    f.save(dst); return n
if __name__ == '__main__':
    print(patch(sys.argv[1], sys.argv[2]))
