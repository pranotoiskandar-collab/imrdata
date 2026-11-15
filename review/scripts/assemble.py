import csv,json,re,collections,html
csv.field_size_limit(10**9)
D='/tmp/claude-0/-home-claude/02493dcd-1fa5-5a7a-8837-b8f092c62a5d/scratchpad/t/'
O=D+'out/'
meta=json.load(open(D+'meta.json'));cx=json.load(open(D+'cx.json'));sel=json.load(open(D+'sel.json'))
hosts=json.load(open(D+'hosts.json'));wf=json.load(open(D+'wf.json'));tg=json.load(open(D+'targets.json'))
UPN=['Cambridge Law Journal','Oxford Journal of Legal Studies','American Journal of International Law','European Journal of International Law','International Journal of Constitutional Law','German Law Journal','Asian Journal of Comparative Law','Asian Journal of Law and Society','Journal of Law and Religion','Journal of African Law']
PTKIN={1,2,3,4,5,6,7,8,9,10,16,17,20,38,43,44,45,47,51,58,59,65,68,71,74,76,82}
def fixmoj(s):
    if s and ('â€' in s or 'Ã' in s):
        try: return s.encode('cp1252').decode('utf8')
        except Exception:
            try: return s.encode('latin1').decode('utf8')
            except Exception: return s
    return s
def clean(a):
    a=re.sub(r'<jats:title>\s*(Abstract|ABSTRACT|Abstrak)\s*</jats:title>',' ',a or '')
    a=html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',html.unescape(a))).strip())
    a=re.sub(r'^(Abstract|ABSTRACT)[\s:.\-–]+','',a)
    return fixmoj(a)
EN=set('the of and to in is this that with for are as by be on study research'.split())
ID=set('yang dan ini dengan untuk dalam adalah dari pada tidak penelitian hukum'.split())
def lang(a):
    w=re.findall(r'[a-z]+',(a or '').lower())
    if len(w)<=20: return 'unknown' if not w else ('en' if sum(x in EN for x in w)/len(w)>0.12 else 'unknown')
    if sum(x in EN for x in w)/len(w)>0.12: return 'en'
    if sum(x in ID for x in w)/len(w)>0.08: return 'id'
    return 'other'
# browser results
R={};BJ={}
for h in hosts.values():
    R.update(h['r']);BJ.update(h['J'])
