import os
from helpers import clean_clear_screen
from queue import Queue

def render_game(state: Queue, shutdown: Queue):
    os.system("clear")

    while shutdown.empty():
        if not state.empty():
            clean_clear_screen()

            frame = state.get()
            render_frame(frame)

def render_frame(frame):
    score = frame["score"] * 100
    grid = frame["grid"]

    sizeY = len(grid)
    sizeX = len(grid[0])

    print(f"\nScore: {score:010d}")
    print("╔" + "═" * (1 + sizeX * 2) + "╗")

    for row in range(sizeY):
        print("║", end=" ")
        for col in range(sizeX):
            print(f"{grid[row][col]}", end=" ")
        print("║")

    print("╚" + "═" * (1 + sizeX * 2) + "╝")
    print(f"Press 'q' any time to give up")
