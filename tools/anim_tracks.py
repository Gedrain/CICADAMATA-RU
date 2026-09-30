# Collects every animated `text` track from the recovered scenes -> WORK/anim_tracks_all.json
import re, glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import WORK
def unq(s): return s.encode('utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8')
def main():
    tracks = []
    for f in sorted(glob.glob(os.path.join(WORK, 'src2') + '/**/*.tscn', recursive=True)):
        if '/addons/' in f: continue
        s = open(f, encoding='utf-8').read()
        for m in re.finditer(r'tracks/(\d+)/path = NodePath\("([^"]*):text"\)(.*?)tracks/\1/keys = \{(.*?)\n\}', s, re.S):
            vals = re.findall(r'"values": \[(.*?)\]\n?', m.group(4), re.S)
            strs = [unq(x) for x in re.findall(r'"((?:[^"\\]|\\.)*)"', ' '.join(vals))]
            strs = [x for x in strs if re.search('[A-Za-z]', x)]
            if strs: tracks.append((f.split('/')[-1], m.group(2), strs))
    json.dump(tracks, open(os.path.join(WORK, 'anim_tracks_all.json'), 'w'), ensure_ascii=False, indent=0)
    print('animated text tracks', len(tracks))
if __name__ == '__main__': main()
