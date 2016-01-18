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
        self.state = MENU
        self.player_state = ALIVE

        self.board = Board()

        self.player = Player()

        # init game assets
        self.screen = GameScreen(self.board, self.player)

    def run(self):
        pygame.time.set_timer(BLOCK_DOWN_EVENT, 1000) # time in milliseconds

        print self.board.cells[0][0]
        running = True

        while running:
            # Handle Input Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False
                elif event.type == KEYDOWN and event.key == K_UP:
                    self.rotate()
                if event.type == BLOCK_DOWN_EVENT:
                    self.move_down()
            self.render()


    def render(self):

        if self.state == PLAYING:
            self.render_playing()
        elif self.state == PAUSED:
            self.render_paused()
        else:
            self.render_menu()

    def render_menu(self):
        self.screen.render_menu()

    def render_paused(self):
        self.screen.render_game_paused()

    def render_playing(self):
        self.screen.render_game_playing()

    def rotate(self):

        self.player.rotate()

    def move_down(self):

        self.player.move_down()
