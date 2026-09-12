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
    return target.read_text(encoding="utf-8")[:40000]


@tool
def replace_project_text(path: str, old_text: str, new_text: str) -> str:
    """Replace exact text inside a UTF-8 project file."""
    target = safe_path(path)
    if not target.exists() or not target.is_file():
        return f"File not found: {path}"
    content = target.read_text(encoding="utf-8")
    if old_text not in content:
        return "Text to replace was not found."
    target.write_text(content.replace(old_text, new_text), encoding="utf-8")
    event("builder", f"Updated {path}")
    return f"Updated {path}"


@tool
def list_project_files() -> str:
    """List files already created in the current task workspace."""
    task_id = ACTIVE_TASK_ID.get()
    base = WORKSPACE / task_id
    if not base.exists():
        return "No files yet."
    files = [str(p.relative_to(base)) for p in base.rglob("*") if p.is_file()]
    return "\n".join(files[:500]) if files else "No files yet."


@tool
def request_approval(action: str, details: str) -> str:
    """Request user approval before consequential external actions."""
    task_id = ACTIVE_TASK_ID.get()
    approval_id = str(uuid.uuid4())
    timestamp = now()
    execute(
        "INSERT INTO approvals(id, task_id, action, details, status, created_at, updated_at) VALUES(?,?,?,?,?,?,?)",
        (approval_id, task_id, action, details, "pending", timestamp, timestamp),
    )
    event("approval", f"Approval requested: {action}")
    return f"Approval request {approval_id} created. Stop before performing that action."


researcher = Agent(
    name="Researcher",
    instructions=(
        "Research only when it materially improves the task. Use web search for current facts. "
        "Prefer primary and authoritative sources, distinguish facts from assumptions, and never invent evidence."
    ),
    tools=[WebSearchTool()],
)

builder = Agent(
    name="Builder",
    instructions=(
        "Turn goals and research into finished project artifacts. Do the work instead of only describing it. "
        "Inspect existing files before changing important work, create complete runnable files, verify key output after writing, "
        "and stay inside the provided task workspace."
    ),
    tools=[write_project_file, read_project_file, replace_project_text, list_project_files],
)

reviewer = Agent(
    name="Reviewer",
    instructions=(
        "Critically check work against the user's exact goal. Look for missing requirements, incomplete code, broken UX, "
        "unsupported claims, obvious security issues and unfinished placeholders. Return PASS or NEEDS WORK with concise fixes."
    ),
)

orchestrator = Agent(
    name="Reza Agent",
    instructions=(
        "You are an autonomous task-completion agent. Repeatedly understand the goal, choose the next useful action, "
        "inspect the result and continue until the deliverable is genuinely complete. Prefer doing work over explaining it. "
        "Use Researcher for current external information, Builder for actual files, and Reviewer before substantial completion. "
        "If a tool fails, diagnose it and try a sensible alternative. Ask questions only when a missing decision truly blocks progress. "
        "Never claim an action or file exists unless a tool result confirms it. Before sending/publishing externally, spending money, "
        "deleting external data, or changing external accounts, request approval and stop. Do not reveal private chain-of-thought. "
        "At completion, give a concise result and list created files."
    ),
    tools=[
        researcher.as_tool(tool_name="research", tool_description="Research current information on the web.", max_turns=10),
        builder.as_tool(tool_name="build", tool_description="Create, inspect and improve project files.", max_turns=16),
        reviewer.as_tool(tool_name="review", tool_description="Review the work against the task.", max_turns=8),
        request_approval,
    ],
)


async def run_goal(task_id: str, goal: str) -> str:
    token = ACTIVE_TASK_ID.set(task_id)
    try:
        event("system", "Understanding goal")
        result = await Runner.run(orchestrator, goal, max_turns=40)
        event("system", "Run finished")
        return str(result.final_output)
    finally:
        ACTIVE_TASK_ID.reset(token)
