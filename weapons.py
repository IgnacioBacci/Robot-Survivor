import threading
import time
import pygame
import math
import random
armas_normales=[]
armas_raras=[]
armas_legendarias=[]

class Arma(pygame.sprite.Sprite):
    def __init__(self, nombre, daño, velocidad, calentamiento, tipo, sprite, sprite_bala, velocidadProyectil, perforacion,distancia_maxima=450,prob_critica=0):
        super().__init__()
        self.nombre = nombre
        self.daño = daño
        self.velocidad = velocidad
        self.calentamiento = calentamiento
        self.tipo = tipo
        self.image = sprite
        self.original_image = sprite
        self.rect = self.image.get_rect()
        self.sprite_bala = sprite_bala
        self.velocidadProyectil = velocidadProyectil
        self.perforacion = perforacion
        self.disparando = True
        self.daño_base = daño
        self.velocidad_base = velocidad
        self.calentamiento_base = calentamiento
        self.velocidadProyectil_base = velocidadProyectil
        self.prob_critica = prob_critica
        self.prob_critica_base= prob_critica
        self.mejoras_temporales = {
            "velocidad": 0
        }
        self.distancia_maxima=distancia_maxima
    def aplicar_mejora_temporal(self, tipo, cantidad):
            if tipo == "velocidad":
                self.mejoras_temporales["velocidad"] += cantidad
                self.velocidad += cantidad

    def revertir_mejoras_temporales(self):
            self.velocidad -= self.mejoras_temporales["velocidad"]
            self.mejoras_temporales["velocidad"] = 0

    def disparar(self, origen_x, origen_y, direccion, jugador,modD=1):
        from main import Bala, balas_sprites
        nueva_bala = Bala(self.daño*modD, self.velocidadProyectil, self.sprite_bala, origen_x, origen_y, direccion,
                          self.perforacion, self.prob_critica, arma=self)
        balas_sprites.add(nueva_bala)
        for mejora in jugador.mejoras:
            if hasattr(mejora, 'aplicar_dis'):
                mejora.aplicar_dis(jugador, nueva_bala)

    def impacto(self,objetivo,bala):
        pass

class RustyCannon(Arma):
    def __init__(self):
        super().__init__(
            nombre="Rusty Cannon",
            daño=14,
            velocidad=0.7,
            calentamiento=3,
            tipo="Primaria",
            sprite=pygame.image.load('Sprites/Armas/RustyCannon.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/Bala-1.png').convert_alpha(),
            velocidadProyectil=10,
            perforacion=2
        )
Rustycannon=RustyCannon()
armas_normales.append(RustyCannon)

class EnergyBlaster(Arma):
    def __init__(self):
        super().__init__(
            nombre="Energy Blaster",
            daño=20,
            velocidad=0.6,
            calentamiento=6,
            tipo="Secundaria",
            sprite=pygame.image.load('Sprites/Armas/EnergyBlaster.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/Bala-2.png').convert_alpha(),
            velocidadProyectil=15,
            perforacion=10
        )
Energyblaster=EnergyBlaster()
armas_normales.append(EnergyBlaster)

class RepHead(Arma):
    def __init__(self):
        super().__init__(
            nombre="Reptilian Head",
            daño=10,
            velocidad=0.6,
            calentamiento=1,
            tipo="Primaria",
            sprite=pygame.image.load('Sprites/Armas/Croc.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/PBala-1.png').convert_alpha(),
            velocidadProyectil=9,
            perforacion=3
        )

    def impacto(self, objetivo, bala):
        from main import jugador
        for suerte in range(jugador.suerte):
            if random.random() <= 0.15:
                objetivo.EnDescomposicion+=3
Head=RepHead()
armas_normales.append(RepHead)
class DartGun(Arma):
    def __init__(self):
        super().__init__(
            nombre="Dart Gun",
            daño=2,
            velocidad=5,
            calentamiento=0.5,
            tipo="Primaria",
            sprite=pygame.image.load('Sprites/Armas/DartGun.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/Dart.png').convert_alpha(),
            velocidadProyectil=12,
            perforacion=1
        )
