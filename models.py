# block.py

import random
import pygame
from constants import *


class Block(object):

    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour

    def __str__(self):
        return 'x: %d y: %d colour: %d' % (self.x, self.y, self.colour)


class Board(object):

    def __init__(self):
        self.reset_board()

    # reset board to empty blocks
    def reset_board(self):
        # fill with blank cells
        self.cells = [
            [Block(x, y, EMPTY) for y in range(BOARD_HEIGHT)] for x in range(BOARD_WIDTH)]

        # add grey surrounding blocks
        y = 0
        for x in range(0, BOARD_WIDTH):
            self.cells[x][y] = Block(x, y, GREY)
        y = BOARD_HEIGHT - 1
        for x in range(0, BOARD_WIDTH):
            self.cells[x][y] = Block(x, y, GREY)
        x = 0
        for y in range(0, BOARD_HEIGHT):
            self.cells[x][y] = Block(x, y, GREY)
        x = BOARD_WIDTH - 1
        for y in range(0, BOARD_HEIGHT):
            self.cells[x][y] = Block(x, y, GREY)

    def can_player_fit_at(self, player, x, y):
        """
        Check if player's shape can move down one row
        without colliding into any other blocks
        """

        blocks = player.get_shape_blocks()
        if blocks is None:
            return False

        for block in blocks:
            # check board is empty for all blocks
            block_x = x + block.x
            block_y = y + block.y
            if self.cells[block_x][block_y].colour is not EMPTY:
                return False

        return True

    def add_shape_to_board(self, player):
        """
        Shape has collided so add it to the permanent board
        """

        blocks = player.get_shape_blocks()
        if blocks is None:
            return

        for block in blocks:
            # check board is empty for all blocks
            block_x = player.x + block.x
            block_y = player.y + block.y
            block.x = block_x
            block.y = block_y
            self.cells[block_x][block_y] = block

    def check_complete_rows(self):
        """
        Check if there are any complete rows 
        """

        full_rows = []

        # remember to ignore first and last grey rows
        for y in range(1, BOARD_HEIGHT - 1):
            row_full = True
            # remember to ignore first and last grey columns
            for x in range(1, BOARD_WIDTH - 1):
                if self.cells[x][y].colour is EMPTY:
                    row_full = False

            if row_full:
                full_rows.append(y)

        if len(full_rows) > 0:
            # publish it
            event = pygame.event.Event(ROWS_COMPLETE_EVENT)
            event.dict['rows'] = full_rows
            pygame.event.post(event)

    def destroy_rows(self, rows):
        """
        This method destroys ALL rows passed in the list
        then readjusts the board to account for the destroyed rows
        """

        # give a list of rows to destroy
        # the rows must be remove and the remaining rows adjusted
        # and the the board must be refilled
        for y in range(1, BOARD_HEIGHT - 1):
            if y in rows:
                # this is a row to destroy
                # move all rows above it down 1 row
                self.move_row_down(y)

    def move_row_down(self, last_row):

        first_row = 1

        for y in range(last_row, first_row, -1):
            for x in range(1, BOARD_WIDTH - 1):
                # copy from row above
                self.cells[x][y] = self.cells[x][y - 1]
                # reset coords
                self.cells[x][y].x = x
                self.cells[x][y].y = y

        # blank top row
        for x in range(1, BOARD_WIDTH - 1):
            self.cells[x][1] = Block(x, 1, EMPTY)


class Player(object):

    def __init__(self):

        self.x = BOARD_WIDTH / 2
        self.y = 2

        self.shape = None
        self.next_shape = None

    def get_shape_blocks(self):
        # gets a rotated version of a shape
        if self.shape is not None:
            return self.shape.get_blocks()
        return None

    def get_next_shape_blocks(self):
        if self.next_shape is not None:
            return self.next_shape.get_blocks()
        return None

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def rotate(self):
        self.shape.rotate()

    def rotate_back(self):
        self.shape.rotate_back()

    def set_next_random_shape(self):

        # copy next_shape
        self.shape = self.next_shape
        colour = random.choice(BLOCK_COLOURS)
        shape_type = random.choice(SHAPE_TYPES)

        if shape_type == SQUARE:
            self.next_shape = SquareShape(colour)
        elif shape_type == BAR:
            self.next_shape = BarShape(colour)
        elif shape_type == LEFT_L:
            self.next_shape = LeftLShape(colour)
        elif shape_type == RIGHT_L:
            self.next_shape = RightLShape(colour)
        elif shape_type == LEFT_STEP:
            self.next_shape = LeftStepShape(colour)
        elif shape_type == RIGHT_STEP:
            self.next_shape = RightStepShape(colour)

        # position at top middle of board
        self.x = BOARD_WIDTH / 2
        self.y = 2


