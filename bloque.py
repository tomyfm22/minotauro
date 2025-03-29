import pygame
from definiciones import TILE,FPS
import math
from colicionable import Colicionable
from interactuable import *

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



class LLave(Bloque):
    def __init__(self, x, y,puerta):
        # surf = pygame.Surface((50,50))
        # surf.fill("yellow")
        super().__init__(x, y, pygame.image.load("sprites/llave.png").convert_alpha())
        self.rect.center = (x * TILE + TILE // 2,y * TILE + TILE // 2)
        self.interactuable = AgarrarLLave(self)
        self.tiempo = 0
        self.posicion_inicial = self.rect.y

        # Recibe la referencia a la puerta que abre
        self.puerta = puerta
        
        self.z_index = 1

    def update(self, dt, juego):
        self.interactuable.interactuar(juego)
        self.tiempo += dt
        self.rect.y = 10 * math.sin(self.tiempo * 4) + self.posicion_inicial
    
class Puerta(Bloque):
    def __init__(self, x, y):
        super().__init__(x, y, pygame.image.load("sprites/puerta.png").convert_alpha())

        self.colicion = Colicionable(self.rect)
        self.esta_abierta = False
        self.abrir_puerta = AbrirPuertas(self)

        self.cantidad_de_llaves_necesarias = 4

        self.z_index = 1

    def update(self, dt, juego):
        self.abrir_puerta.interactuar(juego)
        
        if self.esta_abierta:
            # juego.gano_juego = True
            print("GANO")


class Salida(Bloque):
    def __init__(self, x, y):
        super().__init__(x, y, pygame.image.load("sprites/salida.png").convert_alpha())
        self.ganarJuego = GanarJuego(self)
        self.z_index = 1
    
    def update(self, dt, juego):
        self.ganarJuego.interactuar(juego)


class ItemRompeMuro(Bloque):
    def __init__(self, x, y):
        super().__init__(x, y, pygame.image.load("sprites/rompe_muros.png").convert_alpha())
        self.agarrar_item = AgarrarMartillo(self)
        self.z_index = 1
    def update(self, dt, juego):
        self.agarrar_item.interactuar(juego)

class ItemBotiquin(Bloque):
    def __init__(self, x, y):
        super().__init__(x, y, pygame.image.load("sprites/botiquin.png").convert_alpha())
        self.agarrar_item = AgarrarBotiquin(self)
        self.z_index = 1
    def update(self, dt, juego):
        self.agarrar_item.interactuar(juego)

class ItemAturdirMinotauro(Bloque):
    def __init__(self, x, y):
        super().__init__(x, y,pygame.image.load("sprites/bomba_aturdidora.png").convert_alpha())
        self.agarrar_item = AgarrarBombaAturdidora(self)
        self.z_index = 1
    def update(self, dt, juego):
        self.agarrar_item.interactuar(juego)

class ItemBrujula(Bloque):
    def __init__(self, x, y):
        super().__init__(x, y,pygame.image.load("sprites/brujula.png").convert_alpha())
        self.agarrar_item = AgarrarBrujula(self)
        self.z_index = 1
    def update(self, dt, juego):
        self.agarrar_item.interactuar(juego)