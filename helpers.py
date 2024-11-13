import os

def clear_screen():
    # For some reason if I print something before clearing the screen,
    # the screen does not flicker, idk why
    print("")

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def clean_clear_screen():
    print("\033[H\033[1J", end="")



