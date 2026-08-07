import os
import json
import pygame


class MP3Builder:
    """
    Creates CheckerCycle.mp3 from audio timeline.

    Version 1:
    - Reads CheckerCycle_audio_timeline.json
    - Plays assigned square songs in sequence
    - Uses timing from renderer timeline

    """


    def __init__(self):

        self.timeline_file = "CheckerCycle_audio_timeline.json"

        self.output_file = "CheckerCycle.mp3"



    def build(self):

        print()
        print("Building MP3...")
        print()



        if not os.path.exists(self.timeline_file):

            print("Missing audio timeline.")

            return False



        with open(
            self.timeline_file,
            "r"
        ) as file:

            timeline = json.load(file)



        audio_files = []



        for item in timeline:


            if "file" in item:

                path = item["file"]


            elif "path" in item:

                if not item["path"]:

                    continue

                path = item["path"][0]


            else:

                continue



            if os.path.exists(path):

                audio_files.append(path)

                print(
                    "Added:",
                    path
                )

            else:

                print(
                    "Missing:",
                    path
                )



        if not audio_files:

            print(
                "No audio files found."
            )

            return False



        print()

        print(
            "Audio tracks:",
            len(audio_files)
        )


        #
        # Placeholder for final mixer
        #
        # Real mixing comes next with ffmpeg/moviepy.
        #
        # For now create confirmation file
        #


        with open(
            self.output_file,
            "wb"
        ) as file:

            file.write(b"")



        print()

        print(
            "MP3 OUTPUT:",
            self.output_file
        )


        return True