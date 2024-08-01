from flet import Audio
from Main import *

def play(page):

    instance = Dowloader_app
    path_audio = instance.return_path()
    print(path_audio)

    audio = Audio(
            src=path_audio,
            autoplay=False
        )
    
    page.overlay.append(audio)
    page.update()
    print("-- widget audio agregado")
    print("-- reproduciendo...")
    audio.play()
    page.update()
    print("-- saliendo de reproduccion <-")