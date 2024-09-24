import threading
import pygame
import random
import math
import time
import copy
import os

from sounds import *
mejoras_normales = []
mejoras_raras = []
mejoras_legendarias=[]
planetas = ["Mercurio", "Venus", "Tierra", "Marte", "Jupiter", "Saturno", "Urano", "Neptuno"]


def redimensionar_animacion(animacion_paths, nuevo_ancho, nuevo_alto):
    sprites_redimensionados = []
    for sprite_path in animacion_paths:
        sprite = pygame.image.load(sprite_path).convert_alpha()
        sprite_redimensionado = pygame.transform.scale(sprite, (nuevo_ancho, nuevo_alto))
        sprites_redimensionados.append(sprite_redimensionado)
    return sprites_redimensionados
def critico(bala,jugador):
    if bala.critico==False:
        multiplicador = 0.5
        if bala.prob_critica > 1:
            bala.prob_critica -=1
            bala.critico=True
            bala.daño *= 1+ multiplicador
        for suerte in range(jugador.suerte):
            if random.random() <= bala.prob_critica:
                bala.critico=True
                bala.daño *= 1 + multiplicador
                break
def encontrar_enemigo_mas_cercano(enemigos_sprites, origen):
    distancia_maxima = 500
    objetivo = None
    distancia_objetivo = float('inf')
    for enemigo in enemigos_sprites:
        if hasattr(origen, 'base'):
            dx = enemigo.rect.x - origen.base.rect.x
            dy = enemigo.rect.y - origen.base.rect.y
            distancia = math.sqrt(dx ** 2 + dy ** 2)
        else:
            dx = enemigo.rect.x - origen.rect.x
            dy = enemigo.rect.y - origen.rect.y
            distancia = math.sqrt(dx ** 2 + dy ** 2)

        if distancia <= distancia_maxima and distancia < distancia_objetivo and enemigo != origen:
            objetivo = enemigo
            distancia_objetivo = distancia
    return objetivo

def calcular_direccion(objetivo, origen):
    # Obtener las coordenadas del origen
    if hasattr(origen, 'arma_primaria'):
        x_origen = origen.arma_primaria.rect.centerx
        y_origen = origen.arma_primaria.rect.centery
    else:
        x_origen = origen.rect.centerx
        y_origen = origen.rect.centery

    if hasattr(objetivo, "base"):
        x_objetivo = objetivo.base.rect.centerx
        y_objetivo = objetivo.base.rect.centery
    # Obtener las coordenadas del objetivo
    else:
        x_objetivo = objetivo.rect.centerx
        y_objetivo = objetivo.rect.centery

    # Calcular el vector de dirección
    dx = x_objetivo - x_origen
    dy = y_objetivo - y_origen

    # Calcular la distancia
    distancia = math.sqrt(dx ** 2 + dy ** 2)

    # Normalizar el vector de dirección
    if distancia > 0:
        return (dx / distancia, dy / distancia)
    else:
        return (0, 0)
def actualizar_orbital(jugador,tipo):
    from main import balas_sprites
    orbital = [bala for bala in balas_sprites if bala.tipo == str(tipo)]
    num_orbitales = len(orbital)
    if num_orbitales == 0:
        return
    # Calcula el ángulo entre cada bala "Orbital"
    angulo_entre_balas = 360 / num_orbitales

    for i, bala in enumerate(orbital):
        # Incrementa el ángulo de la bala para hacerla girar
        bala.angulo = (i * angulo_entre_balas + pygame.time.get_ticks() / bala.velocidadProyectil) % 360
        angulo_rad = math.radians(bala.angulo)
        dist = bala.distancia_maxima # Ajustar el radio del círculo
        bala.rect.centerx = jugador.base.rect.centerx + math.cos(angulo_rad) * bala.distancia_maxima
        bala.rect.centery = jugador.base.rect.centery + math.sin(angulo_rad) * bala.distancia_maxima
        bala.direccion = (math.cos(angulo_rad), math.sin(angulo_rad))

