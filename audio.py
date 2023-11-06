import pygame
import replay

class Player:
    def __init__(self):
        self.paused = False
        self.path = None  # Initialize path as None

    def start_player(self, path):
        self.path = path  # Set the path when starting playback
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

    def play(self, game_time):
        if self.path:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            else:
                pygame.mixer.music.set_pos(game_time)
                pygame.mixer.music.play()
                self.paused = False

    def pause(self):
        if self.path:
            if not self.paused:
                pygame.mixer.music.pause()
                self.paused = True
