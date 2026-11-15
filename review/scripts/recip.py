import csv,glob,collections,re,os,math
D='/mnt/project-files/jle-article/'
M={'aelr':'Administrative and Environmental Law Review','ahkam':'Ahkam: Jurnal Ilmu Syariah','aladalah':"Al-'Adalah",'alahkam':'Al-Ahkam','alahkamska':"Al-Ahkam: Jurnal Ilmu Syari'ah dan Hukum",'alahwal':'Al-Ahwal','aldustur':'Jurnal Al-dustur','alihkam':'Al-Ihkam: Jurnal Hukum dan Pranata Sosial','alistinbath':'Al-Istinbath: Jurnal Hukum Islam','almanahij':'Al-Manahij: Jurnal Kajian Hukum Islam','almazaahib':'Al-Mazaahib','alrisalah':'Al-Risalah: Forum Kajian Hukum dan Sosial Kemasyarakatan','alsyirah':"Jurnal Ilmiah Al-Syir'ah",'bestuur':'Bestuur','bonumcommune':'Jurnal Hukum Bisnis Bonum Commune','brawijaya':'Brawijaya Law Journal','ciils':'Contemporary Issues on Interfaith Law and Society','consrev':'Constitutional Review','dejure':"De Jure: Jurnal Hukum dan Syar'iah",'dilrev':'Diponegoro Law Review','elmashlahah':'El-Mashlahah','elusrah':'El-Usrah','halrev':'Hasanuddin Law Review','hrgs':'Human Rights in the Global South','ijals':'Indonesian Journal of Advocacy and Legal Services','ijcls':'Indonesian Journal of Criminal Law Studies','ijel':'Indonesian Journal of Environmental Law and Sustainable Development','ijil':'Indonesian Journal of International Law','ijsls':'Indonesian Journal of Socio-Legal Studies','ijtihad':'Ijtihad: Jurnal Wacana Hukum Islam dan Kemanusiaan','ildisea':'International Law Discourse in Southeast Asia','ilr':'Indonesia Law Review','iplr':'Indonesia Private Law Review','islrev':'Indonesian State Law Review','ius':'Jurnal IUS Kajian Hukum dan Keadilan','jambe':'Jambe Law Journal','jambura':'Jambura Law Review','jcbli':'Journal of Central Banking Law and Institutions','jessd':'Journal of Environmental Science and Sustainable Development','jhcls':'Journal of Human Rights, Culture and Legal System','jhi':'Jurnal Hukum Islam','jil':'Journal of Islamic Law','jils':'Journal of Indonesian Legal Studies','jisel':'Journal of Islamic Economic Laws','jlej':'Journal of Law, Environmental and Justice','jllr':'Journal of Law and Legal Reform','jphi':'Jurnal Pengabdian Hukum Indonesia','jsderi':'Journal of Sustainable Development and Regulatory Issues','jseahr':'Journal of Southeast Asian Human Rights','jurisdictie':'Jurisdictie: Jurnal Hukum dan Syariah','justicia':'Justicia Islamica','khazanah':'Khazanah Hukum','konstitusi':'Jurnal Konstitusi','lajil':'Lampung Journal of International Law','lawreform':'Law Reform: Jurnal Pembaharuan Hukum','legality':'Legality: Jurnal Ilmiah Hukum','lentera':'Lentera Hukum','lexscientia':'Lex Scientia Law Review','litigasi':'Jurnal Litigasi','mazahib':'Mazahib Jurnal Pemikiran Hukum Islam','mediahukum':'Jurnal Media Hukum','mediaiuris':'Media Iuris','milrev':'MILRev: Metro Islamic Law Review','mimbar':'Mimbar Hukum','mizani':'Jurnal Ilmiah Mizani','mmh':'Masalah-Masalah Hukum','novelty':'Jurnal Hukum Novelty','nurani':'Nurani','nusantara':'Nusantara: Journal of Law Studies','padjadjaran':'Padjadjaran Jurnal Ilmu Hukum','petita':'Petita: Jurnal Kajian Ilmu Hukum dan Syariah','peuradeun':'Jurnal Ilmiah Peuradeun','prophetic':'Prophetic Law Review','samarah':'Samarah','sriwijaya':'Sriwijaya Law Review','suarahukum':'Jurnal Suara Hukum','substantive':'Substantive Justice International Journal of Law','tirtayasa':'Tirtayasa Journal of International Law','trunojoyo':'Trunojoyo Law Review','udayana':'Udayana Journal of Law and Culture','unissula':'Jurnal Hukum Unissula','volksgeist':'Volksgeist: Jurnal Ilmu Hukum dan Konstitusi','yuridika':'Yuridika','yustisia':'Yustisia','jlej':'Journal of Law, Environmental and Justice','juris':'Juris: Jurnal Ilmiah Syariah'}
norm=lambda t:re.sub(r'[^a-z0-9]','',t.lower())
t2s={norm(v):k for k,v in M.items()}
# alias: titles in exports may differ slightly
def src2slug(t):
    n=norm(t)
    if n in t2s: return t2s[n]
    for k,v in t2s.items():
        if len(k)>8 and (n.startswith(k) or k.startswith(n) and len(n)>8): return v
    return None
