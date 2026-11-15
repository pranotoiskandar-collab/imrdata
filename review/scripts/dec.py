import json,sys,zlib,re,glob,os
# usage: dec.py outfile file1 file2 ... (tool-result json files, any order)
def val(c):
    o=ord(c)
    if 0x4E00<=o<0x4E00+20992: return o-0x4E00
    if 0xAC00<=o<0xAC00+11172: return 20992+o-0xAC00
    if 0x3400<=o<0x3400+6592: return 32164+o-0x3400
    raise ValueError(hex(o))
chunks={};tot=None;nbytes=None
for f in sys.argv[2:]:
    for it in json.load(open(f)):
      t=it.get('text','')
      for m in re.finditer(r'<<<(\d+)\|(\d+)\|(\d+)\|([^>]*)>>>',t):
        i,n,nb,p=int(m.group(1)),int(m.group(2)),int(m.group(3)),m.group(4)
        chunks[i]=p;tot=n;nbytes=nb
assert sorted(chunks)==list(range(tot)),(sorted(chunks),tot)
s=''.join(chunks[i] for i in range(tot))
bits=0;acc=0;out=bytearray()
for c in s:
    acc=(acc<<15)|val(c);bits+=15
    while bits>=8:
        bits-=8;out.append((acc>>bits)&255)
    acc&=(1<<bits)-1
out=bytes(out[:nbytes])
data=zlib.decompress(out,-15)
open(sys.argv[1],'wb').write(data)
print('ok',len(data))
