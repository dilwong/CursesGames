import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

from random import randint
import time
from enum import Enum, auto

from collections import deque
from itertools import islice

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class Snake(deque):

    def __init__(self, *args, **kwargs):
        self.score = 0
        self.symbol = '#'

        self.up = KEY_UP
        self.down = KEY_DOWN
        self.left = KEY_LEFT
        self.right = KEY_RIGHT

        self._direction = Direction.RIGHT

        super().__init__(*args, **kwargs)

    def addHead(self):
        self.appendleft(
            (
                self[0][0] + (self.direction == Direction.DOWN and 1) + (self.direction == Direction.UP and -1),
                self[0][1] + (self.direction == Direction.LEFT and -1) + (self.direction == Direction.RIGHT and 1)
            )
        )
    
    def removeTail(self):
        return self.pop()
    
    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if isinstance(value, Direction):
            self._direction = value
            return
        if value == self.up:
            self._direction = Direction.UP
        elif value == self.down:
            self._direction = Direction.DOWN
        elif value == self.left:
            self._direction = Direction.LEFT
        elif value == self.right:
            self._direction = Direction.RIGHT

class GameState():
    
    def __init__(self, window):
        self.window = window
        self.snakeList = []
        self.foodList = set()

        self.foodSymbol = 'o'

    def update_state(self, snake, key):

        self.window.addstr(0, 2, 'Score: ' + str(snake.score) + ' ')

        snake.direction = key
        snake.addHead()

        if (snake [0][0] == 0) or (snake[0][0] == height - 1) or (snake[0][1] == 0) or (snake[0][1] == width - 1):
            return False
        
        if snake[0] in islice(snake, 1, None):
            return False

        if snake[0] in self.foodList:
            self.foodList.remove(snake[0])
            snake.score += 1
            self.generateFood()
        else:
            last = snake.removeTail()
            self.window.addch(last[0], last[1], ' ')
        self.window.addch(snake[0][0], snake[0][1], snake.symbol)
        curses.flushinp()

        return True

    def generateFood(self):
        while True:
            candidateFood = (randint(1, (height - 2)), randint(1, (width - 2)))
            if candidateFood in self.foodList:
                continue
            for snake in self.snakeList:
                if candidateFood in snake:
                    continue
            break
        self.foodList.add(candidateFood)
        window.addch(candidateFood[0], candidateFood[1], self.foodSymbol)
        return candidateFood

if __name__ == '__main__':

    fps = 60
    frames_per_update = 6

    curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)

    height = 25
    width = 50
    window = curses.newwin(height, width, 0, 0)
    window.keypad(True)
    window.nodelay(True)
    window.border(0)
    window.addstr(0, width // 2 - 2, ' SNAKE ')
    
    gameState = GameState(window)
    initialSnake = [(height // 3, width // 4 + 2), (height // 3, width // 4 + 1), (height // 3, width // 4)]
    main_snake = Snake(initialSnake)
    gameState.snakeList.append(main_snake)
    gameState.generateFood()
    
    key = KEY_RIGHT
    score = 0
    frame = 0
    try:
        while key != 27:

            event = window.getch()
            key = key if event == -1 else event

            if frame % frames_per_update == 0:
                if not gameState.update_state(main_snake, key):
                    break

            time.sleep(1.0 / fps)
            frame += 1
    finally:
        window.nodelay(False)
        curses.curs_set(True)
        window.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        print("\nScore: " + str(main_snake.score))