import pygame
from  definiciones import TILE

class Jugador(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.imagen = pygame.Surface((50,50))
        self.imagen.fill("red")
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 20
        self.direccion = pygame.math.Vector2(0,0)
        self.muros_cercano = []
        self.llaves = 0

    def obtener_muros_cercanos(self,colicionables):
        
        self.muros_cercano = []
        pos = (self.rect.x//TILE,self.rect.y//TILE)
        direcciones = [(1,0),(-1,0),(1,1),(-1,1),(-1,-1),(0,1),(0,-1),(1,-1)]
        
        
        for direccion in direcciones:
            muro_vecino = (pos[0] + direccion[0],pos[1] + direccion[1])
            if muro_vecino in colicionables:
                self.muros_cercano.append(colicionables[muro_vecino])

    def manejo_movimiento(self,dt,laberinto):
        direccion_normal = pygame.math.Vector2(0,0)
        if self.direccion.length() > 0:
            direccion_normal = pygame.math.Vector2(self.direccion).normalize()

        self.obtener_muros_cercanos(laberinto.obtener_elementos_colicionables())
        
        tamanio = 50
        self.rect.x += self.velocidad * direccion_normal.x
        rect = pygame.Rect(self.rect.x,self.rect.y,tamanio,tamanio)
        for i in self.muros_cercano:
            if rect.colliderect(i.rect):
                if self.direccion.x > 0:
                    rect.right = i.rect.left
                if self.direccion.x < 0:
                    rect.left = i.rect.right
                
                self.rect.x = rect.x
        
        self.rect.y += self.velocidad * direccion_normal.y
        rect = pygame.Rect(self.rect.x,self.rect.y,tamanio,tamanio)
        for i in self.muros_cercano:
            if rect.colliderect(i.rect):
                if self.direccion.y > 0:
                    rect.bottom = i.rect.top
                if self.direccion.y < 0:
                    rect.top = i.rect.bottom
                
                self.rect.y = rect.y



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
    
    def draw(self,superficie,offset:tuple[int,int]):
        superficie.blit(self.imagen,(self.rect.x - offset[0],self.rect.y - offset[1]))
        for i in self.muros_cercano:
            pygame.draw.rect(superficie,"white",(i.rect.x - offset[0],i.rect.y - offset[1],i.rect.width,i.rect.width))
