# The summer holiday, and then i cant't use the codeskulptor.So these are in my mind!--!

import simplegui
import random

WIDTH = 1600  # for 16 cards
HEIGHT = 150
memory = list((range(0, 8)))
memory.extend(range(0, 8))
state = 0
turns = -1


def init_exposed():
    global exposed, WIDTH, paired
    exposed = [False in range(0, WIDTH / 100)]
    paired = [-1, -1]  # for pairing!


def new_game():
    global state, memory, turns
    init_exposed()
    random.shuffle(memory)
    state = 0
    turns = -1


def estimate():  # state judging!
    global state
    if state == 0:
        state = 1
    elif state == 1:
        state = 2
    else:
        state = 1


def run_button():
    global frame
    init_exposed()
    frame.start()


def reset_button():
    new_game()


def mouseclick(pos):
    global turns, paired, exposed, l
    estimate()
    if 0 <= pos[1] <= 150 and 0 <= pos[0] <= 1600:
        clicked = pos[0] // 100
    else:
        return
    if turns == clicked:
        pass
    elif state == 1 and paired[0] == -1 and paired[1] == -1:
        turns = clicked
        paired[0] = turns
        exposed[turns] = True
    elif state == 1 and paired[0] != -1 and paired[1] == -1:
        turns = clicked
        paired[1] = turns
        exposed[turns] = True
    elif state == 1 and memory[paired[0]] == memory[paired[1]]:
        paired[1] = -1
        turns = clicked
        paired[0] = turns
        exposed[turns] = True
    elif state == 1 and memory[paired[0]] != memory[paired[1]]:
        exposed[paired[0]] = False
        exposed[paired[1]] = False
        paired[1] = -1
        turns = clicked
        paired[0] = turns
        exposed[turns] = True
    elif state == 2:
        turns = clicked
        paired[1] = turns
        exposed[turns] = True
    l.set_text('Turns = ' + turns)


def draw(canvas):
    i = 0
    for number in memory:
        assert i <= 15, 'OutOfBoundsError'  # prevent i from crossing the border
        if exposed[i]:
            canvas.draw_text(number, [30 + 100 * i, 75], 24, 'White')
        else:
            canvas.draw_polygon([(100 * i, 0), (100 * (i + 1), 0), (100 * (i + 1), 150), (100 * i, 150)], 12, 'Red',
                                'Green')
        i += 1


frame = simplegui.create_frame('Memory', WIDTH, HEIGHT)
frame.add_button('Run', run_button, 100)
frame.add_button('Reset', reset_button, 100)
l = frame.add_label('Turns = ?')
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
