import pygame
from definiciones import TILE,FPS
import math
from colicionable import Colicionable
from interactuable import *
from rompible import Rompible

# Clase base de un bloque del laberinto.
class Bloque(pygame.sprite.Sprite):
    def __init__(self,x,y,imagen:pygame.Surface):
        super().__init__()
        self.imagen = imagen
        self.rect = imagen.get_rect()
        self.rect.x = x * TILE
        self.rect.y = y * TILE

        self.z_index = 0 # para poder ordenarlo y dibujarlo en el orden correcto.

    def update(self, dt,juego):
        pass
    def draw(self,superficie:pygame.Surface,offset:tuple[int,int]):
        superficie.blit(self.imagen,(self.rect.x - offset[0],self.rect.y - offset[1]))




class Muro(Bloque):
    def __init__(self, x, y,imagen):
        super().__init__(x, y, imagen)
        self.colicion = Colicionable(self.rect)
        self.rompible = Rompible(self)

class Limite(Bloque):
    def __init__(self, x, y,imagen):
        super().__init__(x, y, imagen)
        self.colicion = Colicionable(self.rect)
        



class Puerta(Bloque):
    def __init__(self, x, y):
        super().__init__(x, y, pygame.image.load("sprites/puerta.png").convert_alpha())

        self.colicion = Colicionable(self.rect)
        self.abrir_puerta = AbrirPuertas(self)

        self.cantidad_de_llaves_necesarias = 4

        self.z_index = 1

    def update(self, dt, juego):
        self.abrir_puerta.interactuar(juego)
        self.abrir_puerta.update(dt,juego)
        


class Salida(Bloque):
    def __init__(self, x, y):
        super().__init__(x, y, pygame.image.load("sprites/salida.png").convert_alpha())
        self.ganarJuego = GanarJuego(self)
        self.z_index = 1
    
    def update(self, dt, juego):
        self.ganarJuego.interactuar(juego)



class Item(Bloque):
    def __init__(self,x,y,imagen):
        super().__init__(x,y,imagen)
        self.rect.center = (x * TILE + TILE // 2,y * TILE + TILE // 2)
        self.tiempo = 0
        self.posicion_inicial = self.rect.y
        self.z_index = 1


    def mover_vertical(self,dt):
        self.tiempo += dt
        self.rect.y = 10 * math.sin(self.tiempo * 4) + self.posicion_inicial



class LLave(Item):
    def __init__(self, x, y,puerta):
        super().__init__(x, y, pygame.image.load("sprites/llave.png").convert_alpha())
        self.interactuable = AgarrarLLave(self)

        # Recibe la referencia a la puerta que abre
        self.puerta = puerta
        

    def update(self, dt, juego):
        self.interactuable.interactuar(juego)
        self.mover_vertical(dt)

class ItemRompeMuro(Item):
    def __init__(self, x, y):
        super().__init__(x, y, pygame.image.load("sprites/rompe_muros.png").convert_alpha())
        self.agarrar_item = AgarrarMartillo(self)
    def update(self, dt, juego):
        self.agarrar_item.interactuar(juego)
        self.mover_vertical(dt)

class ItemBotiquin(Item):
    def __init__(self, x, y):
        super().__init__(x, y, pygame.image.load("sprites/botiquin.png").convert_alpha())
        self.agarrar_item = AgarrarBotiquin(self)
    def update(self, dt, juego):
        self.agarrar_item.interactuar(juego)
        self.mover_vertical(dt)

class ItemAturdirMinotauro(Item):
    def __init__(self, x, y):
        super().__init__(x, y,pygame.image.load("sprites/bomba_aturdidora.png").convert_alpha())
        self.agarrar_item = AgarrarBombaAturdidora(self)
    def update(self, dt, juego):
        self.agarrar_item.interactuar(juego)
        self.mover_vertical(dt)

class ItemBrujula(Item):
    def __init__(self, x, y):
        super().__init__(x, y,pygame.image.load("sprites/brujula.png").convert_alpha())
        self.agarrar_item = AgarrarBrujula(self)
    def update(self, dt, juego):
        self.agarrar_item.interactuar(juego)
        self.mover_vertical(dt)