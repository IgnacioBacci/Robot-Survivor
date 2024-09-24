import pygame
import math
import random
configuracion_enemigos=[]
class Animacion(pygame.sprite.Sprite):
    def __init__(self, posicion, frames, derecha, duracion_frame=100, desaparecer=False):
        super().__init__()
        if derecha:
            self.frames = [pygame.transform.flip(frame, True, False) for frame in frames]
        else:
            self.frames = frames
        self.frame_actual = 0
        self.image = self.frames[self.frame_actual]
        self.rect = self.image.get_rect(center=posicion)
        self.tiempo_ultimo_frame = pygame.time.get_ticks()
        self.duracion_frame = duracion_frame
        self.desaparecer = desaparecer
        self.total_frames = len(frames)
        self.alpha_values = [255 - int(255 * (i / (self.total_frames - 1))) for i in range(self.total_frames)]

        if self.desaparecer:
            # Generar valores de alfa que decrezcan más suavemente
            num_frames = len(frames)
            max_alpha = 255
            min_alpha = 60  # Asegúrate de que no desaparezca completamente muy rápido
            step = (max_alpha - min_alpha) / num_frames
            self.alpha_values = [max_alpha - i * step for i in range(num_frames)]

    def update(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_frame > self.duracion_frame:
            self.frame_actual += 1
            self.tiempo_ultimo_frame = ahora
            if self.frame_actual >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.frame_actual]
                if self.desaparecer:
                    alpha = self.alpha_values[self.frame_actual]
                    self.image.set_alpha(alpha)

