import pygame
class Interactuable:
    def __init__(self,padre):
        self.padre = padre
    def interactuar(self,juego):
        pass


class AgarrarLLave(Interactuable):
    def interactuar(self,juego):
        if juego.jugador.rect.colliderect(self.padre.rect):
            juego.cantidad_llaves -= 1
            self.padre.kill()

class AbrirPuertas(Interactuable):
    def __init__(self,padre):
        # Aumento el area del margen para que el jugador pueda interactuar y que no colicione.
        self.area_interactuable = pygame.Rect(self.padre.rect.x-10,self.padre.rect.y-10,self.padre.rect.width+10,self.padre.rect.height+10)
    def interactuar(self, juego):
        if juego.jugador.rect.colliderect(self.area_interactuable):
            if juego.cantidad_llaves < 1:
                self.padre.kill()