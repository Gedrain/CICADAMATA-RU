# Parses recovered .tscn files: for every node -> full path, type, resolved font file, static text.
import re, glob, os, json
DECO = ('N4NOOSE', 'n4noose', 'Dotsies')
def _str(s):
    return json.loads('"%s"' % s, strict=False)
def parse(root):
    out = {}
    for f in sorted(glob.glob(root + '/**/*.tscn', recursive=True)):
        s = open(f, encoding='utf-8').read(); b = os.path.relpath(f, root)
        ext = {m.group(2): os.path.basename(m.group(1)) for m in re.finditer(r'\[ext_resource[^\]]*path="([^"]+)"[^\]]*id="([^"]+)"', s)}
        subs = {}
        for m in re.finditer(r'\[sub_resource type="(\w+)" id="([^"]+)"\](.*?)(?=\n\[|\Z)', s, re.S):
            fm = re.search(r'(?:base_)?font = (Ext|Sub)Resource\("([^"]+)"\)', m.group(3))
            if fm: subs[m.group(2)] = ext.get(fm.group(2), '?') if fm.group(1) == 'Ext' else ('sub:' + fm.group(2))
        for k, v in list(subs.items()):
            if v.startswith('sub:'): subs[k] = subs.get(v[4:], '?')
        nodes = []
        for m in re.finditer(r'\[node name="([^"]+)"([^\]]*)\](.*?)(?=\n\[|\Z)', s, re.S):
            hdr, blk = m.group(2), m.group(3)
            pm = re.search(r'parent="([^"]*)"', hdr); par = pm.group(1) if pm else None
            full = m.group(1) if par in (None,) else (m.group(1) if par == '.' else par + '/' + m.group(1))
            tm = re.search(r'type="([^"]+)"', hdr)
            fonts = []
            for fm in re.finditer(r'^(?:theme_override_fonts/(?:font|normal_font|bold_font|italics_font|mono_font)|font|label_settings) = (Ext|Sub)Resource\("([^"]+)"\)', blk, re.M):
                fonts.append(ext.get(fm.group(2), '?') if fm.group(1) == 'Ext' else subs.get(fm.group(2), ''))
            txt = re.search(r'^text = "((?:[^"\\]|\\.)*)"', blk, re.M | re.S)
            nodes.append(dict(name=m.group(1), path=full, root=par is None, type=tm.group(1) if tm else '', fonts=[x for x in fonts if x],
                              text=_str(txt.group(1)) if txt else None, deco=any(any(d in x for d in DECO) for x in fonts)))
        out[b] = nodes
    return out
def resolve(nodes, track_path, player_parent):
    # AnimationPlayer root_node default '..' = parent of player; track path relative to that.
    p = track_path
    base = player_parent.split('/') if player_parent not in ('', '.') else []
    for part in p.split('/'):
        if part == '..': base = base[:-1]
        elif part == '.': pass
        else: base.append(part)
    full = '/'.join(base)
    for n in nodes:
        if (n['path'] if not n['root'] else '') == full or (full == '' and n['root']): return n
    return None
if __name__ == '__main__':
    import sys
    r = parse(sys.argv[1]); json.dump(r, open(sys.argv[2], 'w'), ensure_ascii=False)
    print(len(r), sum(len(v) for v in r.values()))
