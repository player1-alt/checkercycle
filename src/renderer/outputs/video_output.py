import cv2

from src.renderer.settings import SETTINGS


class VideoOutput:
    """
    Creates an MP4 from saved PNG frames.

    Timing controlled by timeline durations.
    """


    def __init__(self):

        self.output_name = "CheckerCycle.mp4"

        # Frames per second
        self.fps = 2



    def create_video(
        self,
        timeline
    ):

        if not timeline:

            print("No timeline found.")
            return



        print()
        print("=====================")
        print("VIDEO TIMELINE")
        print("=====================")


        for item in timeline:

            print(
                item["frame"],
                "->",
                item["duration"],
                "seconds"
            )


        print()



        first_frame = cv2.imread(
            timeline[0]["frame"]
        )


        if first_frame is None:

            print(
                "Could not load first frame."
            )

            return



        height, width, _ = first_frame.shape



        video = cv2.VideoWriter(

            self.output_name,

            cv2.VideoWriter_fourcc(
                *"mp4v"
            ),

            self.fps,

            (
                width,
                height
            )

        )



        for item in timeline:


            frame = item["frame"]

            duration = item["duration"]


            image = cv2.imread(
                frame
            )


            if image is None:

                print(
                    "Skipping missing frame:",
                    frame
                )

                continue



            frame_count = int(
                self.fps * duration
            )


            print(
                f"Holding {frame} for {duration}s ({frame_count} frames)"
            )



            for _ in range(
                frame_count
            ):

                video.write(
                    image
                )



        video.release()



        print()

        print(
            "====================="
        )

        print(
            "VIDEO OUTPUT:",
            self.output_name
        )

        print(
            "====================="
        )