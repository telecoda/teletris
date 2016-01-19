# block.py

import random
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


class Player(object):

    def __init__(self):

        self.x = 6
        self.y = 3
        # self.shape = SquareShape(RED)
        # self.shape = LeftLShape(YELLOW)
        # self.shape = RightLShape(GREEN)
        # self.shape = BarShape(CYAN)
        # self.shape = LeftStepShape(MAGENTA)
        # self.shape = RightStepShape(GREY)

        self.shape = None

    def get_shape_blocks(self):
        # gets a rotated version of a shape
        if self.shape is not None:
            return self.shape.get_blocks()
        return None

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def rotate(self):
        self.shape.rotate()

    def set_random_shape(self):
        colour = random.choice(BLOCK_COLOURS)
        shape_type = random.choice(SHAPE_TYPES)

        if shape_type == SQUARE:
            self.shape = SquareShape(colour)
            print 'square'
        elif shape_type == BAR:
            self.shape = BarShape(colour)
            print 'bar'
        elif shape_type == LEFT_L:
            self.shape = LeftLShape(colour)
            print 'left L'
        elif shape_type == RIGHT_L:
            self.shape = RightLShape(colour)
            print 'right L'
        elif shape_type == LEFT_STEP:
            self.shape = LeftStepShape(colour)
            print 'left step'
        elif shape_type == RIGHT_STEP:
            self.shape = RightStepShape(colour)
            print 'right step'

        # position at top middle of board
        self.x = 6
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
