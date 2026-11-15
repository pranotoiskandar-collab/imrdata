# Board data transcribed from official board pages, 2026-11-15. NO personal names.
# Each person: (cat, roles_as_listed, institution, country, on_other_board, basis)
# cat: E=editor-in-chief (or top tier), M=managing/executive, D=editor (associate/section/book review/etc), B=editorial/advisory board, O=other
NS="not stated"
def p(cat, roles, inst, country, flag=False, basis="as listed"):
    return dict(cat=cat, roles=roles, inst=inst, country=country, flag=flag, basis=basis)

J = {}
UK="United Kingdom"; US="United States"
# ---------------- Cambridge Law Journal
cam="University of Cambridge"
J["Cambridge Law Journal"] = dict(
 publisher="Cambridge University Press", url="https://cambridge.org/core/journals/cambridge-law-journal/information/editorial-board",
 top_tier="Editor-in-chief", members=[
 p("E","Editor-in-chief; Trustee",cam,UK),
 p("D","General Editor",cam,UK),
 p("D","General Editor; Trustee",cam,UK),
 p("D","Senior Case-Note Editor; Note Editor",cam,UK),
 p("D","Book Review Editor",cam,UK),
 p("O","Secretary & Treasurer; Trustee",cam,UK),
 ]+[p("O","Trustee",cam,UK) for _ in range(4)]+[p("D","Note Editor",cam,UK) for _ in range(6)])

# ---------------- Oxford Journal of Legal Studies
ox="University of Oxford"
ojls=[p("E","General Editor",ox,UK),
 p("D","Articles Editor",ox,UK), p("D","Articles Editor","King's College London",UK),
 p("D","Articles Editor",ox,UK,True), p("D","Articles Editor",ox,UK),
 p("D","Review Articles Editor",ox,UK)]
bd=[("University of Melbourne","Australia",False),(ox,UK,False),(ox,UK,False),(ox,UK,False),("University of Bristol",UK,False),
 (NS,NS,False),(ox,UK,False),(ox,UK,False),("University of Toronto","Canada",False),(ox,UK,False),(ox,UK,False),(ox,UK,False),
 ("University of Hong Kong","Hong Kong SAR, China",False),(ox,UK,False),(cam,UK,False),("Newcastle University",UK,False),
 (ox,UK,False),(ox,UK,True),("National University of Singapore","Singapore",False),(ox,UK,False),("National University of Singapore","Singapore",False)]
ojls+=[p("B","Member of the Editorial Board",i,c,f) for i,c,f in bd]
J["Oxford Journal of Legal Studies"]=dict(publisher="Oxford University Press",url="https://academic.oup.com/ojls/pages/Editorial_Board",
 top_tier="General Editor (no editor-in-chief title; General Editor treated as EiC)", members=ojls)

# ---------------- AJIL
aj=[p("E","Editor in Chief","Fordham University",US), p("E","Editor in Chief","Northwestern University",US),
 p("D","Section Editor; Board of Editors","Dalhousie University","Canada"),
 p("D","Section Editor; Board of Editors","Temple University",US),
 p("D","Section Editor; Board of Editors","University of Cincinnati",US),
 p("D","Section Editor; Board of Editors","Western University","Canada")]
boe=[("Stanford University",US,0),("London School of Economics and Political Science (also University of Georgia)",UK,0),("University of Michigan",US,1),
 ("University of California, Davis",US,0),("Yale University",US,0),("Georgetown University",US,0),("Rutgers University",US,0),("Stanford University",US,0),
 ("Washington University in St. Louis",US,0),("University of Pennsylvania",US,0),("Singapore Management University","Singapore",0),("University of Miami",US,0),
 ("Tsinghua University","China",0),("Wake Forest University",US,0),("Duke University",US,0),("Johns Hopkins University (SAIS)",US,1),("Temple University",US,0),
 ("European University Institute (also University of Arizona)","Italy",0),(ox,UK,0),("Temple University",US,0),("International Criminal Court","Netherlands",0),
 ("University of Maryland",US,0),("University of Iowa",US,0)]
