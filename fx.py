import pygame
from definiciones import FPS,TILE


class Cartel(pygame.sprite.Sprite):
    def __init__(self,x,y,txt):
        super().__init__()
        self.font = pygame.font.Font("configuracion_ui/font/Perfect.ttf", 30)
        self.texto = self.font.render(txt, True, (255, 255, 255))
        self.rect = self.texto.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.delay = 0.5
        self.vely  = 0.3
    
    def update(self,dt,juego):
        self.delay -= dt
        self.rect.y -= self.vely * dt * FPS
        if self.delay < 0:
            self.kill()
    
    def draw(self,superficie,offset):
        rect = self.texto.get_rect()
        superficie.blit(self.texto,(self.rect.x - offset[0] + TILE // 2 - rect.width // 2,self.rect.y - offset[1] + TILE // 2 - rect.height // 2))
    



