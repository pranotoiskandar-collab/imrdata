import csv,json,re,collections
exec(open('dash/refs.py').read().split("R=list(")[0])
out=json.load(open('dash/refs_out.json')); C=json.load(open('dash/connect.json'))
cat={}
for r in csv.reader(open('gs_rows.csv')): cat[norm(r[1])]=r[2]
ind=re.compile(r'\b(jurnal|hukum|syariah|syari|ilmu|kajian|pemikiran|masyarakat|keadilan|pembangunan|peradilan|kebijakan|ekonomi|islam\w*|studi|pendidikan|penelitian|negara|undang|rechtsvinding|rechtsidee|yustisia|iqtishad|tarbiyah|dakwah|ushuluddin|indonesia\w*|nusantara|universitas|fakultas)\b',re.I)
comp=collections.Counter()
for a,c in out.items():
    for s,n in c.items():
        if s.startswith('LIST:'): comp['Own journal' if s[5:]==a else 'Other listed journals']+=n
        elif s.startswith('~'): comp['Books, reports and other works']+=n
        else:
            k=norm(s); g=cat.get(k)
            if g in ('ID law list','Indonesia other') or (g is None and ind.search(s)): comp['Other Indonesian periodicals (approx.)']+=n
            else: comp['Periodicals outside Indonesia (approx.)']+=n
# unparsed count from refs.py run
comp['Unparsed (laws, websites, incomplete)']=74932
print(comp, sum(comp.values()))
with open('dash/refcomp.csv','w') as f:
    w=csv.writer(f); w.writerow(['category','references'])
    for k in ['Own journal','Other listed journals','Other Indonesian periodicals (approx.)','Periodicals outside Indonesia (approx.)','Books, reports and other works','Unparsed (laws, websites, incomplete)']: w.writerow([k,comp[k]])
# network additions
nodes=list(csv.DictReader(open('dash/net_nodes.csv'))); edges=list(csv.DictReader(open('dash/net_edges.csv')))
for n in nodes: n['country']=''
GRP={'Indonesia other':'Indonesia','Global South (non-Indonesian)':'Global South','North publisher: legacy journal or book':'Northern publisher','North publisher: conference series':'Northern publisher','North publisher: high-volume OA / book':'Northern publisher','Eastern Europe':'Eastern Europe','Other North':'Other North','Unplaced international':'Unclear base'}
sel=[d for d in C['rows'] if min(d['cites_list'],d['cited_by_list'])>=10]
names={n['id'] for n in nodes}
for d in sel:
    nm=d['name'] if d['name'] not in names else d['name']+' (outside list)'
    nodes.append(dict(id=nm,kind='connector',quartile='',in_scope='',citing_rows='',self_rows='',received=d['cited_by_list'],given=d['cites_list'],country=GRP.get(d['category'],'')+(' · '+d['country'] if d['country'] not in ('','?','Indonesia') else '')))
    for s,n in C['cit'][d['key']].items():
        if s in M: edges.append(dict(source=nm,target=M[s],rows=n,kind='connector'))
    for s,n in C['refd'][d['key']].items():
        if s in M: edges.append(dict(source=M[s],target=nm,rows=n,kind='connector'))
w=csv.DictWriter(open('dash/net_nodes.csv','w'),fieldnames=list(nodes[0]));w.writeheader();w.writerows(nodes)
w=csv.DictWriter(open('dash/net_edges.csv','w'),fieldnames=['source','target','rows','kind']);w.writeheader();w.writerows(edges)
print(len(sel),len(nodes),len(edges))
