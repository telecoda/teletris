# main controller to keep it all together

import json

from models import *
from views import *
from sounds import *


class Tetris(object):

    def __init__(self):

        self.audio_manager = AudioManager()
        # init high scores
        self.load_high_scores()

        # reset game
        self.new_game()

    def load_high_scores(self):
        try:
            with open('data/scores.json') as data_file:
                self.high_scores = json.load(data_file)
        except:
            self.high_scores = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def save_high_scores(self):
        try:
            with open('data/scores.json', 'w') as data_file:
                json.dump(self.high_scores, data_file)
                data_file.close()
        except:
            pass

    def new_game(self):
        self.score = 0
        self.level = 1
        self.state = MENU
        self.player_state = ALIVE

        self.board = Board()

        self.player = Player()

        # init game assets
        self.screen = GameScreen(self)

    def increase_score(self, amount):
        before_score = self.score
        before_level = before_score / ROWS_PER_LEVEL
        self.score += amount
        after_score = self.score
        after_level = after_score / ROWS_PER_LEVEL

        # if increase level every X rows
        if after_level > before_level:
            event = pygame.event.Event(LEVEL_UP_EVENT)
            pygame.event.post(event)

    def start_game(self):
        self.state = PLAYING
        # do it twice to set current & next shape
        self.player.set_next_random_shape()
        self.player.set_next_random_shape()
        self.audio_manager.start_music()
        # time in milliseconds
        pygame.time.set_timer(BLOCK_DOWN_EVENT, BLOCK_START_SPEED)

    def pause_game(self):
        self.state = PAUSED
        self.audio_manager.pause_music()

    def resume_game(self):
        self.state = PLAYING
        self.audio_manager.resume_music()

    def game_over(self):
        self.state = GAME_OVER

        # save scores
        old_scores = self.high_scores

        self.high_scores.append(self.score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[0:10]

        if old_scores != self.high_scores:
            self.save_high_scores()
            print "New high score entry!"

    def run(self):

        quit = False

        while not quit:
            # Handle Input Events
            if self.state == PLAYING:
                quit = self.handle_playing_events()
            elif self.state == MENU:
                quit = self.handle_menu_events()
            elif self.state == PAUSED:
                quit = self.handle_paused_events()
            elif self.state == GAME_OVER:
                quit = self.handle_game_over_events()

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

    def handle_game_over_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            elif event.type == KEYDOWN and event.key == K_SPACE:
                self.new_game()
        return False

    def handle_playing_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            elif event.type == KEYDOWN and event.key == K_UP:
                self.rotate()
            elif event.type == KEYDOWN and event.key == K_DOWN:
                self.move_down()
            elif event.type == KEYDOWN and event.key == K_LEFT:
                self.move_left()
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                self.move_right()
            elif event.type == KEYDOWN and event.key == K_p:
                self.pause_game()
            if event.type == BLOCK_DOWN_EVENT:
                self.move_down()
            if event.type == ROWS_COMPLETE_EVENT:
                self.destroy_rows(event.dict['rows'])
            if event.type == LEVEL_UP_EVENT:
                self.level_up()
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
        elif self.state == GAME_OVER:
            self.render_game_over()
        else:
            self.render_menu()

    def render_menu(self):
        self.screen.render_menu()

    def render_paused(self):
        self.screen.render_game_paused()

    def render_game_over(self):
        self.screen.render_game_over()

    def render_playing(self):
        self.screen.render_game_playing()

    def rotate(self):
        # rotate shape
        self.player.rotate()
        # check it still fits
        if not self.board.can_player_fit_at(self.player, self.player.x, self.player.y):
            # rotate it back
            self.player.rotate_back()

    def move_down(self):
        # test if player's block fits

        if self.board.can_player_fit_at(self.player, self.player.x, self.player.y + 1):
            self.player.move_down()
        else:
            self.board.add_shape_to_board(self.player)
            self.new_shape()
            self.board.check_complete_rows()

    def move_left(self):
        # test if player's block fits
        if self.board.can_player_fit_at(self.player, self.player.x - 1, self.player.y):
            self.player.move_left()

    def move_right(self):
        # test if player's block fits
        if self.board.can_player_fit_at(self.player, self.player.x + 1, self.player.y):
            self.player.move_right()

    def new_shape(self):
        self.player.set_next_random_shape()
        if not self.board.can_player_fit_at(self.player, self.player.x, self.player.y):
            self.game_over()

    def destroy_rows(self, rows):

        self.audio_manager.play_boom()
        self.board.destroy_rows(rows)

        # increase score
        self.increase_score(len(rows))

    def level_up(self):

        # increase level
        self.level += 1
        # increase speed of blocks
        pygame.time.set_timer(
            BLOCK_DOWN_EVENT, BLOCK_START_SPEED -
            ((self.level - 1) * LEVEL_SPEED_INCREASE))
