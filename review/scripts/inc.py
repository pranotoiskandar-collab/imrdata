import csv,re,collections,json,openpyxl
def norm(t): return re.sub(r'[^a-z0-9]','',re.sub(r'\b(dan|and|the|of|&)\b|&',' ',t.lower()))
sm=json.load(open('srclist/srcmap.json'))
wb=openpyxl.load_workbook('srclist/ext_list_Oct_2026.xlsx',read_only=True)
conf=set()
for sh in ['Serial Conf. Proc. with Profile','All Conf. Proceedings Jun. 2026']:
    ws=wb[sh]; rows=ws.iter_rows(values_only=True); hdr=next(rows)
    for r in rows:
        for c in r[:4]:
            if isinstance(c,str) and len(c)>15: conf.add(norm(c))
print('conf titles',len(conf))
CK=re.compile(r'conference|proceedings|symposium|seminar|congress|workshop|\bicon|\bicl',re.I)
CDOI=re.compile(r'^10\.(2991|1051/(shsconf|e3sconf|matecconf|bioconf|itmconf)|1088/(1755-1315|1742-6596|1757-899x)|1063/|1145/|1109/ic|4108/eai)',re.I)
BDOI=re.compile(r'^10\.\d+/(978|9781|9780|oso|b\d)|/978\d|^10\.4018/978|^10\.1093/oso|^10\.1017/97|^10\.4324/97|^10\.1201/97|^10\.5040/97|^10\.1515/97',re.I)
rows=list(csv.reader(open('gs_rows.csv')))
print('rows',len(rows))
C=collections.Counter(); ex=collections.defaultdict(collections.Counter)
for r in rows:
    j,s,g,c,t,doi=r[:6]; k=norm(s); m=sm.get(k); d=(doi or '').lower()
    if CDOI.search(d) or CK.search(s) or k in conf: typ='Conference proceedings'
    elif m and m['type']=='Book Series': typ='Book series'
    elif BDOI.search(d): typ='Book or chapter'
    elif m: typ='Journal (Scopus-listed)'
    else: typ='Other or unmatched'
    ind = g.startswith('Indonesia') or g=='Listed'
    C[(typ,'Indonesia' if g in('listed','Indonesia other') else 'Abroad')]+=1
    ex[typ][s]+=1
for k,v in sorted(C.items()): print(k,v)
print(collections.Counter(r[2] for r in rows))
for t in ex: print('##',t,ex[t].most_common(8))
