r'''
Snake

Use the keyboard arrow keys to control the direction of the snake.
Collect food to grow.
Don't run into yourself or the boundaries of the game.
'''

# TO DO: Implement multiple snakes for multiplayer

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

from random import randint
import time
from enum import Enum, auto

from collections import deque
from itertools import islice

# Direction of Snake's velocity
class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class Snake(deque):

    r'''
    A Snake object initialized by a list of tuples (y: int, x: int) indicating the positions of the
    segments of its body in 2D space. The first tuple in the list is the head of the Snake.
    '''

    def __init__(self, *args, **kwargs):
        self.score = 0
        self.symbol = '#' # Character used to indicate the body of the Snake

        self.up = KEY_UP
        self.down = KEY_DOWN
        self.left = KEY_LEFT
        self.right = KEY_RIGHT

        self._direction = Direction.RIGHT # The Snake's initial direction

        super().__init__(*args, **kwargs)

    def addHead(self):
        r'''
        Add a new head to the Snake in the current direction of motion.
        '''
        self.appendleft(
            (
                self[0][0] + (self.direction == Direction.DOWN and 1) + (self.direction == Direction.UP and -1),
                self[0][1] + (self.direction == Direction.LEFT and -1) + (self.direction == Direction.RIGHT and 1)
            )
        )
    
    def removeTail(self):
        r'''
        Remove the last segment of the Snake and return it.
        '''
        return self.pop()
    
    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        r'''
        Set the direction of the Snake based on the keypress event 'value'.
        '''
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
        self.snakeList = [] # List of all Snake objects
        self.foodList = set() # List of food items currently on screen

        self.foodSymbol = 'o' # Character used to depict a food item

    def update_state(self, snake):

        r'''
        Update the state of snake by adding a new head in the direction of motion and removing the tail.
        If the snake collides with itself of the boundaries of the game, return False. Otherwise, return True.

        If the snake's head collides with a food item, increment the snake's score by 1, and delete the food item.
        Then generate a new food item at a random location.
        '''

        # The score is displayed in the upper-left corner.
        # This needs to be changed to implement multiple snakes.
        self.window.addstr(0, 2, 'Score: ' + str(snake.score) + ' ')

        snake.addHead()

        # If the snake collides with the boundaries of the game, return False.
        # TO DO: Implement a topological torus game stage, i.e, the snake's head warps to the opposite boundary.
        if (snake [0][0] == 0) or (snake[0][0] == height - 1) or (snake[0][1] == 0) or (snake[0][1] == width - 1):
            return False
        
        # If the head of the snake is equal to any other part of its body, return False.
        # TO DO: Implement collisions with other Snake objects.
        if snake[0] in islice(snake, 1, None):
            return False

        if snake[0] in self.foodList: # If the snake encounters food.
            self.foodList.remove(snake[0])
            snake.score += 1
            self.generateFood()
        else: # If the snake does not encounter food.
            last = snake.removeTail()
            self.window.addch(last[0], last[1], ' ')
        self.window.addch(snake[0][0], snake[0][1], snake.symbol)
        curses.flushinp()

        return True

    def generateFood(self):
        r'''
        Randomly generate a food item, and draw it on the screen.
        This method will not generate a food item that overlaps with a Snake object or another food item.
        '''
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
    initialBody = [
        (height // 3, width // 4 + 2),
        (height // 3, width // 4 + 1),
        (height // 3, width // 4)
    ] # The initial location of the snake.
    main_snake = Snake(initialBody) # Player 1 snake
    gameState.snakeList.append(main_snake)
    gameState.generateFood()
    
    key = -1
    score = 0
    frame = 0
    try:
        while key != 27: # Press ESC to quit the game.

            # Set the direction of motion of the snakes based on keypress.
            key = window.getch()
            for snake in gameState.snakeList:
                snake.direction = key

            # Every frames_per_update frames, update the state of each snake and redraw them.
            # If any gameState.update_state(snake) return False because it collided with something,
            # break the loop and end the game.
            if frame % frames_per_update == 0:
                if any(not gameState.update_state(snake) for snake in gameState.snakeList):
                    break

            # TO DO: Implement a speed up when the snakes get longer...
            time.sleep(1.0 / fps)
            frame += 1
            frame = frame % frames_per_update
    finally:
        window.nodelay(False)
        curses.curs_set(True)
        window.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        # Print the score.
        # This is for one snake, and needs to be modified for multiple snakes.
        print("\nScore: " + str(main_snake.score))