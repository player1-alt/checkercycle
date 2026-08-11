import cv2


class VideoOutput:

    def __init__(self):

        self.output_name = "CheckerCycle.mp4"

        self.fps = 2

        # Every position occupies exactly 13 seconds.
        self.move_interval = 13.0

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

        height, width, _ = (
            first_frame.shape
        )

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

        # ---------------------------------------------
        # STARTING POSITION
        # ---------------------------------------------

        initial_image = cv2.imread(
            frames[0]
        )

        hold_frames = int(
            self.fps * self.move_interval
        )

        print(
            f"Starting position -> "
            f"{self.move_interval}s "
            f"({hold_frames} frames)"
        )

        for _ in range(hold_frames):

            video.write(
                initial_image
            )

        # ---------------------------------------------
        # EVERY MOVE POSITION
        # ---------------------------------------------

        for index, frame in enumerate(
            frames[1:],
            start=1
        ):

            image = cv2.imread(
                frame
            )

            print(
                f"Move {index} -> "
                f"{self.move_interval}s "
                f"({hold_frames} frames)"
            )

            for _ in range(hold_frames):

                video.write(
                    image
                )

        # ---------------------------------------------
        # FINAL POSITION
        # ---------------------------------------------

        video.release()

        print()

        print("=====================")

        print(
            f"VIDEO OUTPUT: "
            f"{self.output_name}"
        )

        print("=====================")