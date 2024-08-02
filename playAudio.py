from flet import Audio
from pathlib import Path

def play(page, ruta):
    print("-- Ingresando a la funcion play")

    path_audio = ruta
    print(path_audio)

    print("-- Antes de la variable audio")
    audio = Audio(
            src=r"C:\Users\divar\Music\Ozuna - Pasado y Presente (Feat. Anuel AA) (Audio Oficial).mp3",
            autoplay=False
        )
    
    print("-- Antes de agregar audio a page en play ")
    page.overlay.append(audio)
    page.update()
    print("-- widget audio agregado")
    print("-- reproduciendo en play...")
    audio.play()
    page.update()
    print("-- saliendo de reproduccion en play <-")