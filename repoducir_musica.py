from pydub import AudioSegment
#from pydub.playback import play
import os
import pygame

mp3_audio = AudioSegment.from_file(os.path.expanduser("~\\Music\\Cris MJ 2024 (LetraLyrics) - Mejores Canciones de Cris MJ - Éxitos De Cris MJ - Mix Reggaeton 2024.mp3"), format="mp3")
cancion_wav = mp3_audio.export("convertida.wav", format="wav")



# Inicializa el mezclador
pygame.mixer.init()

# Ruta completa al archivo WAV
cancion = os.path.expanduser("~\\Music\\Cris-MJ-Ando-Buscando-_Video-Oficial_.wav")

# Carga la canción
pygame.mixer.music.load(cancion)

# Reproduce la canción
pygame.mixer.music.play()

# Espera hasta que termine la reproducción
while pygame.mixer.music.get_busy():
    pass

# Cierra el mezclador
pygame.quit()