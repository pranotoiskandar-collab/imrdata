import json,glob
F='/root/.claude/projects/-home-claude/02493dcd-1fa5-5a7a-8837-b8f092c62a5d/subagents/agent-adc2a4d5ec9ebd378.jsonl'
ids={};out={}
L=[json.loads(l) for l in open(F)]
for d in L:
  c=d.get('message',{}).get('content')
  if isinstance(c,list):
    for x in c:
      if x.get('type')=='tool_use' and x.get('name')=='WebFetch': ids[x['id']]=x['input']['url']
for d in L:
  c=d.get('message',{}).get('content')
  if isinstance(c,list):
    for x in c:
      if x.get('type')=='tool_result' and x.get('tool_use_id') in ids:
        cc=x['content']; t=cc if isinstance(cc,str) else ' '.join(y.get('text','') for y in cc if isinstance(y,dict))
        out[ids[x['tool_use_id']]]=t
json.dump(out,open('/tmp/claude-0/-home-claude/02493dcd-1fa5-5a7a-8837-b8f092c62a5d/scratchpad/t/wf.json','w'),ensure_ascii=False)
print(len(out))
