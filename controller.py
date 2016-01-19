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
        self.screen = GameScreen(self)

    def start_game(self):
        self.state = PLAYING
        self.player.set_random_shape()
        pygame.time.set_timer(BLOCK_DOWN_EVENT, 1000) # time in milliseconds

    def pause_game(self):
        self.state = PAUSED

    def resume_game(self):
        self.state = PLAYING

    def run(self):

        print self.board.cells[0][0]
        quit = False

        while not quit:
            # Handle Input Events
            if self.state == PLAYING:
                quit = self.handle_playing_events()
            elif self.state == MENU:
                quit = self.handle_menu_events()
            elif self.state == PAUSED:
                quit = self.handle_paused_events()

            self.render()

    def handle_paused_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            elif event.type == KEYDOWN and event.key == K_SPACE:
                self.resume_game()
        return False


    def handle_playing_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            elif event.type == KEYDOWN and event.key == K_UP:
                self.rotate()
            elif event.type == KEYDOWN and event.key == K_p:
                self.pause_game()
            if event.type == BLOCK_DOWN_EVENT:
                self.move_down()
        return False

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            elif event.type == KEYDOWN and event.key == K_SPACE:
                self.start_game()                

        return False


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
