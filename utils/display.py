"""CLI display helpers using rich. Owner: YOU."""
from rich.console import Console
from rich.table import Table

console = Console()


def print_table(title: str, headers: list, rows: list) -> None:
    """Print a rich formatted table.
    headers: list of column titles  ['ID', 'Name', ...]
    rows: list of row data [[1, 'Alice'], ...]
    """
    
    table = Table(title=title)
    for h in headers:
        table.add_column(str(h))
    for r in rows:
        table.add_row(*[str(c) for c in r]) # * this unpacks the list into separate arguments
    console.print(table)


def success(msg: str) -> None:
    console.print(f"[green]✔ {msg}[/green]")


def error(msg: str) -> None:
    console.print(f"[red]✘ {msg}[/red]")


def ask(prompt: str) -> str:
    """Prompt and return stripped input."""
    return input(prompt).strip()