# Clase base Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, vida, velocidad, daño, sprite_path, objetivo, valor, boss=False, tipo="Enemigo", ):
        super().__init__()
        self.vida = vida
        self.velocidad = velocidad
        self.velocidad_base = velocidad
        self.daño = daño
        self.path=sprite_path
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.original_image=pygame.image.load(sprite_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.objetivo = objetivo
        self.valor = valor
        self.vida_maxima = vida
        self.mirando_derecha = False
        self.muriendo = False
        self.frame_actual = 0
        self.tiempo_ultimo_frame = 0
        self.duracion_frame = 100
        self.animacion_muerte_hielo = []
        self.boss = boss
        self.barra = boss
        self.tipo = tipo
        self.angulo_actual=None
        self.actualizado=False
        self.colision=True
        self.EnDescomposicion=0
        self.ultima_descomposicion=0
        self.EnQuemadura=0
        self.ultima_quemadora=0
        self.congelado=0
        self.evasion_timer=0
        self.tiempo=0

    def rotar1(self):
        if self.mirando_derecha:
            self.image = pygame.transform.flip(self.image, True, False)
            self.mirando_derecha = not self.mirando_derecha

    def rotar2(self):
        if not self.mirando_derecha:
            self.image = pygame.transform.flip(self.image, True, False)
            self.mirando_derecha = not self.mirando_derecha

    def mover_hacia_objetivo(self):
        dx = self.objetivo.base.rect.x - self.rect.x
        dy = self.objetivo.base.rect.y - self.rect.y
        distancia = math.sqrt(dx ** 2 + dy ** 2)

        if self.velocidad <= 0:
            from main import animaciones, enemigos_sprites
            self.morir()
            animacion = Animacion(self.rect.center, self.animacion_muerte_hielo, self.mirando_derecha)
            animaciones.add(animacion)
            return  # Salir del método si el enemigo ha muerto

        if distancia > 0:
            # Normalizar el vector de dirección
            direccion_x = dx / distancia
            direccion_y = dy / distancia

            # Calcular las velocidades en x e y usando la velocidad deseada
            velocidad_x = self.velocidad * direccion_x
            velocidad_y = self.velocidad * direccion_y

            # Ajustar la posición del enemigo
            self.rect.x += velocidad_x
            self.rect.y += velocidad_y

            # Rotar según la dirección de movimiento
            if velocidad_x > 0 and not self.mirando_derecha:
                self.rotar2()
            elif velocidad_x < 0 and self.mirando_derecha:
                self.rotar1()

    def rotar_en_circulos(self):
        if self.velocidad <= 0:
            from main import animaciones, enemigos_sprites
            self.morir()
            animacion = Animacion(self.rect.center, self.animacion_muerte_hielo, self.mirando_derecha)
            animaciones.add(animacion)
        dx = self.objetivo.base.rect.centerx - self.rect.centerx
        dy = self.objetivo.base.rect.centery - self.rect.centery
        distancia = math.sqrt(dx ** 2 + dy ** 2)

        if 297 <= distancia <= 300:
            centro_x = self.objetivo.base.rect.centerx
            centro_y = self.objetivo.base.rect.centery
            radio = 299

            # Calcular el ángulo actual basándose en la posición actual del enemigo
            self.angulo_actual = math.atan2(self.rect.centery - centro_y, self.rect.centerx - centro_x)

            # Incrementa el ángulo para mover el enemigo en un círculo
            self.angulo_actual += (self.velocidad * 0.75) / radio

            # Calcula la nueva posición en el círculo
            nueva_x = centro_x + radio * math.cos(self.angulo_actual)
            nueva_y = centro_y + radio * math.sin(self.angulo_actual)

            # Mueve el enemigo a la nueva posición
            self.rect.centerx = nueva_x
            self.rect.centery = nueva_y

            # Evitar la superposición con otros enemigos
            self.evitar_superposicion()

            angulo_grados = math.degrees(self.angulo_actual)
            if 90 <= angulo_grados <= 270 and not self.mirando_derecha:
                self.rotar1()
            elif (angulo_grados < 90 or angulo_grados > 270) and self.mirando_derecha:
                self.rotar2()

        elif distancia > 300:
            # Si está a más de 300 de distancia, dirígete hacia el jugador
            if distancia > 0:
                velocidad_x = (dx / distancia) * self.velocidad
                velocidad_y = (dy / distancia) * self.velocidad

                self.rect.centerx += velocidad_x
                self.rect.centery += velocidad_y

                # Evitar la superposición con otros enemigos
                self.evitar_superposicion()

                # Rotar según la dirección de movimiento
                if velocidad_x > 0 and not self.mirando_derecha:
                    self.rotar2()
                elif velocidad_x < 0 and self.mirando_derecha:
                    self.rotar1()
        elif distancia < 297:
            if distancia > 0:
                # Calcula las velocidades invertidas para dirigirse hacia el jugador
                velocidad_x = -(dx / distancia) * self.velocidad
                velocidad_y = -(dy / distancia) * self.velocidad

                self.rect.centerx += velocidad_x
                self.rect.centery += velocidad_y

                # Evitar la superposición con otros enemigos
                self.evitar_superposicion()

                # Rotar según la dirección de movimiento
                if velocidad_x > 0 and not self.mirando_derecha:
                    self.rotar2()
                elif velocidad_x < 0 and self.mirando_derecha:
                    self.rotar1()

    def evitar_superposicion(self):
        if self.colision:
            from main import enemigos_sprites
            colisiones = pygame.sprite.spritecollide(self, enemigos_sprites, False)
            for enemigo in colisiones:
                if enemigo != self:
                    # Calcula la distancia y dirección del otro enemigo
                    dx = self.rect.centerx - enemigo.rect.centerx
                    dy = self.rect.centery - enemigo.rect.centery
                    distancia = math.sqrt(dx ** 2 + dy ** 2)

                    if distancia > 0:
                        # Intentar encontrar una ruta alternativa
                        angulo_alternativo = math.atan2(dy, dx) + random.uniform(-math.pi / 4, math.pi / 4)
                        velocidad_alternativa_x = self.velocidad * math.cos(angulo_alternativo)
                        velocidad_alternativa_y = self.velocidad * math.sin(angulo_alternativo)

                        # Verificar si la nueva posición es válida
                        nueva_posicion_x = self.rect.x + velocidad_alternativa_x
                        nueva_posicion_y = self.rect.y + velocidad_alternativa_y

                        # Actualizar la posición si es válida
                        self.rect.x = nueva_posicion_x
                        self.rect.y = nueva_posicion_y

                        # Rotar según la dirección de movimiento alternativa
                        if velocidad_alternativa_x > 0 and not self.mirando_derecha:
                            self.rotar2()
                        elif velocidad_alternativa_x < 0 and self.mirando_derecha:
                            self.rotar1()

                        # Activar el temporizador de evasión
                        self.evasion_timer = 30  # Número de frames para mantener la evasión
                        break

    def soltar_recurso(self):
        from main import exp_sprites,sprite_exp1,sprite_exp2,sprite_exp3,Exp
        coordenadas=self.rect.center
        if 1<self.valor < 150:
            nuevo_recurso = Exp(sprite_exp1, *coordenadas, nivel=1)
        elif 150<=self.valor < 500:
            nuevo_recurso = Exp(sprite_exp2, *coordenadas, nivel=2)
        elif 500 <= self.valor:
            nuevo_recurso = Exp(sprite_exp3, *coordenadas, nivel=3)
        elif self.valor==1:
            return None
        exp_sprites.add(nuevo_recurso)

    def danio(self,daño,color_daño):
        from main import numeros_de_dano,DamageNumber
        if daño >=1:
            self.vida -= daño
            texto_daño = str(daño)
            coordenadas_enemigo = (self.rect.x, self.rect.y)
            if len(numeros_de_dano) < 10:
                nuevo_dano = DamageNumber(texto_daño, coordenadas_enemigo[0], coordenadas_enemigo[1], color_daño)
                numeros_de_dano.append(nuevo_dano)
            self.barra=True

    def morir(self):
        from main import enemigos_sprites,jugador
        self.soltar_recurso()
        enemigos_sprites.remove(self)
        if self.boss:
            from main import crear_portal,boss_spawn,spawn
            crear_portal(boss_spawn)
            boss_spawn.kill()
            spawn=False
        jugador.puntaje += self.valor

    def aumentar_danio_y_vida(self,presu):
        if not self.actualizado:
            self.daño *= round(0.7 + (presu/500))
            self.vida_maxima *= round(1+(presu/400))
            self.vida *= round(1 + (presu/400))
            self.velocidad_base += round(0.02 * (presu/800))
            self.actualizado=True

    def barra_vida(self):
        from main import pantalla
        if self.barra:
            if self.boss:
                pantalla_ancho = pantalla.get_width()
                barra_ancho = int((pantalla_ancho - pantalla_ancho / 3) * (self.vida / self.vida_maxima))
                barra_fondo_rect = pygame.Rect(pantalla_ancho / 6, 70, pantalla_ancho - pantalla_ancho / 3, 15)
                barra_vida_rect = pygame.Rect(pantalla_ancho / 6, 70, barra_ancho, 15)

                # Dibujar la barra de vida del jefe en la parte superior de la pantalla
                pygame.draw.rect(pantalla, (130, 0, 0), barra_fondo_rect)
                pygame.draw.rect(pantalla, (230, 0, 0), barra_vida_rect)

                # Crear la fuente para el texto
                fuente = pygame.font.Font(None, 20)
                texto = f"{int(self.vida)}/{int(self.vida_maxima)}"
                texto_surface = fuente.render(texto, True, (0, 0, 0))
                texto_rect = texto_surface.get_rect(center=(pantalla_ancho / 2, 77))

                # Dibujar el texto sobre la barra de vida
                pantalla.blit(texto_surface, texto_rect)
            else:
                # Obtener el ancho del sprite del enemigo
                sprite_ancho = self.rect.width

                # Calcular el ancho de la barra de vida basada en la salud actual y el ancho del sprite
                barra_ancho = int(sprite_ancho * (self.vida / self.vida_maxima))
                barra_fondo_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height + 2, sprite_ancho, 5)
                barra_vida_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height + 2, barra_ancho, 5)

                # Dibujar la barra de vida en la pantalla
                pygame.draw.rect(pantalla, (130, 0, 0), barra_fondo_rect)
                pygame.draw.rect(pantalla, (230, 0, 0), barra_vida_rect)

    def update(self):
        if pygame.time.get_ticks() - self.tiempo >= 500:
            if self.EnQuemadura >0:
                self.apply_color_filter((224, 155, 71))
            elif self.EnDescomposicion>0:
                self.apply_color_filter(((28,36,27)))
            elif self.congelado>0:
                self.apply_color_filter((162, 240, 217))
            else:
                self.image=self.original_image
            self.tiempo=pygame.time.get_ticks()
        self.mover_hacia_objetivo()
        self.barra_vida()
        self.ataque()
        if pygame.time.get_ticks() - self.ultima_quemadora >= 1000 and self.EnQuemadura>0:
            self.quemadura()
        if pygame.time.get_ticks() - self.ultima_descomposicion >= 500 and self.EnDescomposicion>0:
            self.descoposicion()

    def ataque(self):
        pass

    def descoposicion(self):
        self.danio(self.vida_maxima/10,(28,36,27))
        self.ultima_descomposicion = pygame.time.get_ticks()
        self.EnDescomposicion -=1

    def descomponer(self,duracion):
        self.EnDescomposicion +=duracion
    def quemadura(self):
        if self.EnQuemadura > 10:
            self.EnQuemadura=10
        self.danio(self.EnQuemadura,(224,155,71))
        self.ultima_quemadora=pygame.time.get_ticks()
        self.EnQuemadura-=1


    def quemar(self,duracion):
        self.EnQuemadura+=duracion

    def aplicar_congelamiento(self, congelamiento):
        if not self.boss:
            if self.velocidad <= 0.70:
                self.velocidad = 0
            else:
                self.velocidad -= congelamiento
            self.congelado+=congelamiento

    def apply_color_filter(self, color, porcentaje=0.2):
        # Asegurarse de que el porcentaje esté entre 0 y 1
        porcentaje = max(0, min(1, porcentaje))

        # Restaurar la imagen original
        self.image = self.original_image.copy()

        # Obtener el tamaño de la imagen
        width, height = self.image.get_size()

        # Bloquear la superficie para el acceso de píxeles directo
        self.image.lock()

        for x in range(width):
            for y in range(height):
                # Obtener el color actual del píxel
                color_actual = self.image.get_at((x, y))

                # Mezclar los componentes de color del píxel con los del color objetivo
                nuevo_color = (
                    int(color_actual.r * (1 - porcentaje) + color[0] * porcentaje),
                    int(color_actual.g * (1 - porcentaje) + color[1] * porcentaje),
                    int(color_actual.b * (1 - porcentaje) + color[2] * porcentaje),
                    color_actual.a  # Mantener el canal alfa original
                )

                # Establecer el nuevo color del píxel
                self.image.set_at((x, y), nuevo_color)

        # Desbloquear la superficie
        self.image.unlock()

