import os
import json
import shutil
import subprocess
import imageio_ffmpeg

from src.renderer.settings import SETTINGS


class AudioTimeline:
    """
    Builds the CheckerCycle audio timeline using FFmpeg.

    For every displayed square:

        10 seconds of that square's MP3
        3 seconds of silence

    Every MP3 starts from 0:00.
    """

    def __init__(self):

        self.audio_map_file = "config/audio_map.json"

        self.audio_duration = (
            SETTINGS["audio"]["square_duration"]
        )

        self.move_pause = (
            SETTINGS["audio"]["move_pause"]
        )

        self.output_directory = (
            "CheckerCycle_audio_clips"
        )

        self.ffmpeg = (
            imageio_ffmpeg.get_ffmpeg_exe()
        )


    def build(self, events):

        print()
        print("Building audio timeline...")
        print()

        print(
            f"Audio duration: {self.audio_duration}s"
        )

        print(
            f"Move pause: {self.move_pause}s"
        )

        print(
            f"Square cycle: "
            f"{self.audio_duration + self.move_pause}s"
        )

        print()


        if not os.path.exists(
            self.audio_map_file
        ):

            print("Audio map missing.")

            return []


        with open(
            self.audio_map_file,
            "r",
            encoding="utf-8"
        ) as file:

            audio_map = json.load(file)


        # Clean old clips.

        if os.path.exists(
            self.output_directory
        ):

            try:

                shutil.rmtree(
                    self.output_directory
                )

            except PermissionError as e:

                print(
                    "Cannot remove old audio clips."
                )

                print(e)

                return []


        os.makedirs(
            self.output_directory,
            exist_ok=True
        )


        timeline = []


        for event_index, event in enumerate(events):

            print(
                f"Audio event {event_index + 1}"
            )

            squares = []


            if isinstance(event, dict):

                squares = event.get(
                    "path",
                    []
                )

            elif hasattr(event, "move"):

                squares = event.move.path


            if not squares:

                print(
                    "No square assigned."
                )

                clip_path = (
                    self._create_silence_clip(
                        event_index + 1
                    )
                )

                timeline.append(
                    {
                        "path": [clip_path],
                        "duration":
                            self.audio_duration
                            + self.move_pause
                    }
                )

                continue


            square = squares[0]

            key = str(square)


            print(
                "Square:",
                square
            )


            if key not in audio_map:

                print(
                    "No song assigned:",
                    square
                )

                clip_path = (
                    self._create_silence_clip(
                        event_index + 1
                    )
                )

                timeline.append(
                    {
                        "path": [clip_path],
                        "duration":
                            self.audio_duration
                            + self.move_pause
                    }
                )

                continue


            audio_file = audio_map[key]

            filepath = os.path.join(
                "assets/audio",
                audio_file
            )


            print(
                "Song:",
                audio_file
            )


            if not os.path.exists(filepath):

                print(
                    "Missing audio:",
                    filepath
                )

                clip_path = (
                    self._create_silence_clip(
                        event_index + 1
                    )
                )

                timeline.append(
                    {
                        "path": [clip_path],
                        "duration":
                            self.audio_duration
                            + self.move_pause
                    }
                )

                continue


            clip_number = event_index + 1

            clip_path = os.path.join(
                self.output_directory,
                f"clip_{clip_number:04d}.mp3"
            )


            try:

                self._create_audio_clip(
                    filepath,
                    clip_path
                )


                print(
                    "Created:",
                    clip_path
                )


                timeline.append(
                    {
                        "path": [clip_path],
                        "duration":
                            self.audio_duration
                            + self.move_pause
                    }
                )


            except Exception as e:

                print(
                    "FFmpeg audio error:",
                    e
                )


                # Create silence with a DIFFERENT
                # filename so we never reuse a
                # potentially locked file.

                fallback_path = os.path.join(
                    self.output_directory,
                    f"silence_{clip_number:04d}.mp3"
                )


                self._create_silence_clip_at(
                    fallback_path
                )


                timeline.append(
                    {
                        "path": [fallback_path],
                        "duration":
                            self.audio_duration
                            + self.move_pause
                    }
                )


        print()

        print(
            "Audio entries:",
            len(timeline)
        )


        with open(
            "CheckerCycle_audio_timeline.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                timeline,
                file,
                indent=4
            )


        print(
            "Saved CheckerCycle_audio_timeline.json"
        )


        return timeline


    def _create_audio_clip(
        self,
        source,
        output
    ):

        audio_ms = int(
            self.audio_duration * 1000
        )

        total_ms = int(
            (
                self.audio_duration
                +
                self.move_pause
            ) * 1000
        )


        # FFmpeg:
        #
        # - start at 0:00
        # - take exactly audio_duration
        # - pad if necessary
        # - output exactly total duration
        #
        # The final portion is silence.

        subprocess.run(
            [
                self.ffmpeg,

                "-y",

                "-i",
                source,

                "-af",
                (
                    f"atrim=start=0:"
                    f"duration={self.audio_duration},"
                    f"apad"
                ),

                "-t",
                str(
                    self.audio_duration
                    + self.move_pause
                ),

                "-vn",

                "-codec:a",
                "libmp3lame",

                "-q:a",
                "2",

                output
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )


    def _create_silence_clip(
        self,
        clip_number
    ):

        clip_path = os.path.join(
            self.output_directory,
            f"silence_{clip_number:04d}.mp3"
        )

        self._create_silence_clip_at(
            clip_path
        )

        print(
            "Created silent clip:",
            clip_path
        )

        return clip_path


    def _create_silence_clip_at(
        self,
        output
    ):

        duration = (
            self.audio_duration
            + self.move_pause
        )


        subprocess.run(
            [
                self.ffmpeg,

                "-y",

                "-f",
                "lavfi",

                "-i",
                "anullsrc="
                "channel_layout=stereo:"
                "sample_rate=44100",

                "-t",
                str(duration),

                "-codec:a",
                "libmp3lame",

                "-q:a",
                "2",

                output
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
