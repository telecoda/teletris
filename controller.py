# main controller to keep it all together

from models import *
from views import *

class Tetris(object):

    def __init__(self):

        # reset game
        self.new_game()

    def new_game(self):
        self.score = 0
        self.level = 1
        self.state = ALIVE

        self.board = Board()

        self.player = Player()

        # init game assets
        self.screen = GameScreen(self.board, self.player)

    def render(self):

        self.screen.render()

    def rotate(self):

        self.player.rotate()