# Clase intermedia Slime

def dash(slime, tiempo_inicio, tiempo_color_cambio):
    tiempo_actual = pygame.time.get_ticks()

    # Si ha pasado suficiente tiempo y el ataque rápido no ha comenzado aún
    if tiempo_actual - tiempo_inicio >= tiempo_color_cambio and not hasattr(slime, 'velocidad_rapida'):
        slime.velocidad_rapida = slime.velocidad*3  # Velocidad aumentada para el ataque
        slime.distancia_recorrida = 0  # Iniciar la distancia recorrida
        slime.direccion_ataque = pygame.math.Vector2(slime.posicion_inicial_jugador) - pygame.math.Vector2(
            slime.rect.center)
        slime.direccion_ataque.normalize_ip()  # Normalizar la dirección
    elif hasattr(slime, 'velocidad_rapida'):
        movimiento = slime.direccion_ataque * slime.velocidad_rapida
        slime.rect.centerx += movimiento.x
        slime.rect.centery += movimiento.y
        slime.distancia_recorrida += movimiento.length()  # Acumular la distancia recorrida

        # Comprobar si el Angry_Slime ha recorrido la distancia de 500 unidades
        if slime.distancia_recorrida >= 700:
            slime.is_attacking = False
            slime.image = slime.original_color  # Volver al color original
            del slime.velocidad_rapida  # Eliminar la velocidad aumentada

