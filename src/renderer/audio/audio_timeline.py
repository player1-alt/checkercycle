import os
import json
import shutil
import subprocess
import imageio_ffmpeg

from src.renderer.settings import SETTINGS


class AudioTimeline:
    """
    Builds the three independent CheckerCycle audio outputs.

    Every square in the move notation becomes one audio event.

    Example:

        9-13 21-17

    becomes:

        9 -> 13 -> 21 -> 17

    Three separate audio files are created:

        CheckerCycle_audio_13s.mp3
        CheckerCycle_audio_8s.mp3
        CheckerCycle_audio_4s.mp3

    Each square receives the FULL duration of its mode.

    There is NO move pause.

    Audio is completely independent of slideshow/video timing.
    """

    def __init__(self):

        self.audio_map_file = (
            "config/audio_map.json"
        )

        self.audio_directory = (
            "assets/audio"
        )

        self.output_directory = (
            "CheckerCycle_audio_clips"
        )

        self.ffmpeg = (
            imageio_ffmpeg.get_ffmpeg_exe()
        )

        # -------------------------------------------------
        # Three audio modes
        # -------------------------------------------------

        self.modes = [
            13.0,
            8.0,
            4.0
        ]


    # =====================================================
    # BUILD ALL THREE AUDIO OUTPUTS
    # =====================================================

    def build(self, events):

        print()
        print("=====================")
        print("BUILDING AUDIO OUTPUTS")
        print("=====================")
        print()

        # -------------------------------------------------
        # Load audio map
        # -------------------------------------------------

        if not os.path.exists(
            self.audio_map_file
        ):

            print(
                "Audio map missing:",
                self.audio_map_file
            )

            return []

        with open(
            self.audio_map_file,
            "r",
            encoding="utf-8"
        ) as file:

            audio_map = json.load(file)

        # -------------------------------------------------
        # Flatten all move paths
        # -------------------------------------------------

        squares = self._extract_squares(
            events
        )

        print(
            "Square events:",
            len(squares)
        )

        print(
            "Sequence:"
        )

        print(
            squares
        )

        print()

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
        # Build each mode
        # -------------------------------------------------

        outputs = []

        for duration in self.modes:

            output = self._build_mode(
                squares,
                audio_map,
                duration
            )

            if output:

                outputs.append(output)

        print()
        print("=====================")
        print("AUDIO OUTPUTS CREATED")
        print("=====================")

        for output in outputs:

            print(
                output
            )

        print("=====================")

        return outputs


    # =====================================================
    # EXTRACT SQUARES
    # =====================================================

    def _extract_squares(
        self,
        events
    ):

        squares = []

        for event in events:

            path = []

            # -------------------------------------------------
            # Dictionary event
            # -------------------------------------------------

            if isinstance(
                event,
                dict
            ):

                path = event.get(
                    "path",
                    []
                )

            # -------------------------------------------------
            # MoveEvent
            # -------------------------------------------------

            elif hasattr(
                event,
                "move"
            ):

                move = event.move

                if hasattr(
                    move,
                    "path"
                ):

                    path = move.path

            # -------------------------------------------------
            # Direct move object
            # -------------------------------------------------

            elif hasattr(
                event,
                "path"
            ):

                path = event.path

            # -------------------------------------------------
            # Add EVERY square
            # -------------------------------------------------

            for square in path:

                squares.append(
                    square
                )

        return squares


    # =====================================================
    # BUILD ONE MODE
    # =====================================================

    def _build_mode(
        self,
        squares,
        audio_map,
        duration
    ):

        print()
        print("=====================")
        print(
            f"AUDIO MODE: {duration:g}s"
        )
        print("=====================")

        print(
            f"Square duration: "
            f"{duration}s"
        )

        print(
            f"Square events: "
            f"{len(squares)}"
        )

        print()

        mode_tag = (
            f"{duration:g}s"
        )

        mode_directory = os.path.join(
            self.output_directory,
            mode_tag
        )

        os.makedirs(
            mode_directory,
            exist_ok=True
        )

        clips = []

        # -------------------------------------------------
        # Create one clip per square
        # -------------------------------------------------

        for index, square in enumerate(
            squares,
            start=1
        ):

            clip_path = os.path.join(
                mode_directory,
                f"clip_{index:04d}.mp3"
            )

            print(
                f"Audio {index}: "
                f"Square {square}"
            )

            key = str(square)

            # -------------------------------------------------
            # Missing mapping = silence
            # -------------------------------------------------

            if key not in audio_map:

                print(
                    "  No song assigned."
                )

                self._create_silence_clip(
                    clip_path,
                    duration
                )

                clips.append(
                    clip_path
                )

                continue

            audio_file = audio_map[key]

            source = os.path.join(
                self.audio_directory,
                audio_file
            )

            print(
                "  Song:",
                audio_file
            )

            # -------------------------------------------------
            # Missing source = silence
            # -------------------------------------------------

            if not os.path.exists(
                source
            ):

                print(
                    "  Missing audio:",
                    source
                )

                self._create_silence_clip(
                    clip_path,
                    duration
                )

                clips.append(
                    clip_path
                )

                continue

            # -------------------------------------------------
            # Create song clip
            # -------------------------------------------------

            try:

                self._create_audio_clip(
                    source,
                    clip_path,
                    duration
                )

                clips.append(
                    clip_path
                )

                print(
                    "  Created:",
                    clip_path
                )

            except Exception as e:

                print(
                    "  FFmpeg error:",
                    e
                )

                self._create_silence_clip(
                    clip_path,
                    duration
                )

                clips.append(
                    clip_path
                )

        # -------------------------------------------------
        # Concatenate all clips
        # -------------------------------------------------

        output_name = (
            f"CheckerCycle_audio_{mode_tag}.mp3"
        )

        output_path = output_name

        print()
        print(
            "Combining audio clips..."
        )

        self._combine_clips(
            clips,
            output_path
        )

        print()
        print("=====================")
        print(
            f"AUDIO CREATED: "
            f"{output_path}"
        )
        print("=====================")

        return output_path


    # =====================================================
    # CREATE SONG CLIP
    # =====================================================

    def _create_audio_clip(
        self,
        source,
        output,
        duration
    ):

        subprocess.run(
            [
                self.ffmpeg,

                "-y",

                "-i",
                source,

                "-af",
                (
                    f"atrim=start=0:"
                    f"duration={duration},"
                    f"apad"
                ),

                "-t",
                str(duration),

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


    # =====================================================
    # CREATE SILENCE
    # =====================================================

    def _create_silence_clip(
        self,
        output,
        duration
    ):

        subprocess.run(
            [
                self.ffmpeg,

                "-y",

                "-f",
                "lavfi",

                "-i",
                (
                    "anullsrc="
                    "channel_layout=stereo:"
                    "sample_rate=44100"
                ),

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


    # =====================================================
    # COMBINE CLIPS
    # =====================================================

    def _combine_clips(
        self,
        clips,
        output
    ):

        if not clips:

            print(
                "No audio clips to combine."
            )

            return

        concat_file = os.path.join(
            self.output_directory,
            "concat.txt"
        )

        # -------------------------------------------------
        # FFmpeg concat file
        # -------------------------------------------------

        with open(
            concat_file,
            "w",
            encoding="utf-8"
        ) as file:

            for clip in clips:

                absolute_path = os.path.abspath(
                    clip
                )

                safe_path = (
                    absolute_path
                    .replace(
                        "\\",
                        "/"
                    )
                    .replace(
                        "'",
                        "'\\''"
                    )
                )

                file.write(
                    f"file '{safe_path}'\n"
                )

        # -------------------------------------------------
        # Concatenate
        # -------------------------------------------------

        subprocess.run(
            [
                self.ffmpeg,

                "-y",

                "-f",
                "concat",

                "-safe",
                "0",

                "-i",
                concat_file,

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