rows=[];cov={}
for m in meta:
    k='I%d'%m['i'];res=cx['res'].get(k,[]);mk=sel['masks'].get(k,[])
    grp='PTKIN' if m['i'] in PTKIN else 'Other'
    st={'name':m['name'],'grp':grp,'crossref':len(res),'sel':len(mk),'en':0,'kw':0,'browser':k in BJ}
    for j in mk:
        x=res[j];a=clean(x['a']);route='crossref';la=lang(a)
        b=R.get('%s_%d'%(k,j),{})
        if la!='en':
            for l,t in b.get('ds',[]) or []:
                t=clean(t)
                if lang(t)=='en': a=t;la='en';route='oai';break
            if la!='en' and b.get('ds2'):
                for t in (b['ds2'] if isinstance(b['ds2'],list) else [b['ds2']]):
                    t=clean(t if isinstance(t,str) else t[-1])
                    if lang(t)=='en': a=t;la='en';route='page';break
        kw=fixmoj(b.get('kw','') or '')
        if kw: route+='+oai_keywords' if b.get('o') else '+page_keywords'
        if not a: route='none'; la=''
        st['en']+=la=='en'; st['kw']+=bool(kw)
        rows.append(dict(journal=m['name'],year=x['y'],doi=x['d'],title=fixmoj(re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',x['t'] or ''))).strip()),abstract=a,keywords=kw,language=la,source_route=route,group=grp))
    cov[k]=st
upr=[]
for i,n in enumerate(UPN):
    k='U%d'%i
    for x in cx['res'][k][:20]:
        a=clean(x['a']);upr.append(dict(journal=n,year=x['y'],doi=x['d'],title=html.unescape(re.sub(r'<[^>]+>','',x['t'] or '')).strip(),abstract=a,keywords='',language=lang(a),source_route='crossref'))
# headings
CHROME=re.compile(r'^(abstract|abstrak|intisari|bahasa abstract|references|recommended citation|authors?|doi|keywords|main article content|article details|how to cite|section|author biographies|footnotes|review products|information|access options|article purchase|temporarily unavailable|cited by|bibliography|daftar pustaka)$',re.I)
ALIAS={'https://e-journal.iain-palangkaraya.ac.id/index.php/maslahah/article/download/7373/pdf':'https://jurnal.uin-palangkaraya.ac.id/index.php/maslahah/article/download/7373/pdf','https://e-journal.iain-palangkaraya.ac.id/index.php/maslahah/article/download/8958/pdf':'https://jurnal.uin-palangkaraya.ac.id/index.php/maslahah/article/download/8958/pdf'}
def parsewf(t):
    if t is None: return None,[],'','not attempted'
    if t.startswith('Not fetched'):
        r=re.search(r'\((\w+)\)',t);return None,[],'','WebFetch '+(r.group(1) if r else 'error')
    if 'SERVER_ERROR' in t: return None,[],'','WebFetch target server error'
    if 'REDIRECT' in t: return None,[],'','redirect'
    H=[re.sub(r'^H:\s*','',l).strip() for l in t.split('\n') if l.startswith('H:')]
    M=' '.join(re.sub(r'^M:\s*','',l).strip() for l in t.split('\n') if l.startswith('M:'))
    M=M.strip().strip('"').replace('" "',' ').replace('," "',' ')
    if re.search(r"^(none|not stated|no method|the article does not|none found)",M,re.I) or M.lower().startswith('the page'): M=''
    w=M.split()
    if len(w)>40: M=' '.join(w[:40])
    H=[h for h in H if h and not re.search(r'no section|none found',h,re.I)]
    body=[h for h in H if not CHROME.match(h.strip(' .:'))]
    note='truncated: page text over 100000 chars, later headings may be missing' if 'WebFetch note' in t else ''
    if not H: return None,[],M,'no headings extracted from fetched text'
    if any(h.lower() in ('paper type','purpose','introduction to the problem') for h in body): return None,[],M,'landing page only (structured abstract), no full-text body'
    if len(body)<2: return None,[],M,'landing page only (abstract/metadata), no full-text body'
    return H,body,M,note
hrow={'id':[],'up':[]};hcov=collections.defaultdict(lambda:[0,0,[]])
for k,idx,doi,url in tg:
    t=wf.get(ALIAS.get(url,url))
    if url.startswith('http://localhost'): t=None; why='resource URL registered at Crossref is localhost (unreachable)'
    H,body,M,note=parsewf(t)
    if t is None and url.startswith('http://localhost'): note='Crossref resource URL is localhost; not reachable'
    if t is None and not url.startswith('http://localhost') and note=='not attempted': note='not attempted: same host failed (error, robots block or landing page only) on its other target URL'
    grp='up' if k.startswith('U') else 'id'
    name=UPN[int(k[1:])] if grp=='up' else meta[int(k[1:])]['name']
    hcov[k][1]+=1
    if H: hcov[k][0]+=1
    else: hcov[k][2].append(note)
    hrow[grp].append(dict(journal=name,doi=doi,headings=' | '.join(H) if H else '',method_sentence=M,source='webfetch:'+url.split('/')[2],note=note if H else 'FAILED: '+note))
# browser headings
for k,J in BJ.items():
    res=cx['res'][k]
    for idx,url in J.get('h',[]):
        b=R.get('H%s_%d'%(k,idx))
        doi=next((x['d'] for x in res if x.get('u')==url),'')
        hcov[k][1]+=1
        if b and b.get('h'):
            hcov[k][0]+=1
            ms=b.get('ms','') or ''
            if not re.search(r'method|approach|metode|pendekatan',ms,re.I): ms=''
            ms=' '.join(ms.split()[:40])
            hrow['id'].append(dict(journal=meta[int(k[1:])]['name'],doi=doi,headings=' | '.join(fixmoj(h) for h in b['h']),method_sentence=ms,source='browser:'+(b.get('src') or ''),note='heuristic extraction from PDF/HTML text layer; may include numbered list items'))
        else:
            hcov[k][2].append('browser: '+str((b or {}).get('e','no result')))
            hrow['id'].append(dict(journal=meta[int(k[1:])]['name'],doi=doi,headings='',method_sentence='',source='browser',note='FAILED: '+str((b or {}).get('e','no result'))))
json.dump({'rows':rows,'upr':upr,'cov':cov,'hrow':hrow,'hcov':hcov},open(D+'assembled.json','w'),ensure_ascii=False)
def w(fn,L,cols):
    with open(O+fn,'w',newline='',encoding='utf-8') as f:
        wr=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');wr.writeheader();[wr.writerow(r) for r in L]
AC=['journal','year','doi','title','abstract','keywords','language','source_route']
HC=['journal','doi','headings','method_sentence','source','note']
w('abstracts_id.csv',rows,AC);w('abstracts_up.csv',upr,AC);w('headings_id.csv',hrow['id'],HC);w('headings_up.csv',hrow['up'],HC)
print(len(rows),len(upr),len(hrow['id']),len(hrow['up']))
print(collections.Counter(r['language'] for r in rows),collections.Counter(r['language'] for r in upr))
print(collections.Counter(r['source_route'] for r in rows))
print('heads ok id',sum(1 for r in hrow['id'] if r['headings']),'up',sum(1 for r in hrow['up'] if r['headings']))