aj+=[p("B","Board of Editors",i,c,bool(f)) for i,c,f in boe]
aj+=[p("O","Ex Officio","American Society of International Law",US),p("O","Ex Officio","Yale University",US)]
hon=[("Northwestern University",US),("New York University",US),("National University of Singapore (also University of Utah)","Singapore"),
 ("University of Cambridge (also Tel Aviv University)",UK),("Arizona State University",US),("Geneva Graduate Institute","Switzerland"),("University of Chicago",US),
 ("not stated (location: The Hague)","Netherlands"),("Georgetown University",US),("University of Toronto","Canada"),("University of Melbourne","Australia"),
 ("Jindal Global Law School","India"),("London School of Economics and Political Science",UK),("not stated (location: Potomac, Maryland)",US),("Columbia University",US),
 ("Princeton University",US),("Tufts University",US),("Duke University (also University of Copenhagen)",US),("Yale University",US),("University of the Pacific",US),
 ("University of Ottawa","Canada"),(ox,UK),("University of Virginia",US),("George Washington University",US),("University of Miami",US),("University of Michigan",US),
 ("Georgetown University",US),("George Washington University",US),("University of Pennsylvania",US),("New America",US),("University of California, Los Angeles",US),
 ("Georgetown University",US),("Stanford University",US),("Tufts University",US),("Covington & Burling LLP",US),("Georgetown University",US)]
aj+=[p("O","Honorary Editor",i,c) for i,c in hon]
aj+=[p("M","Managing Editor","Columbia University",US),p("O","Senior Copyeditor","American Society of International Law",US),p("O","Cite-checker",NS,NS)]
J["American Journal of International Law"]=dict(publisher="Cambridge University Press (for the American Society of International Law)",
 url="https://cambridge.org/core/journals/american-journal-of-international-law/information/editorial-board",top_tier="Editors in Chief",members=aj)

# ---------------- EJIL (journal site ejil.org, current 2026-27 listing; institutions from OUP board page where the same person is listed)
ej=[p("E","Editor-in-Chief; Management Board",cam+" (OUP page also lists European University Institute)",UK),
    p("E","Editor-in-Chief","University of Vienna","Austria")]
ex=[("University of Michigan",US,1),("University of Edinburgh",UK,0),("Australian National University","Australia",0),("University College London",UK,0),
 ("Victoria University of Wellington/Auckland (as listed: 'Victoria University of Auckland')","New Zealand",0),("London School of Economics and Political Science",UK,0),
 (ox,UK,1),("Universite libre de Bruxelles","Belgium",0),("Tel Aviv University","Israel",0),("University of Manchester",UK,0)]
ej+=[p("D","Executive Board (blog/podcast/book review editor)",i,c,bool(f)) for i,c,f in ex]
ej[-3]["roles"]="Executive Board (Book Review editor); Book Review Editor"; ej[-2]["roles"]="Executive Board (Book Review editor); Book Review Editor"
adv=[("European University Institute","Italy","as listed"),(cam,UK,"as listed"),("Harvard University",US,"as listed"),
 ("not stated (location: Tokyo)","Japan","inferred from city"),("not stated (location: Maastricht)","Netherlands","inferred from city"),
 ("not stated (location: Geneva)","Switzerland","inferred from city"),("not stated (location: Haifa)","Israel","inferred from city"),
 ("University of Tartu","Estonia","as listed"),("University of Haifa","Israel","as listed"),("University of Silesia in Katowice","Poland","as listed"),
 ("Universite Paris Cite","France","as listed"),("University of Edinburgh",UK,"as listed"),("not stated (location: Geneva)","Switzerland","inferred from city"),
 ("not stated (location: Bangkok)","Thailand","inferred from city"),("Norwegian Institute of International Affairs","Norway","as listed"),
 ("not stated (location: Durham)",UK,"inferred from city"),("not stated (location: London)",UK,"inferred from city"),
 ("International Court of Justice","Netherlands","inferred (seat of institution)")]
ej+=[p("B","Advisory Board",i,c,False,b) for i,c,b in adv]
ej+=[p("D","Associate Editor","not stated (location: Geneva)","Switzerland",False,"inferred from city"),
     p("D","Associate Editor","not stated (location: Helsinki)","Finland",False,"inferred from city"),
     p("D","Associate Editor","not stated (location: Vienna)","Austria",False,"inferred from city"),
     p("M","Managing Editor","not stated (location: Oxford)",UK,False,"inferred from city")]
ej+=[p("O","Assistant Editor 2026-2027",NS,NS) for _ in range(8)]
ej+=[p("O","Founders Board; EJIL Founder","SAIS Europe (Johns Hopkins), Bologna","Italy"),
     p("O","Founders Board; EJIL Founder","Graduate Institute of International and Development Studies","Switzerland"),
     p("O","Founders Board; EJIL Founder","not stated (location: The Hague)","Netherlands",False,"inferred from city"),
     p("O","Management Board; EJIL Founder","New York University",US),
     p("O","Management Board; EJIL Founder","New York University",US,True)]
