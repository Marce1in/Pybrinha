from getkey import getkey, keys

def listen_input(input):
    while(True):
        key = getkey()
        if key == keys.UP:
            input.put(0)
        elif key == keys.DOWN:
            input.put(1)
        elif key == keys.LEFT:
            input.put(2)
        elif key == keys.RIGHT:
            input.put(3)