class Slime(Enemigo):
    def __init__(self, vida, velocidad, daño, sprite_path, valor, boss=False, objetivo=None):
        super().__init__(vida, velocidad, daño, sprite_path, objetivo, valor, boss, tipo="Slime")
        self.animacion_muerte_hielo = [
            pygame.image.load("Sprites/Enemigos/Slime_ice_death/Slime_ice_death1.png"),
            pygame.image.load("Sprites/Enemigos/Slime_ice_death/Slime_ice_death2.png"),
            pygame.image.load("Sprites/Enemigos/Slime_ice_death/Slime_ice_death3.png"),
            pygame.image.load("Sprites/Enemigos/Slime_ice_death/Slime_ice_death4.png"),
            pygame.image.load("Sprites/Enemigos/Slime_ice_death/Slime_ice_death5.png"),
            pygame.image.load("Sprites/Enemigos/Slime_ice_death/Slime_ice_death6.png")
        ]

    def ataque(self):
        # Método de ataque común para Slimes
        pass

# Clases específicas de enemigos
class Ugly_Slime(Slime):
    def __init__(self, objetivo=None):
        super().__init__(vida=20, velocidad=0.9, daño=23, sprite_path='Sprites/Enemigos/Enemigo-1.png', valor=3,
                         objetivo=objetivo)

    def ataque(self):
        # Implementa el ataque específico de Ugly_Slime
        pass
    def morir(self):
        if self.vida_maxima >=60:
            distancia=32
            for i in range(2):
                from main import enemigos_sprites
                nuevo=Ugly_Slime(objetivo=self.objetivo)
                nuevo.vida_maxima = self.vida_maxima/2
                nuevo.vida= nuevo.vida_maxima
                nuevo.image = pygame.transform.scale(self.image, (self.rect.width * 0.8, self.rect.height * 0.8))
                nuevo.rect.x=self.rect.x + (distancia*i)
                nuevo.rect.y=self.rect.y
                enemigos_sprites.add(nuevo)
        super().morir()
