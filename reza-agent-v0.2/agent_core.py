import contextvars
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from agents import Agent, Runner, WebSearchTool
from agents.decorators import tool

from db import execute

ROOT = Path(__file__).parent.resolve()
WORKSPACE = ROOT / "workspace"
ACTIVE_TASK_ID: contextvars.ContextVar[str] = contextvars.ContextVar("active_task_id", default="")
MODEL = os.getenv("REZA_AGENT_MODEL", "gpt-5.6-luna")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def event(kind: str, message: str) -> None:
    task_id = ACTIVE_TASK_ID.get()
    if task_id:
        execute(
            "INSERT INTO events(task_id, kind, message, created_at) VALUES(?,?,?,?)",
            (task_id, kind, message, now()),
        )


def safe_path(relative_path: str) -> Path:
    task_id = ACTIVE_TASK_ID.get()
    if not task_id:
        raise RuntimeError("No active task workspace")
    base = (WORKSPACE / task_id).resolve()
    base.mkdir(parents=True, exist_ok=True)
    target = (base / relative_path).resolve()
    if target != base and base not in target.parents:
        raise ValueError("Path must stay inside the project workspace")
    return target


@tool
def write_project_file(path: str, content: str) -> str:
    """Create or overwrite a UTF-8 text file inside the current task workspace."""
    target = safe_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    event("builder", f"Created {path}")
    return f"Saved {path}"


@tool
def read_project_file(path: str) -> str:
    """Read a UTF-8 text file from the current task workspace."""
    target = safe_path(path)
    if not target.exists() or not target.is_file():
        return f"File not found: {path}"
    return target.read_text(encoding="utf-8")[:30000]


@tool
def list_project_files() -> str:
    """List files already created in the current task workspace."""
    task_id = ACTIVE_TASK_ID.get()
    base = WORKSPACE / task_id
    if not base.exists():
        return "No files yet."
    files = [str(p.relative_to(base)) for p in base.rglob("*") if p.is_file()]
    return "\n".join(files) if files else "No files yet."


@tool
def request_approval(action: str, details: str) -> str:
    """Request human approval before a consequential external action. Does not perform the action."""
    task_id = ACTIVE_TASK_ID.get()
    approval_id = str(uuid.uuid4())
    timestamp = now()
    execute(
        "INSERT INTO approvals(id, task_id, action, details, status, created_at, updated_at) VALUES(?,?,?,?,?,?,?)",
        (approval_id, task_id, action, details, "pending", timestamp, timestamp),
    )
    event("approval", f"Approval requested: {action}")
    return f"Approval request {approval_id} created. Stop before performing that action."


reza_agent = Agent(
    name="Reza Agent",
    model=MODEL,
    model_settings={"parallel_tool_calls": True, "verbosity": "low"},
    instructions=(
        "You are an efficient autonomous worker. Complete the user's goal rather than merely explaining how. "
        "Minimize model calls because this account has a strict request limit. Plan internally and batch related tool calls whenever possible. "
        "Use web search only when current information is genuinely needed. For build requests, create the actual files directly. "
        "Before finishing, inspect the files you created and self-review them in the same run for missing pieces, broken links, obvious bugs, and security issues. "
        "Fix clear defects without asking unnecessary questions. "
        "Before sending, publishing, spending money, deleting external data, or changing accounts, request approval and stop before that action. "
        "Finish with a concise summary of what was completed and list the files created."
    ),
    tools=[
        WebSearchTool(),
        write_project_file,
        read_project_file,
        list_project_files,
        request_approval,
    ],
)


async def run_goal(task_id: str, goal: str) -> str:
    token = ACTIVE_TASK_ID.set(task_id)
    try:
        event("system", "Understanding goal")
        result = await Runner.run(reza_agent, goal, max_turns=12)
        event("system", "Run finished")
        return str(result.final_output)
    finally:
        ACTIVE_TASK_ID.reset(token)