latest={}
for f in glob.glob(D+'*_citescore_citing_*_raw.csv'):
    s,y=re.match(r'.*/(\w+?)_citescore_citing_(\d+)_raw',f).groups()
    if s not in latest or int(y)>latest[s][0]: latest[s]=(int(y),f)
F=collections.defaultdict(collections.Counter); tot={}
for a,(y,f) in latest.items():
    rows=[r for r in list(csv.reader(open(f,encoding='utf-8-sig')))[1:] if len(r)>10 and r[3]]
    tot[a]=len(rows)
    for r in rows:
        b=src2slug(r[3])
        if b and b!=a: F[b][a]+=1   # b cites a
S=set(latest)
out=collections.Counter(); inn=collections.Counter()
for b in F:
    for a,c in F[b].items():
        if b in S and a in S: out[b]+=c; inn[a]+=c
T=sum(out.values())
pairs=[]
L=sorted(S)
for i,a in enumerate(L):
    for b in L[i+1:]:
        ab=F[a][b]; ba=F[b][a]   # a->b, b->a
        if ab+ba<10: continue
        ea=out[a]*inn[b]/T; eb=out[b]*inn[a]/T
        pairs.append(dict(a=a,b=b,a_to_b=ab,b_to_a=ba,share_of_b_citations_from_a=round(ab/tot[b],3),share_of_a_citations_from_b=round(ba/tot[a],3),imbalance=round(abs(ab-ba)/(ab+ba),2),oe_a_to_b=round(ab/ea,1) if ea else '',oe_b_to_a=round(ba/eb,1) if eb else ''))
pairs.sort(key=lambda p:-(p['a_to_b']+p['b_to_a']))
w=csv.DictWriter(open(D+'reciprocity_pairs.csv','w'),fieldnames=list(pairs[0]));w.writeheader();w.writerows(pairs)
bal=[dict(journal=s,window=latest[s][0],received_in_network=inn[s],given_in_network=out[s],net=inn[s]-out[s],ratio_received_to_given=round(inn[s]/out[s],2) if out[s] else '') for s in L]
bal.sort(key=lambda d:-d['net'])
w=csv.DictWriter(open(D+'reciprocity_balance.csv','w'),fieldnames=list(bal[0]));w.writeheader();w.writerows(bal)
# summary stats
mutual=sum(min(p['a_to_b'],p['b_to_a']) for p in pairs)*2; flow=sum(p['a_to_b']+p['b_to_a'] for p in pairs)
print('journals',len(L),'in-network flow',T,'pairs>=10',len(pairs),'mutual share',round(mutual/flow,2))
print('TOP PAIRS');[print(p) for p in pairs[:20]]
print('MOST LOPSIDED (>=20 flow)');[print(p) for p in sorted([p for p in pairs if p['a_to_b']+p['b_to_a']>=20],key=lambda p:-p['imbalance'])[:15]]
print('MUTUAL HIGH O/E');[print(p) for p in sorted([p for p in pairs if p['oe_a_to_b'] and p['oe_b_to_a'] and min(p['a_to_b'],p['b_to_a'])>=8],key=lambda p:-min(p['oe_a_to_b'],p['oe_b_to_a']))[:12]]
print('TAKERS');[print(d) for d in bal[:10]];print('GIVERS');[print(d) for d in bal[-10:]]
