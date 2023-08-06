from cs import cs
from shuffle import shuffle_library
from browse_library import browse_library
from search import search
from currently_playing import update_layout
from info_panel import info_panel
from playlist_opt import playlist_options
from Colours import colours
from Menu import Menu

from rich import box
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


menu = Menu()
console = Console()
cs()


def main():
    """Application's main function"""
    main_menu_table = Table(
        expand=True,
        box=box.SIMPLE_HEAD,
        row_styles=["", "dim"]
    )
    main_menu_table.add_column("#", ratio=1)
    main_menu_table.add_column("Options", ratio=12)

    display_index = 1
    main_menu = menu.generate_menu([
        "Browse Library",
        "Search Library",
        "Shuffle Library",
        "Playlist Options",
        "Currently Playing",
        "Exit"
    ])

    # generate table
    for entry in main_menu:
        main_menu_table.add_row(
            str(display_index),
            entry
        )
        display_index += 1

    # cs()
    print_again = True
    while True:
        try:
            match print_again:
                case True:
                    main_menu_panel = Panel(
                        main_menu_table,
                        title="Main Menu",
                        style=colours["green"]
                    )
                    console.print(main_menu_panel)
                case False:
                    pass
            menu_opt = int(input("Do: "))

            match menu_opt:
                case 1:
                    cs()
                    browse_library()
                    print_again = True
                case 2:
                    cs()
                    search()
                    print_again = True
                case 3:
                    cs()
                    shuffle_library()
                    print_again = True
                case 4:
                    cs()
                    playlist_options()
                    print_again = True
                case 5:
                    update_layout()
                    print_again = True
                case 6:
                    cs()
                    exit()
                case _:
                    info_panel("Invalid option")
                    print_again = False
        except (ValueError):
            info_panel("Invalid option")
            print_again = False
        except (KeyboardInterrupt):
            cs()
            exit()


# main()
