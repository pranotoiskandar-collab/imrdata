import csv,json,re,collections
exec(open('dash/refs.py').read().split("R=list(")[0])  # M, norm, t2s
out=json.load(open('dash/refs_out.json'))
# citing side from gs_rows: cited journal slug, citing source, category, country
cit=collections.defaultdict(collections.Counter); cat={}; disp={}
for r in csv.reader(open('gs_rows.csv')):
    k=norm(r[1]); 
    if r[2]=='ID law list': continue
    cit[k][r[0]]+=1; cat[k]=(r[2],r[3]); disp.setdefault(k,r[1])
refd=collections.defaultdict(collections.Counter); disp2={}
for a,c in out.items():
    for s,n in c.items():
        if s.startswith(('LIST:','~')): continue
        k=norm(s); k={'sustainabilityswitzerland':'sustainability'}.get(k,k)
        refd[k][a]+=n; disp2.setdefault(k,collections.Counter())[s]+=n
keys=set(cit)&set(refd)
rows=[]
for k in keys:
    ci=sum(cit[k].values()); rf=sum(refd[k].values())
    rows.append(dict(key=k,name=disp.get(k) or disp2[k].most_common(1)[0][0],category=cat[k][0],country=cat[k][1],cites_list=ci,cited_by_list=rf,journals_citing_it=len(refd[k]),journals_it_cites=len(cit[k])))
rows.sort(key=lambda d:-(min(d['cites_list'],d['cited_by_list'])))
print(len(keys))
for d in rows[:45]: print(d['cites_list'],d['cited_by_list'],d['category'][:20],d['country'],'|',d['name'])
json.dump(dict(rows=rows,cit={k:dict(cit[k]) for k in keys},refd={k:dict(refd[k]) for k in keys}),open('dash/connect.json','w'))
