import asyncio
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

from agent_core import WORKSPACE, run_goal
from db import execute, fetchall, fetchone, init_db

load_dotenv()
app = FastAPI(title="Reza Agent", version="0.2.0")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class TaskCreate(BaseModel):
    goal: str = Field(min_length=3, max_length=12000)


class ApprovalDecision(BaseModel):
    approved: bool


@app.on_event("startup")
async def startup() -> None:
    init_db()
    WORKSPACE.mkdir(parents=True, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home():
    return """<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><title>Reza Agent</title><style>
    :root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#0b0d10;color:#f4f5f7;font-family:Inter,system-ui,sans-serif}.wrap{max-width:980px;margin:auto;padding:28px 16px}.top{display:flex;justify-content:space-between;align-items:center;gap:16px}.brand{font-size:28px;font-weight:800}.sub{color:#8d949e;font-size:13px}.card{margin-top:24px;border:1px solid #262b33;border-radius:18px;background:#12151a;padding:18px}.goal{width:100%;min-height:150px;background:transparent;color:white;border:0;outline:0;resize:vertical;font-size:17px;line-height:1.5}.row{display:flex;justify-content:space-between;gap:12px;align-items:center;border-top:1px solid #262b33;padding-top:14px}.btn{border:0;border-radius:11px;background:#e8ff65;color:#111;padding:11px 16px;font-weight:800;cursor:pointer}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}.panel{border:1px solid #262b33;border-radius:16px;background:#111419;min-height:300px;padding:16px}.muted{color:#8d949e}.event{padding:9px 0;border-bottom:1px solid #1d2127}.approval{border:1px solid #5b4930;background:#1a1712;padding:12px;border-radius:12px;margin-top:10px}.approval button{margin-right:8px;padding:8px 10px;border-radius:8px;border:0}.file{display:block;color:#e8ff65;margin-top:7px;text-decoration:none}@media(max-width:760px){.grid{grid-template-columns:1fr}.top{align-items:flex-start;flex-direction:column}}
    </style></head><body><div class='wrap'><div class='top'><div><div class='brand'>Reza Agent</div><div class='sub'>Research · Build · Review</div></div><div id='health' class='sub'>Checking API…</div></div><div class='card'><textarea id='goal' class='goal' placeholder='Tell Reza Agent what you want done…'></textarea><div class='row'><span class='sub'>The agent can research the web and create project files.</span><button id='run' class='btn'>Run task →</button></div></div><div class='grid'><div class='panel'><h3>Activity</h3><div id='activity' class='muted'>No task running.</div></div><div class='panel'><h3>Result</h3><div id='result' class='muted'>Your result will appear here.</div><div id='approvals'></div><div id='files'></div></div></div></div><script>
    let task=null,timer=null; const $=s=>document.querySelector(s); const esc=s=>String(s??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));
    async function health(){try{let r=await fetch('/api/health'),d=await r.json();$('#health').textContent=d.api_key_configured?'API connected':'OpenAI API key needed';}catch{$('#health').textContent='Server unavailable';}}
    async function run(){let goal=$('#goal').value.trim();if(!goal)return;$('#run').disabled=true;let r=await fetch('/api/tasks',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({goal})});let d=await r.json();task=d.id;$('#run').disabled=false;poll();if(timer)clearInterval(timer);timer=setInterval(poll,1200)}
    async function poll(){if(!task)return;let r=await fetch('/api/tasks/'+task);if(!r.ok)return;let t=await r.json();$('#activity').className='';$('#activity').innerHTML=t.events.length?t.events.map(e=>`<div class='event'>${esc(e.message)}</div>`).join(''):'Working…';$('#result').className='';$('#result').textContent=t.error?'Error: '+t.error:(t.result||'The agent is working…');$('#approvals').innerHTML=(t.approvals||[]).filter(a=>a.status==='pending').map(a=>`<div class='approval'><b>${esc(a.action)}</b><p>${esc(a.details)}</p><button onclick=decide('${a.id}',true)>Approve</button><button onclick=decide('${a.id}',false)>Reject</button></div>`).join('');$('#files').innerHTML=(t.files||[]).map(f=>`<a class='file' target='_blank' href='/api/tasks/${task}/files/${encodeURI(f)}'>↳ ${esc(f)}</a>`).join('');if(['completed','failed'].includes(t.status)&&timer){clearInterval(timer);timer=null;}}
    async function decide(id,approved){await fetch('/api/approvals/'+id,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({approved})});poll()} window.decide=decide;$('#run').onclick=run;health();
    </script></body></html>"""


@app.get("/api/health")
async def health():
    return {"ok": True, "version": "0.2.0", "api_key_configured": bool(os.getenv("OPENAI_API_KEY"))}


@app.get("/api/tasks")
async def tasks():
    return fetchall("SELECT * FROM tasks ORDER BY created_at DESC LIMIT 50")


@app.post("/api/tasks")
async def create_task(payload: TaskCreate):
    task_id = str(uuid.uuid4())
    timestamp = now()
    execute("INSERT INTO tasks(id, goal, status, result, error, created_at, updated_at) VALUES(?,?,?,?,?,?,?)", (task_id, payload.goal.strip(), "queued", None, None, timestamp, timestamp))
    asyncio.create_task(process_task(task_id, payload.goal.strip()))
    return {"id": task_id, "status": "queued"}


async def process_task(task_id: str, goal: str) -> None:
    try:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not configured in Railway yet.")
        execute("UPDATE tasks SET status=?, updated_at=? WHERE id=?", ("running", now(), task_id))
        result = await run_goal(task_id, goal)
        pending = fetchone("SELECT id FROM approvals WHERE task_id=? AND status='pending' ORDER BY created_at LIMIT 1", (task_id,))
        status = "awaiting_approval" if pending else "completed"
        execute("UPDATE tasks SET status=?, result=?, updated_at=? WHERE id=?", (status, result, now(), task_id))
    except Exception as exc:
        execute("UPDATE tasks SET status=?, error=?, updated_at=? WHERE id=?", ("failed", str(exc), now(), task_id))


@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    task = fetchone("SELECT * FROM tasks WHERE id=?", (task_id,))
    if not task:
        raise HTTPException(404, "Task not found")
    task["events"] = fetchall("SELECT id, kind, message, created_at FROM events WHERE task_id=? ORDER BY id ASC", (task_id,))
    task["approvals"] = fetchall("SELECT id, action, details, status, created_at, updated_at FROM approvals WHERE task_id=? ORDER BY created_at ASC", (task_id,))
    base = WORKSPACE / task_id
    task["files"] = [str(p.relative_to(base)) for p in base.rglob("*") if p.is_file()] if base.exists() else []
    return task


@app.post("/api/approvals/{approval_id}")
async def decide_approval(approval_id: str, payload: ApprovalDecision):
    approval = fetchone("SELECT * FROM approvals WHERE id=?", (approval_id,))
    if not approval:
        raise HTTPException(404, "Approval not found")
    if approval["status"] != "pending":
        return approval
    new_status = "approved" if payload.approved else "rejected"
    execute("UPDATE approvals SET status=?, updated_at=? WHERE id=?", (new_status, now(), approval_id))
    task_id = approval["task_id"]
    pending = fetchone("SELECT id FROM approvals WHERE task_id=? AND status='pending'", (task_id,))
    if not pending:
        execute("UPDATE tasks SET status=?, updated_at=? WHERE id=? AND status='awaiting_approval'", ("completed", now(), task_id))
    return {"id": approval_id, "status": new_status}


@app.get("/api/tasks/{task_id}/files/{file_path:path}")
async def get_file(task_id: str, file_path: str):
    base = (WORKSPACE / task_id).resolve()
    target = (base / file_path).resolve()
    if target != base and base not in target.parents:
        raise HTTPException(400, "Invalid path")
    if not target.exists() or not target.is_file():
        raise HTTPException(404, "File not found")
    return FileResponse(target, filename=target.name)
