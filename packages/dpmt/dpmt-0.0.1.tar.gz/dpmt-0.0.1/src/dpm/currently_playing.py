from client import client
from playlist import queue
from cs import cs

from rich import box
from rich.console import Group
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.text import Text


def return_current_status():
    current_status = client.status()
    return current_status


def screen_layout():
    # layout definition
    # TODO minimum size
    layout = Layout()
    layout.split_column(
        Layout(name="top"),
        Layout(name="bottom")
    )
    layout["top"].size = 20
    un_table = up_next_table()
    try:
        cs_information = current_song_information()
        current_status = return_current_status()
        pl_settings = playlist_options()

        # items in the top-left panel
        tl_items = Panel(
            Group(
                cs_information["title+panel"],
                cs_information["album+panel"],
                cs_information["artist+panel"],
                Panel(
                    Text(
                        f"[{pl_settings['repeat']}{pl_settings['random']}{pl_settings['consume']}{pl_settings['single']}]",
                        justify="center"
                    ),
                    box=box.SIMPLE_HEAD
                )
            ),
            style="blue",
            padding=3,
            title=(
                Text("⏵︎ Playing", style="reverse")
            ) if current_status["state"] == "play" else (
                Text("⏸︎ Paused")
            ),
            subtitle=Text(cs_information["progress"])
        )

        layout["top"].split(
            Layout(
                tl_items
            )
        )
        layout["bottom"].split(
            Layout(
                un_table
            )
        )

        return layout
    except (TypeError):
        layout["top"].split(
            Layout(
                Panel(
                    Text("MPD not playing", justify="center"),
                    padding=8,
                    style="blue"
                )
            )
        )
        layout["bottom"].split(
            un_table
        )
        return layout


def playlist_options():
    current_status = return_current_status()
    rep_str = "-"
    rand_str = "-"
    cons_str = "-"
    sing_str = "-"

    match current_status["repeat"]:
        case "1":
            rep_str = "r"

    match current_status["random"]:
        case "1":
            rand_str = "z"

    match current_status["consume"]:
        case "1":
            cons_str = "c"

    match current_status["single"]:
        case "1":
            sing_str = "s"

    return {
        "repeat": rep_str,
        "random": rand_str,
        "consume": cons_str,
        "single": sing_str
    }


def up_next_table():
    # up next table
    try:
        un_table = Table(
            expand=True,
            row_styles=["", "dim"],
            box=box.SIMPLE_HEAD
        )
        un_table.add_column("#", width=4)
        un_table.add_column("Title")
        un_table.add_column("Album")
        un_table.add_column("Artist")
        un_table.add_column("Length")

        playlist = queue()
        current_song = current_song_information()
        display_index = 1

        for item in playlist:
            if Text(item["title"]) == current_song["title"]:
                un_table.add_row(
                    Text(str(display_index)),
                    current_song["title"],
                    current_song["album"],
                    current_song["artist"],
                    Text(return_song_duration(item["time"]), justify="right")
                )
            else:
                un_table.add_row(
                    Text("+" + str(display_index)),
                    item["title"],
                    item["album"],
                    item["artist"],
                    Text(return_song_duration(item["time"]), justify="right")
                )
            display_index += 1

        return Panel(
            un_table,
            style="blue",
            title="Up Next"
        )
    except (TypeError):
        playlist = queue()
        display_index = 1

        for item in playlist:
            un_table.add_row(
                Text("+" + str(display_index)),
                item["title"],
                item["album"],
                item["artist"],
                Text(return_song_duration(item["time"]))
            )
            display_index += 1

        return Panel(
            un_table,
            style="blue",
            title="Up Next"
        )


def current_song_information():
    # client information
    try:
        cs_dictionary = client.currentsong()
        current_status = return_current_status()

        # current song strings, not in a panel
        cs_title = Text(
            cs_dictionary["title"],
            style="green"
        )
        cs_album = Text(
            cs_dictionary["album"],
            style="yellow"
        )
        cs_artist = Text(
            cs_dictionary["artist"],
            style="red"
        )

        # current song strings, in a panel
        cs_title_panel = Panel(
            Text(
                cs_dictionary["title"],
                justify="center",
                style="green"
            ),
            box=box.SIMPLE_HEAD
        )
        cs_album_panel = Panel(
            Text(
                cs_dictionary["album"],
                justify="center",
                style="dim yellow"
            ),
            box=box.SIMPLE_HEAD,
            title="From",
            style="blue"
        )
        cs_artist_panel = Panel(
            Text(
                cs_dictionary["artist"],
                justify="center",
                style="dim red"
            ),
            box=box.SIMPLE_HEAD,
            title="By",
            style="blue"
        )

        # current song progress
        cs_progress_array = []
        for item in current_status["time"].split(":"):
            cs_progress_array.append(item)
        cs_progress = (
            f'{return_song_duration(cs_progress_array[0])} / '
            f'{return_song_duration(cs_progress_array[1])}'
        )

        return {
            "title": cs_title,
            "album": cs_album,
            "artist": cs_artist,
            "title+panel": cs_title_panel,
            "album+panel": cs_album_panel,
            "artist+panel": cs_artist_panel,
            "progress": cs_progress,
        }
    except (KeyError):
        return


def return_song_duration(time):
    # get an integer for the minutes
    minutes = int(int(time) / 60)
    seconds = int(time) % 60
    if seconds < 10:
        seconds = f"0{int(time) % 60}"

    return f"{str(minutes)}:{str(seconds)}"


def update_layout():
    with Live(screen_layout(), refresh_per_second=4) as live:
        try:
            while True:
                live.update(screen_layout())
        except (KeyboardInterrupt, EOFError):
            live.stop()
            cs()
            return


