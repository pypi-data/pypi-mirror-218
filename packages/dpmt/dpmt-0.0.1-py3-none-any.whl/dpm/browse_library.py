from cs import cs
from client import client
from info_panel import info_panel
from Menu import Menu
from Colours import colours

from rich import box
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


menu = Menu()
console = Console()

current_level = 0


def browse_library():
    """The main function"""
    global current_level
    current_level = 0
    while True:
        try:
            match current_level:
                # level 0: display table of artists
                case 0:
                    try:
                        cs()
                        artists = common_browse_interface(
                            "",
                            "directory"
                        )
                        current_level += 1
                    except (KeyboardInterrupt, EOFError):
                        pass
                # level 1: ask user to choose an artist
                case 1:
                    try:
                        user_input_1 = input("Choose: ")
                        handle_input(user_input_1, artists)
                    except (KeyboardInterrupt, EOFError):
                        cs()
                        return
                # level 2: display table of albums by the selected artist
                case 2:
                    try:
                        cs()
                        albums = common_browse_interface(
                            # the final index is everything ahead of the 3rd
                            # position in user_input_1
                            artists[int(user_input_1[2:]) - 1],
                            "directory"
                        )
                        current_level += 1
                    except (KeyboardInterrupt, EOFError):
                        pass
                # level 3: ask user to choose an albm
                case 3:
                    try:
                        user_input_3 = input("Choose: ")
                        handle_input(user_input_3, albums)
                    except (KeyboardInterrupt, EOFError):
                        cs()
                        current_level -= 3
                # level 4: display table of tracks in selected album
                case 4:
                    try:
                        cs()
                        titles = common_browse_interface(
                            albums[int(user_input_3[2:]) - 1],
                            "file"
                        )
                        current_level += 1
                    except (KeyboardInterrupt, EOFError):
                        pass
                # level 5: ask user to select tracks
                case 5:
                    try:
                        user_input_5 = input("Choose: ")
                        handle_input(user_input_5, titles)
                    except (KeyboardInterrupt, EOFError):
                        cs()
                        current_level -= 3
        except (ValueError, IndexError):
            pass


def handle_input(input, processed_query):
    """Handle user input"""
    global current_level
    input_array = []
    for item in input.split(" "):
        input_array.append(item)

    # check for length of array
    match len(input_array):
        case 1:
            info_panel("Invalid selection")
        case 2:
            match input_array[0]:
                # check if the letter at the 0th index is acceptable
                # error messaging for a selection out of possible indices
                case "a":
                    if input_array[1].isdigit():
                        # add selection to queue
                        media_selection = processed_query[int(input_array[1]) - 1]
                        info_panel("Added!")
                        client.add(media_selection)
                    else:
                        info_panel("Invalid selection")
                case "v":
                    if current_level == 5:
                        info_panel("Invalid selection")
                    else:
                        if input_array[1].isdigit():
                            if int(input_array[1]) > len(processed_query):
                                info_panel("Invalid selection")
                            else:
                                current_level += 1
                        else:
                            info_panel("Invalid selection")
                case _:
                    info_panel("Invalid selection")
        case _:
            info_panel("Invalid selection")


def common_browse_interface(directory_name, file_type):
    """Common interface for browsing the library"""
    list = menu.list_directory(
        directory_name,
        file_type
    )
    list_display = generate_table(list, file_type)
    console.print(list_display)
    info_panel("⟵ Ctrl+c to return")
    return list


def generate_table(media_list, file_type):
    """Generate a table"""
    display_index = 1

    result_table = Table(
        expand=True,
        box=box.SIMPLE_HEAD,
        row_styles=["", "dim"]
    )
    result_table.add_column("#")
    result_table.add_column("Title")

    match file_type:
        case "directory":
            for item in media_list:
                result_table.add_row(
                    str(display_index),
                    f"🗀  {item}"
                )
                display_index += 1
        case "file":
            for item in media_list:
                result_table.add_row(
                    str(display_index),
                    f"𝅘𝅥𝅮 {item}"
                )
                display_index += 1

    panel = Panel(
        result_table,
        title="Browse Library",
        style=colours["blue"]
    )
    return panel
