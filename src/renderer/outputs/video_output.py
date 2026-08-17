import os
import subprocess
import tempfile
import shutil

import imageio_ffmpeg

from src.renderer.timeline import Timeline


class VideoOutput:

    def __init__(self):

        self.ffmpeg = (
            imageio_ffmpeg.get_ffmpeg_exe()
        )

        self.timeline = Timeline()

        self.fps = 30

        self.transition = 1.0


    # =================================================
    # CREATE ALL THREE SLIDESHOWS
    # =================================================

    def create_video(
        self,
        frames
    ):

        if not frames:

            print(
                "No frames found."
            )

            return


        print()
        print("=====================")
        print("BUILDING SLIDESHOWS")
        print("=====================")


        for mode in [13, 8, 4]:

            self._create_mode(
                frames,
                mode
            )


    # =================================================
    # CREATE ONE SLIDESHOW MODE
    # =================================================

    def _create_mode(
        self,
        frames,
        mode
    ):

        panel_duration = float(
            mode
        )

        transition = float(
            self.transition
        )

        output_name = (
            f"CheckerCycle_{mode}s.mp4"
        )


        print()
        print(
            f"SLIDESHOW MODE: {mode}s"
        )

        print(
            f"Panel duration: "
            f"{panel_duration}s"
        )

        print(
            f"Transition: "
            f"{transition}s"
        )

        print(
            f"Panels: "
            f"{len(frames)}"
        )


        temp_directory = tempfile.mkdtemp(
            prefix="checkercycle_slideshow_"
        )


        try:

            # =========================================
            # CREATE PANEL CLIPS
            # =========================================

            segments = []


            for index, frame in enumerate(
                frames
            ):

                segment = os.path.join(
                    temp_directory,
                    f"panel_{index:04}.mp4"
                )


                print(
                    f"Creating panel "
                    f"{index + 1}: "
                    f"{frame}"
                )


                command = [

                    self.ffmpeg,

                    "-y",

                    "-loop",
                    "1",

                    "-i",
                    frame,

                    "-t",
                    str(panel_duration),

                    "-vf",
                    (
                        f"fps={self.fps},"
                        f"format=yuv420p"
                    ),

                    "-an",

                    "-c:v",
                    "libx264",

                    "-preset",
                    "veryfast",

                    "-pix_fmt",
                    "yuv420p",

                    "-r",
                    str(self.fps),

                    segment
                ]


                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True
                )


                if result.returncode != 0:

                    print()
                    print(
                        "PANEL ERROR:"
                    )

                    print(
                        result.stderr
                    )

                    return


                segments.append(
                    segment
                )


            # =========================================
            # SINGLE PANEL
            # =========================================

            if len(segments) == 1:

                shutil.copyfile(
                    segments[0],
                    output_name
                )

                print()
                print(
                    f"SLIDESHOW CREATED: "
                    f"{output_name}"
                )

                return


            # =========================================
            # BUILD TRANSITION CLIPS
            # =========================================

            transition_segments = []


            for index in range(
                len(segments) - 1
            ):

                first = segments[index]

                second = segments[index + 1]

                transition_file = os.path.join(
                    temp_directory,
                    f"transition_{index:04}.mp4"
                )


                print()
                print(
                    f"Creating transition "
                    f"{index + 1}: "
                    f"Panel {index + 1} -> "
                    f"Panel {index + 2}"
                )


                # Extract the final transition
                # seconds from the first panel.

                first_start = (
                    panel_duration
                    - transition
                )


                # Extract the first transition
                # seconds from the second panel.

                command = [

                    self.ffmpeg,

                    "-y",

                    "-i",
                    first,

                    "-i",
                    second,

                    "-filter_complex",

                    (
                        f"[0:v]"
                        f"trim=start={first_start}:"
                        f"duration={transition},"
                        f"setpts=PTS-STARTPTS,"
                        f"fps={self.fps}"
                        f"[a];"

                        f"[1:v]"
                        f"trim=duration={transition},"
                        f"setpts=PTS-STARTPTS,"
                        f"fps={self.fps}"
                        f"[b];"

                        f"[a][b]"
                        f"blend="
                        f"all_expr="
                        f"'A*(1-T/{transition})"
                        f"+B*(T/{transition})',"
                        f"format=yuv420p"
                    ),

                    "-an",

                    "-c:v",
                    "libx264",

                    "-preset",
                    "veryfast",

                    "-pix_fmt",
                    "yuv420p",

                    "-r",
                    str(self.fps),

                    transition_file
                ]


                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True
                )


                if result.returncode != 0:

                    print()
                    print(
                        "TRANSITION ERROR:"
                    )

                    print(
                        result.stderr
                    )

                    return


                transition_segments.append(
                    transition_file
                )


            # =========================================
            # BUILD FINAL SLIDESHOW
            # =========================================

            print()
            print(
                "Assembling slideshow..."
            )


            # We don't simply concatenate the
            # original panels because the final
            # transition overlaps the end of
            # one panel with the beginning of
            # the next.
            #
            # Instead:
            #
            # Panel 1
            # Transition 1
            # Panel 2
            # Transition 2
            # Panel 3
            #
            # etc.


            final_segments = []


            for index in range(
                len(segments)
            ):

                # For every panel except the
                # first, the first transition
                # second is already represented
                # by the transition clip.

                if index == 0:

                    normal_duration = (
                        panel_duration
                        - transition
                    )

                else:

                    normal_duration = (
                        panel_duration
                        - transition
                    )


                normal_file = os.path.join(
                    temp_directory,
                    f"normal_{index:04}.mp4"
                )


                command = [

                    self.ffmpeg,

                    "-y",

                    "-i",
                    segments[index],

                    "-t",
                    str(normal_duration),

                    "-an",

                    "-c:v",
                    "libx264",

                    "-preset",
                    "veryfast",

                    "-pix_fmt",
                    "yuv420p",

                    "-r",
                    str(self.fps),

                    normal_file
                ]


                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True
                )


                if result.returncode != 0:

                    print()
                    print(
                        "NORMAL SEGMENT ERROR:"
                    )

                    print(
                        result.stderr
                    )

                    return


                final_segments.append(
                    normal_file
                )


                # Add transition after
                # this panel except after
                # the final panel.

                if index < len(
                    segments
                ) - 1:

                    final_segments.append(
                        transition_segments[index]
                    )


            # =========================================
            # CONCAT FINAL SEGMENTS
            # =========================================

            concat_file = os.path.join(
                temp_directory,
                "final_concat.txt"
            )


            with open(
                concat_file,
                "w",
                encoding="utf-8"
            ) as file:

                for segment in final_segments:

                    safe_path = (
                        segment
                        .replace("\\", "/")
                        .replace("'", "'\\''")
                    )

                    file.write(
                        f"file '{safe_path}'\n"
                    )


            command = [

                self.ffmpeg,

                "-y",

                "-f",
                "concat",

                "-safe",
                "0",

                "-i",
                concat_file,

                "-an",

                "-c:v",
                "libx264",

                "-preset",
                "veryfast",

                "-pix_fmt",
                "yuv420p",

                "-r",
                str(self.fps),

                output_name
            ]


            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )


            if result.returncode != 0:

                print()
                print(
                    "FINAL SLIDESHOW ERROR:"
                )

                print(
                    result.stderr
                )

                return


            print()
            print(
                "====================="
            )

            print(
                f"SLIDESHOW CREATED: "
                f"{output_name}"
            )

            print(
                "=====================")


        finally:

            shutil.rmtree(
                temp_directory,
                ignore_errors=True
            )