class Shape(object):

    def __init__(self, colour):
        # each shape can have up to 4 different view when it rotates
        self.views = []
        self.view_index = 0
        self.visible = False

    def rotate(self):
        self.view_index += 1
        if self.view_index > len(self.views) - 1:
            self.view_index = 0

    def rotate_back(self):
        self.view_index -= 1
        if self.view_index < 0:
            self.view_index = len(self.views) - 1

    def get_blocks(self):
        return self.views[self.view_index]


class SquareShape(Shape):

    def __init__(self, colour):
        Shape.__init__(self, colour)  # call Shape intializer

        # square only has one view
        self.views.append(
            (
                Block(0, 0, colour),
                Block(1, 0, colour),
                Block(0, 1, colour),
                Block(1, 1, colour)
            )
        )


class BarShape(Shape):

    def __init__(self, colour):
        Shape.__init__(self, colour)  # call Shape intializer

        # view 0
        self.views.append(
            (
                Block(0, 3, colour),
                Block(1, 3, colour),
                Block(2, 3, colour),
                Block(3, 3, colour)
            )
        )
        # view 1
        self.views.append(
            (
                Block(2, 0, colour),
                Block(2, 1, colour),
                Block(2, 2, colour),
                Block(2, 3, colour)
            )
        )


class LeftLShape(Shape):

    def __init__(self, colour):
        Shape.__init__(self, colour)  # call Shape intializer

        # view 0
        self.views.append(
            (
                Block(0, 0, colour),
                Block(1, 0, colour),
                Block(2, 0, colour),
                Block(2, 1, colour)
            )
        )
        # view 1
        self.views.append(
            (
                Block(2, 0, colour),
                Block(2, 1, colour),
                Block(2, 2, colour),
                Block(1, 2, colour)
            )
        )
        # view 2
        self.views.append(
            (
                Block(0, 2, colour),
                Block(1, 2, colour),
                Block(2, 2, colour),
                Block(0, 1, colour)
            )
        )
        # view 3
        self.views.append(
            (
                Block(0, 0, colour),
                Block(0, 1, colour),
                Block(0, 2, colour),
                Block(1, 0, colour)
            )
        )


class RightLShape(Shape):

    def __init__(self, colour):
        Shape.__init__(self, colour)  # call Shape intializer

        # view 0
        self.views.append(
            (
                Block(0, 0, colour),
                Block(1, 0, colour),
                Block(2, 0, colour),
                Block(0, 1, colour)
            )
        )
        # view 1
        self.views.append(
            (
                Block(2, 0, colour),
                Block(2, 1, colour),
                Block(2, 2, colour),
                Block(1, 0, colour)
            )
        )
        # view 2
        self.views.append(
            (
                Block(0, 2, colour),
                Block(1, 2, colour),
                Block(2, 2, colour),
                Block(2, 1, colour)
            )
        )
        # view 3
        self.views.append(
            (
                Block(0, 0, colour),
                Block(0, 1, colour),
                Block(0, 2, colour),
                Block(1, 2, colour)
            )
        )


class LeftStepShape(Shape):

    def __init__(self, colour):
        Shape.__init__(self, colour)  # call Shape intializer

        # view 0
        self.views.append(
            (
                Block(0, 2, colour),
                Block(1, 2, colour),
                Block(1, 1, colour),
                Block(2, 1, colour)
            )
        )
        # view 1
        self.views.append(
            (
                Block(0, 0, colour),
                Block(0, 1, colour),
                Block(1, 1, colour),
                Block(1, 2, colour)
            )
        )


class RightStepShape(Shape):

    def __init__(self, colour):
        Shape.__init__(self, colour)  # call Shape intializer

        # view 0
        self.views.append(
            (
                Block(0, 1, colour),
                Block(1, 1, colour),
                Block(1, 2, colour),
                Block(2, 2, colour)
            )
        )
        # view 1
        self.views.append(
            (
                Block(0, 2, colour),
                Block(0, 1, colour),
                Block(1, 1, colour),
                Block(1, 0, colour)
            )
        )
