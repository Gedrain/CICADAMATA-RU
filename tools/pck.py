# Minimal Godot 4 .pck reader (format 2/3 directory, as used by CICADAMATA).
import struct, os
def read_dir(path):
    with open(path, 'rb') as f:
        hdr = struct.unpack('<4sIIIIIQQ', f.read(0x28))
        assert hdr[0] == b'GDPC', 'not a Godot pck'
        base, diroff = hdr[6], hdr[7]
        f.seek(diroff); n = struct.unpack('<I', f.read(4))[0]; ents = []
        for _ in range(n):
            l = struct.unpack('<I', f.read(4))[0]; p = f.read(l).rstrip(b'\0').decode()
            off, size = struct.unpack('<QQ', f.read(16)); md5 = f.read(16); fl = struct.unpack('<I', f.read(4))[0]
            ents.append((p, base + off, size, md5, fl))
    return hdr, ents
def extract(path, ents, pred, outdir):
    with open(path, 'rb') as f:
        for p, off, size, md5, fl in ents:
            if pred(p):
                out = os.path.join(outdir, p)
                os.makedirs(os.path.dirname(out), exist_ok=True)
                f.seek(off); open(out, 'wb').write(f.read(size))
