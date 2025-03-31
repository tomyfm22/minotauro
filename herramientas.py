import pygame
from definiciones import *
import math
from bloque import Muro
from fx import ExplosionBombaAturdidora

# Clase base de herramientas
# Recibe como parametro el jugador y el id de la herramienta.
class Herramientas:
    def __init__(self,jugador,Id):
        self.jugador = jugador
        self.id     = Id
    def usar(self,juego):
        pass
    def update(self,dt,juego):
        pass
    def draw(self,superficie,offset):
        pass


class RomperMuro(Herramientas):
    def __init__(self, jugador):
        super().__init__(jugador,MARTILLO)
        self.posicion_bloque = (0,0)
        self.usos = 1
    def usar(self, juego):
        
        self.posicion_bloque = (self.jugador.rect.centerx // TILE * TILE + self.jugador.direccion_mirando.x * TILE,self.jugador.rect.centery // TILE * TILE + self.jugador.direccion_mirando.y * TILE)
        bloques = juego.quad_tree.consulta(pygame.rect.Rect(self.posicion_bloque[0],self.posicion_bloque[1],TILE,TILE))


        if bloques:
            bloque = bloques[0]
            # Verifico si el bloque tiene un componente que lo hace rompible.
            if "rompible" in bloque.__dict__:
                bloque.rompible.romper()
                self.usos -= 1
                juego.laberinto.eliminar_bloque_solido((self.posicion_bloque[0]//TILE,self.posicion_bloque[1]//TILE))
                pygame.mixer.Sound("sonidos/romper.wav").play()
        pygame.mixer.Sound("sonidos/movimiento_invalido.wav").play()
          
    def update(self,dt,juego):
        self.posicion_bloque = (self.jugador.rect.centerx // TILE * TILE + self.jugador.direccion_mirando.x * TILE,self.jugador.rect.centery // TILE * TILE + self.jugador.direccion_mirando.y * TILE)

    def draw(self,superficie,offset):
        pygame.draw.rect(superficie,"white",(self.posicion_bloque[0] - offset[0],self.posicion_bloque[1] - offset[1],TILE,TILE),2)

class Botiquin(Herramientas):
    def __init__(self, jugador):
        super().__init__(jugador,BOTIQUIN)
        self.usos = 1
    def usar(self, juego):
        if self.jugador.vida < 3:
            pygame.mixer.Sound("sonidos/curarse.wav").play()
            self.jugador.vida += 1
            self.usos -= 1
            juego.vida_ui.actualizar_texto(juego.jugador)

class AturdirMinotauro(Herramientas):
    def __init__(self, jugador):
        super().__init__(jugador,BOMBAATURDIDORA)
        self.usos = 1
        self.pos_minotauro = (0,0)
        self.posicion_bloque = (0,0)
    def update(self,dt,juego):
        self.posicion_bloque = (self.jugador.rect.centerx // TILE * TILE + self.jugador.direccion_mirando.x * TILE,self.jugador.rect.centery // TILE * TILE + self.jugador.direccion_mirando.y * TILE)
    def usar(self, juego):
        self.pos_minotauro = (juego.minotauro.rect.centerx // TILE,juego.minotauro.rect.centery // TILE)
        posicion_jugador_mirando = (self.jugador.rect.centerx // TILE + self.jugador.direccion_mirando.x ,self.jugador.rect.centery // TILE + self.jugador.direccion_mirando.y)
        posicion_jugador = (self.jugador.rect.centerx // TILE,self.jugador.rect.centery // TILE)
        if self.pos_minotauro == posicion_jugador or self.pos_minotauro == posicion_jugador_mirando:
            juego.minotauro.aturdir()
            pygame.mixer.Sound("sonidos/bomba_aturdidora.wav").play()
            juego.camara.sacudir_camara(10,2)
            juego.elementos_actualizables.add(ExplosionBombaAturdidora(self.pos_minotauro[0] * TILE,self.pos_minotauro[1] * TILE))
            self.usos -= 1
        pygame.mixer.Sound("sonidos/movimiento_invalido.wav").play()
    def draw(self,superficie,offset):
        pygame.draw.rect(superficie,"white",(self.posicion_bloque[0] - offset[0],self.posicion_bloque[1] - offset[1],TILE,TILE),2)

class Brujula(Herramientas):
    def __init__(self,jugador):
        super().__init__(jugador,BRUJULA)
        self.usos = 1
    
    def usar(self,juego):
        self.usos -= 1
        elementos = pygame.sprite.Group()
        for i in juego.laberinto.objetos["llaves"]:
            elementos.add(i)
        for i in  juego.laberinto.objetos["puerta"]:
            elementos.add(i)
            
        juego.elementos_actualizables.add(BrujulaVisual(elementos))

class BrujulaVisual(pygame.sprite.Sprite):
    def __init__(self,objetos_interes):
        super().__init__()
        self.delay = 20
        self.imagen = pygame.image.load("sprites/flecha.png").convert_alpha()
        self.objetivo = None
        self.objetos_interes = objetos_interes
        self.pos_jugador = None

        self.mostrar_imagen = True
        self.frecuencia_max = 0.5
        self.frecuencia = 0.5

    def obtener_elemento_cercano(self,jugador):
        if self.objetos_interes:
            self.pos_jugador = pygame.math.Vector2(jugador.rect.x,jugador.rect.y)
            
            self.objetivo = min(self.objetos_interes, key=lambda objeto: self.pos_jugador.distance_to(pygame.math.Vector2(objeto.rect.x,objeto.rect.y)))
        else:
            self.kill()

    def update(self,dt,juego):
        self.delay -= dt

        if self.delay < 5:
            # Empieza a parpadear la imagen cada vez mas rapido.
            self.frecuencia -= dt
            if self.frecuencia < 0:
                self.mostrar_imagen = not self.mostrar_imagen
                self.frecuencia = self.frecuencia_max
            self.frecuencia_max = max(0.1,self.frecuencia_max - 0.1 * dt)

            



        if self.delay < 0:
            self.kill()
        jugador = juego.jugador
        self.obtener_elemento_cercano(jugador)
        


    def draw(self,superficie,offset):
        if not self.objetivo or not self.mostrar_imagen:
            return
        dx = self.objetivo.rect.x - self.pos_jugador[0]
        dy = self.objetivo.rect.y - self.pos_jugador[1]
        angulo = math.degrees(math.atan2(dy, dx))


        rotada = pygame.transform.rotate(self.imagen, -angulo)
        rect = rotada.get_rect(center=(self.pos_jugador[0] - offset[0] + TILE // 2,self.pos_jugador[1] - offset[1] + TILE // 2))
        superficie.blit(rotada, rect)



class ManenjoHerramientas:
    def __init__(self):
        self.indice = -1 #-1 porque no hay herramientas al principio.
        self.herramientas = []
    def agregar(self,herramienta:Herramientas):
        self.herramientas.append(herramienta)
        # self.indice = len(self.herramientas) - 1
    def usar_herramienta(self,juego,teclas):
        if self.indice == -1 and len(self.herramientas) > 0:
            self.indice = 0
            juego.inventario_ui.actualizar_imagen(self.herramientas[self.indice].id)
            

            
        if len(self.herramientas) > 0:
            if teclas[pygame.K_SPACE]:
                self.herramientas[self.indice].usar(juego)
                if self.herramientas[self.indice].usos <= 0:
                    self.herramientas.pop(self.indice)
                    if len(self.herramientas) == 0:
                        self.indice = -1
                        juego.inventario_ui.actualizar_imagen(self.indice)

                    else:
                        self.indice = len(self.herramientas) - 1
                        juego.inventario_ui.actualizar_imagen(self.herramientas[self.indice].id)
                    

            if teclas[pygame.K_z]:
                self.indice -= 1
                if self.indice < 0:
                    self.indice = len(self.herramientas)-1
                juego.inventario_ui.actualizar_imagen(self.herramientas[self.indice].id)
                

            if teclas[pygame.K_x]:
                self.indice += 1
                if self.indice == len(self.herramientas):
                    self.indice = 0
                juego.inventario_ui.actualizar_imagen(self.herramientas[self.indice].id)
        
        # if len(self.herramientas) == 0:
        #     juego.inventario_ui.item = juego.inventario_ui.actualizar_imagen(-1)
    def update(self,dt,juego):
        if len(self.herramientas) > 0:
            self.herramientas[self.indice].update(dt,juego)
        
    def draw(self,superficie,offset):
        if len(self.herramientas) > 0:
            self.herramientas[self.indice].draw(superficie,offset)