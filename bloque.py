import pygame
from definiciones import TILE
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
    def update(self, dt,juego):
        pass
    def draw(self,superficie:pygame.Surface,offset:tuple[int,int]):
        superficie.blit(self.imagen,(self.rect.x - offset[0],self.rect.y - offset[1]))




class Muro(Bloque):
    def __init__(self, x, y):
        imagen = pygame.Surface((TILE,TILE))
        imagen.fill("green")
        super().__init__(x, y, imagen)
        self.colicion = Colicionable(self.rect)





class LLave(Bloque):
    def __init__(self, x, y):
        surf = pygame.Surface((50,50))
        surf.fill("yellow")
        super().__init__(x, y, surf)
        self.interactuable = AgarrarLLave(self)
    
    def update(self, dt, juego):
        # self.colicion_con_jugador(juego)
        self.interactuable.interactuar(juego)
        self.rect.y += 2 * math.sin(dt * 4)


    def colicion_con_jugador(self, juego):
        jugador = juego.jugador
        if self.rect.colliderect(jugador.rect):
            jugador.llaves += 1
            juego.laberinto.eliminar_elemento("llaves",(self.rect.x//TILE,self.rect.y//TILE))
            # self.kill()
            # del self
    
class Puerta(Bloque):
    def __init__(self, x, y):
        surf = pygame.Surface((TILE,TILE))
        surf.fill("orange")
        super().__init__(x, y, surf)

        self.colicion = Colicionable(self.rect)
        self.esta_abierta = False
        self.abrir_puerta = AbrirPuertas(self)
    def update(self, dt, juego):
        self.abrir_puerta.interactuar(juego)
        
        if self.esta_abierta:
            # juego.gano_juego = True
            print("GANO")