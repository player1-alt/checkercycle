import cv2

from src.renderer.settings import SETTINGS


class VideoOutput:

    def __init__(self):

        self.output_name = "CheckerCycle.mp4"

        self.fps = 2


    def create_video(
        self,
        frames,
        events=None
    ):

        if not frames:

            print(
                "No frames found."
            )

            return


        first_frame = cv2.imread(
            frames[0]
        )

        height, width, _ = first_frame.shape


        video = cv2.VideoWriter(

            self.output_name,

            cv2.VideoWriter_fourcc(
                *"mp4v"
            ),

            self.fps,

            (width, height)

        )


        print()
        print("=====================")
        print("VIDEO TIMELINE")
        print("=====================")


        for index, frame in enumerate(frames):

            image = cv2.imread(
                frame
            )

            hold_seconds = 13.0


            if events and index < len(events):

                hold_seconds = events[index]["duration"]


            print(
                f"{frame} -> {hold_seconds}s"
            )


            hold_frames = int(
                self.fps * hold_seconds
            )


            print(
                f"Holding {frame} for "
                f"{hold_seconds}s "
                f"({hold_frames} frames)"
            )


            for _ in range(
                hold_frames
            ):

                video.write(
                    image
                )


        # Final position hold.

        final_hold = SETTINGS.get(
            "video",
            {}
        ).get(
            "final_hold",
            5.0
        )


        final_image = cv2.imread(
            frames[-1]
        )


        print()

        print(
            f"Holding final position for "
            f"{final_hold} seconds"
        )


        final_hold_frames = int(
            self.fps * final_hold
        )


        for _ in range(
            final_hold_frames
        ):

            video.write(
                final_image
            )


        video.release()


        print()

        print("=====================")

        print(
            f"VIDEO OUTPUT: "
            f"{self.output_name}"
        )

        print("=====================")
