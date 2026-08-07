import os
import json
import subprocess


class MP3Builder:
    """
    Creates CheckerCycle_generated_audio.mp3 from the
    CheckerCycle audio timeline.

    Version 1:
    - Reads CheckerCycle_audio_timeline.json
    - Uses every timeline entry
    - Preserves each entry's duration
    - Uses silence when no song is assigned
    - Produces an audio track matching the COMPLETE
      renderer timeline
    """

    def __init__(self):

        self.timeline_file = "CheckerCycle_audio_timeline.json"

        self.output_file = "CheckerCycle_generated_audio.mp3"

        self.audio_list_file = "audio_list.txt"

        self.ffmpeg = (
            r"C:\Users\Hello\AppData\Local\Python\pythoncore-3.14-64"
            r"\Lib\site-packages\imageio\_ffmpeg\binaries"
            r"\ffmpeg-win-x86_64-v7.1.exe"
        )

    # ==========================================================
    # BUILD
    # ==========================================================

    def build(self):

        print()
        print("Building audio track...")
        print()

        if not os.path.exists(self.timeline_file):

            print(
                "Missing audio timeline:",
                self.timeline_file
            )

            return False

        if not os.path.exists(self.ffmpeg):

            print(
                "FFmpeg not found:",
                self.ffmpeg
            )

            return False

        # ------------------------------------------------------
        # LOAD TIMELINE
        # ------------------------------------------------------

        with open(
            self.timeline_file,
            "r"
        ) as file:

            timeline = json.load(file)

        if not timeline:

            print(
                "Audio timeline is empty."
            )

            return False

        print(
            "Timeline entries:",
            len(timeline)
        )

        # ------------------------------------------------------
        # CREATE TEMP DIRECTORY
        # ------------------------------------------------------

        temp_dir = "audio_temp"

        os.makedirs(
            temp_dir,
            exist_ok=True
        )

        segment_files = []

        # ------------------------------------------------------
        # BUILD EACH TIMELINE SEGMENT
        # ------------------------------------------------------

        for index, item in enumerate(timeline):

            duration = float(
                item.get(
                    "duration",
                    0
                )
            )

            paths = item.get(
                "path",
                []
            )

            if not isinstance(
                paths,
                list
            ):

                paths = [paths]

            valid_paths = []

            for path in paths:

                if not path:
                    continue

                if os.path.exists(path):

                    valid_paths.append(
                        path
                    )

                else:

                    print(
                        "Missing:",
                        path
                    )

            segment_file = os.path.join(
                temp_dir,
                f"segment_{index:04d}.mp3"
            )

            # --------------------------------------------------
            # NO AUDIO = SILENCE
            # --------------------------------------------------

            if not valid_paths:

                print(
                    f"Segment {index + 1}: "
                    f"silence for {duration:.2f}s"
                )

                command = [

                    self.ffmpeg,

                    "-y",

                    "-f",
                    "lavfi",

                    "-i",
                    "anullsrc=r=48000:cl=stereo",

                    "-t",
                    str(duration),

                    "-c:a",
                    "libmp3lame",

                    "-b:a",
                    "192k",

                    segment_file
                ]

                subprocess.run(
                    command,
                    check=True
                )

                segment_files.append(
                    segment_file
                )

                continue

            # --------------------------------------------------
            # AUDIO ASSIGNED
            #
            # For multiple square assignments inside one
            # timeline entry, concatenate the assigned songs
            # and trim the result to this entry duration.
            # --------------------------------------------------

            print(
                f"Segment {index + 1}: "
                f"{len(valid_paths)} audio file(s) "
                f"for {duration:.2f}s"
            )

            input_args = []

            filter_parts = []

            for audio_index, path in enumerate(valid_paths):

                input_args.extend(
                    [
                        "-i",
                        path
                    ]
                )

                filter_parts.append(
                    f"[{audio_index}:a]"
                )

            if len(valid_paths) == 1:

                filter_complex = (
                    "[0:a]"
                    "atrim=0:"
                    + str(duration)
                    + ","
                    "asetpts=N/SR/TB,"
                    "apad,"
                    "atrim=0:"
                    + str(duration)
                    + "[a]"
                )

            else:

                concat_inputs = "".join(
                    filter_parts
                )

                filter_complex = (
                    concat_inputs
                    + f"concat=n={len(valid_paths)}:v=0:a=1,"
                    + f"atrim=0:{duration},"
                    + "asetpts=N/SR/TB,"
                    + "apad,"
                    + f"atrim=0:{duration}[a]"
                )

            command = [

                self.ffmpeg,

                "-y",

                *input_args,

                "-filter_complex",
                filter_complex,

                "-map",
                "[a]",

                "-c:a",
                "libmp3lame",

                "-b:a",
                "192k",

                segment_file
            ]

            subprocess.run(
                command,
                check=True
            )

            segment_files.append(
                segment_file
            )

        # ------------------------------------------------------
        # CREATE CONCAT LIST
        # ------------------------------------------------------

        with open(
            self.audio_list_file,
            "w",
            encoding="utf-8"
        ) as file:

            for segment in segment_files:

                absolute_path = os.path.abspath(
                    segment
                )

                file.write(
                    "file '"
                    + absolute_path.replace(
                        "\\",
                        "/"
                    )
                    + "'\n"
                )

        # ------------------------------------------------------
        # JOIN ALL SEGMENTS
        # ------------------------------------------------------

        print()
        print(
            "Joining audio segments..."
        )

        command = [

            self.ffmpeg,

            "-y",

            "-f",
            "concat",

            "-safe",
            "0",

            "-i",
            self.audio_list_file,

            "-c:a",
            "libmp3lame",

            "-b:a",
            "192k",

            self.output_file
        ]

        subprocess.run(
            command,
            check=True
        )

        # ------------------------------------------------------
        # CLEANUP
        # ------------------------------------------------------

        for segment in segment_files:

            try:

                os.remove(
                    segment
                )

            except OSError:

                pass

        try:

            os.remove(
                self.audio_list_file
            )

        except OSError:

            pass

        try:

            os.rmdir(
                temp_dir
            )

        except OSError:

            pass

        # ------------------------------------------------------
        # COMPLETE
        # ------------------------------------------------------

        print()
        print(
            "AUDIO OUTPUT:",
            self.output_file
        )

        print()

        return True
