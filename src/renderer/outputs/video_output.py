import cv2

from src.renderer.settings import SETTINGS


class VideoOutput:
    """
    Creates an MP4 from saved PNG frames.

    Timing controlled by MoveEvents.

    Uses:
    - animation duration
    - position hold time
    - final hold config
    """


    def __init__(self):

        self.output_name = "CheckerCycle.mp4"
        self.fps = 2



    def create_video(
        self,
        frames,
        events=None
    ):

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



            # Animation frames

            if frame.startswith("animation"):

                video.write(image)



            # Board positions

            elif frame.startswith("frame"):


                hold_seconds = 5


                if events:

                    hold_seconds = events[0].hold_time



                hold_frames = int(
                    self.fps * hold_seconds
                )


                print(
                    f"Holding board position: {frame} for {hold_seconds}s"
                )


                for _ in range(hold_frames):

                    video.write(image)



        # Final position hold

        final_image = cv2.imread(
            frames[-1]
        )


        final_hold = SETTINGS["final_hold"]


        print()

        print(
            f"Holding final position for {final_hold} seconds"
        )


        for i in range(
            self.fps * final_hold
        ):

            video.write(final_image)


            print(
                f"Final hold {i+1}/{self.fps * final_hold}"
            )



        video.release()


        print()

        print(
            f"VIDEO OUTPUT: Saved {self.output_name}"
        )