class Angry_Slime(Slime):
    def __init__(self, objetivo=None):
        super().__init__(vida=50, velocidad=1, daño=60, sprite_path='Sprites/Enemigos/Enemigo-2.png', valor=20,
                         objetivo=objetivo)
        self.original_color = self.image.copy()  # Guardar el sprite original
        self.is_attacking = False  # Estado de si está en proceso de ataque especial
        self.tiempo_color_cambio = 600  # Tiempo en ms para quedarse quieto y cambiar de color
        self.tiempo_inicio = 0  # Inicializar el tiempo de inicio
        self.posicion_inicial_jugador = None  # Inicializar la posición inicial del jugador
        self.cd=3500
        self.ultimo_ataque=0

    def ataque(self):
        from main import jugador
        if self.daño >= 340:
            # Calcular la distancia al jugador
            distancia = pygame.math.Vector2(self.rect.center).distance_to(jugador.base.rect.center)
            tiempo_actual=pygame.time.get_ticks()
            if (300 < distancia < 450 and not self.is_attacking) and tiempo_actual-self.cd >= self.ultimo_ataque:
                self.iniciar_ataque_especial()
                self.ultimo_ataque=pygame.time.get_ticks()

    def iniciar_ataque_especial(self):
        from main import jugador
        self.is_attacking = True
        self.tiempo_inicio = pygame.time.get_ticks()
        self.posicion_inicial_jugador = jugador.base.rect.center
        self.image.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_ADD)  # Cambiar el color a rojizo

    def update(self):
        if self.is_attacking:
            dash(self, self.tiempo_inicio, self.tiempo_color_cambio)
            self.barra_vida()
        else:
            super().update()

class Fast_Slime(Slime):
    def __init__(self, objetivo=None):
        super().__init__(vida=80, velocidad=1.4, daño=70, sprite_path='Sprites/Enemigos/Enemigo-3.png', valor=90,
                         objetivo=objetivo)
        self.colision=False

    def ataque(self):
        # Implementa el ataque específico de Fast_Slime
        pass

class Tank_Slime(Slime):
    def __init__(self, objetivo=None):
        super().__init__(vida=120, velocidad=0.9, daño=120, sprite_path='Sprites/Enemigos/Enemigo-4.png', valor=130,
                         objetivo=objetivo)

    def ataque(self):
        # Implementa el ataque específico de Tank_Slime
        pass

    def update(self):
        if self.vida_maxima >= 300:
            if self.vida < self.vida_maxima:
                self.vida += ((self.vida_maxima/10) / 60)
        super().update()

class Pink_Slime(Slime):
    def __init__(self, objetivo=None):
        super().__init__(vida=100, velocidad=1.1, daño=100, sprite_path='Sprites/Enemigos/Enemigo-5.png', valor=180,
                         objetivo=objetivo)
        self.tiempo_entre_ataques = 5000
        self.tiempo_ultimo_ataque=0

    def ataque(self):
        if pygame.time.get_ticks() - self.tiempo_entre_ataques>=self.tiempo_ultimo_ataque:
            from main import Bala, balas_enemigos
            from mejoras import calcular_direccion
            direccion=calcular_direccion(self.objetivo,self)
            nueva_bala =Bala(self.daño / 2, 5+(self.velocidad/2),
                                    pygame.image.load('Sprites/Enemigos/Two-Headed-Slime/Two-Slime-At.png').convert_alpha(),
                                    self.rect.x, self.rect.y, direccion, 1, distancia=550)
            balas_enemigos.add(nueva_bala)
            self.tiempo_ultimo_ataque=pygame.time.get_ticks()

    def update(self):

        self.ataque()
        self.rotar_en_circulos()
        self.barra_vida()

