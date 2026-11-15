import json,sys,zlib,re,glob,os
def val(c):
    o=ord(c)
    if 0x4E00<=o<0x4E00+20992: return o-0x4E00
    if 0xAC00<=o<0xAC00+11172: return 20992+o-0xAC00
    if 0x3400<=o<0x3400+6592: return 32164+o-0x3400
    raise ValueError(hex(o))
def unpack(s,nb):
    bits=0;acc=0;out=bytearray()
    for c in s:
        acc=(acc<<15)|val(c);bits+=15
        while bits>=8:
            bits-=8;out.append((acc>>bits)&255)
        acc&=(1<<bits)-1
    return zlib.decompress(bytes(out[:nb]),-15)
groups={}
D='/root/.claude/projects/-home-claude/02493dcd-1fa5-5a7a-8837-b8f092c62a5d/tool-results/'
for f in sorted(glob.glob(D+'toolu_*.json')):
    for it in json.load(open(f)):
        t=it.get('text','')
        for m in re.finditer(r'<<<(\d+)\|(\d+)\|(\d+)\|([^>]*)>>>',t):
            i,n,nb,p=int(m.group(1)),int(m.group(2)),int(m.group(3)),m.group(4)
            groups.setdefault((n,nb),{})[i]=p
res={}
for (n,nb),ch in groups.items():
    if sorted(ch)!=list(range(n)): print('incomplete',n,nb);continue
    d=json.loads(unpack(''.join(ch[i] for i in range(n)),nb))
    if 'host' in d: res[d['host']]=d
old=json.load(open('hosts.json')) if os.path.exists('hosts.json') else {}
old.update(res);json.dump(old,open('hosts.json','w'))
for h,d in old.items(): print(h,{k:(J.get('og'),J.get('oe'),J.get('me')) for k,J in d['J'].items()},len(d['r']))
