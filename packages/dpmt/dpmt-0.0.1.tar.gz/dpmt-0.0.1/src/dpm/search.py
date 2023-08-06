from cs import cs
from client import client
from info_panel import info_panel

from Menu import Menu
from Colours import colours
from rich import box
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


console = Console()
menu = Menu()


def search():
    # initial level
    current_level = 1
    while True:
        try:
            match current_level:
                case 1:
                    try:
                        info_panel("⟵ Ctrl+c to return to main menu")

                        # ask user for input
                        user_query = input("Search: ")
                        user_query_result = client.search("any", user_query)
                        user_query_processed = process_query_result(user_query_result)

                        # generate & print table of search results
                        table = generate_table(user_query_processed)
                        cs()
                        console.print(table)
                        info_panel("⟵ Ctrl+c to return to search")

                        # increase level
                        current_level += 1
                    except (KeyboardInterrupt, EOFError):
                        cs()
                        return
                case 2:
                    try:
                        # ask user for input
                        query_option = input("Choose: ")

                        # handle input
                        handle_input(query_option, current_level, user_query_processed)
                    except (KeyboardInterrupt, EOFError):
                        cs()
                        current_level -= 1
        except (ValueError, IndexError):
            pass


def process_query_result(query_result):
    # process the result of a query and add it to an array
    query_result_array = []
    for item in query_result:
        query_result_array.append(item)

    return query_result_array


def handle_input(input, current_level, processed_query):
    # split input and put into array
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
                case "a":
                    if input_array[1].isdigit():
                        # add selection to queue
                        media_selection = processed_query[int(input_array[1]) - 1]
                        info_panel("Added!")
                        client.add(media_selection["file"])
                    else:
                        info_panel("Invalid selection")
                case _:
                    info_panel("Invalid selection")
        case _:
            info_panel("Invalid selection")


def generate_table(processed_query):
    # generate a table of search results
    display_index = 1

    # define the table
    query_result_table = Table(
        expand=True,
        box=box.SIMPLE_HEAD,
        row_styles=["", "dim"]
    )
    query_result_table.add_column("Artist")
    query_result_table.add_column("#")
    query_result_table.add_column("Title")
    query_result_table.add_column("Album")

    # add items to table
    for item in processed_query:
        query_result_table.add_row(
            item["artist"],
            str(display_index),
            item["title"],
            item["album"]
        )
        display_index += 1

    # put table into panel
    panel = Panel(query_result_table, title="Search Results", style=colours["magenta"])
    return panel
