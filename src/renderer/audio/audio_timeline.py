
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

    IMPORTANT:
    Every square in a move path gets its own audio clip.

    Example:

        9-13

    becomes:

        square 9  -> 10s audio + 3s silence
        square 13 -> 10s audio + 3s silence
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

        # -------------------------------------------------
        # Clean old clips
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Build timeline
        # -------------------------------------------------

        timeline = []

        clip_number = 0

        for event_index, event in enumerate(events):

            print(
                f"Audio event {event_index + 1}"
            )

            squares = []

            # -------------------------------------------------
            # Get move path
            # -------------------------------------------------

            if isinstance(event, dict):

                squares = event.get(
                    "path",
                    []
                )

            elif hasattr(event, "move"):

                squares = event.move.path

            # -------------------------------------------------
            # No path
            # -------------------------------------------------

            if not squares:

                print(
                    "No square assigned."
                )

                clip_number += 1

                clip_path = (
                    self._create_silence_clip_at_number(
                        clip_number
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

            # -------------------------------------------------
            # IMPORTANT:
            #
            # Process EVERY square in the move path.
            #
            # 9-13
            #
            # path = [9, 13]
            #
            # Both squares get audio.
            # -------------------------------------------------

            for square in squares:

                print(
                    "Square:",
                    square
                )

                key = str(square)

                clip_number += 1

                clip_path = os.path.join(
                    self.output_directory,
                    f"clip_{clip_number:04d}.mp3"
                )

                # -------------------------------------------------
                # No audio assigned to square
                # -------------------------------------------------

                if key not in audio_map:

                    print(
                        "No song assigned:",
                        square
                    )

                    self._create_silence_clip_at(
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

                    continue

                # -------------------------------------------------
                # Audio file
                # -------------------------------------------------

                audio_file = audio_map[key]

                filepath = os.path.join(
                    "assets/audio",
                    audio_file
                )

                print(
                    "Song:",
                    audio_file
                )

                # -------------------------------------------------
                # Missing audio file
                # -------------------------------------------------

                if not os.path.exists(filepath):

                    print(
                        "Missing audio:",
                        filepath
                    )

                    self._create_silence_clip_at(
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

                    continue

                # -------------------------------------------------
                # Create audio clip
                # -------------------------------------------------

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

        # -------------------------------------------------
        # Finished
        # -------------------------------------------------

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

    # =========================================================
    # CREATE AUDIO CLIP
    # =========================================================

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

        # -------------------------------------------------
        # FFmpeg:
        #
        # Start at 0:00
        # Take exactly audio_duration
        # Pad if necessary
        # Output exactly total duration
        #
        # Final portion is silence.
        # -------------------------------------------------

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

    # =========================================================
    # CREATE SILENCE CLIP
    # =========================================================

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

    # =========================================================
    # CREATE NUMBERED SILENCE CLIP
    # =========================================================

    def _create_silence_clip_at_number(
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

    # =========================================================
    # CREATE SILENCE AT SPECIFIC PATH
    # =========================================================

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
