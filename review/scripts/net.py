import csv,collections,re,sys
sys.argv=['x']
src=open('recip.py').read().split('S=set(latest)')[0]
exec(src)  # gives M, latest, F (b cites a), tot
# quartiles from journals.csv by name
Q={r['journal']:r['quartile'] for r in csv.DictReader(open('dash/journals.csv'))}
selfc=collections.Counter()
for a,(y,f) in latest.items():
    for r in list(csv.reader(open(f,encoding='utf-8-sig')))[1:]:
        if len(r)>10 and r[3] and src2slug(r[3])==a: selfc[a]+=1
grp=collections.defaultdict(collections.Counter)
G={'Indonesia other':'Other Indonesian venues','Unplaced international':'Unclear base','Global South (non-Indonesian)':'Global South (outside Indonesia)','North publisher: legacy journal or book':'Northern journals and books','North publisher: conference series':'Northern conference series','North publisher: high-volume OA / book':'Northern high-volume OA','Eastern Europe':'Eastern Europe','Other North':'Other North'}
for r in csv.reader(open('gs_rows.csv')):
    if r[2] in G: grp[G[r[2]]][r[0]]+=1
nodes=[];edges=[]
inn=collections.Counter();out=collections.Counter()
S=set(latest)&set(M)
for b in F:
    for a,c in F[b].items():
        if a not in S: continue
        edges.append(dict(source=M.get(b,b),target=M[a],rows=c,kind='journal'))
        if b in S: out[b]+=c; inn[a]+=c
for g,cnt in grp.items():
    for a,c in cnt.items():
        if a in S: edges.append(dict(source=g,target=M[a],rows=c,kind='outside'))
names=set()
for a in sorted(S):
    nodes.append(dict(id=M[a],kind='journal',quartile=Q.get(M[a],''),in_scope='yes',citing_rows=tot[a],self_rows=selfc[a],received=inn[a],given=out[a])); names.add(M[a])
for b in F:
    n=M.get(b,b)
    if n not in names: nodes.append(dict(id=n,kind='journal',quartile=Q.get(n,''),in_scope='no',citing_rows='',self_rows='',received='',given=sum(F[b].values()))); names.add(n)
for g in grp: nodes.append(dict(id=g,kind='outside',quartile='',in_scope='',citing_rows='',self_rows='',received='',given=sum(grp[g].values())))
w=csv.DictWriter(open('dash/net_nodes.csv','w'),fieldnames=list(nodes[0]));w.writeheader();w.writerows(nodes)
w=csv.DictWriter(open('dash/net_edges.csv','w'),fieldnames=list(edges[0]));w.writeheader();w.writerows(edges)
print(len(nodes),len(edges),sum(e['rows'] for e in edges if e['kind']=='journal'),sum(e['rows'] for e in edges if e['kind']=='outside'))
print([n for n in nodes if n['in_scope']=='no'])
print(sum(1 for n in nodes if n['kind']=='journal' and not n['quartile']))
