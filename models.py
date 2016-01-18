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

    # reset board to empty blocks
    def reset_board(self):
        # fill with blank cells
        self.cells = [[Block(x,y,EMPTY) for y in range(BOARD_HEIGHT)] for x in range(BOARD_WIDTH)]

        # add grey surrounding blocks
        y = 0
        for x in range(0,BOARD_WIDTH):
            self.cells[x][y] = Block(x,y,GREY)
        y = BOARD_HEIGHT -1
        for x in range(0,BOARD_WIDTH):
            self.cells[x][y] = Block(x,y,GREY)
        x = 0
        for y in range(0,BOARD_HEIGHT):
            self.cells[x][y] = Block(x,y,GREY)
        x = BOARD_WIDTH -1
        for y in range(0,BOARD_HEIGHT):
            self.cells[x][y] = Block(x,y,GREY)


class Player(object):

    def __init__(self):
        
        self.x = 5
        self.y = 5
        #self.shape = SquareShape(RED)
        #self.shape = LeftLShape(YELLOW)
        #self.shape = RightLShape(GREEN)
        #self.shape = BarShape(CYAN)
        #self.shape = LeftStepShape(MAGENTA)
        self.shape = RightStepShape(GREY)

    def get_shape_blocks(self):
        # gets a rotated version of a shape
        return self.shape.get_blocks()

    def move_down(self):
        self.y += 1

    def rotate(self):
        self.shape.rotate()

class Shape(object):

    def __init__(self,colour):
        # each shape can have up to 4 different view when it rotates
        self.views = []
        self.view_index = 0
        self.visible = False

    def rotate(self):
        self.view_index += 1
        if self.view_index > len(self.views) -1:
            self.view_index = 0

    def get_blocks(self):
        return self.views[self.view_index]


class SquareShape(Shape):

    def __init__(self,colour):
        Shape.__init__(self,colour) #call Shape intializer

        # square only has one view
        self.views.append(
            (
                Block(0,0,colour),
                Block(1,0,colour),
                Block(0,1,colour),
                Block(1,1,colour)
            )
        )

class BarShape(Shape):

    def __init__(self,colour):
        Shape.__init__(self,colour) #call Shape intializer

        # view 0
        self.views.append(
            (
                Block(0,3,colour),
                Block(1,3,colour),
                Block(2,3,colour),
                Block(3,3,colour)
            )
        )
        # view 1
        self.views.append(
            (
                Block(2,0,colour),
                Block(2,1,colour),
                Block(2,2,colour),
                Block(2,3,colour)
            )
        )

class LeftLShape(Shape):

    def __init__(self,colour):
        Shape.__init__(self,colour) #call Shape intializer

        # view 0
        self.views.append(
            (
                Block(0,0,colour),
                Block(1,0,colour),
                Block(2,0,colour),
                Block(2,1,colour)
            )
        )
        # view 1
        self.views.append(
            (
                Block(2,0,colour),
                Block(2,1,colour),
                Block(2,2,colour),
                Block(1,2,colour)
            )
        )
        # view 2
        self.views.append(
            (
                Block(0,2,colour),
                Block(1,2,colour),
                Block(2,2,colour),
                Block(0,1,colour)
            )
        )
        # view 3
        self.views.append(
            (
                Block(0,0,colour),
                Block(0,1,colour),
                Block(0,2,colour),
                Block(1,0,colour)
            )
        )

class RightLShape(Shape):

    def __init__(self,colour):
        Shape.__init__(self,colour) #call Shape intializer

        # view 0
        self.views.append(
            (
                Block(0,0,colour),
                Block(1,0,colour),
                Block(2,0,colour),
                Block(0,1,colour)
            )
        )
        # view 1
        self.views.append(
            (
                Block(2,0,colour),
                Block(2,1,colour),
                Block(2,2,colour),
                Block(1,0,colour)
            )
        )
        # view 2
        self.views.append(
            (
                Block(0,2,colour),
                Block(1,2,colour),
                Block(2,2,colour),
                Block(2,1,colour)
            )
        )
        # view 3
        self.views.append(
            (
                Block(0,0,colour),
                Block(0,1,colour),
                Block(0,2,colour),
                Block(1,2,colour)
            )
        )

class LeftStepShape(Shape):

    def __init__(self,colour):
        Shape.__init__(self,colour) #call Shape intializer

        # view 0
        self.views.append(
            (
                Block(0,2,colour),
                Block(1,2,colour),
                Block(1,1,colour),
                Block(2,1,colour)
            )
        )
        # view 1
        self.views.append(
            (
                Block(0,0,colour),
                Block(0,1,colour),
                Block(1,1,colour),
                Block(1,2,colour)
            )
        )

class RightStepShape(Shape):

    def __init__(self,colour):
        Shape.__init__(self,colour) #call Shape intializer

        # view 0
        self.views.append(
            (
                Block(0,1,colour),
                Block(1,1,colour),
                Block(1,2,colour),
                Block(2,2,colour)
            )
        )
        # view 1
        self.views.append(
            (
                Block(0,2,colour),
                Block(0,1,colour),
                Block(1,1,colour),
                Block(1,0,colour)
            )
        )