J["European Journal of International Law"]=dict(publisher="Oxford University Press",
 url="https://www.ejil.org/about/management.php (current list; institutions cross-checked with https://academic.oup.com/ejil/pages/Editorial_Board)",
 top_tier="Editors-in-Chief",members=ej)

# ---------------- I-CON
nyu="New York University"
ic=[p("O","Founder",nyu,US),p("O","Emeritus Editor-in-Chief","Yeshiva University (Cardozo Law School)",US),
    p("E","Co-Editor-in-Chief; Editorial Director",nyu,US,True),p("E","Co-Editor-in-Chief",nyu,US),
    p("M","Managing Editor","not stated (location: Florence)","Italy",False,"inferred from city"),
    p("D","Senior Associate Editor",nyu,US),
    p("D","Associate Editor","European University Institute","Italy"),p("D","Associate Editor","Trinity College Dublin","Ireland"),
    p("D","Associate Editor; Book Review Editor","Academia Sinica","Taiwan"),p("D","Associate Editor","Bocconi University","Italy"),
    p("D","Spanish Issue Editor-in-Chief","University of Southern California",US),p("D","Spanish Issue Editor-in-Chief","IE University","Spain")]
ab=[("International IDEA","Netherlands",0),("Instituto Tecnologico Autonomo de Mexico","Mexico",0),("Universidad Autonoma de Madrid","Spain",0),
 ("University of Texas at Austin",US,0),("Universidad de los Andes","Colombia",0),("Bocconi University","Italy",0),("IMT School for Advanced Studies Lucca","Italy",0),
 ("LUISS University","Italy",0),("University of Hong Kong","Hong Kong SAR, China",1),("National Taiwan University","Taiwan",1),("Universidad Externado de Colombia","Colombia",0),
 ("University of Pretoria","South Africa",0),("Universidad del Desarrollo","Chile",0),("University of New South Wales","Australia",0),("Loyola University Chicago",US,1),
 ("University of Chicago",US,1),("University of St. Gallen","Switzerland",0),("Supreme Court of India (Senior Advocate)","India",0),("Yonsei University","South Korea",0),
 ("University of Giessen","Germany",0),("University of Toronto","Canada",0),("Universitat de Barcelona","Spain",0),(ox+" (also University of Melbourne)",UK,0),
 ("Trinity College Dublin","Ireland",0),("Florida State University",US,0),("Queen's University Belfast (also University of Michigan)",UK,0),
 ("National University of Singapore","Singapore",1),("University of Sydney (also University of Warsaw)","Australia",0),("University of Wroclaw","Poland",0),
 ("College of Law and Business","Israel",0)]
ic+=[p("B","Advisory Board",i,c,bool(f)) for i,c,f in ab]
ic+=[p("O","Assistant Editor 2025-2026",NS,NS) for _ in range(18)]
em=[("Court of Justice of the European Union","Luxembourg",0),("WZB Berlin Social Science Center / Center for Constitutional Transitions","Germany",0),
 ("University of Warsaw","Poland",0),("Harvard University",US,0),("WZB Berlin Social Science Center (also New York University)","Germany",0),
 ("Seton Hall University",US,0),("University of Melbourne","Australia",1),("Harvard University",US,0)]
ic+=[p("O","Emeritus Editor",i,c,bool(f)) for i,c,f in em]
J["International Journal of Constitutional Law (I-CON)"]=dict(publisher="Oxford University Press",url="https://academic.oup.com/icon/pages/Editorial_Board",
 top_tier="Co-Editors-in-Chief",members=ic)

# ---------------- German Law Journal
gl=[p("E","Editor in Chief","University of Amsterdam","Netherlands"),p("E","Editor in Chief","Chinese University of Hong Kong","Hong Kong SAR, China"),
    p("E","Editor in Chief","Washington and Lee University",US),p("E","Editor in Chief","University of Bristol",UK),
    p("E","Editor in Chief","University of Lausanne (also Max Planck Institute, Freiburg)","Switzerland"),
    p("E","Editor in Chief","EBS Law School Wiesbaden (also Peking University STL; MPI Bonn)","Germany")]
