from src.renderer.audio.audio_player import AudioPlayer
from src.renderer.audio.move_audio import move_to_audio


player = AudioPlayer()


move = "25-29"

files = move_to_audio(move)

player.play_sequence(files, pause=2)


print("Move audio complete")