armas_normales.append(DartGun)
d=DartGun()
class Shotgun(Arma):
    def __init__(self):
        super().__init__(
            nombre="Shotgun",
            daño=8,
            velocidad=0.3,
            calentamiento=9,
            tipo="Secundaria",
            sprite=pygame.image.load('Sprites/Armas/Shotgun.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/Bala-1.png').convert_alpha(),
            velocidadProyectil=9,
            perforacion=3,
            distancia_maxima=350
        )

    def disparar(self, origen_x, origen_y, direccion, jugador,modD=1):
        from main import Bala,balas_sprites

        for i in range(4):
            # Generar un pequeño desvío en la dirección
            desvio_direccion = random.uniform(-0.75, 0.75)
            nueva_direccion = (direccion[0] + desvio_direccion, direccion[1] + desvio_direccion)

            # Generar un pequeño desvío en la velocidad del proyectil
            desvio_velocidad = random.uniform(-2, 0)
            nueva_velocidad = self.velocidadProyectil + desvio_velocidad

            nueva_bala = Bala(self.daño*modD, nueva_velocidad, self.sprite_bala, origen_x, origen_y, nueva_direccion,
                              self.perforacion, self.prob_critica, arma=self,distancia=450, eficiencia=0.4)
            balas_sprites.add(nueva_bala)
        for mejora in jugador.mejoras:
            if hasattr(mejora, 'aplicar_dis'):
                mejora.aplicar_dis(jugador, nueva_bala)
armas_normales.append(Shotgun)

class DShotgun(Arma):
    def __init__(self):
        super().__init__(
            nombre="Double Shotgun",
            daño=10,
            velocidad=0.45,
            calentamiento=12,
            tipo="Secundaria",
            sprite=pygame.image.load('Sprites/Armas/DShotgun.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/Bala-1.png').convert_alpha(),
            velocidadProyectil=7,
            perforacion=2,
            distancia_maxima=350
        )
        self.hilo_disparo_continuo = None

    def disparar(self, origen_x, origen_y, direccion, jugador,modD=1):
        from main import Bala, balas_sprites

        def disparar_balas():
            for _ in range(3):
                desvio_direccion = random.uniform(-0.5, 0.75)
                nueva_direccion = (direccion[0] + desvio_direccion, direccion[1] + desvio_direccion)

                desvio_velocidad = random.uniform(-2, 0)
                nueva_velocidad = self.velocidadProyectil + desvio_velocidad

                nueva_bala = Bala(self.daño*modD, nueva_velocidad, self.sprite_bala, origen_x, origen_y, nueva_direccion,
                                  self.perforacion, self.prob_critica, arma=self, distancia=450, eficiencia=0.4)
                balas_sprites.add(nueva_bala)
            return nueva_bala
        nueva_bala=disparar_balas()
        for mejora in jugador.mejoras:
            if hasattr(mejora, 'aplicar_dis'):
                mejora.aplicar_dis(jugador, nueva_bala)



        def repetir_disparo(tiempo):
            time.sleep(tiempo)
            nueva_bala=disparar_balas()
            for mejora in jugador.mejoras:
                if hasattr(mejora, 'aplicar_dis'):
                    mejora.aplicar_dis(jugador, nueva_bala)

        def iniciar_hilos():
            hilos = [
                threading.Thread(target=repetir_disparo, args=(0.2,))
            ]
            for hilo in hilos:
                hilo.daemon = True
                hilo.start()

        if self.hilo_disparo_continuo is None or not self.hilo_disparo_continuo.is_alive():
            self.hilo_disparo_continuo = threading.Thread(target=iniciar_hilos)
            self.hilo_disparo_continuo.daemon = True
            self.hilo_disparo_continuo.start()
dshot=DShotgun()
armas_normales.append(DShotgun)

class GShroom(Arma):
    def __init__(self):
        super().__init__(
            nombre="Poision Shroom",
            daño=3,
            velocidad=0.25,
            calentamiento=0,
            tipo="Secundaria",
            sprite=pygame.image.load('Sprites/Armas/GreenShroom.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/GSpores.png').convert_alpha(),
            velocidadProyectil=1,
            perforacion=0,
            distancia_maxima=350
        )

    def disparar(self, origen_x, origen_y, direccion,jugador,modD=1):
        from main import Bala_temporal,balas_sprites
        nueva_bala = Bala_temporal(self.daño*modD, self.velocidadProyectil, self.sprite_bala, origen_x-16, origen_y-16, direccion, prob_critica=self.prob_critica, arma=self,duracion=2000,eficiencia=0.4)
        balas_sprites.add(nueva_bala)
        for mejora in jugador.mejoras:
            if hasattr(mejora, 'aplicar_dis'):
                mejora.aplicar_dis(jugador, nueva_bala)

    def impacto(self,objetivo,bala):
        objetivo.EnDescomposicion += 2

