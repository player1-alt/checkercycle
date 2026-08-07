import os
import json


class AudioTimeline:
    """
    Builds audio timeline from renderer frame events.

    Converts:

    frame path:
        [11,15]

    into:

    audio:
        [
          test.mp3,
          test.mp3
        ]

    using audio_map.json
    """



    def __init__(self):

        self.audio_map_file = "config/audio_map.json"



    def build(self, events):

        print()
        print("Building audio timeline...")
        print()



        if not os.path.exists(self.audio_map_file):

            print("Audio map missing.")
            return []



        with open(
            self.audio_map_file,
            "r"
        ) as file:

            audio_map = json.load(file)



        timeline = []



        for event in events:



            # Frame dictionary

            if isinstance(event, dict):


                squares = event.get(
                    "path",
                    []
                )


                duration = event.get(
                    "duration",
                    1
                )


                audio_paths = []



                for square in squares:


                    key = str(square)



                    if key in audio_map and audio_map[key]:


                        audio_file = audio_map[key]


                        audio_paths.append(
                            audio_file
                        )


                        print(
                            "Square",
                            square,
                            "->",
                            audio_file
                        )


                    else:

                        print(
                            "No song assigned:",
                            square
                        )



                timeline.append(
                    {
                        "path": audio_paths,
                        "duration": duration
                    }
                )


                continue




            # MoveEvent fallback

            if hasattr(event, "move"):


                audio_paths = []


                for square in event.move.path:


                    key = str(square)


                    if key in audio_map and audio_map[key]:

                        audio_paths.append(
                            audio_map[key]
                        )


                timeline.append(
                    {
                        "path": audio_paths,
                        "duration":
                            event.duration
                    }
                )



        print()

        print(
            "Audio entries:",
            len(timeline)
        )



        with open(
            "CheckerCycle_audio_timeline.json",
            "w"
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