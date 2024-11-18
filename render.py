import os
from helpers import clean_clear_screen
from queue import Queue
from settings import settings

def render_game(state: Queue, shutdown: Queue):
    os.system("clear")

    text = settings.get_game_text("game_loop")

    while shutdown.empty():
        if not state.empty():
            clean_clear_screen()

            frame = state.get()
            render_frame(frame, text)

def render_frame(frame, text):
    score = frame["score"] * 100
    grid = frame["grid"]

    sizeY = len(grid)
    sizeX = len(grid[0])

    print(f"\n{text["score"]}: {score:010d}")
    print("╔" + "═" * (1 + sizeX * 2) + "╗")

    for row in range(sizeY):
        print("║", end=" ")
        for col in range(sizeX):
            print(f"{grid[row][col]}", end=" ")
        print("║")

    print("╚" + "═" * (1 + sizeX * 2) + "╝")
    print(text["give_up"])