armas_normales.append(GShroom)

class RShroom(Arma):
    def __init__(self):
        super().__init__(
            nombre="Spicy Shroom",
            daño=3,
            velocidad=0.3,
            calentamiento=6,
            tipo="Primaria",
            sprite=pygame.image.load('Sprites/Armas/RedShroom.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/RSpores.png').convert_alpha(),
            velocidadProyectil=1,
            perforacion=0,
            distancia_maxima=350
        )

    def disparar(self, origen_x, origen_y, direccion,jugador,modD=1):
        from main import Bala_temporal,balas_sprites
        nueva_bala = Bala_temporal(self.daño*modD, self.velocidadProyectil, self.sprite_bala, origen_x-16, origen_y-16, direccion, prob_critica=self.prob_critica, arma=self,duracion=2000,eficiencia=0.4)
        balas_sprites.add(nueva_bala)
        for mejora in jugador.mejoras:
            if hasattr(mejora, 'aplicar_dis'):
                mejora.aplicar_dis(jugador, nueva_bala)

    def impacto(self,objetivo,bala):
        objetivo.EnQuemadura += 2

armas_normales.append(RShroom)
class FlameSpitter(Arma):
    def __init__(self):
        super().__init__(
            nombre="Flame Spitter",
            daño=2,
            velocidad=14,
            calentamiento=0.5,
            tipo="Secundaria",
            sprite=pygame.image.load('Sprites/Armas/Flame.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/Flame.png').convert_alpha(),
            velocidadProyectil=3,
            perforacion=100,
            distancia_maxima=250
        )
    def impacto(self,objetivo,bala):
        objetivo.EnQuemadura+=0.5
        pass
    def disparar(self, origen_x, origen_y, direccion,jugador,modD=1):
        from main import Bala,balas_sprites
        nueva_bala = Bala(self.daño*modD, self.velocidadProyectil, self.sprite_bala, origen_x-16, origen_y-16, direccion, self.perforacion, self.prob_critica, arma=self,distancia=200,eficiencia=0.2)
        balas_sprites.add(nueva_bala)
        for mejora in jugador.mejoras:
            if hasattr(mejora, 'aplicar_dis'):
                mejora.aplicar_dis(jugador, nueva_bala)

armas_raras.append(FlameSpitter)
llamas=FlameSpitter()

class Electric(Arma):
    def __init__(self):
        super().__init__(
            nombre="Tesla Coil",
            daño=9,
            velocidad=0.9,
            calentamiento=5,
            tipo="Secundaria",
            sprite=pygame.image.load('Sprites/Armas/Tesla_coil.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/Thunder.png').convert_alpha(),
            velocidadProyectil=10,
            perforacion=1,
            distancia_maxima=400
        )

    def disparar(self, origen_x, origen_y, direccion, jugador, modD=1):
        from main import Bala, balas_sprites, enemigos_sprites

        # Convertir temporalmente enemigos_sprites a una lista para seleccionar al azar
        enemigos_lista = list(enemigos_sprites)

        enemigos_validos = [
            enemigo for enemigo in enemigos_lista
            if math.sqrt((enemigo.rect.centerx - jugador.base.rect.centerx) ** 2 + (
                        enemigo.rect.centery - jugador.base.rect.centery) ** 2) <= 450
        ]
        if len(enemigos_validos) == 0:
            return

        if len(enemigos_validos) == 1:
            enemigo = enemigos_validos[0]
            nueva_bala = Bala(
                self.daño*modD,
                self.velocidadProyectil,
                self.sprite_bala,
                enemigo.rect.centerx,
                enemigo.rect.centery,
                direccion,
                self.perforacion,
                self.prob_critica,
                arma=self
            )
            balas_sprites.add(nueva_bala)
            return

        enemigos_seleccionados = random.sample(enemigos_validos, 2)

        for enemigo in enemigos_seleccionados:
            nueva_bala = Bala(
                self.daño*modD,
                self.velocidadProyectil,
                self.sprite_bala,
                enemigo.rect.centerx,
                enemigo.rect.centery,
                direccion,
                self.perforacion,
                self.prob_critica,
                arma=self
            )
            balas_sprites.add(nueva_bala)

    def impacto(self, objetivo, bala):
        from main import enemigos_sprites, Animacion, animaciones
        daño_explosion = self.daño / 3
        radio_explosion = (daño_explosion * 5) + 50
        for enemigo_cercano in enemigos_sprites:
            if enemigo_cercano != objetivo:
                distancia = math.sqrt(
                    (enemigo_cercano.rect.centerx - objetivo.rect.centerx) ** 2 +
                    (enemigo_cercano.rect.centery - objetivo.rect.centery) ** 2
                )
                if distancia <= radio_explosion:
                    enemigo_cercano.danio(daño_explosion, (88, 196, 236))

        anima = [
            pygame.image.load("Sprites\\Armas\\Balas\\Elec.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Elec3.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Elec4.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Elec5.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Elec2.png"),
        ]
        animacion = Animacion(objetivo.rect.center, anima, False, duracion_frame=50, desaparecer=True)
        animaciones.add(animacion)

