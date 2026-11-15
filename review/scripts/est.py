import csv,re,statistics as st
P='/mnt/project-files/jle-article/'
docs={r['law_rank']:int(r['docs_2025'] or 0) for r in csv.DictReader(open(P+'scimago2025_law_indonesia.csv'))}
rows=list(csv.DictReader(open(P+'references/apc/apc_journals.csv')))
FX=16300
def idr(v,c):
    ns=[float(x) for x in v.split('-')]
    c=c.strip()
    if c=='not stated': c='IDR'
    k=FX if c=='USD' else 1
    return [n*k for n in ns]
ch=[];none=[];unk=[]
for r in rows:
    n=docs.get(r['law_rank'],0); a=r['apc_amount']
    if a=='not found': unk.append(n);continue
    if a=='0': none.append(n);continue
    vals=[];cs=r['currency'].split(';')
    for i,p in enumerate(a.split(';')): vals.append(idr(p.strip(),cs[i] if i<len(cs) else cs[-1]))
    first=min(vals[0]); hi=max(max(v) for v in vals)
    ch.append((r['title'],n,first,hi))
T=sum(docs.values()); print('docs2025 total',T,'charge',sum(x[1] for x in ch),'none',sum(none),'unk',sum(unk))
lo=sum(n*f for _,n,f,_ in ch); hi=sum(n*h for _,n,_,h in ch)
med=st.median([f for *_,f,_ in ch]); mn=st.mean([f for *_,f,_ in ch])
print('median %.1fm mean %.1fm'%(med/1e6,mn/1e6))
print('2025 low %.2f bn, high %.2f bn, high+unk %.2f bn'%(lo/1e9,hi/1e9,(hi+sum(unk)*med)/1e9))
print('USD: %.0fk %.0fk %.0fk'%(lo/FX/1e3,hi/FX/1e3,(hi+sum(unk)*med)/FX/1e3))
f=7046/T; print('4yr factor',round(f,2),'4yr low %.1f bn high %.1f bn'%(lo*f/1e9,(hi+sum(unk)*med)*f/1e9))
for t,n,a,b in sorted(ch,key=lambda x:-x[1]*x[2])[:10]: print(t[:40],n,a/1e6,round(n*a/1e9,2))
