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

    print game.board.cells[0][0]
    running = True

    while running:
        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        game.render()

if __name__ == "__main__":
    main()
