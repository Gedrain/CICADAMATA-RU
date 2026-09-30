#!/usr/bin/env python3
# Writes Russian copies of compiled scripts: string constants replaced via scripts_map_v2.json.
# Token stream, identifiers and non-string constants are verified unchanged.
import sys, os, glob, json, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import gdc
from compression import zstd
from common import WORK as W
X = W + '/x'; OUT = W + '/out_v2'
MAP = json.load(open(W + '/scripts_map_v2.json'))
UNSAFE = set(json.load(open(W + '/unsafe.json'))) - {'SPHERE ', 'PROTO ', 'BONUS '}
# per-file: constants that must stay English (QR-code payloads)
KEEP = {'Scripts/UI/cicadaranking.gdc': {'CI'}, 'Scripts/UI/end_of_demo.gdc': {'CI'}}
report = {}
for p in sorted(glob.glob(X + '/**/*.gdc', recursive=True)):
    rel = p[len(X) + 1:]
    if rel.startswith('addons/'): continue
    info = gdc.parse(p); b = info['body']; o = info['cstart']; out = bytearray(); changed = []
    for _ in range(info['counts'][1]):
        v, o2 = gdc.parse_variant(b, o)
        if v[0] == 'str' and v[1] in MAP and v[1] not in UNSAFE and v[1] not in KEEP.get(rel, ()):
            out += gdc.encode_variant(('str', MAP[v[1]])); changed.append(v[1])
        else: out += b[o:o2]
        o = o2
    assert o == info['cend']
    if not changed: continue
    body = b[:info['cstart']] + bytes(out) + b[info['cend']:]
    dst = os.path.join(OUT, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'wb').write(b'GDSC' + struct.pack('<II', info['ver'], len(body)) + zstd.compress(body))
    n = gdc.parse(dst)
    assert n['idents'] == info['idents'] and n['counts'] == info['counts']
    for a, c in zip(info['consts'], n['consts']):
        if a != c: assert a[0] == 'str' and c[1] == MAP[a[1]]
    assert n['body'][n['cend']:] == b[info['cend']:]
    report[rel] = len(changed)
json.dump(report, open(W + '/patch_report.json', 'w'), indent=0)
print('files', len(report), 'strings', sum(report.values()))
used = {s for p in glob.glob(X + '/**/*.gdc', recursive=True) if '/addons/' not in p for k, s in gdc.parse(p)['consts'] if k == 'str'}
print('map keys not found in any script:', [k[:30] for k in MAP if k not in used][:20])
print('map keys skipped as unsafe:', sorted(k for k in MAP if k in UNSAFE))
