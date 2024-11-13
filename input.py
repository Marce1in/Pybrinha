from getkey import getkey, keys

def listen_input(input):
    while(True):
        key = getkey()
        if key == keys.UP:
            input.put("u")
        elif key == keys.DOWN:
            input.put("d")
        elif key == keys.LEFT:
            input.put("l")
        elif key == keys.RIGHT:
            input.put("r")
