import struct, sys, os
from compression import zstd

def u32(b,o): return struct.unpack_from('<I',b,o)[0]

def load(path):
    raw=open(path,'rb').read()
    assert raw[:4]==b'GDSC', path
    ver=u32(raw,4); dsize=u32(raw,8)
    body=zstd.decompress(raw[12:]) if dsize else raw[12:]
    if dsize: assert len(body)==dsize
    return ver, body

def parse_variant(b,o):
    """returns (value, new_offset). value is ('type', python value)"""
    h=u32(b,o); t=h&0xff; f64=h&(1<<16); o+=4
    if t==0: return ('nil',None),o
    if t==1: return ('bool',u32(b,o)),o+4
    if t==2:
        if f64: return ('int',struct.unpack_from('<q',b,o)[0]),o+8
        return ('int',struct.unpack_from('<i',b,o)[0]),o+4
    if t==3:
        if f64: return ('float',struct.unpack_from('<d',b,o)[0]),o+8
        return ('float',struct.unpack_from('<f',b,o)[0]),o+4
    if t in (4,21):
        l=u32(b,o); o+=4
        s=b[o:o+l].decode('utf-8'); o+=l
        o+=(-l)%4
        return (('str' if t==4 else 'sname'),s),o
    if t==22:  # NodePath
        n=u32(b,o); o+=4
        assert n&0x80000000
        n&=0x7fffffff
        sub=u32(b,o); o+=4
        flags=u32(b,o); o+=4
        parts=[]
        for _ in range(n+sub):
            l=u32(b,o); o+=4
            parts.append(b[o:o+l].decode()); o+=l+((-l)%4)
        return ('nodepath',(n,sub,flags,parts)),o
    raise ValueError('unsupported variant type %d at %d'%(t,o-4))

def encode_variant(v):
    k,val=v
    if k in('str','sname'):
        t=4 if k=='str' else 21
        e=val.encode('utf-8')
        return struct.pack('<II',t,len(e))+e+b'\0'*((-len(e))%4)
    raise ValueError(k)

def parse(path):
    ver,b=load(path)
    idc,cc,lc,tc=struct.unpack_from('<IIII',b,0)
    o=16
    idents=[]
    for _ in range(idc):
        l=u32(b,o); o+=4
        chars=[u32(b,o+4*i)^0xb6b6b6b6 for i in range(l)]
        idents.append(''.join(map(chr,chars))); o+=4*l
    cstart=o
    consts=[]
    for _ in range(cc):
        v,o=parse_variant(b,o); consts.append(v)
    return dict(ver=ver,body=b,idents=idents,consts=consts,cstart=cstart,cend=o,counts=(idc,cc,lc,tc))

def rebuild(info, consts):
    b=info['body']
    mid=b''
    for v in consts:
        # re-encode only strings; keep others raw by re-parsing positions
        mid+=encode_variant(v) if v[0] in('str','sname') else None
    raise NotImplementedError

if __name__=='__main__':
    for p in sys.argv[1:]:
        i=parse(p)
        print('==',p,i['ver'],i['counts'])
        for k,v in i['consts']:
            if k=='str': print('  ',repr(v))