DE="Germany"
ed=[("Graduate School of Government and European Studies, Maribor","Slovenia"),("Virtual University of Senegal (also MPI Munich)","Senegal"),("University of Milan","Italy"),
 ("College of Management Academic Studies","Israel"),("Texas A&M University",US),("Austral University of Chile","Chile"),("McGill University","Canada"),
 ("Queen's University Belfast",UK),("University of Twente","Netherlands"),("University of Amsterdam","Netherlands"),("University of California, Los Angeles",US),
 ("University of Tubingen",DE),("University College London",UK),("Goethe University Frankfurt (also MPI Heidelberg)",DE),("Northeastern University",US),
 ("University of Gottingen",DE),("Max Planck Institute for the Study of Crime, Security and Law",DE),("Masaryk University","Czechia"),("Seoul National University","South Korea"),
 ("Ruhr University Bochum",DE),("Flensburg University",DE),("University of Munster",DE),("York University","Canada"),("Pennsylvania State University",US),
 ("University of Montreal","Canada"),("University of Luxembourg","Luxembourg"),("Goethe University Frankfurt",DE),("University of Sussex",UK),("University of Munster",DE),
 ("University of Pisa","Italy"),("University of Bristol",UK),("University of Augsburg",DE),("Johannes Gutenberg University Mainz",DE),("University of Cape Town","South Africa"),
 ("KU Leuven","Belgium"),("University of Helsinki","Finland"),("London School of Economics and Political Science",UK)]
gl+=[p("D","Editor",i,c) for i,c in ed]
ad=[("Humboldt University of Berlin",DE,0),("Vermont Law School",US,0),("Justus Liebig University Giessen",DE,0),("University of Bristol",UK,0),("University of Bremen",DE,0),
 ("University of Munster",DE,0),("McGill University","Canada",0),("University of Gottingen",DE,0),("Pontifical Catholic University of Rio de Janeiro","Brazil",0),
 ("Leipzig University",DE,0),("Max Planck Institute for Comparative Public Law and International Law",DE,0),("Copenhagen Business School","Denmark",0),(NS,NS,0),
 ("Max Planck Institute (as listed: Comparative Public Law and International Law, Hamburg)",DE,1),("American University",US,0),("Berlin Administrative Court",DE,0),
 ("Friedrich-Alexander University Erlangen-Nurnberg",DE,0),("University of Gottingen",DE,0)]
gl+=[p("B","Advisory Board",i,c,bool(f)) for i,c,f in ad]
stu=[("Lead Executive Editor; Junior Editor",1),("Managing Editor (student)",1),("Executive Editor (student)",2),("Senior Articles Editor (student)",6),
     ("Lead Articles Editor (student)",12),("Junior Editor (student)",21)]
for r,n in stu:
    gl+=[p("O","Student Editor Roster 2024-2025: "+r,NS,NS) for _ in range(n)]
J["German Law Journal"]=dict(publisher="Cambridge University Press",url="https://cambridge.org/core/journals/german-law-journal/information/editorial-board",
 top_tier="Editors in Chief (6)",members=gl)

# ---------------- Asian Journal of Comparative Law
nus="National University of Singapore"; SG="Singapore"; HK="Hong Kong SAR, China"
ac=[p("E","Editor-in-Chief",nus,SG),p("E","Editor-in-Chief",nus,SG),p("D","Book Review Editor","Chinese University of Hong Kong",HK),p("M","Managing Editor",nus,SG)]
eds=[("Western Sydney University","Australia",0),("Queen Mary University of London",UK,0),(ox,UK,0),("University of Sydney","Australia",0),("University of Hong Kong",HK,1),
 ("National Law School of India University, Bangalore","India",0),("National Taiwan University","Taiwan",1),("National Taiwan University","Taiwan",0),(nus,SG,0),
 ("Singapore Management University",SG,0),("University of New South Wales","Australia",1),("Qatar University","Qatar",0),("American University (as listed: 'American University of Washington')",US,1),
 ("International Centre for Ethnic Studies","Sri Lanka",0),("University of Tokyo","Japan",0),("Peking University","China",0),("University of Tokyo","Japan",0),
 ("University of Melbourne","Australia",0),("Chinese University of Hong Kong",HK,0),("Nagoya University","Japan",0),("University of Melbourne","Australia",0),
 ("Yonsei University","South Korea",0),("Seoul National University","South Korea",0),(nus,SG,0),(nus,SG,0),(nus,SG,1),("Thammasat University","Thailand",0),
 ("Chulalongkorn University","Thailand",0),("Singapore Management University",SG,0),(nus,SG,0),("National Law School of India University, Bangalore","India",0),(nus,SG,0),
 ("City University of Hong Kong",HK,0)]
