from typing import Any

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import time

class BackGround:
    def __init__(self, path: str = '') -> None:
        self.path = path
    def play_background_music(self):
        print("Hello, thank you for using MusicBGX (:")
        pygame.mixer.init()
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(1)

        return True