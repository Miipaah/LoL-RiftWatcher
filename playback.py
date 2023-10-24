import pygame

class playback:
    def __init__(self, audio_path):
        self.path = audio_path
        self.pause = False
        self.time = 0.0

        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play(start=self.time)

    def play(self, gameTime):
        if self.paused:
            pygame.mixer.music.set_pos(gameTime)
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            pygame.mixer.music.set_pos(gameTime)
            pygame.mixer.music.unpause()
            self.paused = False

    def pause(self):
        if self.paused:
            pass
        else:
            pygame.mixer.music.pause
            self.paused = True



        