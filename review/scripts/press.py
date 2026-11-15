import json,re,csv,collections
def norm(t): return re.sub(r'[^a-z0-9]','',re.sub(r'\b(dan|and|the|of|&)\b|&',' ',str(t).lower()))
L=json.load(open('srclist/srcmap.json'))
out=json.load(open('dash/refs_out.json'))
EXC=re.compile(r'Tsinghua|Istanbul|Lodz|Zhejiang|Jagiellonian|Vilnius|Ljubljana|Tartu|Utara|Putra|Bucharest|Galati|Cherkas|AGH|Maribor|Military|Pretoria|Tokyo|Hong Kong|IUC|Universa Press|International Universities|MCB|Kazan|Moscow|Seoul|Kyoto|Peking|Shanghai|Wuhan|Malaya|Malaysia|Universiti|Qatar|Multimedia|Indonesia|Gadjah|Cairo|Tehran|King Saud|Sultan',re.I)
def pclass(p):
    if not p: return 'Not identified'
    if (re.search(r'univ.*press|press.*univ|MIT Press|Presses Universitaires|UCOPress',p,re.I) and not EXC.search(p)): return 'Western university press'
    if re.search(r'Elsevier|Springer|Wiley|Taylor|Routledge|SAGE|Emerald|Brill|De Gruyter|Kluwer|Hart|Edward Elgar|Palgrave|Bloomsbury',p,re.I): return 'Major Western commercial publisher'
    return 'Other publisher'
SSH=re.compile(r'^(12|14|18|20|32|33)\d\d$')
def sclass(codes):
    cs=[c.strip() for c in codes.split(';') if c.strip()]
    if not cs: return 'Not identified'
    if '3308' in cs: return 'Law'
    if any(SSH.match(c) for c in cs): return 'Other social sciences and humanities'
    if all(c.startswith('10') for c in cs): return 'Multidisciplinary'
    return 'Sciences, engineering, health'
def look(s):
    r=L.get(norm(s))
    if r is None:
        n=norm(s); 
        if n.endswith('switzerland'): r=L.get(n[:-11])
    return r
# incoming
inc_p=collections.Counter(); inc_s=collections.Counter(); inc_up=collections.Counter(); inc_far=collections.Counter()
inc_up_j=collections.defaultdict(set)
M={}
for r in csv.reader(open('gs_rows.csv')):
    if r[2]=='ID law list': inc_p['(listed journals)']+=1; inc_s['Law']+=1; continue
    rec=look(r[1]); p=pclass(rec['publisher']) if rec else 'Not identified'; sc=sclass(rec['asjc']) if rec else 'Not identified'
    inc_p[p]+=1; inc_s[sc]+=1
    if p=='Western university press': inc_up[(r[1],rec['publisher'])]+=1; inc_up_j[(r[1],rec['publisher'])].add(r[0])
    if sc=='Sciences, engineering, health': inc_far[(r[1],rec['asjc'])]+=1
# outgoing
out_p=collections.Counter(); out_s=collections.Counter(); out_up=collections.Counter(); out_far=collections.Counter(); out_up_j=collections.defaultdict(set)
for a,c in out.items():
    for s,n in c.items():
        if s.startswith('LIST:'): out_p['(listed journals)']+=n; out_s['Law']+=n; continue
        if s.startswith('~'): out_p['Books and other works']+=n; out_s['Books and other works']+=n; continue
        rec=look(s); p=pclass(rec['publisher']) if rec else 'Not identified'; sc=sclass(rec['asjc']) if rec else 'Not identified'
        out_p[p]+=n; out_s[sc]+=n
        if p=='Western university press': out_up[(rec['title'],rec['publisher'])]+=n; out_up_j[(rec['title'],rec['publisher'])].add(a)
        if sc=='Sciences, engineering, health': out_far[(rec['title'],rec['asjc'])]+=n
print('INCOMING pub',inc_p); print('INCOMING subj',inc_s)
print('OUT pub',out_p); print('OUT subj',out_s)
print('UP citing list:',sum(inc_up.values()),len(inc_up)); print(inc_up.most_common(20))
print('UP cited by list:',sum(out_up.values()),len(out_up)); print(out_up.most_common(25))
print('FAR in', inc_far.most_common(10)); print('FAR out', out_far.most_common(10))
json.dump(dict(inc_p=inc_p,inc_s=inc_s,out_p=out_p,out_s=out_s,inc_up=[[k[0],k[1],v,len(inc_up_j[k])] for k,v in inc_up.most_common()],out_up=[[k[0],k[1],v,len(out_up_j[k])] for k,v in out_up.most_common()],inc_far=[[k[0],k[1],v] for k,v in inc_far.most_common(40)],out_far=[[k[0],k[1],v] for k,v in out_far.most_common(40)]),open('dash/press.json','w'))
