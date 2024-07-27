from pygame import mixer
import pygame
import tkinter
import os



# Ruta completa al archivo WAV
cancion = os.path.expanduser("~\\Music\\Cris MJ - No Ponga Excusas (Video Oficial).mp3")

pygame.mixer.init()

# Carga la canción
pygame.mixer.music.load(cancion)

# Reproduce la canción
pygame.mixer.music.play()

# Espera hasta que termine la reproducción
while pygame.mixer.music.get_busy():
    pass

# Cierra el mezclador
pygame.mixer.quit()