import csv,json,re,collections
csv.field_size_limit(10**9)
meta=json.load(open('meta.json'));cx=json.load(open('cx.json'))
r=list(csv.DictReader(open('/mnt/project-files/jle-article/references/refs_87journals_2022-2025_raw.csv',encoding='utf-8-sig')))
norm=lambda s:re.sub(r'[^a-z0-9]','',re.sub(r'<[^>]+>','',(s or '').lower()))[:60]
SD=collections.defaultdict(set);ST=collections.defaultdict(set)
for x in r: SD[x['Source title']].add(x['DOI'].lower().strip()); ST[x['Source title']].add(norm(x['Title']))
def clean(a): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',a or '')).strip()
EN=set('the of and to in is this that with for are as by be on study research'.split())
def isen(a):
    w=re.findall(r'[a-z]+',clean(a).lower());
    return len(w)>20 and sum(1 for x in w if x in EN)/len(w)>0.12
masks={};nds={};summ=[]
for m in meta:
    k='I%d'%m['i'];res=cx['res'].get(k,[])
    ins=[(x['d'] in SD[m['name']]) or (norm(x['t']) in ST[m['name']]) for x in res]
    sel=[];
    for j,f in enumerate(ins):
        if f and len(sel)<40: sel.append(j)
    masks[k]=sel
    nds[k]=[j for j in sel if not (res[j]['a'] and isen(res[j]['a']))]
    summ.append((k,len(res),sum(ins),len(sel),len(nds[k])))
json.dump({'masks':masks,'nds':nds},open('sel.json','w'))
print([s for s in summ if s[3]<40 or s[4]>5])
# compact for browser: per journal list of selected indices as base36 string
enc=lambda L:''.join('%02d'%j for j in L)
print(json.dumps({k:enc(v) for k,v in masks.items()},separators=(',',':')).__len__())