elec=Electric()
armas_raras.append(Electric)
class BigShot(Arma):
    def __init__(self):
        super().__init__(
            nombre="Big Shot",
            daño=12,
            velocidad=0.40,
            calentamiento=9,
            tipo="Secundaria",
            sprite=pygame.image.load('Sprites/Armas/Bigshot.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/Big-Bala-1.png').convert_alpha(),
            velocidadProyectil=9,
            perforacion=2,
            distancia_maxima=350
        )
        self.hilo_disparo_continuo = None
        self.hilo_disparo_continuo2= None
        self.a=0

    def disparar(self, origen_x, origen_y, direccion, jugador,modD=1):
        from main import Bala, balas_sprites

        def disparar_balas():
            for _ in range(3):
                desvio_direccion = random.uniform(-0.5, 0.75)
                nueva_direccion = (direccion[0] + desvio_direccion, direccion[1] + desvio_direccion)

                desvio_velocidad = random.uniform(-2, 0)
                nueva_velocidad = self.velocidadProyectil + desvio_velocidad

                nueva_bala = Bala(self.daño*modD, nueva_velocidad, self.sprite_bala, origen_x, origen_y, nueva_direccion,
                                  self.perforacion, self.prob_critica, arma=self, distancia=450, eficiencia=0.1)
                balas_sprites.add(nueva_bala)
                for bala in balas_sprites:
                    self.a += 1
                    print(self.a)
                self.a=0

            return nueva_bala
        nueva_bala=disparar_balas()
        for mejora in jugador.mejoras:
            if hasattr(mejora, 'aplicar_dis'):
                mejora.aplicar_dis(jugador, nueva_bala)



        def repetir_disparo(tiempo):
            time.sleep(tiempo)
            nueva_bala=disparar_balas()
            for mejora in jugador.mejoras:
                if hasattr(mejora, 'aplicar_dis'):
                    mejora.aplicar_dis(jugador, nueva_bala)

        def iniciar_hilos():
            hilos = [
                threading.Thread(target=repetir_disparo, args=(0.2,)),
                threading.Thread(target=repetir_disparo, args=(0.4,))
            ]
            for hilo in hilos:
                hilo.daemon = True
                hilo.start()

        if self.hilo_disparo_continuo is None or not self.hilo_disparo_continuo.is_alive():
            self.hilo_disparo_continuo = threading.Thread(target=iniciar_hilos)
            self.hilo_disparo_continuo.daemon = True
            self.hilo_disparo_continuo.start()

armas_raras.append(BigShot)

class TriRocket(Arma):
    def __init__(self):
        super().__init__(
            nombre="Tri Rocket",
            daño=6,
            velocidad=0.4,
            calentamiento=5,
            tipo="Primaria",
            sprite=pygame.image.load('Sprites/Armas/MissileLauncher.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/Misil-1.png').convert_alpha(),
            velocidadProyectil=2,
            perforacion=1,
        )
        self.hilo_disparo_continuo = None
        self.hilo_disparo_continuo2= None

    def disparar(self, origen_x, origen_y, direccion,jugador,modD=1):
        from main import Bala, balas_sprites

        def disparar_balas():

                nueva_bala = Bala(self.daño*modD, self.velocidadProyectil, self.sprite_bala, origen_x, origen_y,direccion,
                                  self.perforacion, self.prob_critica, arma=self, eficiencia=0.6, tipo="misil")
                balas_sprites.add(nueva_bala)
                return nueva_bala


        # Disparar las balas inicialmente
        nueva_bala = disparar_balas()
        for mejora in jugador.mejoras:
            if hasattr(mejora, 'aplicar_dis'):
                mejora.aplicar_dis(jugador, nueva_bala)
        # Función para disparar nuevamente después de un tiempo
        def repetir_disparo(tiempo):
            time.sleep(tiempo)
            disparar_balas()

        # Iniciar los hilos para disparar nuevamente después de 0.2 y 0.4 segundos
        if self.hilo_disparo_continuo is None or not self.hilo_disparo_continuo.is_alive():
            self.hilo_disparo_continuo = threading.Thread(target=repetir_disparo, args=(0.1,))
            self.hilo_disparo_continuo2 = threading.Thread(target=repetir_disparo, args=(0.2,))
            self.hilo_disparo_continuo.start()
            self.hilo_disparo_continuo2.start()

