import pygame
import definiciones
import ventana
pygame.init()


class Main:
    def __init__(self):
        self.window = pygame.display.set_mode((definiciones.ANCHO,definiciones.ALTO))
        self.clock = pygame.time.Clock()
        self.ventana_actual = ventana.VentanaJuego()
    
    
    def draw(self):
        self.window.fill((0,0,0,0))

        self.ventana_actual.draw(self.window)
    
    def update(self,dt):
        self.ventana_actual.update(dt)
    
    def run(self):
        dt = 0
        while True:
            self.update(min(1,dt/1000))
            self.draw()
            pygame.display.flip()
            dt = self.clock.tick(definiciones.FPS)



main = Main()

main.run()
    