#!/usr/bin/env python3
# CICADAMATA Russian localization v2 - command-line patcher.
#   ru_patch.py build  <original.pck> <out.pck> [payload_dir]   build a patched pck
#   ru_patch.py install [game_dir]                                patch the installed game (keeps .orig backup)
#   ru_patch.py restore [game_dir]                                restore the original pck
import os, sys, json, struct, hashlib, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
DEF_PAYLOAD = os.path.join(HERE, '..', 'payload')

def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 24), b''): h.update(c)
    return h.hexdigest()

def read_dir(path):
    with open(path, 'rb') as f:
        hdr = struct.unpack('<4sIIIIIQQ', f.read(0x28))
        assert hdr[0] == b'GDPC', 'not a Godot pck'
        base, diroff = hdr[6], hdr[7]
        f.seek(diroff); n = struct.unpack('<I', f.read(4))[0]; ents = []
        for _ in range(n):
            l = struct.unpack('<I', f.read(4))[0]; p = f.read(l).rstrip(b'\0').decode()
            off, size = struct.unpack('<QQ', f.read(16)); m = f.read(16); fl = struct.unpack('<I', f.read(4))[0]
            ents.append((p, off, size, m, fl))
    return hdr, ents

def build(orig, out, payload=DEF_PAYLOAD, progress=None):
    man = json.load(open(os.path.join(payload, 'manifest.json')))
    hdr, ents = read_dir(orig); base, diroff = hdr[6], hdr[7]
    names = {p for p, *_ in ents}
    repl = {k: os.path.join(payload, 'files', k) for k in man['files']}
    for k in repl:
        if not k.startswith('localization_ru/') and k not in names:
            raise SystemExit('original pck has no %s - wrong game version?' % k)
    tmp = out + '.part'
    with open(orig, 'rb') as src, open(tmp, 'wb') as dst:
        left = diroff
        while left:
            c = src.read(min(left, 1 << 24)); dst.write(c); left -= len(c)
            if progress: progress(1 - left / diroff)
        pos, info = diroff, {}
        for k, path in sorted(repl.items()):
            pad = (-pos) % 32; dst.write(b'\0' * pad); pos += pad
            data = open(path, 'rb').read(); dst.write(data)
            info[k] = (pos - base, len(data), hashlib.md5(data).digest()); pos += len(data)
        pad = (-pos) % 32; dst.write(b'\0' * pad); pos += pad
        newdir, rows = pos, []
        for p, off, size, m, fl in ents:
            rows.append((p,) + info[p] + (0,) if p in info else (p, off, size, m, fl))
        rows += [(k,) + v + (0,) for k, v in info.items() if k not in names]
        d = bytearray(struct.pack('<I', len(rows)))
        for p, o, s, m, fl in rows:
            pb = p.encode(); pb += b'\0' * ((-len(pb)) % 4)
            d += struct.pack('<I', len(pb)) + pb + struct.pack('<QQ', o, s) + m + struct.pack('<I', fl)
        dst.write(d); dst.seek(0x20); dst.write(struct.pack('<Q', newdir))
    os.replace(tmp, out)

def default_game_dir():
    for c in ('~/.local/share/Steam/steamapps/common/CICADAMATA', '~/.steam/steam/steamapps/common/CICADAMATA',
              '~/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/common/CICADAMATA',
              'C:/Program Files (x86)/Steam/steamapps/common/CICADAMATA'):
        c = os.path.expanduser(c)
        if os.path.isfile(os.path.join(c, 'CICADAMATA.pck')): return c
    return None

def install(game, payload=DEF_PAYLOAD):
    man = json.load(open(os.path.join(payload, 'manifest.json')))
    pck, orig = os.path.join(game, 'CICADAMATA.pck'), os.path.join(game, 'CICADAMATA.pck.orig')
    want = man['original_pck_md5']
    if os.path.exists(orig):
        if md5(orig) != want: raise SystemExit('CICADAMATA.pck.orig is not the expected original.')
    else:
        if md5(pck) != want: raise SystemExit('CICADAMATA.pck is not the version this translation was made for.')
        shutil.copy2(pck, orig)
    build(orig, pck, payload)
    print('Russian localization v%s installed.' % man['version'])

def restore(game):
    pck, orig = os.path.join(game, 'CICADAMATA.pck'), os.path.join(game, 'CICADAMATA.pck.orig')
    if not os.path.exists(orig): raise SystemExit('No backup (CICADAMATA.pck.orig) found.')
    shutil.copy2(orig, pck); print('Original restored.')

if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['build']: build(a[1], a[2], a[3] if len(a) > 3 else DEF_PAYLOAD); print('built', a[2])
    elif a[:1] in (['install'], ['restore']):
        g = a[1] if len(a) > 1 else default_game_dir()
        if not g: raise SystemExit('Game folder not found; pass it as an argument.')
        (install if a[0] == 'install' else restore)(g)
    else: print(__doc__ or open(__file__).read().split('\n')[1:5])
