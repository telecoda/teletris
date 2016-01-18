#!/usr/bin/env python2

"""
Teletris - by @telecoda

An experiment in learning pygame

"""

import pygame
from pygame.locals import *

from constants import *
from controller import *

def main():
    """
    Main routine and main loop
    """
    # Initialize Everything
    pygame.init()

    pygame.display.set_caption(GAME_TITLE)
    pygame.mouse.set_visible(0)

    game = Tetris()
    game.new_game()
    game.run()


if __name__ == "__main__":
    main()
