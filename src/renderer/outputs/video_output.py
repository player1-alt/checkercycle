import cv2


class VideoOutput:
    """
    Creates an MP4 from saved PNG frames.
    """

    def __init__(self):

        self.output_name = "CheckerCycle.mp4"


    def create_video(self, frames):

        if not frames:

            print("No frames found.")
            return


        print()
        print("Frames going into video:")

        for frame in frames:
            print(frame)

        print()


        first_frame = cv2.imread(
            frames[0]
        )

        height, width, _ = first_frame.shape


        video = cv2.VideoWriter(
            self.output_name,
            cv2.VideoWriter_fourcc(*"mp4v"),
            2,
            (width, height)
        )


        for frame in frames:

            image = cv2.imread(frame)

            video.write(image)


        # Hold the final board position
        final_image = cv2.imread(
            frames[-1]
        )


        final_hold_seconds = 5
        fps = 2

        hold_frames = final_hold_seconds * fps


        print(
            f"Holding final position for {final_hold_seconds} seconds"
        )


        for _ in range(hold_frames):

            video.write(
                final_image
            )


        video.release()


        print(
            f"VIDEO OUTPUT: Saved {self.output_name}"
        )