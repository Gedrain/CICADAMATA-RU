import struct,sys
def u32(b,o): return struct.unpack_from('<I',b,o)[0]
def read(path):
    b=open(path,'rb').read(); assert b[:4]==b'ECFG'
    n=u32(b,4); o=8; out=[]
    for _ in range(n):
        l=u32(b,o); o+=4; k=b[o:o+l].decode(); o+=l
        vl=u32(b,o); o+=4; v=b[o:o+vl]; o+=vl
        out.append((k,v))
    assert o==len(b),(o,len(b))
    return out
def write(path,entries):
    b=bytearray(b'ECFG'+struct.pack('<I',len(entries)))
    for k,v in entries:
        kb=k.encode(); b+=struct.pack('<I',len(kb))+kb+struct.pack('<I',len(v))+v
    open(path,'wb').write(bytes(b))
def s_enc(s):
    e=s.encode(); return struct.pack('<II',4,len(e))+e+b'\0'*((-len(e))%4)
def psa_enc(lst):
    b=struct.pack('<II',34,len(lst))
    for s in lst:
        e=s.encode(); b+=struct.pack('<I',len(e))+e+b'\0'*((-len(e))%4)
    return b
if __name__=='__main__':
    for k,v in read(sys.argv[1]):
        if k.startswith(('internationalization','application/config/name','gui/','autoload/Global','application/run')): print(k,v[:80])
