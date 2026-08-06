from src.renderer.audio.audio_map import AUDIO_MAP


def move_to_audio(move):

    start, end = move.split("-")

    start = int(start)
    end = int(end)

    return [
        f"assets/audio/{AUDIO_MAP[start]}",
        f"assets/audio/{AUDIO_MAP[end]}"
    ]