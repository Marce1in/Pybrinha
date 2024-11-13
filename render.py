import os
from helpers import clean_clear_screen

def render_game(state):
    os.system("clear")

    while(True):
        if not state.empty():
            clean_clear_screen()
            render_frame(state.get())

def render_frame(state):
    sizeY = len(state)
    sizeX = len(state[0])

    print("╔" + "═" * (1 + sizeX * 2) + "╗")

    for row in range(sizeY):
        print("║", end=" ")
        for col in range(sizeX):
            print(f"{state[row][col]}", end=" ")
        print("║")

    print("╚" + "═" * (1 + sizeX * 2) + "╝")