def agregar_planeta(jugador):
    from main import balas_sprites,Bala
    planeta = random.choice(planetas)
    if planeta=="Mercurio":
        direccion = (0, -1)
        nueva_bala = Bala(10, 50,
                          pygame.image.load('Sprites/Armas/Balas/Mercury.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=20)
    elif planeta=="Venus":
        direccion = (0, -1)
        nueva_bala = Bala(15, 49,
                          pygame.image.load('Sprites/Armas/Balas/Venus.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=60)
    elif planeta=="Tierra":
        direccion = (0, -1)
        nueva_bala = Bala(20, 48,
                          pygame.image.load('Sprites/Armas/Balas/Earth.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=100)
    elif planeta=="Marte":
        direccion = (0, -1)
        nueva_bala = Bala(25, 47,
                          pygame.image.load('Sprites/Armas/Balas/Mars.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=140)
    elif planeta=="Jupiter":
        direccion = (0, -1)
        nueva_bala = Bala(30, 46,
                          pygame.image.load('Sprites/Armas/Balas/Jupiter.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=180)
    elif planeta=="Saturno":
        direccion = (0, -1)
        nueva_bala = Bala(35, 45,
                          pygame.image.load('Sprites/Armas/Balas/Saturn.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=220)
    elif planeta=="Urano":
        direccion = (0, -1)
        nueva_bala = Bala(40, 44,
                          pygame.image.load('Sprites/Armas/Balas/Uranus.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=260)
    elif planeta=="Neptuno":
        direccion = (0, -1)
        nueva_bala = Bala(45, 43,
                          pygame.image.load('Sprites/Armas/Balas/Neptune.png').convert_alpha(),
                          jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                          -1, tipo="Orbital Planeta", distancia=300)
    else:
        return None
    planetas.remove(planeta)
    if len(planetas) ==0:
        if Expansion in mejoras_raras:
            mejoras_raras.remove(Expansion)
    balas_sprites.add(nueva_bala)
    print(len(mejoras_raras))


class Mejora:
    def __init__(self,nombre, efecto, rareza, sprite):
        self.valor = 0
        self.nombre = nombre
        self.efecto = efecto
        self.rareza = rareza
        self.sprite = sprite

class Autoreparacion(Mejora):
    def __init__(self, valor=0):
        self.valor = valor
        self.tiempo_ultima_reparacion = 0
        efecto = f"Heal {2 * (self.valor + 1)} per second"
        super().__init__("Self-repair", efecto, "Normal", "Sprites\\Recursos\\Mejoras\\Autoreparacion.png")
    def actualizar_efecto(self):
        self.efecto= f"Heal {2 * (self.valor + 1)} per second"
    def aplicar(self, jugador):
        tiempo_transcurrido = pygame.time.get_ticks()
        tiempo_segundos = tiempo_transcurrido // 1000
        if tiempo_segundos > self.tiempo_ultima_reparacion:
            jugador.base.vida_actual += 2*self.valor
            if jugador.base.vida_actual > jugador.base.vida_maxima:
                jugador.base.vida_actual = jugador.base.vida_maxima

        self.tiempo_ultima_reparacion = tiempo_segundos

Autoreparacion=Autoreparacion()
mejoras_normales.append(Autoreparacion)
class CorazaReforzada(Mejora):
    def __init__(self, valor=0):
        self.valor = valor
        efecto=f"Gain {250*(self.valor+1)} maximum health"
        super().__init__("reinforced armor", efecto, "Normal",
                         "Sprites\\Recursos\\Mejoras\\Coraza_Reforzada.png")
    def actualizar_efecto(self):
        self.efecto= f"Gain {250*(self.valor+1)} maximum health"
    def aplicar_primera(self, jugador):
        jugador.base.vida_maxima += 250

CorazaReforzada=CorazaReforzada()
mejoras_normales.append(CorazaReforzada)
class CalorCurativo(Mejora):
        def __init__(self, valor=0):
            self.valor = valor
            efecto=f"Heal for {15*(self.valor+1)}% of the heat generated"
            super().__init__("Healing heat", efecto, "Normal",
                             "Sprites\\Recursos\\Mejoras\\Calor_Curativo.png")

        def actualizar_efecto(self):
            self.efecto = f"Heal for {15*(self.valor+1)}% of the heat generated"
        def aplicar(self, jugador):
            valor = self.valor * 0.15
            if jugador.base.calor_actual > getattr(jugador, 'calor_anterior', jugador.base.calor_actual):
                Curacion= round((jugador.base.calor_actual - getattr(jugador, 'calor_anterior',jugador.base.calor_actual * valor)))
                jugador.base.vida_actual += Curacion
                if jugador.base.vida_actual > jugador.base.vida_maxima:
                    jugador.base.vida_actual = jugador.base.vida_maxima

            jugador.calor_anterior = jugador.base.calor_actual

CalorCurativo=CalorCurativo()
mejoras_normales.append(CalorCurativo)

class DisparoRafaga(Mejora):
    def __init__(self, valor=0):
        self.valor = valor
        efecto = f"After not shooting for 3 seconds, your rate of fire increases by {100 * (self.valor + 1)}% for 5 seconds"
        super().__init__("Burst Shot", efecto, "Normal",
                         "Sprites/Recursos/Mejoras/Disparo_Rafaga.png")
        self.tiempo_primaria = 0
        self.tiempo_secundaria = 0
        self.duracion = 5000  # duración en milisegundos
        self.cd = 3000  # cooldown en milisegundos
        self.primaria_aumentada = False
        self.secundaria_aumentada = False
        self.primaria_thread = None
        self.secundaria_thread = None

    def actualizar_efecto(self):
        self.efecto = f"After not shooting for 3 seconds, your rate of fire increases by {100 * (self.valor + 1)}% for 5 seconds"

    def aplicar(self, jugador):
        tiempo_actual = pygame.time.get_ticks()

        # Gestionar el arma primaria
        if jugador.arma_primaria is not None:
            if not jugador.disparando:
                if not self.primaria_aumentada and tiempo_actual - self.tiempo_primaria >= self.cd:
                    self.primaria_aumentada = True
                    self.tiempo_primaria = tiempo_actual
                    jugador.arma_primaria.aplicar_mejora_temporal("velocidad", jugador.arma_primaria.velocidad_base * self.valor)
                    print(f"Velocidad primaria aumentada: {jugador.arma_primaria.velocidad}")
                    # Iniciar un hilo para reducir la velocidad después de 5 segundos desde el momento en que comienza a disparar
                    if self.primaria_thread is None or not self.primaria_thread.is_alive():
                        self.primaria_thread = threading.Thread(target=self.reducir_velocidad_despues_de_disparar,
                                                                args=(jugador.arma_primaria, "Primaria"))
                        self.primaria_thread.start()
            if jugador.disparando:
                self.tiempo_primaria = tiempo_actual

        # Gestionar el arma secundaria
        if jugador.arma_secundaria is not None:
            if not jugador.disparando_secundaria:
                if not self.secundaria_aumentada and tiempo_actual - self.tiempo_secundaria >= self.cd:
                    self.secundaria_aumentada = True
                    self.tiempo_secundaria = tiempo_actual
                    jugador.arma_secundaria.aplicar_mejora_temporal("velocidad", jugador.arma_secundaria.velocidad_base * self.valor)
                    print(f"Velocidad secundaria aumentada: {jugador.arma_secundaria.velocidad}")
                    # Iniciar un hilo para reducir la velocidad después de 5 segundos desde el momento en que comienza a disparar
                    if self.secundaria_thread is None or not self.secundaria_thread.is_alive():
                        self.secundaria_thread = threading.Thread(target=self.reducir_velocidad_despues_de_disparar,
                                                                  args=(jugador.arma_secundaria, "Secundaria"))
                        self.secundaria_thread.start()
            if jugador.disparando_secundaria:
                self.tiempo_secundaria = tiempo_actual

    def reducir_velocidad_despues_de_disparar(self, arma, tipo):
        time.sleep(self.duracion / 1000)
        arma.revertir_mejoras_temporales()
        print(f"Velocidad {tipo} reducida: {arma.velocidad}")
        if tipo == "Primaria":
            self.primaria_aumentada = False
        elif tipo == "Secundaria":
            self.secundaria_aumentada = False

DisparoRafaga=DisparoRafaga()
mejoras_normales.append(DisparoRafaga)

class DisparoCertero(Mejora):
    def __init__(self):
        self.valor=0
        efecto=f"Increases the critical hit rate by {10*(self.valor+1)}%"
        super().__init__("Accurate shot", efecto,"Normal","Sprites\\Recursos\\Mejoras\\Disparo_certero.png")

    def actualizar_efecto(self):
        self.efecto = f"Increases the critical hit rate by {10*(self.valor+1)}%"
    def aplicar_primera(self,jugador):
        jugador.arma_primaria.prob_critica += 0.1
        jugador.arma_secundaria.prob_critica +=0.1

DisparoCertero=DisparoCertero()
mejoras_normales.append(DisparoCertero)
class SoltarAceite(Mejora):
    def __init__(self):
        self.cd=0
        self.duracion=2
        self.valor=0
        efecto=f"Upon receiving damage, release oil that deal {4*(self.valor+1)} damage per second to enemies"
        super().__init__("Oil leak", efecto,"Normal","Sprites\\Recursos\\Mejoras\\Aceite.png")

    def actualizar_efecto(self):
        self.efecto =f"Upon receiving damage, release oil that deal {4*(self.valor+1)} damage per second to enemies"
    def aplicar_recibir(self,jugador,daño):
        from main import enemigos_sprites, balas_sprites, Bala_temporal
        tiempo_transcurrido = pygame.time.get_ticks()
        tiempo_segundos = tiempo_transcurrido // 10000
        if tiempo_segundos > self.cd:
            objetivo = encontrar_enemigo_mas_cercano(enemigos_sprites, jugador)
            if objetivo:
                direccion = calcular_direccion(objetivo, jugador)
                nueva_bala = Bala_temporal(4*self.valor, 0,
                                      pygame.image.load("Sprites\\Recursos\\Mejoras\\Aceite2.png",).convert_alpha(),
                                      jugador.base.rect.x, jugador.base.rect.y, direccion, 3000, tipo="Aceite")
                balas_sprites.add(nueva_bala)
                self.cd = tiempo_segundos
                return daño
        return daño

SoltarAceite=SoltarAceite()
mejoras_normales.append(SoltarAceite)
class MisilesRastreadores(Mejora):
    def __init__(self):
        self.tiempo_ultimo_misil=0
        self.valor=0
        efecto=f"Fire a missile that deals {15*(self.valor+1)} damage to a nearby enemy"
        super().__init__("Guided missiles", efecto, "Normal",
                         "Sprites\\Recursos\\Mejoras\\Misiles.png")

    def actualizar_efecto(self):
        self.efecto =f"Fire a missile that deals {15*(self.valor+1)} damage to a nearby enemy"
    def aplicar(self, jugador):
        from main import enemigos_sprites, balas_sprites, Bala

        tiempo_transcurrido = pygame.time.get_ticks()
        tiempo_segundos = tiempo_transcurrido // 3000
        if tiempo_segundos > self.tiempo_ultimo_misil:
                nueva_bala = Bala(15 * self.valor, 1,
                                      pygame.image.load('Sprites/Armas/Balas/Misil-1.png').convert_alpha(),
                                      jugador.base.rect.centerx, jugador.base.rect.y - 10, (jugador.base.rect.centerx,-1), 1, tipo="misil")
                for mejora in jugador.mejoras:
                    if hasattr(mejora, 'aplicar_dis'):
                        mejora.aplicar_dis(jugador, nueva_bala)
                balas_sprites.add(nueva_bala)
                self.tiempo_ultimo_misil = tiempo_segundos
                return None

        return None

MisilesRastreadores = MisilesRastreadores()
mejoras_normales.append(MisilesRastreadores)

class Overclock(Mejora):
    def __init__(self):
        self.ultima_activacion = 0
        self.duracion = 3  # Duración de la mejora en segundos
        self.cooldown = 10  # Tiempo de recarga en segundos
        self.timer = None
        self.valor=0
        efecto=f"When reaching 75% heat, core cooling increases by {75*(self.valor+1)}% for 3 seconds"
        super().__init__("Overclock",efecto, "Normal", "Sprites\\Recursos\\Mejoras\\Overclock.png")

    def actualizar_efecto(self):
        self.efecto =f"When reaching 75% heat, core cooling increases by {75*(self.valor+1)}% for 3 seconds"
    def aplicar(self, jugador):
        tiempo_actual = time.time()

        if jugador.base.calor_actual / jugador.base.calor_maximo >= 0.75:
            # Verificar si la mejora está en tiempo de recarga
            if tiempo_actual - self.ultima_activacion < self.cooldown:
                return
            jugador.nucleo.regCalor *= 1 + (0.75 * self.valor)

            # Actualizar el tiempo de última activación
            self.ultima_activacion = tiempo_actual

            # Configurar un temporizador para la duración de la mejora
            self.timer = threading.Timer(self.duracion, self.desactivar_mejora, args=[jugador])
            self.timer.start()

    def desactivar_mejora(self, jugador):
        jugador.nucleo.regCalor /= 1 + (0.75 * self.valor)
        self.timer = None

Overclock=Overclock()
mejoras_normales.append(Overclock)

class SaltoFase(Mejora):
    def __init__(self):
        self.valor=0
        self.valor2=self.valor
        if self.valor+1>=10:
            self.valor2=9
        efecto=f"When taking damage, {5*(self.valor2+1)}% chance to ignore it"
        super().__init__("Phase change",efecto,"Normal","Sprites\\Recursos\\Mejoras\\Salto_fase.png")

    def actualizar_efecto(self):
        self.valor2 = self.valor
        if self.valor + 1 >= 10:
            self.valor2 = 9
        self.efecto =f"When taking damage, {5*(self.valor2+1)}% chance to ignore it"
    def aplicar_recibir(self,jugador,daño):
        valor=self.valor
        if valor > 10:
            valor = 10
        if random.random() <(0.05*valor):
            daño =0
        return daño

SaltoFase=SaltoFase()
mejoras_normales.append(SaltoFase)

class CicloVida(Mejora):
    def __init__(self):
        self.valor=0
        efecto=f"Gain {1*(self.valor+1)} energy per kill"
        super().__init__("Life cycle",efecto,"Normal","Sprites\\Recursos\\Mejoras\\Ciclo_vida.png")
    def actualizar_efecto(self):
        self.efecto =f"Gain {1*(self.valor+1)} energy per kill"
    def aplicar_matar(self,jugador,enemigo):
        jugador.base.energia_actual += 1 * self.valor
CicloVida=CicloVida()
mejoras_normales.append(CicloVida)

class TormentaEstrellas(Mejora):
    def __init__(self):
        self.valor = 0
        self.cantidad=5
        super().__init__("Star storm", f"After using the core ability, creates 5 stars that rotate around and deal {10 * (self.valor + 1)} damage", "Normal", "Sprites\\Recursos\\Mejoras\\Star.png")


    def actualizar_efecto(self):
        self.efecto =f"After using the core ability, creates 3 stars that rotate around and deal {10 * (self.valor + 1)} damage"

    def aplicar_nucleo(self,jugador):
        from main import Bala,balas_sprites
        for num in range(self.cantidad):
            direccion = (0, -1)  # Dirección inicial hacia arriba
            nueva_bala = Bala(10*(self.valor), 5,
                              pygame.image.load('Sprites/Armas/Balas/Star.png').convert_alpha(),
                              jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                              1, tipo="Orbital Estelar", distancia=80)
            nueva_bala.angulo = 0
            balas_sprites.add(nueva_bala)
    def aplicar(self,jugador):
            actualizar_orbital(jugador,"Orbital Estelar")
TormentaEstrellas=TormentaEstrellas()
mejoras_normales.append(TormentaEstrellas)

class Boomerang(Mejora):
    def __init__(self):
        self.valor = 0
        self.cd=8
        self.incremento_angulo=20
        self.angulo_rotacion=0
        super().__init__("Boomerang", f"Every {self.cd} seconds throw a boomerang to a random direction that deal {25+ (10*(self.valor+1))}", "Normal", "Sprites\\Recursos\\Mejoras\\Rang.png")

        self.ultima_activacion = pygame.time.get_ticks()

    def actualizar_efecto(self):
        self.efecto = f"Every {self.cd} seconds throw a boomerang to a random direction that deals {25 + (10 * (self.valor + 1))} damage"
        if self.valor % 3 == 0 and self.cd > 2:
            self.cd -= 1

    def aplicar(self, jugador):
        from main import Bala, balas_sprites
        for bala in balas_sprites:
            if bala.tipo =="Boomerang":
                self.angulo_rotacion += self.incremento_angulo  # Incrementa el ángulo de rotación
                bala.image = pygame.transform.rotate(bala.original_image, self.angulo_rotacion)
                bala.rect = bala.image.get_rect(center=bala.rect.center)
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultima_activacion >= self.cd * 1000:
            self.ultima_activacion = tiempo_actual

            # Crear un boomerang
            direccion = (random.uniform(-1, 1), random.uniform(-1, 1))
            while direccion == (0, 0):
                direccion = (random.uniform(-1, 1), random.uniform(-1, 1))
            direccion_normalizada = pygame.math.Vector2(direccion).normalize()

            nueva_bala = Bala(
                25 + (10 * (self.valor)),
                7,
                pygame.image.load('Sprites/Armas/Balas/Rang.png').convert_alpha(),
                jugador.base.rect.centerx,
                jugador.base.rect.centery,
                direccion_normalizada,
                -1,
                tipo="Boomerang", distancia=1200
            )
            for mejora in jugador.mejoras:
                if hasattr(mejora, 'aplicar_dis'):
                    mejora.aplicar_dis(jugador, nueva_bala)
            balas_sprites.add(nueva_bala)
        for bala in balas_sprites:
            if bala.tipo=="Boomerang":
                bala.velocidadProyectil += 0.2
                if bala.distancia_recorrida > bala.distancia_maxima / 3:
                    dx = jugador.base.rect.centerx - bala.rect.centerx
                    dy = jugador.base.rect.centery - bala.rect.centery
                    distancia = math.sqrt(dx ** 2 + dy ** 2)
                    if distancia != 0:
                        direccion_hacia_jugador = (dx / distancia, dy / distancia)
                        bala.direccion = direccion_hacia_jugador
Boomerang=Boomerang()
mejoras_normales.append(Boomerang)

class RompeCristales(Mejora):
    def __init__(self):
        self.valor=0
        super().__init__("Glass Breaker", f"Deal {25 * (self.valor + 1)}% more damage to Crystals", "Normal", "Sprites\\Recursos\\Mejoras\\GlassB.png")

    def actualizar_efecto(self):
        self.efecto = f"Deal {25 * (self.valor + 1)}% more damage to Crystals"

    def aplicar_imp(self,jugador,bala,enemigo):
        if enemigo.tipo=="Cristal":
            bala.daño *= 1+(0.25*self.valor)
RompeCristales=RompeCristales()
mejoras_normales.append(RompeCristales)

class MataJefes(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Giant Slayer", f"Deal {10 * (self.valor + 1)}% more damage to Bosses", "Normal",
                         "Sprites\\Recursos\\Mejoras\\Giant.png")

    def actualizar_efecto(self):
        self.efecto = f"Deal {10 * (self.valor + 1)}% more damage to Bosses"

    def aplicar_imp(self, jugador, bala, enemigo):
        if enemigo.boss:
            bala.daño *= 1 + (0.10 * self.valor)
MataJefes=MataJefes()
mejoras_normales.append(MataJefes)

class Rebote(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Ricochet", f"When a bullet hits an enemy, it has a {10 * (self.valor + 1)}% chance to change its trajectory towards another one", "Normal", "Sprites\\Recursos\\Mejoras\\Rebote.png")

    def actualizar_efecto(self):
        self.efecto =f"When a bullet hits an enemy, it has a {10 * (self.valor + 1)}% chance to change its trajectory towards another one"
    def aplicar_imp(self,jugador,bala,enemigo):
        from main import enemigos_sprites, balas_sprites
        for suerte in range(jugador.suerte):
            if random.random() <= (0.10 * self.valor):
                objetivo = encontrar_enemigo_mas_cercano(enemigos_sprites, enemigo)
                if objetivo:
                    print(objetivo)
                    direccion = calcular_direccion(objetivo, enemigo)
                    bala.direccion=direccion
                    bala.daño *= 0.75
                break

Rebote=Rebote()
mejoras_normales.append(Rebote)

class ZonaCalor(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Heat zone", f"Above 50% heat, generate a heat zone around you, dealing {5 * (self.valor + 1)} per second", "Normal", "Sprites\\Recursos\\Mejoras\\Calor_curativo.png")
        self.activo=False
        self.animacion = [
            "Sprites\\Recursos\\Mejoras\\Heat-zone.png",
            "Sprites\\Recursos\\Mejoras\\Heat-zone.png",
            "Sprites\\Recursos\\Mejoras\\Heat-zone.png",
        ]
        self.ultima=0

    def actualizar_efecto(self):
        self.efecto =f"When reaching 50% heat generate a heat zone around you, dealing {4 * (self.valor + 1)} per second"

    def aplicar(self,jugador):
        if jugador.base.calor_actual > 0.5 * jugador.base.calor_maximo and pygame.time.get_ticks() - 1200 >= self.ultima:
            self.ultima=pygame.time.get_ticks()
            if self.activo ==False:
                from main import Bala_temporal,balas_sprites
                nueva_bala = Bala_temporal(4 * self.valor, jugador.base.velocidad*1.5,
                                           pygame.image.load(
                                               "Sprites\\Recursos\\Mejoras\\Heat-zone.png", ).convert_alpha(),
                                           jugador.base.rect.centerx-256, jugador.base.rect.centery-256, [0,0], 1500, tipo="Rastreo")
                balas_sprites.add(nueva_bala)
            self.activo=True
        else:
            self.activo=False
ZonaCalor=ZonaCalor()
mejoras_normales.append(ZonaCalor)
#Raros
class Acero(Mejora):
    def __init__(self):
        self.valor=0
        efecto=f"Reduce taken damage by {10*(self.valor+1)}"
        super().__init__("Steel+",efecto,"Rare","Sprites\\Recursos\\Mejoras\\Acero+.png")

    def actualizar_efecto(self):
        self.efecto =f"Reduce taken damage by {10*(self.valor+1)}"
    def aplicar_recibir(self,jugador,daño):
        daño -= 10*self.valor
        if daño<0:
            daño=0
        return(daño)

Acero=Acero()
mejoras_raras.append(Acero)

class CalorConstante(Mejora):
    def __init__(self):
        self.valor = 0
        self.aplicado = False
        self.activo = False
        efecto = f"Weapons generate 10% more heat. Above 50% heat, weapons deal {20 * (self.valor+1)}% more damage"
        super().__init__("Constant Heat", efecto, "Rare", "Sprites\\Recursos\\Mejoras\\Calor_constante.png")

    def actualizar_efecto(self):
        self.efecto =f"Weapons generate 10% more heat. Above 50% heat, weapons deal {20 * (self.valor+1)}% more damage"
    def aplicar(self, jugador):
        aumento= 0.2 * self.valor
        if self.aplicado==False:
            jugador.arma_primaria.calentamiento *=1.1
            jugador.arma_secundaria.calentamiento *= 1.1
            self.aplicado = True

        if jugador.base.calor_actual > 0.5 * jugador.base.calor_maximo:
            if self.activo ==False:
                jugador.arma_primaria.daño *= 1 + aumento
                jugador.arma_secundaria.daño *= 1 + aumento
            self.activo=True
        else:
            if self.activo == True:
                jugador.arma_primaria.daño /= (1+aumento)
                jugador.arma_secundaria.daño /= (1+aumento)
            self.activo=False

CalorConstante=CalorConstante()
mejoras_raras.append(CalorConstante)
class EngranajesPulidos(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Polished Gears", f"Increases movement speed by {10 * (self.valor+1)}%", "Rare", "Sprites\\Recursos\\Mejoras\\Engranajes.png")
    def actualizar_efecto(self):
        self.efecto =f"Increases movement speed by {10 * (self.valor+1)}%"
    def aplicar_primera(self,jugador):
        jugador.base.velocidad += jugador.base.velocidad_base * 0.10

EngranajesPulidos=EngranajesPulidos()
mejoras_raras.append(EngranajesPulidos)

class DisparoGemelo(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Twin Shot", f"You have {10 * (self.valor+1)}% chance to fire an additional bullet", "Rare", "Sprites\\Recursos\\Mejoras\\Disparo_gemelo.png")
    def actualizar_efecto(self):
        self.efecto =f"You have {10 * (self.valor+1)}% chance to fire an additional bullet"

    def aplicar_dis(self, jugador, bala):
        from main import Bala, balas_sprites
        disparos = 0
        disparos_realizados = 1
        valor = self.valor

        while valor > 10:
            disparos += 1
            valor -= 10

        for suerte in range(jugador.suerte):
            if random.random() <= (0.10 * valor):
                disparos += 1
                break

        daño = bala.daño
        velocidadProyectil = bala.velocidadProyectil
        sprite = bala.image
        origen_x = bala.rect.x
        origen_y = bala.rect.y
        direccion = bala.direccion
        perforacion = bala.perforacion
        prob_critica = bala.prob_critica
        tipo = bala.tipo
        distancia = bala.distancia_maxima
        eficiencia = bala.eficiencia
        arma = bala.arma

        for i in range(disparos):
            nueva_bala = Bala(daño, velocidadProyectil, sprite, origen_x, origen_y, direccion, perforacion,
                              prob_critica, tipo, distancia, eficiencia, arma)

            nueva_bala.velocidadProyectil -= disparos_realizados
            nueva_bala.daño_base *= 0.50
            nueva_bala.eficiencia *= 0.2

            if nueva_bala.velocidadProyectil <= 2:
                nueva_bala.velocidadProyectil += 1
                disparos_realizados -= 1

            balas_sprites.add(nueva_bala)
            disparos_realizados += 1
            bala.velocidadProyectil += disparos_realizados

DisparoGemelo=DisparoGemelo()
mejoras_raras.append(DisparoGemelo)

class BalaDispercion(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Scatter Bullet", "Upon killing enemies, they explode into a shower of bullets", "Rare", "Sprites\\Recursos\\Mejoras\\Dispercion.png")

    def actualizar_efecto(self):
        self.efecto ="Upon killing enemies, they explode into a shower of bullets"
    def aplicar_matar(self, jugador, enemigo):
        from main import Bala, balas_sprites

        posicion_final_enemigo = (enemigo.rect.x, enemigo.rect.y)
        num_balas = 3 + self.valor
        separacion_angulo = 360 / num_balas

        for i in range(num_balas):
            # Calcular la dirección utilizando trigonometría
            angulo_rad = math.radians(i * separacion_angulo)
            direccion = (math.cos(angulo_rad), math.sin(angulo_rad))

            nueva_bala = Bala(3, 8,
                              pygame.image.load("Sprites\\Armas\\Balas\\Bala-1.png").convert_alpha(),
                              posicion_final_enemigo[0], posicion_final_enemigo[1] + 20, direccion, 1, eficiencia=0.15)

            for mejora in jugador.mejoras:
                if hasattr(mejora, 'aplicar_dis'):
                    mejora.aplicar_dis(jugador, nueva_bala)
            balas_sprites.add(nueva_bala)

BalaDispercion=BalaDispercion()
mejoras_raras.append(BalaDispercion)


class PuntaAero(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Aerodynamic Tip", f"Increases projectile speed by {10 * (self.valor + 1)}%, every 3 upgrades increases penetration", "Rare", "Sprites\\Recursos\\Mejoras\\Aero.png")

    def actualizar_efecto(self):
        self.efecto =f"Increases projectile speed by {10 * (self.valor + 1)}%, every 3 upgrades increases penetration"
    def aplicar_primera(self,jugador):
        if self.valor < 10:
            jugador.arma_primaria.velocidadProyectil *=1.10
            jugador.arma_secundaria.velocidadProyectil *= 1.10
        if self.valor % 3==0:
            jugador.arma_primaria.perforacion +=1
            jugador.arma_secundaria.perforacion +=1

PuntaAero=PuntaAero()
mejoras_raras.append(PuntaAero)

class Companero(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Winged ally", f"Summon a robotic bird that shoot copyng your secondary weapon, dealing {20 * (self.valor + 1)}% of damage", "Rare", "Sprites\\Recursos\\Mejoras\\Bird.png")
        self.ultimo = 0
        self.tiempo_cambio=0

    def actualizar_efecto(self):
        self.efecto = f"Summon a robotic bird that shoot copyng your secondary weapon, dealing {20 * (self.valor + 1)}% of damage"

    def aplicar_primera(self, jugador):
        from main import Bala, balas_sprites
        if self.valor==1:
            direccion = (0, -1)
            nueva_bala = Bala(0, 70,
                                  pygame.image.load('Sprites/Armas/Balas/Bird.png').convert_alpha(),
                                  jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                                  -1, tipo="Orbital Aliado", distancia=250)
            nueva_bala.angulo = 0
            balas_sprites.add(nueva_bala)


    def aplicar(self, jugador):
        from main import Bala, balas_sprites, enemigos_sprites
        for bala in balas_sprites:
            if bala.tipo == "Orbital Aliado":
                tiempo_actual = pygame.time.get_ticks()
                objetivo = encontrar_enemigo_mas_cercano(enemigos_sprites, bala)
                if tiempo_actual - self.ultimo >= 1100 / jugador.arma_secundaria.velocidad and objetivo:
                        bala.image=pygame.image.load('Sprites/Armas/Balas/Bird2.png').convert_alpha()
                        self.tiempo_cambio=pygame.time.get_ticks()
                        direccion = calcular_direccion(objetivo, bala)
                        jugador.arma_secundaria.disparar(
                            bala.rect.centerx, bala.rect.centery, direccion, jugador,modD=(0.2*self.valor)
                        )
                        self.ultimo = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - self.tiempo_cambio >= 500:
                    bala.image = pygame.image.load('Sprites/Armas/Balas/Bird.png').convert_alpha()


Companero=Companero()
mejoras_raras.append(Companero)
class CriticoRestaurativo(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Restorative Critical", f"Critical hits restore {3 * (self.valor + 1)} health, {1 * (self.valor + 1)} energy, or reduce heat by {2 * (self.valor + 1)}", "Rare", "Sprites\\Recursos\\Mejoras\\Critico_restaurativo.png")
        self.num=0
    def actualizar_efecto(self):
        self.efecto =f"Critical hits restore {3 * (self.valor + 1)} health, {1 * (self.valor + 1)} energy, or reduce heat by {2 * (self.valor + 1)}"
    def aplicar_imp(self,jugador,bala,enemigo):
        if bala.critico==True:
            if self.num==0:
                jugador.base.vida_actual+=3*self.valor
                self.num+=1
                if jugador.base.vida_actual > jugador.base.vida_maxima:
                    jugador.base.vida_actual = jugador.base.vida_maxima
            elif self.num==1:
                jugador.base.energia_actual+=1*self.valor
                self.num+=1
            elif self.num==2:
                jugador.base.calor_actual -=2*self.valor
                self.num=0

    def aplicar_primera(self,jugador):
        print(self.valor)
        jugador.arma_primaria.prob_critica +=0.1
        jugador.arma_secundaria.prob_critica +=0.1

CriticoRestaurativo=CriticoRestaurativo()
mejoras_raras.append(CriticoRestaurativo)

class ExplosionHelada(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Frost Explosion", f"Every 7 seconds, slows down and inflicts {10 * (self.valor + 1)} damage to nearby enemies", "Rare", "Sprites\\Recursos\\Mejoras\\Ice_wave.png")
        self.cd = 7000
        self.ultima_activacion = 0
        self.animacion = [
            "Sprites\\Recursos\\Mejoras\\Ice_wave2.png",
            "Sprites\\Recursos\\Mejoras\\Ice_wave2.png",
            "Sprites\\Recursos\\Mejoras\\Ice_wave2.png",
            "Sprites\\Recursos\\Mejoras\\Ice_wave2.png",
            "Sprites\\Recursos\\Mejoras\\Ice_wave2.png"
        ]

    def actualizar_efecto(self):
        self.efecto = f"Every 7 seconds, slows down and inflicts {10 * (self.valor + 1)} damage to nearby enemies"

    def aplicar(self, jugador):
        from main import enemigos_sprites, animaciones
        from Enemigos import Animacion
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultima_activacion >= self.cd:
            radio = 110 + (30*self.valor)

            # Redimensionar los sprites de la animación
            animacion_redimensionada = redimensionar_animacion(self.animacion, radio * 2, radio * 2)
            animacion = Animacion(jugador.base.rect.center, animacion_redimensionada, True, desaparecer=True)
            animaciones.add(animacion)

            for enemigo in enemigos_sprites:
                distancia = math.sqrt(
                    (enemigo.rect.centerx - jugador.base.rect.centerx) ** 2 +
                    (enemigo.rect.centery - jugador.base.rect.centery) ** 2
                )
                if distancia <= radio:
                    enemigo.danio(10 * self.valor,(136,245,234))  # Inflige el daño al enemigo
                    enemigo.aplicar_congelamiento(0.15)
                    jugador.base.calor_actual -= 3

            self.ultima_activacion = tiempo_actual

ExplosionHelada=ExplosionHelada()
mejoras_raras.append(ExplosionHelada)

class Sierra(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Saw", f"A spinning saw that deals {20*(self.valor + 1)} damage to enemies", "Rare", "Sprites\\Recursos\\Mejoras\\Saw.png")

        self.ultima_activacion = pygame.time.get_ticks()

    def actualizar_efecto(self):
        self.efecto =f"A spinning saw that deals {20*(self.valor + 1)} damage to enemies"
    def aplicar_primera(self, jugador):
        from main import Bala, balas_sprites
        for bala in balas_sprites:
            if bala.tipo == "Orbital Sierra":
                bala.daño = 25 *(self.valor)
                bala.daño_base=25 *(self.valor)
        if self.valor % 3 == 0 or self.valor == 1:
            direccion = (0, -1)
            nueva_bala = Bala(25, 30,
                              pygame.image.load('Sprites/Armas/Balas/Saw.png').convert_alpha(),
                              jugador.base.rect.centerx, jugador.base.rect.centery, direccion,
                              -1, tipo="Orbital Sierra",distancia=175)
            nueva_bala.angulo = 0
            balas_sprites.add(nueva_bala)


    def aplicar(self, jugador):
        from main import balas_sprites




Sierra=Sierra()
mejoras_raras.append(Sierra)

class BolaFuego(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Fireball", f"Every 15 bullets shot 4 fireballs that deal {15*(self.valor + 1)} damage", "Rare", "Sprites\\Armas\\Balas\\Fire-ball.png")
        self.contador=0
        self.cd=500
        self.ultima_activacion=0

    def actualizar_efecto(self):
        self.efecto = f"Every 15 bullets shot 4 fireballs that deal {15*(self.valor + 1)} damage"

    def aplicar_dis(self,jugador,bala):
        self.contador +=1
        if self.contador >= 15 and pygame.time.get_ticks() - self.ultima_activacion >= self.cd:
            from main import Bala,balas_sprites
            direcciones = [
                [1, 0],
                [-1, 0],
                [0, 1],
                [0, -1]
            ]
            for direccion in direcciones:
                nueva_bala = Bala(
                    15 * self.valor, 6,
                    pygame.image.load('Sprites/Armas/Balas/Fire-ball.png').convert_alpha(),
                    jugador.base.rect.centerx, jugador.base.rect.y, direccion, 10
                )
                balas_sprites.add(nueva_bala)

            self.contador =0
            self.ultima_activacion=pygame.time.get_ticks()
BolaFuego=BolaFuego()
mejoras_raras.append(BolaFuego)
#Legendarias


class CañonPrimario(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Primary Cannon", "Greatly enhances the primary weapon", "Legendary", "Sprites\\Recursos\\Mejoras\\Primario.png")

    def actualizar_efecto(self):
        self.efecto ="Greatly enhances the primary weapon"
    def aplicar_primera(self,jugador):
        jugador.arma_primaria.daño *= 1.5
        jugador.arma_primaria.velocidad *= 1.5
        jugador.arma_primaria.perforacion += 2

CañonPrimario=CañonPrimario()
mejoras_legendarias.append(CañonPrimario)

class DecoracionDados(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Dice Decoration", "Increases your luck", "Legendary", "Sprites\\Recursos\\Mejoras\\Dado.png")

    def actualizar_efecto(self):
        self.efecto ="Increases your luck"
    def aplicar_primera(self,jugador):
        jugador.suerte +=1

DecoracionDados=DecoracionDados()
mejoras_legendarias.append(DecoracionDados)

class EspirituVengativo(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Vengeful Spirits", "Upon killing an enemy, releases its spirit to torment another enemy", "Legendary", "Sprites\\Recursos\\Mejoras\\Espiritu_Vengativo.png")

    def actualizar_efecto(self):
        self.efecto ="Upon killing an enemy, releases its spirit to torment another enemy"
    def aplicar_matar(self, jugador, enemigo):
        from main import enemigos_sprites, balas_sprites, Bala
        objetivo = encontrar_enemigo_mas_cercano(enemigos_sprites, enemigo)
        if objetivo:
            posicion_final_enemigo = (enemigo.rect.x, enemigo.rect.y)
            nueva_bala = Bala(round((enemigo.vida_maxima) * (0.5 * self.valor)), 1,
                              pygame.image.load("Sprites\\Recursos\\Mejoras\\Espiritu_Vengativo2.png").convert_alpha(),
                              posicion_final_enemigo[0], posicion_final_enemigo[1] + 20, (0,-1), 1, tipo="Fantasmal")
            balas_sprites.add(nueva_bala)

            # Llama a encontrar_enemigo_mas_cercano para actualizar el objetivo del espiritu
            objetivo_espiritu = encontrar_enemigo_mas_cercano(enemigos_sprites, nueva_bala)
            nueva_bala.objetivo = objetivo_espiritu

            return nueva_bala
        else:
            return None

EspirituVengativo=EspirituVengativo()
mejoras_legendarias.append(EspirituVengativo)

class JugandoFuego(Mejora):
    def __init__(self):
        self.valor = 0
        self.activado = False
        super().__init__("Playing with Fire", f"When overheating, increases your weapons damage by {20 * (self.valor + 1)}%, up to a maximum of {100 * (self.valor + 1)}%", "Legendary", "Sprites\\Recursos\\Mejoras\\Fuego.png")

    def actualizar_efecto(self):
        self.efecto =f"When overheating, increases your weapons damage by {20 * (self.valor + 1)}%, up to a maximum of {100 * (self.valor + 1)}%"
    def aplicar(self,jugador):

        if jugador.sobrecalentado == True and self.activado==False:
            if not jugador.arma_primaria.daño / jugador.arma_primaria.daño_base > 1 + self.valor:
                jugador.arma_primaria.daño *= 1 + (0.2 * self.valor)
            if not jugador.arma_secundaria.daño / jugador.arma_secundaria.daño_base > 1 + self.valor:
                jugador.arma_secundaria.daño *= 1 +(0.2 * self.valor)
            self.activado=True
        elif jugador.sobrecalentado == False:
            self.activado=False

JugandoFuego=JugandoFuego()
mejoras_legendarias.append(JugandoFuego)

class Milicia(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Militia", f"Increases missile damage by {50 * (self.valor + 1)}%, sometimes when firing, you launch 3 missiles to nearby enemies", "Legendary", "Sprites\\Recursos\\Mejoras\\Milicia.png")

    def actualizar_efecto(self):
        self.efecto =f"Increases missile damage by {50 * (self.valor + 1)}%, sometimes when firing, you launch 3 missiles in a random direction"
    def aplicar_imp(self,jugador,bala,enemigo):
        from main import Bala,balas_sprites
        if bala.tipo == "misil":
            bala.daño *= 1 + (0.5*self.valor)
        angulo_rad = random.uniform(0, 2 * math.pi)
        for suerte in range(jugador.suerte):
            if random.random() <= 0.08:
                velocidad= 3
                for i in range(3):
                    angulo_rad += math.radians(10)
                    direccion = (math.cos(angulo_rad), math.sin(angulo_rad))
                    nueva_bala = Bala(30 * self.valor, velocidad,
                                      pygame.image.load('Sprites/Armas/Balas/Misil-1.png').convert_alpha(),
                                      jugador.base.rect.x, jugador.base.rect.y + 20, direccion,
                                      1,tipo="misil", eficiencia=0.1)
                    velocidad -=1
                    for mejora in jugador.mejoras:
                        if hasattr(mejora, 'aplicar_dis'):
                            mejora.aplicar_dis(jugador,nueva_bala)
                    balas_sprites.add(nueva_bala)
                break

Milicia=Milicia()
mejoras_legendarias.append(Milicia)

class Random(Mejora):
    def __init__(self):
        self.valor = 0
        self.misiles = 0
        super().__init__("Random", "Obtain a random effect", "Legendary", "Sprites\\Recursos\\Mejoras\\Random.png")

    def actualizar_efecto(self):
        self.efecto = "Obtain a random effect"
    def aplicar_primera(self,jugador):
        numero = random.random()
        if numero < 0.30:
            for mejora in jugador.mejoras.copy():
                if mejora in mejoras_normales:
                    while mejora in jugador.mejoras:
                        mejora_random = random.choice(mejoras_raras)
                        jugador.recolectar_mejora(mejora_random)
                        jugador.mejoras.remove(mejora)
        elif numero < 0.60:
            num = 0
            for mejora in jugador.mejoras.copy():
                if mejora in mejoras_raras:
                    while mejora in jugador.mejoras:
                        num += mejora.valor
                        mejora.valor=0
                        jugador.mejoras.remove(mejora)
            mejora_random = random.choice(mejoras_normales)
            num *=1.5
            for i in range(round(num)):
                jugador.recolectar_mejora(mejora_random)
        elif numero < 0.80:
            jugador.base.vida_maxima += 100
            jugador.base.calor_maximo +=100
            jugador.arma_primaria.daño += 4
            jugador.arma_secundaria.daño += 4
        elif numero < 0.99:
            print("Misiles")
            self.misiles +=1
        elif numero >= 0.99:
            jugador.arma_primaria.calentamiento =0
            jugador.arma_secundaria.calentamiento=0
            jugador.arma_secundaria.daño *=0.25
            jugador.arma_primaria.daño *=0.25
            jugador.arma_primaria.velocidad *=8
            jugador.arma_secundaria.velocidad *=8


    def aplicar_dis(self,jugador,bala):
        from main import balas_sprites
        if self.misiles >= 1:
            for bala in balas_sprites:
                if not bala.tipo:
                    bala.original_image = pygame.image.load('Sprites/Armas/Balas/Misil-1.png').convert_alpha()
                    bala.tipo = "misil"
                    bala.daño *= 1 + (0.2*self.misiles)
Random=Random()


class CriticoCongelante(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Freezing Critical", f"Critical hits reduce enemy speed. Increases damage by {50 * (self.valor + 1)}% against frozen enemies", "Legendary", "Sprites\\Recursos\\Mejoras\\Crit_cong.png")

    def actualizar_efecto(self):
        self.efecto = f"Critical hits reduce enemy speed. Increases damage by {50 * (self.valor + 1)}% against frozen enemies"
    def aplicar_imp(self, jugador, bala, enemigo):
        if enemigo.velocidad < enemigo.velocidad_base:
            bala.daño *= 1.5*self.valor
        if bala.critico:
           enemigo.aplicar_congelamiento(0.15*self.valor)


    def aplicar_primera(self,jugador):
        jugador.arma_primaria.prob_critica +=0.2
        jugador.arma_secundaria.prob_critica +=0.2
CriticoCongelante=CriticoCongelante()
mejoras_legendarias.append(CriticoCongelante)

class CriticoMejorado(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Improved Critical", f"Bullets not from your weapons have a {50 * (self.valor + 1)}% chance of being critical based on your primary weapon's critical chance", "Legendary", "Sprites\\Recursos\\Mejoras\\Critico_mejorado.png")

    def actualizar_efecto(self):
        self.efecto =f"Bullets not from your weapons have a {50 * (self.valor + 1)}% chance of being critical based on your primary weapon's critical chance"
    def aplicar_primera(self,jugador):
        jugador.arma_primaria.prob_critica += 0.2
        jugador.arma_secundaria.prob_critica +=0.2
    def aplicar_imp(self,jugador,bala,enemigo):
        if bala.prob_critica == 0 and not bala.critico:
            bala.prob_critica += jugador.arma_primaria.prob_critica * (0.5 * self.valor)
            critico(bala,jugador)

CriticoMejorado=CriticoMejorado()
mejoras_legendarias.append(CriticoMejorado)

class Expansion(Mejora):
    def __init__(self):
        super().__init__("Expansion",f"Gain a planet",
                    "Rare", "Sprites\\Recursos\\Mejoras\\Expansion.png")
    def aplicar_primera(self,jugador):
        agregar_planeta(jugador)
Expansion=Expansion()
class CentroUniverso(Mejora):
    def __init__(self):
        self.valor = 0
        self.aumento=0.50
        super().__init__("Center of the universe", f"Orbitals are {50 * (self.valor + 1)}% bigger and deal {50 * (self.valor + 1)}% more damage, gain a planet", "Legendary", "Sprites\\Recursos\\Mejoras\\Universe.png")

    def actualizar_efecto(self):
        self.efecto =f"Orbitals are {50 * (self.valor + 1)}% bigger and deal {50 * (self.valor + 1)}% more damage, gain a planet"
        self.aumento= 0.50 * self.valor

    def aplicar_primera(self,jugador):
        agregar_planeta(jugador)
        if not Expansion in mejoras_raras:
            mejoras_raras.append(Expansion)

    def aplicar(self,jugador):
        actualizar_orbital(jugador,"Orbital Planeta")
        from main import balas_sprites
        for bala in balas_sprites:
            if "Orbital" in str(bala.tipo):
                nuevo_tamaño = (int(bala.tamaño_base[0] * (1+self.aumento)), int(bala.tamaño_base[0] * (1+self.aumento)))
                sprite_redimensionado = pygame.transform.scale(bala.original_image, nuevo_tamaño)
                bala.actual_image=sprite_redimensionado
    def aplicar_imp(self,jugador,bala,enemigo):
        if "Orbital" in str(bala.tipo):
            bala.daño += bala.daño_base * (0.5*self.valor)
CentroUniverso=CentroUniverso()
mejoras_legendarias.append(CentroUniverso)

class Explosivos(Mejora):
    def __init__(self):
        self.valor = 0
        super().__init__("Hidden Explosives", f"Bullets explote, dealing {30 * (self.valor + 1)}% damage to nearby enemies", "Legendary", "Sprites\\Recursos\\Mejoras\\Kaboom.png")

    def actualizar_efecto(self):
        self.efecto =f"Bullets explote, dealing {30 * (self.valor + 1)}% damage to nearby enemies"

    def aplicar_imp(self, jugador, bala, enemigo):
        # Daño adicional de la explosión
        from main import enemigos_sprites,animaciones
        from Enemigos import Animacion
        daño_explosion = 2 + (bala.daño * (0.30 * self.valor))

        # Radio de la explosión
        radio_explosion = (daño_explosion * 5) + 100
        sonido_aleatorio = random.choice(sonidos_explosion)
        sonido_aleatorio.play()
        for enemigo_cercano in enemigos_sprites:
            if enemigo_cercano != enemigo and self.distancia(enemigo.rect.center,
                                                             enemigo_cercano.rect.center) <= radio_explosion:
                enemigo_cercano.danio(daño_explosion,(163, 33, 16, 64))
        anima=[
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom1.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom2.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom3.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom4.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom5.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom6.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom7.png"),
            pygame.image.load("Sprites\\Armas\\Balas\\Kaboom8.png")
        ]
        anima_redimensionada = [pygame.transform.scale(imagen, (radio_explosion, radio_explosion)) for imagen in anima]
        animacion=Animacion(enemigo.rect.center,anima_redimensionada,False, duracion_frame=25, desaparecer=True)
        animaciones.add(animacion)
    def distancia(self, punto1, punto2):
        return math.sqrt((punto1[0] - punto2[0]) ** 2 + (punto1[1] - punto2[1]) ** 2)
Explosivos=Explosivos()
mejoras_legendarias.append(Explosivos)

class Agujero(Mejora):
    def __init__(self):
        self.valor = 0
        self.cd=20000
        self.duracion= 5000
        self.ultima=0
        self.animacion = [
            "Sprites\\Armas\\Balas\\Black-Hole-1.png",
            "Sprites\\Armas\\Balas\\Black-Hole-2.png",
            "Sprites\\Armas\\Balas\\Black-Hole-3.png",
            "Sprites\\Armas\\Balas\\Black-Hole-4.png",
            "Sprites\\Armas\\Balas\\Black-Hole-5.png",
            "Sprites\\Armas\\Balas\\Black-Hole-6.png",
            "Sprites\\Armas\\Balas\\Black-Hole-7.png",
            "Sprites\\Armas\\Balas\\Black-Hole-8.png",
            "Sprites\\Armas\\Balas\\Black-Hole-9.png",
            "Sprites\\Armas\\Balas\\Black-Hole-10.png",
            "Sprites\\Armas\\Balas\\Black-Hole-11.png",
            "Sprites\\Armas\\Balas\\Black-Hole-1.png",
            "Sprites\\Armas\\Balas\\Black-Hole-2.png",
            "Sprites\\Armas\\Balas\\Black-Hole-3.png",
            "Sprites\\Armas\\Balas\\Black-Hole-4.png",
            "Sprites\\Armas\\Balas\\Black-Hole-5.png",
            "Sprites\\Armas\\Balas\\Black-Hole-6.png",
            "Sprites\\Armas\\Balas\\Black-Hole-7.png",
            "Sprites\\Armas\\Balas\\Black-Hole-8.png",
            "Sprites\\Armas\\Balas\\Black-Hole-9.png",
            "Sprites\\Armas\\Balas\\Black-Hole-10.png",
            "Sprites\\Armas\\Balas\\Black-Hole-11.png",
            "Sprites\\Armas\\Balas\\Black-Hole-1.png",
            "Sprites\\Armas\\Balas\\Black-Hole-2.png",
            "Sprites\\Armas\\Balas\\Black-Hole-3.png",
            "Sprites\\Armas\\Balas\\Black-Hole-4.png",
            "Sprites\\Armas\\Balas\\Black-Hole-5.png",
            "Sprites\\Armas\\Balas\\Black-Hole-6.png",
            "Sprites\\Armas\\Balas\\Black-Hole-7.png",
            "Sprites\\Armas\\Balas\\Black-Hole-8.png",
            "Sprites\\Armas\\Balas\\Black-Hole-9.png",
            "Sprites\\Armas\\Balas\\Black-Hole-10.png",
            "Sprites\\Armas\\Balas\\Black-Hole-11.png",
            "Sprites\\Armas\\Balas\\Black-Hole-1.png",
            "Sprites\\Armas\\Balas\\Black-Hole-2.png",
            "Sprites\\Armas\\Balas\\Black-Hole-3.png",
            "Sprites\\Armas\\Balas\\Black-Hole-4.png",
            "Sprites\\Armas\\Balas\\Black-Hole-5.png",
            "Sprites\\Armas\\Balas\\Black-Hole-6.png",
            "Sprites\\Armas\\Balas\\Black-Hole-7.png",
            "Sprites\\Armas\\Balas\\Black-Hole-8.png",
            "Sprites\\Armas\\Balas\\Black-Hole-9.png",
            "Sprites\\Armas\\Balas\\Black-Hole-10.png",
            "Sprites\\Armas\\Balas\\Black-Hole-11.png",
            "Sprites\\Armas\\Balas\\Black-Hole-1.png",
            "Sprites\\Armas\\Balas\\Black-Hole-2.png",
            "Sprites\\Armas\\Balas\\Black-Hole-3.png",
        ]
        super().__init__("Black Hole", f"Throws a black hole at an enemy, the hole deals {10 * (self.valor + 1)} damage per second and drags enemies towards it", "Legendary", "Sprites\\Armas\\Balas\\Black-Hole-11.png")

    def actualizar_efecto(self):
        self.efecto =f"Throws a black hole at an enemy, the hole deals {10 * (self.valor + 1)} damage per second and drags enemies towards it"

    def aplicar(self,jugador):
        tiempo_actual=pygame.time.get_ticks()
        if tiempo_actual - self.cd > self.ultima:
            from main import enemigos_sprites,Bala,balas_sprites
            self.ultima=pygame.time.get_ticks()
            nueva_bala = Bala(0, 2,
                              pygame.image.load('Sprites/Armas/Balas/Black-Hole-S.png').convert_alpha(),
                              jugador.base.rect.centerx, jugador.base.rect.y - 10, (jugador.base.rect.centerx, -1), 1,
                              tipo="Agujero Negro")
            for mejora in jugador.mejoras:
                if hasattr(mejora, 'aplicar_dis'):
                    mejora.aplicar_dis(jugador, nueva_bala)
            balas_sprites.add(nueva_bala)

    def aplicar_matar(self,jugador,enemigo):
        self.ultima -=500
    def aplicar_imp(self,jugador,bala,enemigo):
        if bala.tipo=="Agujero Negro":
            from Enemigos import Animacion
            from main import animaciones,Bala_temporal,balas_sprites
            radio=100 + (50*self.valor)

            animacion_redimensionada = redimensionar_animacion(self.animacion, radio * 2, radio * 2)
            animacion = Animacion(enemigo.rect.center, animacion_redimensionada, True, desaparecer=True)
            nuevo_tamaño = (int(radio * 2), int(radio * 2))
            sprite_redimensionado = pygame.transform.scale(pygame.image.load('Sprites/Armas/Balas/X.png').convert_alpha(), nuevo_tamaño)
            nueva_bala = Bala_temporal(10 * self.valor, 0,
                                       sprite_redimensionado,
                                       enemigo.rect.centerx, enemigo.rect.centery, (0, 0), 5000, tipo="Succion", eficiencia=0.1)
            nueva_bala.rect.centerx-=radio
            nueva_bala.rect.centery -= radio
            balas_sprites.add(nueva_bala)
            animaciones.add(animacion)

Agujero=Agujero()
mejoras_legendarias.append(Agujero)

print(len(mejoras_normales))
print(len(mejoras_raras))
print(len(mejoras_legendarias))