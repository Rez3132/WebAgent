import asyncio, os, traceback, uuid
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from agent_core import WORKSPACE, run_goal
from db import execute, fetchall, fetchone, init_db

app = FastAPI(title='Reza Agent', version='1.0')

def now(): return datetime.now(timezone.utc).isoformat()

class TaskCreate(BaseModel):
    goal: str = Field(min_length=3, max_length=12000)

class ApprovalDecision(BaseModel):
    approved: bool

@app.on_event('startup')
async def startup():
    init_db(); WORKSPACE.mkdir(parents=True, exist_ok=True)

@app.get('/', response_class=HTMLResponse)
async def home():
    return '''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Reza Agent</title><style>
    :root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#0b0d10;color:#f3f4f6;font-family:Inter,system-ui,sans-serif}.wrap{max-width:1000px;margin:auto;padding:28px 16px 60px}.top{display:flex;justify-content:space-between;align-items:center;gap:16px}.brand{font-size:30px;font-weight:900;letter-spacing:-.04em}.sub{color:#8d949e;font-size:13px}.card,.panel{border:1px solid #262b33;background:#12151a;border-radius:18px}.card{margin-top:24px;padding:18px}.goal{width:100%;min-height:170px;background:transparent;color:white;border:0;outline:0;resize:vertical;font-size:18px;line-height:1.55}.row{display:flex;justify-content:space-between;gap:12px;align-items:center;border-top:1px solid #262b33;padding-top:14px}.btn{border:0;border-radius:12px;background:#e8ff65;color:#111;padding:13px 18px;min-height:48px;font-weight:900;cursor:pointer}.btn:disabled{opacity:.5}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}.panel{min-height:320px;padding:16px}.event{padding:9px 0;border-bottom:1px solid #1d2127}.file{display:block;color:#e8ff65;margin-top:7px}.ok{color:#b9e86a}.err{color:#ff8e8e}.working{color:#f0d77a}.approval{border:1px solid #5b4930;background:#1a1712;padding:12px;border-radius:12px;margin-top:10px}.approval button{margin-right:8px;padding:9px 11px}.notice{margin-top:12px;font-size:14px}@media(max-width:760px){.grid{grid-template-columns:1fr}.row,.top{align-items:stretch;flex-direction:column}.btn{width:100%;min-height:54px}.goal{min-height:210px}}</style></head><body><div class="wrap"><div class="top"><div><div class="brand">Reza Agent</div><div class="sub">Autonomous research · build · review</div></div><div id="health" class="sub">Checking API…</div></div><div class="card"><textarea id="goal" class="goal" placeholder="Tell Reza Agent what you want done…"></textarea><div class="row"><span class="sub">The agent can research the web, create files and review its own work.</span><button id="run" class="btn">Run task →</button></div><div id="notice" class="notice sub">Type a goal, then tap Run task.</div></div><div class="grid"><div class="panel"><h3>Activity</h3><div id="activity" class="sub">No task running.</div></div><div class="panel"><h3>Result</h3><div id="result" class="sub">Your result will appear here.</div><div id="approvals"></div><div id="files"></div></div></div></div><script>
    let task=null,timer=null;const $=s=>document.querySelector(s);const esc=s=>String(s??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));
    async function health(){try{const r=await fetch('/api/health');const d=await r.json();$('#health').textContent=d.api_key_configured?'API connected':'API key needed';$('#health').className='sub '+(d.api_key_configured?'ok':'err')}catch(e){$('#health').textContent='Server unavailable';$('#health').className='sub err'}}
    function notice(t,k='sub'){const n=$('#notice');n.textContent=t;n.className='notice '+k}
    async function runTask(){const goal=$('#goal').value.trim();if(goal.length<3){notice('Type a task first.','err');return}const b=$('#run');b.disabled=true;b.textContent='Starting…';notice('Starting task…','working');try{const r=await fetch('/api/tasks',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({goal})});const d=await r.json();if(!r.ok)throw new Error(d.detail||r.status);task=d.id;await poll();timer=setInterval(poll,1200)}catch(e){notice('Could not start: '+e.message,'err')}finally{b.disabled=false;b.textContent='Run task →'}}
    async function poll(){if(!task)return;const r=await fetch('/api/tasks/'+task);const t=await r.json();$('#activity').innerHTML=t.events.length?t.events.map(e=>`<div class="event">${esc(e.message)}</div>`).join(''):'Working…';$('#result').textContent=t.error?'Error: '+t.error:(t.result||'The agent is working…');$('#result').className=t.error?'err':'';$('#approvals').innerHTML=(t.approvals||[]).filter(a=>a.status==='pending').map(a=>`<div class="approval"><b>${esc(a.action)}</b><p>${esc(a.details)}</p><button onclick="decide('${a.id}',true)">Approve</button><button onclick="decide('${a.id}',false)">Reject</button></div>`).join('');$('#files').innerHTML=(t.files||[]).map(f=>`<a class="file" target="_blank" href="/api/tasks/${task}/files/${encodeURI(f)}">↳ ${esc(f)}</a>`).join('');if(['completed','failed'].includes(t.status)){clearInterval(timer);timer=null;notice(t.status==='completed'?'Task completed.':'Task failed.',''+(t.status==='completed'?'ok':'err'))}else if(t.status==='awaiting_approval')notice('Approval needed.','working');else notice('Status: '+t.status,'working')}
    async function decide(id,approved){await fetch('/api/approvals/'+id,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({approved})});poll()}window.decide=decide;$('#run').addEventListener('click',runTask);health();</script></body></html>'''

