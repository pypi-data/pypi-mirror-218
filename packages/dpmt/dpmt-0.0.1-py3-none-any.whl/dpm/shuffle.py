# from client import client
from client import client
from info_panel import info_panel


def shuffle_library():
    client.clear()
    client.add("")
    client.shuffle()
    client.play()
    info_panel("Shuffled!")
