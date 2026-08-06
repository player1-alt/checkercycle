from src.renderer.audio.audio_map import AUDIO_MAP


def square_to_audio(square):

    if square not in AUDIO_MAP:

        return None

    return f"assets/audio/{AUDIO_MAP[square]}"



def move_to_audio(move):

    start, end = move.split("-")

    start = int(start)
    end = int(end)


    audio_sequence = []


    start_audio = square_to_audio(start)

    if start_audio:
        audio_sequence.append(start_audio)



    end_audio = square_to_audio(end)

    if end_audio:
        audio_sequence.append(end_audio)



    return audio_sequence