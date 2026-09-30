#!/usr/bin/env python3
# Builds v2 translation data: scripts_map_v2.json (compiled-script constants) and catalog_v2.json
# (Godot translation catalog) from the v1 data + v2_revise.py + v2_new.py.
import json, re, sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import KIT as K, WORK as W, SRC
sys.path.insert(0, SRC)
import v2_revise as R, v2_new as N

M = json.load(open(K + '/translations_src/scripts_map.json'))
C = json.load(open(SRC + '/catalog_v1_final.json'))
tracks = json.load(open(W + '/anim_tracks_all.json'))
nodes = json.load(open(W + '/nodes.json'))
static = {n['text'] for v in nodes.values() for n in v if n['text']}

# 1. drop v1 typewriter partials (regenerated below)
finals_any, partial_any = set(), set()
for f, p, strs in tracks:
    core = [x.rstrip('\n') for x in strs]
    for i, c in enumerate(core):
        if any(j != i and core[j].startswith(c) and len(core[j]) > len(c) for j in range(len(core))):
            partial_any.add(strs[i])
        else:
            finals_any.add(strs[i])
drop = {k for k in C if k in partial_any and k not in finals_any and k not in static}
for k in drop: C.pop(k)

# 2. revisions
miss = []
def revise(d):
    for k in list(d):
        if k in R.FULL: d[k] = R.FULL[k]
        subs = list(R.SUB.get(k, []))
        for pre, s in R.SUB_PREFIX.items():
            if k.startswith(pre): subs += s
        for a, b in subs:
            if a not in d[k]: miss.append((k[:40], a))
            d[k] = d[k].replace(a, b)
revise(M); revise(C)
for k in R.FULL:
    if k not in M and k not in C: C[k] = R.FULL[k]   # e.g. finals that only existed as v1 anim entries

# 3. new strings
M.update(N.SCRIPT); C.update(N.CAT)

# 4. regenerate typewriter partials from finals
def partial(v, en_f, ru_f):
    core = v.rstrip('\n')
    el = en_f.rstrip('\n').split('\n'); rl = ru_f.rstrip('\n').split('\n')
    cl = core.split('\n'); k = len(cl) - 1
    if k >= len(rl): return None
    out = rl[:k]
    frac = len(cl[k]) / max(1, len(el[k]))
    n = math.ceil(frac * len(rl[k])) if frac < 1 else len(rl[k])
    if frac > 0 and n == 0: n = 1
    out.append(rl[k][:n].rstrip(' '))
    r = '\n'.join(out)
    return r + '\n' * (v.count('\n') - r.count('\n'))
gen, conflicts, untr = {}, [], set()
for f, p, strs in tracks:
    fin = [s for s in strs if s in C and s not in gen]
    for v in strs:
        if v in C and v not in gen: continue
        cands = [s for s in fin if s.rstrip('\n').startswith(v.rstrip('\n')) and s != v]
        if not cands:
            if re.search('[A-Za-z]', v): untr.add((f, v))
            continue
        en_f = min(cands, key=len)
        ru = partial(v, en_f, C[en_f])
        if ru is None: continue
        if v in gen and gen[v] != ru: conflicts.append((v, gen[v], ru)); continue
        gen[v] = ru
C.update(gen)

# 5. checks
issues = []
ph = lambda s: sorted(re.findall(r'%[-0-9.]*[dsfx]|\[/?(?:wave|pulse|color|b|i|shake|rainbow|center|url)[^\]]*\]', s))
for tag, d in (('M', M), ('C', C)):
    for k, v in d.items():
        if ph(k) != ph(v): issues.append((tag, 'PH', k[:50]))
        if k.count('\n') != v.count('\n') and k not in gen: issues.append((tag, 'NL', k[:50]))
        if (k.startswith('+ ') != v.startswith('+ ')) or (k.endswith(' ') != v.endswith(' ')) or (k.startswith('\n') != v.startswith('\n')):
            issues.append((tag, 'EDGE', k[:50]))

json.dump(M, open(W + '/scripts_map_v2.json', 'w'), ensure_ascii=False, indent=0)
json.dump(C, open(W + '/catalog_v2.json', 'w'), ensure_ascii=False, indent=0)
print('scripts', len(M), 'catalog', len(C), 'dropped partials', len(drop), 'regenerated', len(gen))
print('missing SUB targets', miss)
print('partial conflicts', conflicts[:8])
print('issues', len(issues)); [print('  ', i) for i in issues[:40]]
json.dump(sorted(untr), open(W + '/anim_untranslated.json', 'w'), ensure_ascii=False, indent=0)
