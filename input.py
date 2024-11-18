from queue import Queue
from getkey import getkey, keys

def listen_input(input_queue: Queue, shutdown_queue: Queue):
    key_maps = {
        keys.UP:    "u",
        keys.DOWN:  "d",
        keys.LEFT:  "l",
        keys.RIGHT: "r",

        keys.LATIN_SMALL_LETTER_W: "u",
        keys.LATIN_SMALL_LETTER_S: "d",
        keys.LATIN_SMALL_LETTER_D: "r",
        keys.LATIN_SMALL_LETTER_A: "l",

        keys.LATIN_SMALL_LETTER_Q: -1
    }

    forbidden_keys_sequence = {
        keys.UP:    keys.DOWN,
        keys.DOWN:  keys.UP,
        keys.LEFT:  keys.RIGHT,
        keys.RIGHT: keys.LEFT,

        keys.LATIN_SMALL_LETTER_W: keys.LATIN_SMALL_LETTER_S,
        keys.LATIN_SMALL_LETTER_S: keys.LATIN_SMALL_LETTER_W,
        keys.LATIN_SMALL_LETTER_D: keys.LATIN_SMALL_LETTER_A,
        keys.LATIN_SMALL_LETTER_A: keys.LATIN_SMALL_LETTER_D,
    }

    previous_key = None

    while shutdown_queue.empty():
        key = getkey()

        if key == previous_key:
            continue
        elif forbidden_keys_sequence.get(previous_key, None) == key:
            continue
        elif key in key_maps:
            input_queue.put(key_maps[key])
            previous_key = key
