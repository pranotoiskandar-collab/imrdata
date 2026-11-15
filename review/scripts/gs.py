import csv,glob,collections,re,json
D='/mnt/project-files/jle-article/'
key=lambda t:t.lower().split(':')[0].strip()
IDL={key(r['title']) for r in csv.DictReader(open(D+'scimago2025_law_indonesia.csv',encoding='utf-8-sig'))}
latest={}
for f in glob.glob(D+'*_citescore_citing_*_raw.csv'):
    s,y=re.match(r'.*/(\w+?)_citescore_citing_(\d+)_raw',f).groups()
    if s not in latest or int(y)>latest[s][0]: latest[s]=(int(y),f)
# Indonesian DOI prefixes: every prefix seen on law-list citers, plus known Indonesian publishers
IDP=set('10.31538 10.20414 10.24252 10.15642 10.15575 10.30821 10.14421 10.59373 10.31291 10.20885 10.22437 10.19105 10.53754 10.18326 10.14710 10.22373 10.18592 10.21043 10.22219 10.24815 10.29244 10.7226 10.22146 10.21512 10.21098 10.34306 10.25217 10.11591 10.58524 10.15294 10.24090 10.18860 10.21107 10.19184 10.29300 10.51825 10.20961 10.30996 10.56784 10.26740 10.7454 10.62264 10.53955 10.31958 10.30984 10.26532 10.52496 10.18326 10.24815 10.35905 10.21009 10.23917 10.20473 10.23969'.split())
NORTH_PUB={'10.1016':'Elsevier','10.1007':'Springer','10.1057':'Springer','10.1080':'Taylor & Francis','10.4324':'Taylor & Francis','10.1201':'Taylor & Francis','10.1002':'Wiley','10.1111':'Wiley','10.1177':'Sage','10.1093':'OUP','10.1017':'CUP','10.1163':'Brill','10.1108':'Emerald','10.1515':'De Gruyter','10.1109':'IEEE','10.1063':'AIP','10.1061':'ASCE','10.3390':'MDPI','10.3389':'Frontiers','10.1088':'IOP','10.1051':'EDP','10.4018':'IGI','10.1371':'PLOS','10.1097':'Wolters Kluwer','10.1186':'Springer','10.1038':'Springer'}
# venue -> region, by prefix or title keyword (hand-checked for venues with >=4 rows; long tail by keyword)
SOUTH_PFX={'10.33102':'Malaysia','10.22452':'Malaysia','10.32890':'Malaysia','10.47836':'Malaysia','10.17576':'Malaysia','10.31436':'Malaysia','10.24035':'Malaysia','10.7187':'Malaysia','10.21837':'Malaysia','10.37934':'Malaysia','10.55188':'Malaysia','10.21315':'Malaysia',
 '10.57239':'Pakistan','10.62271':'Pakistan','10.32350':'Pakistan','10.58256':'Pakistan',
 '10.24857':'Brazil','10.52028':'Brazil','10.18316':'Brazil','10.26668':'Brazil','10.9771':'Brazil','10.21902':'Brazil','10.26512':'Brazil','10.51798':'Brazil','10.31893':'Brazil',
 '10.14718':'Colombia','10.15332':'Colombia','10.54588':'Colombia',
 '10.46222':'South Africa','10.4102':'South Africa','10.35516':'Jordan','10.48161':'Iraq','10.22034':'Iran','10.22122':'Iran','10.21608':'Egypt','10.21533':'Bosnia',
 '10.31548':'Ukraine','10.32518':'Ukraine','10.33327':'Ukraine','10.21511':'Ukraine','10.15826':'Russia','10.47750':'Romania','10.62768':'Romania','10.13165':'Lithuania','10.34625':'Portugal','10.14198':'Spain','10.3280':'Italy','10.35784':'Poland','10.7225':'Croatia','10.22495':'Ukraine','10.14330':'South Korea','10.14391':'South Korea','10.12924':'Germany'}
