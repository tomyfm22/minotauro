import pygame
from definiciones import TILE
import math
class ItemBase(pygame.sprite.Sprite):
    def __init__(self,x,y,imagen:pygame.Surface):
        super().__init__()
        self.imagen = imagen
        self.rect = imagen.get_rect()
        self.rect.x = x * TILE
        self.rect.y = y * TILE
    
    def update(self,dt,juego):
        pass
    def draw(self,superficie,offset):
        superficie.blit(self.imagen,(self.rect.x - offset[0],self.rect.y - offset[1]))

    def colicion_con_jugador(self,jugador):
        pass




class LLave(ItemBase):
    def __init__(self, x, y):
        surf = pygame.Surface((50,50))
        surf.fill("yellow")
        super().__init__(x, y, surf)
    
    def update(self, dt, juego):
        self.colicion_con_jugador(juego)
        self.rect.y += 2 * math.sin(dt * 4)


    def colicion_con_jugador(self, juego):
        jugador = juego.jugador
        if self.rect.colliderect(jugador.rect):
            jugador.llaves += 1
            juego.laberinto.eliminar_elemento("llaves",(self.rect.x//TILE,self.rect.y//TILE))
            # self.kill()
            # del self
    
class Puerta(ItemBase):
    def __init__(self, x, y):
        surf = pygame.Surface((TILE,TILE))
        surf.fill("orange")
        super().__init__(x, y, surf)

        self.esta_abierta = False
    
    def update(self, dt, juego):
        self.colicion_con_jugador(juego)
        if self.esta_abierta:
            # juego.gano_juego = True
            print("GANO")

    def colicion_con_jugador(self, juego):
        jugador = juego.jugador        
        if self.rect.colliderect(jugador.rect):
            juego.laberinto.eliminar_elemento("puerta",(self.rect.x//TILE,self.rect.y//TILE))
                        
