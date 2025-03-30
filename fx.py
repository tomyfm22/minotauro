import pygame
from definiciones import FPS,TILE

# Clase que se encarga de mostrar un texto durante un tiempo.
class Cartel(pygame.sprite.Sprite):
    def __init__(self,x,y,txt,delay = 0.5):
        super().__init__()
        self.font = pygame.font.Font("configuracion_ui/font/Perfect.ttf", 30)
        self.texto = self.font.render(txt, True, (255, 255, 255))
        self.rect = self.texto.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.delay = delay
        self.vely  = 0.3
    
    def update(self,dt,juego):
        self.delay -= dt
        self.rect.y -= self.vely * dt * FPS
        if self.delay < 0:
            self.kill()
    
    def draw(self,superficie,offset):
        rect = self.texto.get_rect()
        superficie.blit(self.texto,(self.rect.x - offset[0] + TILE // 2 - rect.width // 2,self.rect.y - offset[1] + TILE // 2 - rect.height // 2))
    


# Clase que se encarga de mostrar una explosion cuando el jugador lanza una bomba aturdidora.
class ExplosionBombaAturdidora(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.superficie = pygame.Surface((TILE,TILE),pygame.SRCALPHA)
        self.superficie.fill("white")
        self.rect = self.superficie.get_rect()
        self.rect.center = (x + TILE // 2,y + TILE // 2)
        self.delay_max = 0.5
        self.delay = self.delay_max
    

    def update(self,dt,juego):
        self.delay -= dt
        # agranda la imagen y bajo el alpha para que se vea como una explosion.
        self.superficie = pygame.transform.scale(self.superficie,(self.rect.width + (1 - self.delay/self.delay_max) * 2,self.rect.height + (1 - self.delay/self.delay_max) * 2 ))
        self.superficie.set_alpha(255 * self.delay/self.delay_max)
        self.rect = self.superficie.get_rect(center=self.rect.center)
        if self.delay <= 0:
            self.kill()
    def draw(self,superficie,offset):
        superficie.blit(self.superficie,(self.rect.x - offset[0],self.rect.y - offset[1]))