class Two_Headed_Slime(Slime):
    def __init__(self, objetivo=None):
        super().__init__(vida=240, velocidad=1.4, daño=20, sprite_path='Sprites/Enemigos/Two-Headed-Slime/Two-Slime.png', valor=3000,
                         boss=False, objetivo=objetivo)
        self.num = 0
        self.ultimo_ataque = 0
        self.timer = pygame.time.get_ticks()
        self.tiempo_entre_ataques = 4000
        self.intervalo = 500
        self.animacion_ataque=[
            pygame.image.load("Sprites/Enemigos/Two-Headed-Slime/Two-Slime-Attack1.png"),
            pygame.image.load("Sprites/Enemigos/Two-Headed-Slime/Two-Slime-Attack2.png"),
            pygame.image.load("Sprites/Enemigos/Two-Headed-Slime/Two-Slime-Attack3.png"),
            pygame.image.load("Sprites/Enemigos/Two-Headed-Slime/Two-Slime-Attack4.png"),
            pygame.image.load("Sprites/Enemigos/Two-Headed-Slime/Two-Slime-Attack5.png"),
            pygame.image.load("Sprites/Enemigos/Two-Headed-Slime/Two-Slime-Attack6.png"),
            pygame.image.load("Sprites/Enemigos/Two-Headed-Slime/Two-Slime-Attack7.png")
        ]
        self.sprite_original = self.image
        self.animando = False
        self.tiempo_ultimo_frame = 0
        self.frame_actual = 0
        self.duracion_frame = 100


    def ataque(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_ataque >= self.tiempo_entre_ataques:
            self.ultimo_ataque = tiempo_actual
            self.num = random.randint(1, 3)
            if self.num == 1:
                print("Invocar")
                self.invocar_enemigos()
            elif self.num == 2:
                print("Disparando")
                self.tipo_ataque_2()
            elif self.num == 3:
                self.tipo_ataque_3()
        if not self.animando:
            if tiempo_actual - self.ultimo_ataque >= self.tiempo_entre_ataques:
                self.animando = True
                self.frame_actual = 0
                self.image = self.animacion_ataque[self.frame_actual]
                self.tiempo_ultimo_frame = tiempo_actual
                self.ultimo_ataque = tiempo_actual  # Actualizar el tiempo del último ataque para el siguiente ciclo
        else:
            if tiempo_actual - self.tiempo_ultimo_frame >= self.duracion_frame:
                self.tiempo_ultimo_frame = tiempo_actual
                self.frame_actual += 1
                if self.frame_actual >= len(self.animacion_ataque):
                    self.frame_actual = 0
                    self.animando = False
                    self.image = self.sprite_original
                    self.tipo_ataque_2()
                else:
                    self.image = self.animacion_ataque[self.frame_actual]

    def invocar_enemigos(self):
        from main import enemigos_sprites
        for _ in range(4):
            nuevo_enemigo = Enemigo(vida=self.vida/100, velocidad=(1.3+(_*0.1)), daño=self.daño/5, sprite_path='Sprites/Enemigos/Two-Headed-Slime/Slimy.png',
                                    objetivo=self.objetivo, valor=1, boss=False)
            nuevo_enemigo.rect.center = self.rect.center
            enemigos_sprites.add(nuevo_enemigo)

    def tipo_ataque_2(self):
        from main import balas_enemigos, Bala
        from mejoras import calcular_direccion

        # Calcular la dirección hacia el objetivo
        direccion_original = calcular_direccion(self.objetivo, self)

        # Convertir la dirección a un vector unitario
        distancia = math.sqrt(direccion_original[0] ** 2 + direccion_original[1] ** 2)
        if distancia != 0:
            direccion_unitaria = (direccion_original[0] / distancia, direccion_original[1] / distancia)
        else:

            direccion_unitaria = (0, 0)

        # Calcular el ángulo en radianes para desviar las balas
        angulo_desvio = math.radians(10)  # 15 grados de desviación

        # Calcular las direcciones desviadas usando rotación
        def rotar_vector(vector, angulo):
            x, y = vector
            cos_ang = math.cos(angulo)
            sin_ang = math.sin(angulo)
            return (x * cos_ang - y * sin_ang, x * sin_ang + y * cos_ang)

        direccion_izquierda = rotar_vector(direccion_unitaria, -angulo_desvio)
        direccion_derecha = rotar_vector(direccion_unitaria, angulo_desvio)

        # Crear las tres balas con las direcciones calculadas
        nueva_bala_centro = Bala(self.daño / 2, 6,
                                 pygame.image.load('Sprites/Enemigos/Two-Headed-Slime/Two-Slime-At.png').convert_alpha(),
                                 self.rect.x, self.rect.y, direccion_unitaria, 1, distancia=1100)
        nueva_bala_izquierda = Bala(self.daño / 2, 6,
                                    pygame.image.load('Sprites/Enemigos/Two-Headed-Slime/Two-Slime-At.png').convert_alpha(),
                                    self.rect.x, self.rect.y, direccion_izquierda, 1, distancia=1100)
        nueva_bala_derecha = Bala(self.daño / 2, 6,
                                  pygame.image.load('Sprites/Enemigos/Two-Headed-Slime/Two-Slime-At.png').convert_alpha(),
                                  self.rect.x, self.rect.y, direccion_derecha, 1, distancia=1100)

        # Agregar las balas al grupo de sprites de balas enemigas
        balas_enemigos.add(nueva_bala_centro)
        balas_enemigos.add(nueva_bala_izquierda)
        balas_enemigos.add(nueva_bala_derecha)

    def tipo_ataque_3(self):
        pass
        from main import balas_enemigos, Bala_temporal
        from mejoras import calcular_direccion
        direccion=calcular_direccion(self.objetivo,self)
        nueva_bala=Bala_temporal(self.daño/4, 3,
                                      pygame.image.load("Sprites\\Enemigos\\Two-Headed-Slime\\Two-Slime-At2.png",).convert_alpha(),
                                      self.rect.x, self.rect.y, direccion, 3000, tipo="Rastreo")
        balas_enemigos.add(nueva_bala)

    def update(self):
        self.ataque()
        self.rotar_en_circulos()
        self.barra_vida()

class Cofre(Enemigo):
    def __init__(self, vida, velocidad, daño, sprite_path, valor, boss=False, objetivo=None):
        super().__init__(vida, velocidad, daño, sprite_path, objetivo, valor, boss, tipo="Cofre")

    def mover_hacia_objetivo(self):
        pass
class CofreN(Cofre):
    def __init__(self, objetivo=None):
        super().__init__(vida=100, velocidad=0, daño=0, sprite_path='Sprites/Recursos/Chest1.png', valor=0,
                         boss=False, objetivo=objetivo)

    def soltar_recurso(self):
        from main import Exp,exp_sprites,sprite_exp1,arma_sprites
        from weapons import armas_normales
        coordenadas = self.rect.center
        num=random.randint(3,5)
        for i in range(num):
            nuevo_recurso = Exp(sprite_exp1, coordenadas[0]+random.randint(-50,50), coordenadas[1]+random.randint(-50,50), nivel=1)
            exp_sprites.add(nuevo_recurso)

        # Seleccionar y soltar un arma aleatoria
        arma_clase = random.choice(armas_normales)
        nueva_arma = arma_clase()  # Crear una instancia del arma seleccionada
        nueva_arma.rect.center = (coordenadas[0] + random.randint(-50, 50), coordenadas[1] + random.randint(-50, 50))
        arma_sprites.add(nueva_arma)
class CofreR(Cofre):
    def __init__(self, objetivo=None):
        super().__init__(vida=200, velocidad=0, daño=0, sprite_path='Sprites/Recursos/Chest2.png', valor=0,
                         boss=False, objetivo=objetivo)

    def soltar_recurso(self):
        from main import Exp,exp_sprites,sprite_exp2,arma_sprites
        from weapons import armas_raras
        coordenadas = self.rect.center
        num=random.randint(3,6)
        for i in range(num):
            nuevo_recurso = Exp(sprite_exp2, coordenadas[0]+random.randint(-50,50), coordenadas[1]+random.randint(-50,50), nivel=1)
            exp_sprites.add(nuevo_recurso)


        # Seleccionar y soltar un arma aleatoria
        arma_clase = random.choice(armas_raras)
        nueva_arma = arma_clase()  # Crear una instancia del arma seleccionada
        nueva_arma.rect.center = (coordenadas[0] + random.randint(-50, 50), coordenadas[1] + random.randint(-50, 50))
        arma_sprites.add(nueva_arma)
class CofreL(Cofre):
    def __init__(self, objetivo=None):
        super().__init__(vida=300, velocidad=0, daño=0, sprite_path='Sprites/Recursos/Chest3.png', valor=0,
                         boss=False, objetivo=objetivo)

    def soltar_recurso(self):
        from main import Exp,exp_sprites,sprite_exp2,arma_sprites
        from weapons import armas_legendarias
        coordenadas = self.rect.center
        num=random.randint(5,14)
        for i in range(num):
            nuevo_recurso = Exp(sprite_exp2, coordenadas[0]+random.randint(-50,50), coordenadas[1]+random.randint(-50,50), nivel=1)
            exp_sprites.add(nuevo_recurso)

            # Seleccionar y soltar un arma aleatoria
        arma_clase = random.choice(armas_legendarias)
        nueva_arma = arma_clase()  # Crear una instancia del arma seleccionada
        nueva_arma.rect.center = (
        coordenadas[0] + random.randint(-50, 50), coordenadas[1] + random.randint(-50, 50))
        arma_sprites.add(nueva_arma)

class Cristal(Enemigo):
    def __init__(self, objetivo=None):
        super().__init__(vida=70, velocidad=0, daño=5, sprite_path='Sprites/Recursos/Crystal.png', valor=25,
                         boss=False, objetivo=objetivo)
        self.tipo="Cristal"


    def update(self):
        from main import enemigos_sprites
        for enemigo in enemigos_sprites:
            if enemigo.boss:
                enemigo.vida_maxima +=1/60
                enemigo.daño +=0.25/60
                if enemigo.vida < enemigo.vida_maxima:
                    enemigo.vida = enemigo.vida_maxima
        self.barra_vida()





def spawn_enemigos(enemigos_sprites, jugador):
    from main import presupuesto_invocacion,etapa_actual
    if len(enemigos_sprites) <= 150:
        valor_total = 0
        enemigos_disponibles = etapa_actual.enemy_configs.copy()
        while presupuesto_invocacion >= 1 and enemigos_disponibles:
            enemigo_clase = random.choice(enemigos_disponibles)
            enemigo = enemigo_clase(objetivo=jugador)
            if enemigo.valor + valor_total <= presupuesto_invocacion:
                # Calcular un ángulo aleatorio en radianes
                angulo_rad = random.uniform(0, 2 * math.pi)

                 # Calcular la posición relativa en el círculo
                radio = random.uniform(600, 700)
                pos_x_rel = radio * math.cos(angulo_rad)
                pos_y_rel = radio * math.sin(angulo_rad)

                # Calcular las coordenadas absolutas en relación con la posición del jugador
                enemigo.rect.x = jugador.base.rect.x + pos_x_rel
                enemigo.rect.y = jugador.base.rect.y + pos_y_rel

                enemigos_sprites.add(enemigo)
                valor_total += enemigo.valor
            else:
                enemigos_disponibles.remove(enemigo_clase)
    presupuesto_invocacion += 2
    presupuesto_invocacion *= 1.01
    nuevo_tiempo_ultimo_spawn_enemigos = pygame.time.get_ticks()
    for enemigo in enemigos_sprites:
        enemigo.aumentar_danio_y_vida(presupuesto_invocacion)
    return presupuesto_invocacion, nuevo_tiempo_ultimo_spawn_enemigos

def spawn_boss(enemigos_sprites,jugador):
    boss_c= random.choice(boss_config)
    boss= boss_c(objetivo=jugador)
    angulo_rad = random.uniform(0, 2 * math.pi)

    # Calcular la posición relativa en el círculo
    radio = random.uniform(750, 800)
    pos_x_rel = radio * math.cos(angulo_rad)
    pos_y_rel = radio * math.sin(angulo_rad)

    # Calcular las coordenadas absolutas en relación con la posición del jugador
    boss.rect.x = jugador.base.rect.x + pos_x_rel
    boss.rect.y = jugador.base.rect.y + pos_y_rel

    enemigos_sprites.add(boss)

enemigos_slime = [
        Ugly_Slime,
        Angry_Slime,
        Pink_Slime,
        Tank_Slime,
        Fast_Slime,
        Two_Headed_Slime
    ]
boss_config=[
        Two_Headed_Slime
    ]




cofres=[CofreN,CofreR,CofreL]