import pygame
from  definiciones import TILE , FPS
from herramientas import *

# Clase del jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()



        self.imagen = pygame.image.load("sprites/jugador.png").convert_alpha()
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocidad = 20
        self.direccion = pygame.math.Vector2(0,0)
        self.muros_cercano = []
        self.vida  = 3
        self.inmune = False 
        self.delay_inmune = 2 # segundos
        self.direccion_mirando = pygame.math.Vector2(0,0)

        self.manejo_herramientas = ManenjoHerramientas()


    def recibir_danio(self):
        if self.inmune:
            return
        pygame.mixer.Sound("sonidos/golpeado.wav").play()
        self.vida -= 1
        self.delay_inmune = 2
        self.inmune = True

    def manejo_movimiento(self,dt,bloques):
        direccion_normal = pygame.math.Vector2(0,0)
        if self.direccion.length() > 0:
            direccion_normal = pygame.math.Vector2(self.direccion).normalize()

        self.muros_cercano = []
        self.muros_cercano = bloques
        self.rect.x += self.velocidad * direccion_normal.x * dt * FPS
        rect = pygame.Rect(self.rect.x,self.rect.y,self.rect.width,self.rect.height)
        
        for i in self.muros_cercano:
            if "colicion" in i.__dict__:
                self.rect.x = i.colicion.chequear_colicion_x(rect,self.direccion)

        
        self.rect.y += self.velocidad * direccion_normal.y * dt * FPS
        rect = pygame.Rect(self.rect.x,self.rect.y,self.rect.width,self.rect.height)
        for i in self.muros_cercano:

            if "colicion" in i.__dict__:
                self.rect.y = i.colicion.chequear_colicion_y(rect,self.direccion)




    def manejo_entrada(self,eventos):
        teclas = pygame.key.get_pressed()
        self.direccion = pygame.math.Vector2(0,0)
        if teclas[pygame.K_LEFT]:
            self.direccion.x = -1
            self.direccion_mirando.x = -1
            self.direccion_mirando.y = 0
        if teclas[pygame.K_RIGHT]:
            self.direccion.x = 1
            self.direccion_mirando.x = 1
            self.direccion_mirando.y = 0
        if teclas[pygame.K_UP]:
            self.direccion.y = -1
            self.direccion_mirando.y = -1
            self.direccion_mirando.x = 0
        if teclas[pygame.K_DOWN]:
            self.direccion.y = 1
            self.direccion_mirando.y = 1
            self.direccion_mirando.x = 0
       
        # teclas = pygame.key.get_just_pressed()
        # if teclas[pygame.K_SPACE]:
            # self.inventario[0].usar()
        



    def update(self,dt,juego):
        self.manejo_movimiento(dt,juego.quad_tree.consulta(pygame.Rect(self.rect.x - TILE * 2,self.rect.y - TILE * 2,self.rect.width + TILE * 4,self.rect.height + TILE * 4)))
        
        juego.texto_vida.set_text( "Vida: " + str(self.vida))
        if self.inmune:
            self.delay_inmune -= dt
            if self.delay_inmune < 0:
                self.inmune = False

        teclas = pygame.key.get_just_pressed()
        self.manejo_herramientas.usar_herramienta(juego,teclas)
        self.manejo_herramientas.update(dt,juego)
            

    def draw(self,superficie,offset:tuple[int,int]):
        superficie.blit(self.imagen,(self.rect.x - offset[0],self.rect.y - offset[1]))
        self.manejo_herramientas.draw(superficie,offset)
        # for i in self.muros_cercano:
            # pygame.draw.rect(superficie,"white",(i[0].rect.x - offset[0],i[0].rect.y - offset[1],i[0].rect.width,i[0].rect.width))