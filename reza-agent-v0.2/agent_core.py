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


researcher = Agent(
    name="Researcher",
    instructions=(
        "Research only when it materially improves the task. Use web search for current facts. "
        "Return concise findings and do not invent evidence."
    ),
    tools=[WebSearchTool()],
)

builder = Agent(
    name="Builder",
    instructions=(
        "Turn goals and research into useful project artifacts. Create complete runnable files when asked. "
        "Use only the provided workspace tools and do not perform external side effects."
    ),
    tools=[write_project_file, read_project_file, list_project_files],
)

reviewer = Agent(
    name="Reviewer",
    instructions=(
        "Critically check the result against the user's exact goal. Look for missing pieces, broken UX, "
        "incomplete code, unsupported claims and obvious security issues. Return PASS or NEEDS WORK with fixes."
    ),
)

orchestrator = Agent(
    name="Reza Agent",
    instructions=(
        "Take the user's goal and drive it toward a finished result. Use Researcher for current information, "
        "Builder for actual files, and Reviewer before substantial completion. Keep moving without unnecessary questions. "
        "Before sending, publishing, spending money, deleting external data or changing accounts, request approval and stop. "
        "Summarize what was completed and list created files."
    ),
    tools=[
        researcher.as_tool(tool_name="research", tool_description="Research current information.", max_turns=8),
        builder.as_tool(tool_name="build", tool_description="Create and inspect project files.", max_turns=12),
        reviewer.as_tool(tool_name="review", tool_description="Review work quality.", max_turns=6),
        request_approval,
    ],
)


async def run_goal(task_id: str, goal: str) -> str:
    token = ACTIVE_TASK_ID.set(task_id)
    try:
        event("system", "Understanding goal")
        result = await Runner.run(orchestrator, goal, max_turns=30)
        event("system", "Run finished")
        return str(result.final_output)
    finally:
        ACTIVE_TASK_ID.reset(token)
