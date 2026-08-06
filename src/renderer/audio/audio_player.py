import os

os.environ["SDL_AUDIODRIVER"] = "directsound"

import pygame
import time


class AudioPlayer:

    def __init__(self):
        pygame.mixer.init()

    def play(self, file_path):
        print(f"Playing: {file_path}")

        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    def play_sequence(self, files, pause=2):

        for file in files:
            self.play(file)

            print(f"Hold {pause} seconds")
            time.sleep(pause)