import cv2
import os


class VideoOutput:
    """
    Converts PNG animation frames into MP4 video.
    """

    def __init__(self):
        self.frame_folder = "."
        self.output_name = "CheckerCycle.mp4"


    def create_video(self):

        frames = []


        for file in sorted(
            os.listdir(self.frame_folder)
        ):

            if file.startswith("animation") and file.endswith(".png"):

                frames.append(file)


        if not frames:

            print("No animation frames found.")
            return


        first_frame = cv2.imread(
            frames[0]
        )


        height, width, layers = first_frame.shape


        video = cv2.VideoWriter(
            self.output_name,
            cv2.VideoWriter_fourcc(*"mp4v"),
            2,
            (width, height)
        )


        for frame in frames:

            image = cv2.imread(frame)

            video.write(image)


        video.release()


        print(
            f"VIDEO OUTPUT: Saved {self.output_name}"
        )