ac+=[p("D","Editor",i,c,bool(f)) for i,c,f in eds]
iab=[("London School of Economics and Political Science",UK,0),("University of Hong Kong",HK,1),("University of Pennsylvania",US,0),(nus,SG,1),("Waseda University","Japan",0),
 ("University of Michigan",US,0),("Monash University","Australia",0),("City University of Hong Kong",HK,0),("Max Planck Institute for Comparative and International Private Law","Germany",1),
 ("Stanford University",US,0),("Supreme Court of Singapore",SG,0),("University of the Philippines","Philippines",0),("Federal Court of Malaysia","Malaysia",0),
 ("Singapore International Commercial Court",SG,0),("University of Melbourne","Australia",1),("National Taiwan University","Taiwan",0)]
ac+=[p("B","International Advisory Board",i,c,bool(f)) for i,c,f in iab]
J["Asian Journal of Comparative Law"]=dict(publisher="Cambridge University Press (for the Asian Law Institute)",
 url="https://cambridge.org/core/journals/asian-journal-of-comparative-law/information/editorial-board",top_tier="Editors-in-Chief",members=ac)

# ---------------- Asian Journal of Law and Society
sj="Shanghai Jiao Tong University"; CN="China"
al=[p("E","Editor-in-Chief","Leiden University","Netherlands"),p("E","Editor-in-Chief","State University of New York",US),
    p("E","Editor-in-Chief","University of Chicago",US,True),p("E","Editor-in-Chief",sj,CN),p("E","Editor-in-Chief","Kobe University","Japan")]
eb=[("University of California, Davis",US,0),("University of California, Irvine",US,0),("University of Melbourne","Australia",0),("National Yang Ming Chiao Tung University","Taiwan",0),
 ("National Taiwan University","Taiwan",1),("University of Hong Kong",HK,1),(sj,CN,0),("University of New South Wales","Australia",1),("Yale University",US,0),(ox,UK,1),
 ("University of Pennsylvania",US,0),("University of California, Santa Cruz",US,0),("Monash University","Australia",0),(nus,SG,1),("University of Tokyo","Japan",0),
 ("Leiden University","Netherlands",0),("Indiana University",US,0),("Yonsei University","South Korea",0),("University of Calgary","Canada",0),("University of Hong Kong",HK,0),
 ("University of British Columbia","Canada",0),("Kobe University","Japan",0),("Meiji University","Japan",0),(ox,UK,1),("Emory University",US,0),
 ("Queen Mary University of London",UK,1),("University of Wisconsin-Madison",US,0),("University of California, Berkeley",US,0),("Chulalongkorn University","Thailand",0),
 ("University of California, Irvine",US,0),("Australian National University","Australia",0),("Universitas Indonesia","Indonesia",0),("Peking University",CN,0),
 ("Fudan University",CN,0),("Tsinghua University",CN,0),("University of Macau","Macao SAR, China",0),("Yale University",US,0)]
al+=[p("B","Editorial Board",i,c,bool(f)) for i,c,f in eb]
al[5+11]["roles"]="Editorial Board; Book Review Editor"
al+=[p("D","Book Review Editor","University of Sydney","Australia"),p("D","Book Review Editor","City University of Hong Kong",HK),p("D","Book Review Editor","Duke University",US)]
al+=[p("M","Associate Managing Editor; Social Media Team",sj,CN),p("O","Social Media Team; Assistant Editor","King's College London",UK),
     p("M","Managing Editor","Hasselt University","Belgium"),p("M","Associate Managing Editor",sj,CN)]
al+=[p("O","Assistant Editor",sj,CN) for _ in range(6)]+[p("O","Assistant Editor","University of Hong Kong",HK)]
J["Asian Journal of Law and Society"]=dict(publisher="Cambridge University Press (in association with KoGuan School of Law, Shanghai Jiao Tong University)",
 url="https://www.cambridge.org/core/journals/asian-journal-of-law-and-society/information/about-this-journal/editorial-board",top_tier="Editors-in-Chief (5)",members=al)

