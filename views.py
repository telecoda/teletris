from constants import *

import os
import pygame
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

# functions to create our resources


def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    return surface.convert_alpha()


class GameScreen(object):

    def __init__(self, game):

        self.game = game
        self.screen = pygame.display.set_mode(
            (BOARD_WIDTH * BLOCK_PIXELS + INFO_PANEL_WIDTH, BOARD_HEIGHT * BLOCK_PIXELS))
        self.board = game.board
        self.player = game.player
        self.init_assets()
        self.clock = pygame.time.Clock()

    def init_assets(self):
        # this is where we load all the game assets
        self.images = {}
        self.images[RED] = load_image('red_block.png')
        self.images[BLUE] = load_image('blue_block.png')
        self.images[GREEN] = load_image('green_block.png')
        self.images[YELLOW] = load_image('yellow_block.png')
        self.images[MAGENTA] = load_image('magenta_block.png')
        self.images[CYAN] = load_image('cyan_block.png')
        self.images[GREY] = load_image('grey_block.png')

    # Rendered when @ playing state
    def render_game_playing(self):
        self.render_game_panel()
        self.render_info_panel()
        pygame.display.flip()

    # Rendered when @ paused state
    def render_game_paused(self):
        self.render_game_panel()
        self.render_info_panel()
        self.render_pause_menu()
        pygame.display.flip()

    # Rendered when @ game over state
    def render_game_over(self):
        self.render_game_panel()
        self.render_info_panel()
        self.render_game_over_menu()
        pygame.display.flip()

    # Rendered when @ menu state
    def render_menu(self):
        self.render_game_panel()
        self.render_info_panel()
        self.render_start_menu()
        pygame.display.flip()

    def render_game_panel(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))
        self.render_blocks()
        self.render_player()
        self.clock.tick()
        # print (self.clock.get_fps())

    def render_info_panel(self):
        if pygame.font:
            # title
            font = pygame.font.Font(None, 36)
            text = font.render("Teletris", 1, (255, 0, 0))
            x_offset = text.get_width() / 2
            y_offset = text.get_height() / 2

            panel_centre_x = BOARD_WIDTH * BLOCK_PIXELS + INFO_PANEL_WIDTH / 2
            self.screen.blit(text, (panel_centre_x - x_offset, y_offset))

            # score
            score = 'Score: %d' % self.game.score
            text = font.render(score, 1, (255, 0, 0))
            x_offset = text.get_width() / 2
            y_offset = text.get_height()
            self.screen.blit(text, (panel_centre_x - x_offset, y_offset * 2))

            # level
            level = 'Level: %d' % self.game.level
            text = font.render(level, 1, (255, 0, 0))
            x_offset = text.get_width() / 2
            y_offset = text.get_height()
            self.screen.blit(text, (panel_centre_x - x_offset, y_offset * 4))

    def render_game_over_menu(self):
        if pygame.font:
            # start menu
            font = pygame.font.Font(None, 36)
            text = font.render(
                "Game Over: press SPACE to play again", 1, (255, 255, 0))
            x_offset = text.get_width() / 2
            y_offset = text.get_height() / 2

            panel_centre_x = BOARD_WIDTH * BLOCK_PIXELS / 2
            panel_centre_y = BOARD_HEIGHT * BLOCK_PIXELS / 2
            self.screen.blit(
                text, (panel_centre_x - x_offset, panel_centre_y - y_offset))

    def render_pause_menu(self):
        if pygame.font:
            # start menu
            font = pygame.font.Font(None, 36)
            text = font.render(
                "Paused: press SPACE to resume", 1, (255, 255, 0))
            x_offset = text.get_width() / 2
            y_offset = text.get_height() / 2

            panel_centre_x = BOARD_WIDTH * BLOCK_PIXELS / 2
            panel_centre_y = BOARD_HEIGHT * BLOCK_PIXELS / 2
            self.screen.blit(
                text, (panel_centre_x - x_offset, panel_centre_y - y_offset))

    def render_start_menu(self):
        if pygame.font:
            # start menu
            font = pygame.font.Font(None, 36)
            text = font.render("Press SPACE to start", 1, (255, 255, 0))
            x_offset = text.get_width() / 2
            y_offset = text.get_height() / 2

            panel_centre_x = BOARD_WIDTH * BLOCK_PIXELS / 2
            panel_centre_y = BOARD_HEIGHT * BLOCK_PIXELS / 2
            self.screen.blit(
                text, (panel_centre_x - x_offset, panel_centre_y - y_offset))

    def render_blocks(self):
        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                block = self.board.cells[x][y]
                self.render_block(block)

    def render_block(self, block):
        self.render_block_at(block.x, block.y, block.colour)

    def render_block_at(self, x, y, colour):
        xCoord = x * BLOCK_PIXELS
        yCoord = y * BLOCK_PIXELS

        if colour == EMPTY:
            return

        self.screen.blit(self.images[colour], (xCoord, yCoord))

    def render_player(self):
        # render player shape
        blocks = self.player.get_shape_blocks()
        if blocks is not None:
            for block in blocks:
                # shape is composed of blocks, all blocks are relative to
                # players position
                self.render_block_at(
                    self.player.x + block.x, self.player.y + block.y, block.colour)