tri=TriRocket()
armas_raras.append(TriRocket)

class Cristalisis(Arma):
    def __init__(self):
        super().__init__(
            nombre="Cristalisis",
            daño=13,
            velocidad=0.8,
            calentamiento=3,
            tipo="Primaria",
            sprite=pygame.image.load('Sprites/Armas/Cristalisis.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/Crystal_ball.png').convert_alpha(),
            velocidadProyectil=6,
            perforacion=1,
        )

    def impacto(self,objetivo,bala):
        from main import Bala,balas_sprites,jugador
        for _ in range(3):
            direccion = (random.uniform(-1, 1), random.uniform(-1, 1))
            while direccion == (0, 0):
                direccion = (random.uniform(-1, 1), random.uniform(-1, 1))
            direccion_normalizada = pygame.math.Vector2(direccion).normalize()

            nueva_bala = Bala(
                self.daño/2,
                4,
                pygame.image.load('Sprites/Armas/Balas/Crystal_shard.png').convert_alpha(),
                objetivo.rect.centerx,
                objetivo.rect.centery,
                direccion_normalizada,
                2,
                )
            nueva_bala.impactos.add(objetivo)
            for mejora in jugador.mejoras:
                if hasattr(mejora, 'aplicar_dis'):
                    mejora.aplicar_dis(jugador, nueva_bala)
            balas_sprites.add(nueva_bala)

armas_raras.append(Cristalisis)

class PCristalisis(Arma):
    def __init__(self):
        super().__init__(
            nombre="Pink Cristalisis",
            daño=9,
            velocidad=1.1,
            calentamiento=5,
            tipo="Primaria",
            sprite=pygame.image.load('Sprites/Armas/PCristalisis.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/PCrystal_ball.png').convert_alpha(),
            velocidadProyectil=8,
            perforacion=1,
        )

    def impacto(self,objetivo,bala):
        from main import Bala,balas_sprites,jugador
        for _ in range(5):
            direccion = (random.uniform(-1, 1), random.uniform(-1, 1))
            while direccion == (0, 0):
                direccion = (random.uniform(-1, 1), random.uniform(-1, 1))
            direccion_normalizada = pygame.math.Vector2(direccion).normalize()

            nueva_bala = Bala(
                self.daño/3,
                3,
                pygame.image.load('Sprites/Armas/Balas/PCrystal_shard.png').convert_alpha(),
                objetivo.rect.centerx,
                objetivo.rect.centery,
                direccion_normalizada,
                1,
                )
            nueva_bala.impactos.add(objetivo)
            for mejora in jugador.mejoras:
                if hasattr(mejora, 'aplicar_dis'):
                    mejora.aplicar_dis(jugador, nueva_bala)
            balas_sprites.add(nueva_bala)
armas_raras.append(PCristalisis)

class GhostShroom(Arma):
    def __init__(self):
        super().__init__(
            nombre="Ghost Shroom",
            daño=8,
            velocidad=0.4,
            calentamiento=0,
            tipo="Primaria",
            sprite=pygame.image.load('Sprites/Armas/GhostShroom.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/GhostSpores.png').convert_alpha(),
            velocidadProyectil=1,
            perforacion=0,
            distancia_maxima=350
        )

    def disparar(self, origen_x, origen_y, direccion,jugador,modD=1):
        from main import Bala_temporal,balas_sprites
        nueva_bala = Bala_temporal(0, self.velocidadProyectil, self.sprite_bala, origen_x -16, origen_y-16, direccion, prob_critica=self.prob_critica, arma=self,duracion=2000,eficiencia=0.4)
        balas_sprites.add(nueva_bala)
        for mejora in jugador.mejoras:
            if hasattr(mejora, 'aplicar_dis'):
                mejora.aplicar_dis(jugador, nueva_bala)

    def impacto(self,objetivo,bala):
        from main import Bala_temporal, balas_sprites
        nueva_bala = Bala_temporal(self.daño, self.velocidadProyectil, self.sprite_bala, objetivo.rect.centerx,
                                   objetivo.rect.centery, [0,0], prob_critica=self.prob_critica, duracion=1000,
                                   eficiencia=0.4)
        balas_sprites.add(nueva_bala)
