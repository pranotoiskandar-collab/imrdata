import csv,re,collections,json
csv.field_size_limit(10**9)
src=open('recip.py').read().split('latest={}')[0]
exec(src)   # M, norm, t2s, src2slug
M['alsyirah']="Jurnal Ilmiah Al-Syir'ah"; M['ijicl']='Indonesian Journal of International and Comparative Law'; M['mawaddah']='Mawaddah: Jurnal Hukum Keluarga Islam'
import re as _re
def norm(t): return _re.sub(r'[^a-z0-9]','',_re.sub(r'\b(dan|and|the|of|&)\b|&',' ',t.lower()))
t2s={norm(v):k for k,v in M.items()}
SL=set(json.load(open('srclist/srcmap.json')))
R=list(csv.DictReader(open('/mnt/project-files/jle-article/references/refs_87journals_2022-2025_raw.csv',encoding='utf-8-sig')))
R=[r for r in R if not r['Source title'].startswith('Constitutional Review ')]
def slug_of(t):
    n=norm(t)
    if n in t2s: return t2s[n]
    best=None
    for k,v in t2s.items():
        if len(k)>=6 and (n.startswith(k) or (k.startswith(n) and len(n)>=8)):
            if best is None or len(k)>len(best[0]): best=(k,v)
    return best[1] if best else None
num=re.compile(r'^(pp\.|p\.|[0-9ivxlcIVXLC\-–]+$|[0-9]+[A-Za-z]?$|e[0-9]+$|Art\. ?No)')
def parse(x):
    x=x.strip(); y=None
    m=re.search(r'\((\d{4})\)\s*$',x)
    if m: y=int(m.group(1)); x=x[:m.start()].rstrip(', ')
    seg=[s.strip() for s in x.split(', ')]
    had=False
    while len(seg)>2 and num.match(seg[-1]): seg.pop(); had=True
    if len(seg)<3: return None,y,had
    for k in (3,2):
        if len(seg)>k:
            j=', '.join(seg[-k:])
            if slug_of(j) or norm(j) in SL: return j,y,had
    return seg[-1],y,had
out=collections.defaultdict(collections.Counter)  # citing listed journal -> cited source string
kinds=collections.Counter()
for r in R:
    a=slug_of(r['Source title'])
    for x in re.split(r'(?<=\(\d{4}\)); ',r['References']):
        if not x.strip(): continue
        s,y,had=parse(x)
        if s is None: kinds['author-only or short']+=1; continue
        b=slug_of(s)
        if b: out[a]['LIST:'+b]+=1; kinds['listed journal']+=1
        elif had: out[a][s]+=1; kinds['other with volume/pages']+=1
        else: out[a]['~'+s]+=1; kinds['no volume (book, report, other)']+=1
print(kinds, sum(kinds.values()))
json.dump({k:dict(v) for k,v in out.items()},open('dash/refs_out.json','w'))
ext=collections.Counter()
for a,c in out.items():
    for s,n in c.items():
        if not s.startswith(('LIST:','~')): ext[norm(s)]+=n
print(len(ext)); print(ext.most_common(15))
print('refs per doc',sum(kinds.values())/len(R))
