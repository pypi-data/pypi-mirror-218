from typing import Any

from os import *
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import time

class BackGround:
    def __init__(self, paths: list = []) -> None:
        self.paths = paths
        print(f"Start {__file__}")
    def play_background_music(self, Vol: float = 50.5):
        print("Hello, thank you for using MusicBGX (:")
        try:
            for i, item in enumerate(self.paths):
                print(f'Play Music {i + 1} : {item}')
                pygame.mixer.init()
                pygame.mixer.music.load(item)
                pygame.mixer.music.set_volume(Vol)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(1)

            raise Exception('Pygame Error !')
        except Exception as e:
            return False