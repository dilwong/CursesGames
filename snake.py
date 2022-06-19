# Heavily inspired by:
# https://levelup.gitconnected.com/build-a-snake-game-in-python-in-under-50-lines-of-code-faed4bfc5acf
# https://twitter.com/eigenbom/status/734234895883456514

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
import time 

fps = 60
frames_per_update = 6

curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(False)

window = curses.newwin(30, 60, 0, 0)
window.keypad(True)
window.nodelay(True)
window.border(0)

window.addstr(0, 27, 'SNAKE! ')

key = KEY_RIGHT
score = 0

first_food = (10,25)
food = set()
food.add(first_food)
window.addch(first_food[0], first_food[1], 'O')

class Snake(list):

    def __init__(self, *args, **kwargs):
        self.score = 0
        super().__init__(*args, **kwargs)

main_snake = Snake([(5,8), (5,7), (5,6)])

def update_state(snake, food, key):
    window.addstr(0, 2, 'Score: ' + str(snake.score) + ' ')

    snake.insert(0, (snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)))

    if snake [0][0] == 0 or snake[0][0] == 29 or snake[0][1] == 0 or  snake[0][1] == 59:
        return None
    
    if snake[0] in snake[1:]:
        return None

    if snake[0] in food:
        food.remove(snake[0])
        snake.score += 1
        while len(food) == 0:
            new_food = (randint(1, 28), randint(1, 58))
            if new_food not in snake:
                food.add(new_food)
        window.addch(new_food[0], new_food[1], 'O')
        food.add(new_food)
    else:
        last = snake.pop()
        window.addch(last[0], last[1], ' ')
    window.addch(snake[0][0], snake[0][1], '#')
    curses.flushinp()

    return 1

frame = 0
while key != 27:

    event = window.getch()
    key = key if event == -1 else event

    if frame % frames_per_update == 0:
        status = update_state(main_snake, food, key)
        if status is None:
            break

    time.sleep(1.0 / fps)
    frame += 1

window.nodelay(False)
curses.curs_set(True)
window.keypad(False)
curses.nocbreak()
curses.echo()
curses.endwin()
print("\nScore: " + str(main_snake.score))