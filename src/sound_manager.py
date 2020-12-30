import pygame.mixer
import sys

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.path = sys.path[0] + '/res/sound/'
        self.game_over = pygame.mixer.Sound(self.path + 'game_over.wav')
        self.damage = pygame.mixer.Sound(self.path + 'damage.wav')
        self.start = pygame.mixer.Sound(self.path + 'start.wav')
        self.win = pygame.mixer.Sound(self.path + 'win.wav')

    def play_music(self):
        pygame.mixer.music.load(self.path + 'game.wav')
        pygame.mixer.music.play(-1)

    def play_sound(self, sound):
        if sound == 'game_over':
            pygame.mixer.Sound.play(self.game_over)
        elif sound == 'damage':
            pygame.mixer.Sound.play(self.damage)
        elif sound == 'start':
            pygame.mixer.Sound.play(self.start)
        elif sound == 'win':
            pygame.mixer.Sound.play(self.win)

    @staticmethod
    def stop_music():
        pygame.mixer.music.stop()

    @staticmethod
    def pause_music():
        pygame.mixer.music.pause()

    @staticmethod
    def unpause_music():
        pygame.mixer.music.unpause()
