import json,re,collections,statistics as S
D='/tmp/claude-0/-home-claude/02493dcd-1fa5-5a7a-8837-b8f092c62a5d/scratchpad/t/'
A=json.load(open(D+'assembled.json'))
AIM=re.compile(r"\b(this|the present|the|our|current) (study|research|article|paper|work|writing)( \w+)? (aims?|aimed|intends|seeks|attempts|tries)\b|\b(the )?(main |primary )?(purpose|aim|objective|goal)s? of (this|the) (study|research|article|paper|writing)\b",re.I)
MET=re.compile(r"\b(method(s|ology)?|approach(es)?|research design|normative|juridical|doctrinal|socio-legal|empirical|qualitative|quantitative|library research|literature (review|study))\b",re.I)
RES=re.compile(r"\b(the )?(results?|findings?)( of (this|the) (study|research|article))? (show|shows|showed|indicate[sd]?|reveal(s|ed)?|demonstrate[sd]?|suggest(s|ed)?|state[sd]?|prove[sd]?|conclude[sd]?)\b|\b(this|the) (study|research|article|paper) (concludes|concluded|finds|found|shows|showed|reveals|revealed|demonstrates)\b|\b(it|we) (is|can be)? ?conclude[sd]?\b|\bin conclusion\b",re.I)
NJD=re.compile(r"\bnormative\b|\bjuridical\b|\bdoctrinal\b",re.I)
STAT=re.compile(r"\bstatut(e|ory) approach",re.I);CONC=re.compile(r"\bconceptual approach",re.I)
AIMS=re.compile(r'\b(this study aims?|this research aims?|the purpose of this study)\b',re.I)
RESS=re.compile(r'\b(the results? (of this study )?shows?|the findings? (of this study )?shows?|this study concludes?)\b',re.I)
METS=re.compile(r'\b(method|methods|methodology)\b',re.I)
def code(a):
    sa=AIMS.search(a);sm=METS.search(a,sa.end()) if sa else None;sr=RESS.search(a,sm.end()) if sm else None
    ma=AIM.search(a);p=ma.end() if ma else None
    mm=MET.search(a,p) if p is not None else None
    mr=RES.search(a,mm.end()) if mm else None
    return dict(aimS=bool(sa),metS=bool(METS.search(a)),resS=bool(RESS.search(a)),seqS=bool(sr),aim=bool(ma),met=bool(MET.search(a)),res=bool(RES.search(a)),seq=bool(mr),njd=bool(NJD.search(a)),stat=bool(STAT.search(a)),conc=bool(CONC.search(a)),either=bool(STAT.search(a) or CONC.search(a)),wc=len(a.split()),g4=' '.join(re.findall(r"[a-z0-9'’-]+",a.lower())[:4]))
def summ(L):
    C=[code(r['abstract']) for r in L];n=len(C)
    if not n: return {'n':0}
    pct=lambda k:round(100*sum(c[k] for c in C)/n,1)
    return dict(n=n,STRICT_aim=pct('aimS'),STRICT_method_word=pct('metS'),STRICT_results=pct('resS'),STRICT_all3_in_order=pct('seqS'),aim=pct('aim'),method_any=pct('met'),results=pct('res'),aim_method_results_in_order=pct('seq'),normative_juridical_doctrinal=pct('njd'),statute_approach=pct('stat'),conceptual_approach=pct('conc'),statute_or_conceptual=pct('either'),mean_words=round(S.mean(c['wc'] for c in C),1),median_words=S.median(c['wc'] for c in C),top_4grams=collections.Counter(c['g4'] for c in C).most_common(10))
idE=[r for r in A['rows'] if r['language']=='en' and r['abstract']]
upE=[r for r in A['upr'] if r['language']=='en' and r['abstract']]
out={'ID_all':summ(idE),'ID_PTKIN':summ([r for r in idE if r['group']=='PTKIN']),'ID_Other':summ([r for r in idE if r['group']=='Other']),'UP':summ(upE)}
# journal-level spread for ID: share per journal of seq & njd
pj=collections.defaultdict(list)
for r in idE: pj[r['journal']].append(r)
js=[summ(v) for v in pj.values() if len(v)>=10]
out['ID_journal_level']=dict(journals=len(js),median_seq=S.median(j['aim_method_results_in_order'] for j in js),median_njd=S.median(j['normative_juridical_doctrinal'] for j in js),journals_seq_ge50=sum(j['aim_method_results_in_order']>=50 for j in js),journals_njd_ge50=sum(j['normative_juridical_doctrinal']>=50 for j in js))
# headings IMRAD
I=re.compile(r"^\W*([0-9IVX]+\.?|[A-Z]\.)?\s*(introduction|pendahuluan)\b",re.I)
M=re.compile(r"^\W*([0-9IVX]+\.?\d*\.?|[A-Z]\.)?\s*(research )?(method(s|ology)?|metode( penelitian)?|research methods?)\b",re.I)
RD=re.compile(r"^\W*([0-9IVX]+\.?|[A-Z]\.)?\s*(results?( (and|&) (discussion|analysis))?|findings( and (discussion|analysis))?|discussion|analysis and discussion|hasil( dan pembahasan| penelitian dan (analisis|pembahasan))?|pembahasan)\b",re.I)
C=re.compile(r"^\W*([0-9IVX]+\.?|[A-Z]\.)?\s*(conclusions?|concluding remarks|kesimpulan|simpulan|penutup|closing)\b",re.I)
def hcode(h):
    H=[x.strip() for x in h.split('|')]
    f=lambda R:any(R.match(x.replace(' ','') if False else x) for x in H)
    return dict(i=f(I),m=f(M),rd=f(RD),c=f(C))
def hsum(L,srcfilter=None):
    L=[r for r in L if r['headings'] and (srcfilter is None or r['source'].startswith(srcfilter))]
    if not L: return {'n':0}
    X=[hcode(r['headings']) for r in L];n=len(X);p=lambda f:round(100*sum(1 for x in X if f(x))/n,1)
    return dict(n=n,introduction=p(lambda x:x['i']),method_heading=p(lambda x:x['m']),results_discussion_heading=p(lambda x:x['rd']),conclusion=p(lambda x:x['c']),full_IMRAD_all4=p(lambda x:all(x.values())),I_RD_C_without_method=p(lambda x:x['i'] and x['rd'] and x['c'] and not x['m']))
PT=set(r['journal'] for r in A['rows'] if r['group']=='PTKIN')
out['H_ID_all']=hsum(A['hrow']['id']);out['H_ID_webfetch']=hsum(A['hrow']['id'],'webfetch');out['H_ID_browser']=hsum(A['hrow']['id'],'browser')
out['H_ID_PTKIN']=hsum([r for r in A['hrow']['id'] if r['journal'] in PT]);out['H_ID_Other']=hsum([r for r in A['hrow']['id'] if r['journal'] not in PT])
out['H_UP']=hsum(A['hrow']['up'])
# method sentence in headings files
for g in ['id','up']:
    L=[r for r in A['hrow'][g] if r['headings']]
    out['H_%s_method_sentence_present'%g]=sum(1 for r in L if r['method_sentence']);out['H_%s_method_sentence_njd'%g]=sum(1 for r in L if NJD.search(r['method_sentence']) or re.search('normatif|yuridis',r['method_sentence'],re.I))
json.dump(out,open(D+'measures.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(out,ensure_ascii=False,indent=1))
