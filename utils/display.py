"""CLI display helpers using rich. Owner: YOU."""
from rich.console import Console
from rich.table import Table

console = Console()


def print_table(title: str, headers: list, rows: list) -> None:
    """Print a rich table.
    headers: ['ID', 'Name', ...]
    rows:    [[1, 'Alice'], ...]
    """
    # TODO (YOU)
    table = Table(title=title)
    for h in headers:
        table.add_column(str(h))
    for r in rows:
        table.add_row(*[str(c) for c in r])
    console.print(table)


def success(msg: str) -> None:
    console.print(f"[green]✔ {msg}[/green]")


def error(msg: str) -> None:
    console.print(f"[red]✘ {msg}[/red]")


def ask(prompt: str) -> str:
    """Prompt and return stripped input."""
    # TODO (YOU)
    return input(prompt).strip()