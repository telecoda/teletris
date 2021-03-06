from constants import *

import os
import pygame
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

# functions to create our resources


def load_image(file):
    "loads an image"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    return surface.convert_alpha()


def load_font(file, size):
    "loads a font"
    file = os.path.join(main_dir, 'data', file)
    try:
        font = pygame.font.Font(file, size)
    except pygame.error:
        raise SystemExit('Could not load font "%s" %s' %
                         (file, pygame.get_error()))
    return font


class GameScreen(object):

    def __init__(self, game):

        self.game = game
        self.screen = pygame.display.set_mode(
            (BOARD_WIDTH * BLOCK_PIXELS + INFO_PANEL_WIDTH, BOARD_HEIGHT * BLOCK_PIXELS))
        self.board = game.board
        self.player = game.player
        self.init_assets()
        self.clock = pygame.time.Clock()

        self.fading_blocks = []

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

        self.images[GAME_BACKGROUND] = load_image('space_background.jpg')

        self.fading_images = {}
        self.fading_images[9] = load_image('white_block_10.png')
        self.fading_images[8] = load_image('white_block_20.png')
        self.fading_images[7] = load_image('white_block_30.png')
        self.fading_images[6] = load_image('white_block_40.png')
        self.fading_images[5] = load_image('white_block_50.png')
        self.fading_images[4] = load_image('white_block_60.png')
        self.fading_images[3] = load_image('white_block_70.png')
        self.fading_images[2] = load_image('white_block_80.png')
        self.fading_images[1] = load_image('white_block_90.png')
        self.fading_images[0] = load_image('white_block_100.png')
        self.font_16 = load_font('space age.ttf', 16)
        self.font_24 = load_font('space age.ttf', 24)
        self.font_36 = load_font('space age.ttf', 36)

    def add_fading_row(self, row):
        # create fading blocks for each row
        for x in range(1, BOARD_WIDTH - 1):
            self.fading_blocks.append(
                FadingBlock(self.screen, self.fading_images, x, row, 30))

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
        self.screen.blit(self.images[GAME_BACKGROUND], (0, 0))
        self.render_blocks()
        self.render_fading_blocks()
        self.render_player()
        self.clock.tick()

    def render_info_panel(self):
        # render grey block border
        for x in range(0, BOARD_WIDTH - 1):
            self.render_block_at(BOARD_WIDTH + x, 0, GREY)
            self.render_block_at(BOARD_WIDTH + x, BOARD_HEIGHT - 1, GREY)
        for y in range(1, BOARD_HEIGHT - 1):
            self.render_block_at((BOARD_WIDTH * 2) - 2, y, GREY)

        if pygame.font:

            panel_edge_x = BOARD_WIDTH * BLOCK_PIXELS
            panel_centre_x = BOARD_WIDTH * \
                BLOCK_PIXELS + INFO_PANEL_WIDTH / 2 - BLOCK_PIXELS / 2

            x = panel_centre_x
            y = 25
            # title
            self.render_shadow_text(
                self.font_36, GAME_TITLE, x, y, (255, 0, 0), -2)

            y += 40
            self.render_shadow_text(
                self.font_16, "by @telecoda", x, y, (255, 255, 0), -2)

            # score
            y += 40
            score = 'Score: %d' % self.game.score
            self.render_shadow_text(
                self.font_24, score, panel_edge_x + 10, y, (255, 255, 255), -2, LEFT)

            # level
            y += 40
            level = 'Level: %d' % self.game.level
            self.render_shadow_text(
                self.font_24, level, panel_edge_x + 10, y, (255, 255, 255), -2, LEFT)

            y += 40
            top_scores_title = 'Top %d scores' % len(self.game.high_scores)
            self.render_shadow_text(
                self.font_24, top_scores_title, panel_centre_x + 10, y, (0, 255, 0), -2, CENTRE)

            scores = [30, 20, 10, 5, 2, 1, 1, 1, 1, 1]

            i = 0
            for score in self.game.high_scores:
                i += 1
                y += 30
                score_str = '%d. %06d' % (i, score)
                self.render_shadow_text(
                    self.font_24, score_str, panel_centre_x - 100, y, (255, 0, 0), -2, LEFT)

            next = 'Next:'
            self.render_shadow_text(
                self.font_24, next, panel_edge_x + 10, (BOARD_HEIGHT - 4) * BLOCK_PIXELS, (255, 255, 255), -2, LEFT)

            # next block
            self.render_next_shape(
                BOARD_WIDTH + 4, (BOARD_HEIGHT - 4))

    def render_shadow_text(self, font, text, x, y, colour, shadow_offset=-2, align=CENTRE):
        surface = font.render(text, 1, (0, 0, 0))

        # default to top left , no offset
        x_offset = 0
        y_offset = 0

        if align == CENTRE:
            # calc x offset
            x_offset = - surface.get_width() / 2
        elif align == LEFT:
            x_offset = 0
        elif align == RIGHT:
            x_offset = - surface.get_width()

        self.screen.blit(surface, (x + x_offset, y + y_offset))

        surface = font.render(text, 1, colour)
        self.screen.blit(
            surface, (x + x_offset - shadow_offset, y + y_offset - shadow_offset))

    def render_game_over_menu(self):
        self.render_alert_text("Game Over")
        self.render_alert_text(
            "press SPACE to play again", y_offset=40)

    def render_pause_menu(self):
        self.render_alert_text("Paused")
        self.render_alert_text("press SPACE to resume", y_offset=40)

    def render_start_menu(self):

        self.render_alert_text("Press SPACE to start")

    def render_alert_text(self, text, colour=(255, 255, 0), y_offset=0):
        if pygame.font:
            screen_centre_x = (
                BOARD_WIDTH * BLOCK_PIXELS) - BLOCK_PIXELS
            screen_centre_y = (
                BOARD_HEIGHT / 2) * BLOCK_PIXELS - BLOCK_PIXELS

            x = screen_centre_x
            y = screen_centre_y
            self.render_shadow_text(
                self.font_36, text, x, y + y_offset, colour, -2, CENTRE)

    def render_blocks(self):
        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                block = self.board.cells[x][y]
                self.render_block(block)

    def render_fading_blocks(self):
        for block in self.fading_blocks:
            if block.render():
                # remove block
                self.fading_blocks.remove(block)

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

    def render_next_shape(self, x_block, y_block):
        # render player shape
        blocks = self.player.get_next_shape_blocks()
        if blocks is not None:
            for block in blocks:
                # shape is composed of blocks, all blocks are relative to
                # players position
                self.render_block_at(
                    x_block + block.x, y_block + block.y, block.colour)


class FadingBlock(object):
    def __init__(self, screen, images, x, y, fade_speed):
        self.screen = screen
        self.images = images
        self.fade_speed = fade_speed
        self.current_frame = 0
        self.opacity = 0
        self.x = x * BLOCK_PIXELS
        self.y = y * BLOCK_PIXELS

    def render(self):
        """
        Returns True is fading is complete
        """
        self.current_frame += 1
        if self.current_frame >= self.fade_speed:
            self.opacity += 1

        if self.opacity < 0 or self.opacity > len(self.images) - 1:
            return True

        self.screen.blit(self.images[self.opacity], (self.x, self.y))
        return False
