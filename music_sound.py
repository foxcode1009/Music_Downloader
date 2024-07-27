import pygame

file = r"C:\Users\divar\Music\Casper Magico, Bryant Myers, Alex Rose & Juhn - Fantasmita Remix (Video Oficial).mp3"
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pass

pygame.quit()