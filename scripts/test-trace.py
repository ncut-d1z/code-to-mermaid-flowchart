import copy, hashlib, importlib.util, json, subprocess, tempfile
from pathlib import Path
p=Path(__file__).resolve().parents[1]
s=p/'scripts/validate-trace.py'
with tempfile.TemporaryDirectory() as t:
 r=Path(t); (r/'s.py').write_text('def solve():\n    return 1\n'); (r/'d.mmd').write_text('flowchart TD\n A[Input] --> B[Return]\n')
 h=hashlib.sha256((r/'s.py').read_bytes()).hexdigest()
 d={'commit':None,'analysis':'static','dirty':False,'algorithms':[{'id':'solve','entry':'s.py:solve','calls':[],'uncertainties':[],'diagram':'d.mmd','nodes':['A','B'],'edges':['A-B'],'evidence':[{'kind':kind,'id':i,'file':'s.py','symbol':'solve','start':1,'end':2,'sha256':h,'condition':'entry' if kind=='node' else 'unconditional'} for kind,i in [('node','A'),('node','B'),('edge','A-B')]]}]}
 def run(name, obj, expected):
  (r/'trace.json').write_text(json.dumps(obj)); q=subprocess.run(['python',str(s),str(r/'trace.json'),'--root',str(r)],capture_output=True,text=True)
  assert q.returncode==expected,(name,q.returncode,q.stdout,q.stderr)
  print('PASS:',name)
 run('valid manifest',d,0)
 for name,mutate in [
  ('missing edge evidence',lambda x:x['algorithms'][0]['evidence'].pop()),
  ('stale source hash',lambda x:x['algorithms'][0]['evidence'][0].update(sha256='bad')),
  ('out of range line',lambda x:x['algorithms'][0]['evidence'][0].update(end=99)),
  ('path traversal',lambda x:x['algorithms'][0]['evidence'][0].update(file='../secret')),
  ('invalid algorithm type',lambda x:x['algorithms'].append(3)),
  ('invalid identity',lambda x:x['algorithms'][0]['evidence'][0].update(id=[]))]:
  c=copy.deepcopy(d); mutate(c); run(name,c,1)
 c=copy.deepcopy(d); c['commit']='a'*40; run('unavailable Git provenance',c,2)
 subprocess.run(['git','init','-q',str(r)],check=True)
 subprocess.run(['git','-C',str(r),'add','s.py','d.mmd'],check=True)
 subprocess.run(['git','-C',str(r),'-c','user.name=Test','-c','user.email=test@example.com','commit','-qm','fixture'],check=True)
 c['commit']=subprocess.check_output(['git','-C',str(r),'rev-parse','HEAD'],text=True).strip(); c['dirty']=True; run('Git SHA and dirty state',c,0)
 c['dirty']=False; run('incorrect dirty state',c,1)
 q=subprocess.run(['python',str(s),str(r/'missing.json'),'--root',str(r)],capture_output=True); assert q.returncode==2; print('PASS: missing manifest blocked')
for f in p.glob('**/*.md'):
 import re
 for link in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  if '://' not in link:
   assert (f.parent/link).is_file(),(f,link)
print('PASS: local Markdown resource links')
