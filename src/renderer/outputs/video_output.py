import cv2


class VideoOutput:
    """
    Creates an MP4 from saved PNG frames.
    Board positions are held longer than animation frames.
    """

    def __init__(self):

        self.output_name = "CheckerCycle.mp4"
        self.fps = 2


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
            self.fps,
            (width, height)
        )


        for frame in frames:

            image = cv2.imread(
                frame
            )


            # Moving pieces
            if frame.startswith("animation"):

                video.write(image)


            # Board positions
            # Hold so the learner can study the position
            elif frame.startswith("frame"):

                print(
                    f"Holding board position: {frame}"
                )


                for _ in range(8):

                    video.write(image)


        # Final position extra hold

        final_image = cv2.imread(
            frames[-1]
        )


        print()
        print(
            "Holding final position for 5 seconds"
        )


        for i in range(self.fps * 5):

            video.write(final_image)

            print(
                f"Final hold {i+1}/{self.fps * 5}"
            )


        video.release()


        print()
        print(
            f"VIDEO OUTPUT: Saved {self.output_name}"
        )