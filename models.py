# block.py

from constants import *





class Block(object):

    def __init__(self,x,y, colour):
        self.x = x
        self.y = y
        self.colour = colour
    def __str__(self):
        return 'x: %d y: %d colour: %d' % (self.x, self.y, self.colour)


class Board(object):

    def __init__(self):
        self.reset_board()

        self.cells[1][1].colour = RED
        self.cells[2][1].colour = BLUE
        self.cells[3][1].colour = GREEN
        self.cells[4][1].colour = YELLOW
        self.cells[5][1].colour = MAGENTA
        self.cells[6][1].colour = CYAN
        self.cells[7][1].colour = GREY

        self.square = SquareBlock(5,5,RED)

    # reset board to empty blocks
    def reset_board(self):
        self.cells = [[Block(x,y,EMPTY) for y in range(BOARD_HEIGHT)] for x in range(BOARD_WIDTH)]

class SquareBlock(Block):

    def __init__(self,x,y,colour):
        self.blocks = []
        self.blocks.extend(Block(x,y,colour))
        self.blocks.extend(Block(x+1,y,colour))
        self.blocks.extend(Block(x,y+1,colour))
        self.blocks.extend(Block(x+1,y+1,colour))

