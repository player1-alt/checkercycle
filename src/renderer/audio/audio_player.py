import os

os.environ["SDL_AUDIODRIVER"] = "directsound"

import pygame
import time



class AudioPlayer:

    def __init__(self):

        pygame.mixer.init()



    def play(self, file_path):

        print(f"Playing: {file_path}")

        pygame.mixer.music.load(
            file_path
        )

        pygame.mixer.music.play()


        while pygame.mixer.music.get_busy():

            time.sleep(0.1)



    def play_sequence(
        self,
        files,
        move_time=2,
        hold_time=2
    ):

        """
        Plays audio following the renderer timeline.

        move_time:
        Time used while piece travels.

        hold_time:
        Time used after landing for study.
        """


        for index, file in enumerate(files):


            self.play(file)



            # Between squares = movement time

            if index < len(files) - 1:

                print(
                    f"Move timing {move_time} seconds"
                )

                time.sleep(
                    move_time
                )


            # After final square = study hold

            else:

                print(
                    f"Study hold {hold_time} seconds"
                )

                time.sleep(
                    hold_time
                )