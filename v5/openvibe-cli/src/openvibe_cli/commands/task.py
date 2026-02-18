"""vibe task commands (approval queue)."""

import httpx
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Manage approval tasks")
console = Console()


def _host(ctx: typer.Context) -> str:
    return ctx.obj.get("host", "http://localhost:8000") if ctx.obj else "http://localhost:8000"


@app.command("list")
def list_tasks(
    ctx: typer.Context,
    workspace: str = typer.Option(..., "--workspace", help="Workspace ID"),
) -> None:
    """List pending approval requests."""
    host = _host(ctx)
    resp = httpx.get(f"{host}/api/v1/workspaces/{workspace}/approvals")
    resp.raise_for_status()
    data = resp.json()
    if not data:
        console.print("No pending approvals.")
        return
    table = Table("ID", "Role", "Action", "Status")
    for item in data:
        table.add_row(item.get("id", ""), item.get("role_id", ""),
                      item.get("action", ""), item.get("status", ""))
    console.print(table)


@app.command("approve")
def approve_task(
    ctx: typer.Context,
    request_id: str = typer.Argument(..., help="Approval request ID"),
) -> None:
    """Approve a pending request."""
    host = _host(ctx)
    resp = httpx.post(f"{host}/api/v1/approvals/{request_id}/approve")
    resp.raise_for_status()
    console.print(f"[green]Approved request '{request_id}'[/green]")


@app.command("reject")
def reject_task(
    ctx: typer.Context,
    request_id: str = typer.Argument(..., help="Approval request ID"),
    reason: str = typer.Option("", "--reason", help="Rejection reason"),
) -> None:
    """Reject a pending request."""
    host = _host(ctx)
    resp = httpx.post(f"{host}/api/v1/approvals/{request_id}/reject",
                      json={"reason": reason})
    resp.raise_for_status()
    console.print(f"[yellow]Rejected request '{request_id}'[/yellow]")