# ---------------- Journal of Law and Religion
em_="Emory University"
jl=[p("M","Co-Editor; Executive Editor",em_,US)]
co=[(em_,US,0),("Sapir Academic College","Israel",0),("University of Texas at Austin",US,0),(em_+" (also University of Navarra)",US,0),("University of Johannesburg","South Africa",0),
 (em_,US,0),("Boston College",US,0),("Netherlands Institute for Advanced Study","Netherlands",0),("Boston University",US,0),("St. John's University",US,0),(nus,SG,1),
 ("University of Edinburgh",UK,0),("Duke University",US,0),(em_,US,0)]
jl+=[p("D","Co-Editor",i,c,bool(f)) for i,c,f in co]
jl[6]["roles"]="Co-Editor; Symposium and Book Review Editor"
jl+=[p("M","Managing Editor",em_,US),p("O","Senior Editorial Assistant",em_,US),p("O","Editorial Assistant",em_,US)]
ia=[(em_,US,0),("University of Adelaide","Australia",0),("University of Colorado",US,0),("Yale University",US,0),("Pontificia Universidad Catolica de Chile","Chile",0),
 ("Academia Sinica","Taiwan",0),("Macalester College",US,0),("Rutgers University",US,0),("Cardiff University",UK,0),("Max Planck Institute for Legal History and Legal Theory (as listed: European Legal History)","Germany",0),
 ("University of Toronto","Canada",0),("University of Melbourne","Australia",0),("State University of New York",US,0),("Valparaiso University",US,0),("University of Notre Dame",US,0),
 ("St. Mary's University",US,0),("University of Chicago",US,0),("Moscow State University","Russian Federation",0),("Georgetown University",US,0),("Touro University (Law Center)",US,0),
 ("University of Melbourne","Australia",0),("Georgetown University",US,0),("University of Lucerne","Switzerland",0),("Southern Methodist University",US,0),("Columbia University",US,0),
 ("SOAS University of London",UK,0),("Tennessee Claims Commission",US,0),("University of Notre Dame",US,0),("University of Toronto","Canada",0),("Toyo Eiwa University","Japan",0),
 (ox,UK,1),("University of Notre Dame",US,0),("Boston University",US,0),("University of Wisconsin",US,0),("Bar-Ilan University","Israel",0),("Chulalongkorn University","Thailand",0),
 ("Queen Mary University of London",UK,1),("University of San Diego",US,0),("Yeshiva University",US,0),("European Centre for Minority Issues","Germany",0),
 ("Georgia Christian College",US,0),("Georgetown University",US,0),("Vrije Universiteit Amsterdam","Netherlands",0),("University of Heidelberg","Germany",0),("Purdue University",US,0)]
jl+=[p("B","International Advisory Board",i,c,bool(f)) for i,c,f in ia]
J["Journal of Law and Religion"]=dict(publisher="Cambridge University Press (journal based at Emory University Center for the Study of Law and Religion; host not stated on board page)",
 url="https://cambridge.org/core/journals/journal-of-law-and-religion/information/editorial-board",
 top_tier="Co-Editors (15; no editor-in-chief title)",members=jl)

# ---------------- Journal of African Law
so="SOAS University of London"; ZA="South Africa"
ja=[p("E","Editor","University of Pretoria",ZA),p("E","Editor",so,UK),p("E","Editor",so,UK),p("E","Editor","University of Lagos","Nigeria")]
eb2=[(so,UK,0),(so,UK,0),("La Trobe University","Australia",0),(so,UK,0),("University of the Western Cape",ZA,0),("Loyola University Chicago",US,1),
 ("Bahir Dar University (also University of Bristol)","Ethiopia",0),("University of Bayreuth","Germany",0),("Open Society Initiative for Eastern Africa","Kenya",0),
 ("Monash University","Australia",0),("University of the Western Cape",ZA,0),("University of the Witwatersrand",ZA,0),("University of Bristol",UK,0),("University of Cape Town",ZA,0),
 ("Cornell University",US,0),("University of Derby",UK,0),("University of Saskatchewan","Canada",0),(so,UK,0),("Johns Hopkins University (SAIS)",US,1),("SUNY Buffalo",US,0),
 ("University of Cape Town",ZA,0),("Stellenbosch University",ZA,0)]
ja+=[p("B","Editorial Board",i,c,bool(f)) for i,c,f in eb2]
J["Journal of African Law"]=dict(publisher="Cambridge University Press (journal edited at SOAS)",
 url="https://www.cambridge.org/core/journals/journal-of-african-law/information/about-this-journal/editorial-board",
 top_tier="Editors (4; no editor-in-chief title; treated as top tier)",members=ja)