@app.get('/api/health')
async def health(): return {'ok':True,'version':'1.0','api_key_configured':bool(os.getenv('OPENAI_API_KEY'))}

@app.get('/api/tasks')
async def tasks(): return fetchall('SELECT * FROM tasks ORDER BY created_at DESC LIMIT 50')

@app.post('/api/tasks')
async def create_task(payload: TaskCreate):
    tid=str(uuid.uuid4()); ts=now(); execute('INSERT INTO tasks(id,goal,status,result,error,created_at,updated_at) VALUES(?,?,?,?,?,?,?)',(tid,payload.goal.strip(),'queued',None,None,ts,ts)); asyncio.create_task(process_task(tid,payload.goal.strip())); return {'id':tid,'status':'queued'}

async def process_task(task_id, goal):
    try:
        if not os.getenv('OPENAI_API_KEY'): raise RuntimeError('OPENAI_API_KEY is not configured in Railway.')
        execute('UPDATE tasks SET status=?,updated_at=? WHERE id=?',('running',now(),task_id)); result=await run_goal(task_id,goal); pending=fetchone("SELECT id FROM approvals WHERE task_id=? AND status='pending' LIMIT 1",(task_id,)); status='awaiting_approval' if pending else 'completed'; execute('UPDATE tasks SET status=?,result=?,updated_at=? WHERE id=?',(status,result,now(),task_id))
    except Exception as exc:
        traceback.print_exc(); execute('UPDATE tasks SET status=?,error=?,updated_at=? WHERE id=?',('failed',f'{type(exc).__name__}: {exc}',now(),task_id))

@app.get('/api/tasks/{task_id}')
async def get_task(task_id:str):
    task=fetchone('SELECT * FROM tasks WHERE id=?',(task_id,));
    if not task: raise HTTPException(404,'Task not found')
    task['events']=fetchall('SELECT id,kind,message,created_at FROM events WHERE task_id=? ORDER BY id',(task_id,)); task['approvals']=fetchall('SELECT id,action,details,status,created_at,updated_at FROM approvals WHERE task_id=? ORDER BY created_at',(task_id,)); base=WORKSPACE/task_id; task['files']=[str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()] if base.exists() else []; return task

@app.post('/api/approvals/{approval_id}')
async def approve(approval_id:str,payload:ApprovalDecision):
    a=fetchone('SELECT * FROM approvals WHERE id=?',(approval_id,));
    if not a: raise HTTPException(404,'Approval not found')
    status='approved' if payload.approved else 'rejected'; execute('UPDATE approvals SET status=?,updated_at=? WHERE id=?',(status,now(),approval_id)); pending=fetchone("SELECT id FROM approvals WHERE task_id=? AND status='pending'",(a['task_id'],));
    if not pending: execute("UPDATE tasks SET status=?,updated_at=? WHERE id=? AND status='awaiting_approval'",('completed',now(),a['task_id']))
    return {'id':approval_id,'status':status}

@app.get('/api/tasks/{task_id}/files/{file_path:path}')
async def get_file(task_id:str,file_path:str):
    base=(WORKSPACE/task_id).resolve(); target=(base/file_path).resolve();
    if target!=base and base not in target.parents: raise HTTPException(400,'Invalid path')
    if not target.exists() or not target.is_file(): raise HTTPException(404,'File not found')
    return FileResponse(target,filename=target.name)
