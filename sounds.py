"""
All the sound related code for the game
"""

import os.path
import sys
import pygame.mixer
import pygame.time

mixer = pygame.mixer
time = pygame.time

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')


def load_sound(file_name):

    file_path = os.path.join(main_dir, 'data', file_name)
    try:
        # load the sound
        sound = mixer.Sound(file_path)
    except pygame.error:
        raise SystemExit('Could not load sound "%s" %s' %
                         (file_name, pygame.get_error()))
    return sound


class AudioManager(object):

    def __init__(self):

        # choose a desired audio format
        mixer.init(11025)  # raises exception on fail

        # load all game sounds
        self.boom_sound = load_sound('boom.wav')
        self.game_music = load_sound('game_music.wav')

    def play_sound(self, sound, loops=1):

        return sound.play(loops)

    def play_boom(self):
        self.play_sound(self.boom_sound)

    def start_music(self):
        self.game_music_channel = self.play_sound(self.game_music, loops=-1)

    def pause_music(self):
        self.game_music_channel.pause()

    def resume_music(self):
        self.game_music_channel.unpause()
