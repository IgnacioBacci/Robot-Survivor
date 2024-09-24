import pygame

pygame.mixer.init()

# Cargar el sonido del impacto
sonidos_impacto = [
    pygame.mixer.Sound('Sound/Enemy_hit.wav'),
    pygame.mixer.Sound('Sound/Enemy_hit2.wav'),
    pygame.mixer.Sound('Sound/Enemy_hit3.wav')
]

sonidos_explosion = [
    pygame.mixer.Sound("Sound/Explosion.wav"),
    pygame.mixer.Sound("Sound/Explosion2.wav"),
    pygame.mixer.Sound("Sound/Explosion3.wav")
]


lista_sonidos=[
    sonidos_impacto,
    sonidos_explosion
]
for lista in lista_sonidos:
    for sonido in lista:
        sonido.set_volume(0.4)