import json,re,collections,sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import WORK as W
M=json.load(open(W+'/scripts_map_v2.json')); C=json.load(open(W+'/catalog_v2.json'))
NAMES=set('''JOYEUSE Joyeuse JOYEU JOYE JOY JY SE USE FAWN-A2 FAWN Fawn fawn FAWNA2 AUGUST August Celeste AEGIS-017 AEGIS Aegis DEMETER demeter DIONYSUS CLOVER ceres
MARCH March DECEMBER-C1 DECEMBER-A1 D-C1 SABLE-L3 S-L3 MIYA-H5 ROWAN-K4 HALCA-O6 TAINA-I7 JACK-L3 GALWAY-O6 EZRA HAINE SOL KYRIE VALENTINE HAUTECLERE CLARENT
JANUARY CICADAMATA CCDAMTA CCDAMTA_ FLOWERGARDEN FLWRGRDN01 FLWRGRDN00 MATA mata GODOT Godot ST_SANVEI St Sanvei SANVEI ST David
CRT FPS FOV ID WASD CTRL SHIFT II VII IV Y E J X L R D M P O W F T C S A B TEST5 XX
LB RB LT RT LS RS'''.split())
bad=collections.Counter(); ex={}
for tag,d in (('M',M),('C',C)):
    for k,v in d.items():
        t=re.sub(r'\[/?[a-z_]+[^\]]*\]','',v); t=re.sub(r'%[-0-9.]*[a-z]','',t)
        t=re.sub(r'AEGIS-017_ENTRY\d+|CONVLOG\d+|\bstr__|_\$','',t)
        for w in re.findall(r"[A-Za-z][A-Za-z0-9\-]*",t):
            if w in NAMES or re.fullmatch(r'[A-Z]\d*|\d+[A-Za-z]+',w): continue
            bad[w]+=1; ex.setdefault(w,(tag,k[:70],v[:90]))
for w,n in bad.most_common():
    print(n,w,'|',ex[w])
