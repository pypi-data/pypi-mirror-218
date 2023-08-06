from typing import Any
import pygame
import time

class BackGround:
    def __init__(self, path: str = '') -> None:
        self.path = path
    def play_background_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(1)

        return True