KW=[('malaysia','Malaysia'),('iium','Malaysia'),('ukm','Malaysia'),('pakistan','Pakistan'),('india','India'),('nigeria','Nigeria'),('africa','Africa'),('brasil','Brazil'),('brazil','Brazil'),('revista','Latin America/Iberia'),('cadernos','Brazil'),('egypt','Egypt'),('arab','Arab world'),('iran','Iran'),('turk','Turkey'),('bangladesh','Bangladesh'),('philippin','Philippines'),('thai','Thailand'),('viet','Vietnam'),('ukrain','Ukraine'),('kazakh','Kazakhstan'),('geopolitics quarterly','Iran'),('juridical tribune','Romania')]
GS_SOUTH={'Malaysia','Pakistan','India','Nigeria','Africa','South Africa','Brazil','Latin America/Iberia','Colombia','Egypt','Arab world','Iran','Iraq','Jordan','Turkey','Bangladesh','Philippines','Thailand','Vietnam','Kazakhstan','Bosnia'}
EAST={'Ukraine','Russia','Romania','Lithuania','Poland','Croatia'}
def classify(src,doi):
    p=doi.split('/')[0] if doi else ''
    if key(src) in IDL: return 'ID law list','Indonesia'
    t=src.lower()
    if p in IDP or 'indonesia' in t or t.startswith('jurnal') or 'nusantara' in t or 'jurnal' in t: return 'Indonesia other','Indonesia'
    if p in SOUTH_PFX: reg=SOUTH_PFX[p]
    else:
        reg=next((r for k,r in KW if k in t),None)
    if reg:
        return ('Global South (non-Indonesian)' if reg in GS_SOUTH else 'Eastern Europe' if reg in EAST else 'Other North'),reg
    if p in NORTH_PUB:
        pub=NORTH_PUB[p]
        if pub in ('EDP','IOP','AIP','IEEE') or 'conference' in t or 'proceedings' in t or 'lecture notes' in t: return 'North publisher: conference series',pub
        if pub in ('MDPI','IGI','Frontiers') or src.startswith('Cogent') or 'Heliyon' in src or 'Open' in src: return 'North publisher: high-volume OA / book',pub
        return 'North publisher: legacy journal or book',pub
    return 'Unplaced international','?'
rows=[];perj=collections.defaultdict(collections.Counter)
for s,(y,f) in latest.items():
    for r in list(csv.reader(open(f,encoding='utf-8-sig')))[1:]:
        if len(r)<11 or not r[3]: continue
        c,reg=classify(r[3],r[10]); rows.append((s,r[3],c,reg,r[1],r[10])); perj[s][c]+=1
T=len(rows); C=collections.Counter(x[2] for x in rows)
print('rows',T)
for c,n in C.most_common(): print(f'{c:45s}{n:6d} {100*n/T:5.1f}%')
R=collections.Counter(x[3] for x in rows if x[2]=='Global South (non-Indonesian)'); print('GS regions',R.most_common())
gsv=collections.Counter(x[1] for x in rows if x[2]=='Global South (non-Indonesian)'); print('GS top venues',gsv.most_common(15))
nl=collections.Counter(x[1] for x in rows if x[2]=='North publisher: legacy journal or book'); print('North legacy top',nl.most_common(25))
print('N legacy distinct venues',len(nl))
up=collections.Counter(x[1] for x in rows if x[2]=='Unplaced international'); print('unplaced',len(up),up.most_common(25))
# per journal: GS share vs north legacy share
out=[]
for s,cc in perj.items():
    n=sum(cc.values()); out.append((s,n,round(100*cc['Global South (non-Indonesian)']/n,1),round(100*cc['North publisher: legacy journal or book']/n,1),round(100*(cc['ID law list']+cc['Indonesia other'])/n,1)))
z=sum(1 for o in out if o[2]==0); print('journals with zero GS citations',z,'of',len(out)); print('journals with zero North legacy',sum(1 for o in out if o[3]==0))
print('top GS',sorted(out,key=lambda o:-o[2])[:10]); print('top Nleg',sorted(out,key=lambda o:-o[3])[:10])
json.dump(dict(C=C,R=R),open('gs_summary.json','w'))
csv.writer(open('gs_rows.csv','w')).writerows(rows)
csv.writer(open('gs_perjournal.csv','w')).writerows([('journal','rows','global_south_pct','north_legacy_pct','indonesia_pct')]+sorted(out))
