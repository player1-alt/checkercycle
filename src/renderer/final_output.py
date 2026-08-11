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

        # Read timeline using UTF-8
        with open(
            self.timeline_file,
            "r",
            encoding="utf-8"
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
        # IMPORTANT:
        # UTF-8 is required because some audio filenames
        # contain Japanese/Unicode characters.
        #

        with open(
            "audio_list.txt",
            "w",
            encoding="utf-8"
        ) as file:

            for audio in audio_files:

                absolute_path = os.path.abspath(audio)

                # FFmpeg concat files use single quotes.
                # Escape single quotes in Windows paths if needed.
                safe_path = absolute_path.replace(
                    "'",
                    "'\\''"
                )

                file.write(
                    "file '{}'\n".format(
                        safe_path
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

