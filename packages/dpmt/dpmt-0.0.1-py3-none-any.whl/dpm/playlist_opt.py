from client import client
from cs import cs
from info_panel import info_panel
from Colours import colours
import os

from rich import box
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.console import Console


console = Console()
# status = client.status()

# repeat_tgl = 1 if status["repeat"] == "1" else 0
# random_tgl = 1 if status["random"] == "1" else 0
# consume_tgl = 1 if status["consume"] == "1" else 0
# single_tgl = 1 if status["single"] == "1" else 0


def generate_layout():
    # left table
    ltable = Table(
        expand=True,
        row_styles=["", "dim"],
        box=box.SIMPLE_HEAD
    )
    ltable.add_column("#")
    ltable.add_column("Option")

    # right table
    rtable = Table(
        expand=True,
        row_styles=["", "dim"],
        box=box.SIMPLE_HEAD
    )
    rtable.add_column("#")
    rtable.add_column("Option")

    # layout
    layout = Layout()
    layout.split_row(
        Layout(name="left"),
        Layout(name="right"),
    )

    # layout size
    _width, _height = os.get_terminal_size()
    console.size = (_width, 12)

    lstrings = [
        "Toggle Repeat",
        "Toggle Random",
        "Toggle Consume",
        "Toggle Single",
        "Toggle Playback",
    ]

    rstrings = [
        "Shuffle Playlist",
        "Previous Track",
        "Next Track",
        "Stop Playback",
        "Clear Playlist",
    ]

    display_index = 1
    for item in lstrings:
        ltable.add_row(str(display_index), item)
        display_index += 1

    for item in rstrings:
        rtable.add_row(str(display_index), item)
        display_index += 1

    # add to layout
    layout["left"].split(
        Layout(
            Panel(
                ltable,
                title="Toggles",
                style=colours["yellow"]
            )
        )
    )
    layout["right"].split(
        Layout(
            Panel(
                rtable,
                title="Playback",
                style=colours["yellow"]
            )
        )
    )

    return layout


def playlist_options():
    current_level = 1
    while True:
        match current_level:
            case 1:
                console.print(generate_layout())
                info_panel("⟵ Ctrl+c to return")
                current_level += 1
            case 2:
                try:
                    operation = input("Do: ")
                    handle_input(operation)
                except (KeyboardInterrupt, EOFError):
                    cs()
                    return
            case _:
                pass


def handle_input(input):
    # update if there are ever more than 10 options
    global repeat_tgl, random_tgl, consume_tgl, single_tgl
    confirmation = ""
    status = client.status()

    repeat_tgl = 1 if status["repeat"] == "1" else 0
    random_tgl = 1 if status["random"] == "1" else 0
    consume_tgl = 1 if status["consume"] == "1" else 0
    single_tgl = 1 if status["single"] == "1" else 0

    while True:
        if len(input) <= 10:
            match input:
                case "1":
                    repeat_tgl ^= 1
                    client.repeat(repeat_tgl)
                    confirmation = "Repeat is on" if repeat_tgl == 1 else "Repeat is off"
                    info_panel(confirmation)
                    break
                case "2":
                    random_tgl ^= 1
                    client.random(random_tgl)
                    confirmation = "Random mode is on" if random_tgl == 1 else "Random mode is off"
                    info_panel(confirmation)
                    break
                # SHUFFLE
                case "3":
                    consume_tgl ^= 1
                    client.consume(consume_tgl)
                    confirmation = "Consume is on" if consume_tgl == 1 else "Consume is off"
                    info_panel(confirmation)
                    break
                case "4":
                    single_tgl ^= 1
                    client.single(single_tgl)
                    confirmation = "Single mode is on" if single_tgl == 1 else "Single mode is off"
                    info_panel(confirmation)
                    break
                case "5":
                    # check if toggle is needed
                    client.pause()
                    info_panel("Playback toggled")
                    break
                case "6":
                    client.shuffle()
                    info_panel("Shuffled")
                    break
                case "7":
                    client.previous()
                    info_panel("Playing previous song")
                    break
                case "8":
                    client.next()
                    info_panel("Playing next song")
                    break
                case "9":
                    client.stop()
                    info_panel("Playback stopped")
                    break
                case "10":
                    client.clear()
                    info_panel("Playlist cleared")
                    break
                case _:
                    info_panel("Invalid selection")
                    break
        else:
            info_panel("Invalid selection")
            break
