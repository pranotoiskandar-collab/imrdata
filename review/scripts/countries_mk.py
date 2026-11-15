import json,sys,csv
S=json.load(open('sc.json'))
names={'PK':'Pakistan','BD':'Bangladesh','LK':'Sri Lanka','NP':'Nepal','NG':'Nigeria','KE':'Kenya','GH':'Ghana','ET':'Ethiopia','EG':'Egypt','MA':'Morocco','TN':'Tunisia','CO':'Colombia','UA':'Ukraine','AU':'Australia','FR':'France','NZ':'New Zealand','BE':'Belgium','SE':'Sweden','DK':'Denmark','GR':'Greece','MY':'Malaysia','IN':'India','CN':'China','SG':'Singapore','BR':'Brazil','TR':'Türkiye','SA':'Saudi Arabia','AE':'United Arab Emirates','JO':'Jordan','IQ':'Iraq','IR':'Iran','QA':'Qatar','KW':'Kuwait','OM':'Oman','DZ':'Algeria','KZ':'Kazakhstan','UZ':'Uzbekistan','AZ':'Azerbaijan','GE':'Georgia','AM':'Armenia','VN':'Vietnam','PH':'Philippines','TH':'Thailand','KR':'South Korea','JP':'Japan','TW':'Taiwan','HK':'Hong Kong','AR':'Argentina','CL':'Chile','PE':'Peru','MX':'Mexico','RU':'Russia','ZA':'South Africa','RO':'Romania','RS':'Serbia','HR':'Croatia','SI':'Slovenia','CZ':'Czech Republic','SK':'Slovakia','HU':'Hungary','BG':'Bulgaria','LT':'Lithuania','LV':'Latvia','EE':'Estonia','PL':'Poland','ES':'Spain','IT':'Italy','DE':'Germany','NL':'Netherlands','CA':'Canada','US':'United States','GB':'United Kingdom','ID':'Indonesia','IE':'Ireland','CH':'Switzerland','AT':'Austria','NO':'Norway','FI':'Finland','PT':'Portugal','IL':'Israel'}
asia=set('PK BD LK NP MY IN CN SG SA AE JO IQ IR QA KW OM KZ UZ AZ GE AM VN PH TH KR JP TW HK TR IL ID'.split())
w=csv.writer(open('countries.csv','w',newline='')); w.writerow(['country','code','journals','q1','q2','q3','q4','asia'])
for k,v in S.items():
    if not isinstance(v,str) or v in('fail','blocked'): print('skip',k,v); continue
    n,q1,q2,q3,q4=map(int,v.split(','))
    w.writerow([names[k],k,n,q1,q2,q3,q4,1 if k in asia else 0])
