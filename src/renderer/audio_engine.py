import json
import pygame


class AudioEngine:


    def __init__(self):

        print("Audio Engine loaded")

        self.map_file = "config/audio_map.json"

        self.audio_map = self.load_map()

        self.audio_ready = False


        try:

            pygame.mixer.init()

            self.audio_ready = True

            print("Audio system ready")


        except Exception as e:

            print(
                "Audio disabled:",
                e
            )



    def load_map(self):

        with open(
            self.map_file,
            "r"
        ) as file:

            return json.load(file)



    def play_square(self, square):


        if not self.audio_ready:

            return



        song = self.audio_map.get(
            str(square),
            ""
        )



        if not song:

            return



        print(
            f"AUDIO PLAY: Square {square}"
        )



        try:

            pygame.mixer.music.load(
                song
            )


            pygame.mixer.music.play()



        except Exception as e:

            print(
                "Audio playback error:",
                e
            )