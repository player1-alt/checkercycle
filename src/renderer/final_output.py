import os
import subprocess
import json
import imageio_ffmpeg


class FinalOutput:
    """
    Combines rendered video with generated audio timeline.
    """

    def __init__(self):

        self.video_file = "CheckerCycle.mp4"

        self.timeline_file = "CheckerCycle_audio_timeline.json"

        self.audio_output = "CheckerCycle_generated_audio.mp3"

        self.output_file = "CheckerCycle_Final.mp4"

        # Use Python's bundled FFmpeg
        self.ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()



    def combine(self):

        print()
        print("=====================")
        print("FINAL OUTPUT ENGINE")
        print("=====================")



        if not os.path.exists(self.video_file):

            print(
                "Missing video:",
                self.video_file
            )

            return



        if not os.path.exists(self.timeline_file):

            print(
                "Missing timeline:",
                self.timeline_file
            )

            return



        with open(
            self.timeline_file,
            "r"
        ) as file:

            timeline = json.load(file)



        audio_files = []



        for item in timeline:

            paths = item.get(
                "path",
                []
            )


            for path in paths:

                if path and os.path.exists(path):

                    audio_files.append(path)



        print()

        print(
            "Audio clips found:",
            len(audio_files)
        )



        if not audio_files:

            print(
                "No audio clips found."
            )

            return



        print()

        for audio in audio_files:

            print(
                audio
            )



        #
        # Create FFmpeg audio concat file
        #

        with open(
            "audio_list.txt",
            "w"
        ) as file:


            for audio in audio_files:

                file.write(
                    "file '{}'\n".format(
                        os.path.abspath(audio)
                    )
                )



        print()

        print(
            "Building audio track..."
        )



        subprocess.run(
            [
                self.ffmpeg,

                "-y",

                "-f",
                "concat",

                "-safe",
                "0",

                "-i",
                "audio_list.txt",

                "-c",
                "copy",

                self.audio_output
            ],

            check=True
        )



        print()

        print(
            "Combining video + audio..."
        )



        subprocess.run(
            [
                self.ffmpeg,

                "-y",

                "-i",
                self.video_file,

                "-i",
                self.audio_output,

                "-c:v",
                "copy",

                "-c:a",
                "aac",

                "-shortest",

                self.output_file
            ],

            check=True
        )



        print()

        print(
            "FINAL VIDEO CREATED:",
            self.output_file
        )