from Enemigos import enemigos_slime
class Etapa:
    def __init__(self, nombre,bg_image_path, enemy_configs,musica):
        self.nombre=nombre
        self.bg_image_path = bg_image_path
        self.enemy_configs = enemy_configs
        self.musica=musica

etapas=[
Etapa("Ancient City", 'Sprites/BG.png',
    enemigos_slime,"Sound/Music-1.wav"),
Etapa("Infernal Landscape", 'Sprites/BG2.png',
    enemigos_slime, "Sound/Music-1.wav")
]

