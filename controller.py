# main controller to keep it all together

from models import *
from views import *

class Tetris(object):

	def __init__(self):

		# init game models
		self.board = Board()

		# init game assets
		self.screen = GameScreen(self.board)

	def render(self):

		self.screen.render()