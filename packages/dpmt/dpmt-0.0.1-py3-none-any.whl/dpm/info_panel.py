from rich.panel import Panel
from rich.console import Console
from Colours import colours


def info_panel(information):
    console = Console()
    panel = ""
    panel = Panel(
        information,
        style=colours["red"]
    )
    console.print(panel)