armas_raras.append(GhostShroom)

class NigthShroom(Arma):
    def __init__(self):
        super().__init__(
            nombre="Nigth Shroom",
            daño=2,
            velocidad=0.25,
            calentamiento=4,
            tipo="Secundaria",
            sprite=pygame.image.load('Sprites/Armas/NightShroom.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/NightSpores.png').convert_alpha(),
            velocidadProyectil=1,
            perforacion=0,
            distancia_maxima=350
        )

    def disparar(self, origen_x, origen_y, direccion,jugador,modD=1):
        from main import Bala_temporal,balas_sprites
        nueva_bala = Bala_temporal(self.daño*modD, self.velocidadProyectil, self.sprite_bala, origen_x-16, origen_y-16, direccion, prob_critica=self.prob_critica, arma=self,duracion=2000,eficiencia=0.4)
        balas_sprites.add(nueva_bala)
        for mejora in jugador.mejoras:
            if hasattr(mejora, 'aplicar_dis'):
                mejora.aplicar_dis(jugador, nueva_bala)

    def impacto(self,objetivo,bala):
        objetivo.EnQuemadura += 2
        objetivo.EnDescomposicion +=2
armas_raras.append((NigthShroom))
class DragonRifle(Arma):
    def __init__(self):
        super().__init__(
            nombre="Dragon Rifle",
            daño=23,
            velocidad=1.2,
            calentamiento=3,
            tipo="Primaria",
            sprite=pygame.image.load('Sprites/Armas/DragonRifle.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/Flame2.png').convert_alpha(),
            velocidadProyectil=6,
            perforacion=1,
        )

    def impacto(self,objetivo,bala):
        from main import Bala_temporal,balas_sprites
        objetivo.EnQuemadura+=2
        if type(bala) != Bala_temporal:
            nueva_bala = Bala_temporal(10, 0,
                                   pygame.image.load("Sprites/Armas/Balas/Fire_circle.png", ).convert_alpha(),
                                   objetivo.rect.x, objetivo.rect.y, [0,0], 2000, tipo="Aceite", eficiencia=0.2, arma=self)
            balas_sprites.add(nueva_bala)

Dragonrifle=DragonRifle()
armas_legendarias.append(DragonRifle)
class IceDragonRifle(Arma):
    def __init__(self):
        super().__init__(
            nombre="Ice Dragon Rifle",
            daño=27,
            velocidad=0.8,
            calentamiento=0,
            tipo="Secundaria",
            sprite=pygame.image.load('Sprites/Armas/IceDragonRifle.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/Ice_bolt.png').convert_alpha(),
            velocidadProyectil=7,
            perforacion=1,
        )


    def impacto(self,objetivo,bala):
        from main import Bala_temporal,balas_sprites
        objetivo.aplicar_congelamiento(0.1)
        if type(bala)!= Bala_temporal:
            nueva_bala = Bala_temporal(5, 0,
                                       pygame.image.load("Sprites/Armas/Balas/Ice_circle.png", ).convert_alpha(),
                                       objetivo.rect.x, objetivo.rect.y, [0,0], 3000, tipo="Aceite", eficiencia=0.2,arma=self)
            balas_sprites.add(nueva_bala)
armas_legendarias.append(IceDragonRifle)

class SoulShatter(Arma):
    def __init__(self):
        super().__init__(
            nombre="Soul Shatter",
            daño=34,
            velocidad=0.55,
            calentamiento=10,
            tipo="Primaria",
            sprite=pygame.image.load('Sprites/Armas/SoulShatter.png').convert_alpha(),
            sprite_bala=pygame.image.load('Sprites/Armas/Balas/Shatter.png').convert_alpha(),
            velocidadProyectil=18,
            perforacion=6,
            prob_critica=0.5,
            distancia_maxima=650
        )

armas_legendarias.append(SoulShatter)




print(len(armas_normales))
print(len(armas_raras))
print(len(armas_legendarias))
