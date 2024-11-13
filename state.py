import time
import random
import queue

def game_state(state_q: queue.Queue, input_q: queue.Queue):

    cur_state: list[list[str]] = state_q.get()
    size_y: int = len(cur_state)
    size_x: int = len(cur_state[0])

    head: list[int] = [size_y // 2, size_x // 2]
    buffer: list[list[int]] = [head]
    snake_size: int = 3

    update_head(cur_state, head, "v")
    state_q.put(cur_state)

    input_current: int = input_q.get()
    generate_fruit(cur_state, size_x, size_y)

    while(True):
        time.sleep(0.1)

        if not input_q.empty():
            input_current = input_q.get()

        if not state_q.empty():
            cur_state = state_q.get()

        if snake_size <= len(buffer):
            update_tail(cur_state, buffer)


        match input_current:
            case 0:
                update_head(cur_state, head, "o")
                buffer.append(head.copy())

                head[0] -= 1
                if (tile_have_fruit(cur_state, head)):
                    snake_size += 1
                    generate_fruit(cur_state, size_x, size_y)

                update_head(cur_state, head, "ʌ")
                state_q.put(cur_state)
            case 1:
                update_head(cur_state, head, "o")
                buffer.append(head.copy())

                head[0] += 1
                if (tile_have_fruit(cur_state, head)):
                    snake_size += 1
                    generate_fruit(cur_state, size_x, size_y)

                update_head(cur_state, head, "v")
                state_q.put(cur_state)
            case 2:
                update_head(cur_state, head, "o")
                buffer.append(head.copy())

                head[1] -= 1
                if (tile_have_fruit(cur_state, head)):
                    snake_size += 1
                    generate_fruit(cur_state, size_x, size_y)

                update_head(cur_state, head, "<")
                state_q.put(cur_state)
            case 3:
                update_head(cur_state, head, "o")
                buffer.append(head.copy())

                head[1] += 1
                if (tile_have_fruit(cur_state, head)):
                    snake_size += 1
                    generate_fruit(cur_state, size_x, size_y)

                update_head(cur_state, head, ">")
                state_q.put(cur_state)

def update_head(state: list[list[str]], head: list[int], char: str):
    state[head[0]][head[1]] = char

def update_tail(state: list[list[str]], buffer):
    tail = buffer.pop(0)
    state[tail[0]][tail[1]] = " "

def generate_fruit(state: list[list[str]], size_x: int, size_y: int):
    rand_x = random.randint(0, size_x - 1)
    rand_y = random.randint(0, size_y - 1)

    if tile_is_busy(state, [rand_y, rand_x]):
        generate_fruit(state, size_x, size_y)
    else:
        state[rand_y][rand_x] = "@"

def tile_have_fruit(state: list[list[str]], head: list[int]) -> bool:
    if (state[head[0]][head[1]] == "@"):
        return True
    else:
        return False

def tile_is_busy(state: list[list[str]], head: list[int]) -> bool:
    if (state[head[0]][head[1]] == " "):
        return False
    else:
        return True
