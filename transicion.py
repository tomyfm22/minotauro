import pygame
from definiciones import *



class Transicion:
    def __init__(self):
        self.superficie = pygame.Surface((ANCHO,ALTO))
        self.superficie.fill("black")
        self.pos_objetivo = 0
        self.posicion = [0,-ALTO]
        self.delay_max = 0.5
        self.delay = self.delay_max
        self.estado = TERMINO
    
    def iniciar(self):
        self.estado = FADEIN

    def update(self,dt):
        if self.estado == TERMINO:
            return
        
        if self.estado == FADEIN:

            self.posicion[1] += (self.pos_objetivo - self.posicion[1]) * 0.5
            if abs(self.posicion[1] - self.pos_objetivo) < 1:
                self.posicion[1] = 0
                self.estado = ESPERANDO
        elif self.estado == ESPERANDO:       
            self.delay -= dt
            if self.delay < 0:
                self.delay = self.delay_max
                self.estado = FADEOUT
        elif self.estado == FADEOUT:
            self.posicion[1] += (-ALTO - self.posicion[1]) * 0.125
            if abs(self.posicion[1] + ALTO) < 1:
                self.posicion[1] = -ALTO
                self.estado = TERMINO



    def draw(self,superficie:pygame.Surface):
        if self.estado == TERMINO:
            return
        superficie.blit(self.superficie,self.posicion)
    