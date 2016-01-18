from pygame.locals import *

GAME_TITLE = 'Tetris'

# Board constants
BOARD_WIDTH = 12
BOARD_HEIGHT = 22
BOARD_OFFSET_X = 32
BOARD_OFFSET_Y = 32
BLOCK_PIXELS = 32
INFO_PANEL_WIDTH = 300

# Block types
EMPTY = 0
RED = 1
GREEN = 2
BLUE = 3
YELLOW = 4
MAGENTA = 5
CYAN =6
GREY = 7

# Player states
DEAD = 0
ALIVE = 1

# Game states
MENU = 0
PLAYING = 1
PAUSED = 3

# Game events
BLOCK_DOWN_EVENT = USEREVENT + 1
