import re,itertools
from PIL import ImageFont
def mk(path,size):
    f=ImageFont.truetype(path,size); return lambda s: f.getlength(s)
def blanks(line,w):
    # centered layout; returns list of (start,end) for runs of >=3 spaces
    W=w(line); x0=-W/2; out=[]
    for m in re.finditer(r' {3,}',line):
        a=x0+w(line[:m.start()]); b=x0+w(line[:m.end()]); out.append((a,b))
    return out
def fit(en_line,segs,w,maxpad=4,maxgap=40):
    """segs: russian text pieces between blanks. Returns best line."""
    target=blanks(en_line,w); k=len(target); assert len(segs)==k+1
    sp=w(' ')
    best=None
    def padded(seg,p):
        # insert p extra spaces after existing spaces inside segment (spread), or nothing if no spaces
        if p==0: return seg
        parts=seg.split(' ')
        if len(parts)<2: return None
        for i in range(p): parts[1+(i%(len(parts)-1))-1]+=' '
        return ' '.join(parts)
    for pads in itertools.product(range(maxpad+1),repeat=k+1):
        ps=[padded(s,p) for s,p in zip(segs,pads)]
        if None in ps: continue
        # choose gap sizes greedily per blank by search
        for ns in itertools.product(range(3,maxgap),repeat=k):
            line=ps[0]
            for n,s in zip(ns,ps[1:]): line+=' '*n+s
            bl=blanks(line,w)
            if len(bl)!=k: continue
            ok=all(a<=ta+2 and b>=tb-2 for (a,b),(ta,tb) in zip(bl,target))
            if not ok: continue
            cost=sum((a-ta)**2+(b-tb)**2 for (a,b),(ta,tb) in zip(bl,target))+sum(pads)*50
            if best is None or cost<best[0]: best=(cost,line)
    return best
