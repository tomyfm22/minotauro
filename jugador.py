import pygame
import definiciones

class Jugador(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.imagen = pygame.Surface((50,50))
        self.imagen.fill("red")
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 10
        self.direccion = pygame.math.Vector2(0,0)


    def manejo_movimiento(self,dt,laberinto):
        direccion_normal = pygame.math.Vector2(0,0)
        if self.direccion.length() > 0:
            direccion_normal = pygame.math.Vector2(self.direccion).normalize()
            self.rect.x += direccion_normal.x * self.velocidad
            self.rect.y += direccion_normal.y * self.velocidad


    def manejo_entrada(self,eventos):
        teclas = pygame.key.get_pressed()
        self.direccion = pygame.math.Vector2(0,0)
        if teclas[pygame.K_LEFT]:
            self.direccion.x = -1
        if teclas[pygame.K_RIGHT]:
            self.direccion.x = 1
        if teclas[pygame.K_UP]:
            self.direccion.y = -1
        if teclas[pygame.K_DOWN]:
            self.direccion.y = 1

        
        



    def update(self,dt,juego):
        self.manejo_movimiento(dt,juego.laberinto)
    
    def draw(self,superficie):
        superficie.blit(self.imagen,self.rect)
