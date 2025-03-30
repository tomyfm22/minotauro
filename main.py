import pygame
import definiciones
import manejo_ventanas
pygame.init()

# Punto de entrada del juego.
class Main:
    def __init__(self):
        self.window = pygame.display.set_mode((definiciones.ANCHO,definiciones.ALTO))
        self.clock = pygame.time.Clock()
        self.manejo_ventana = manejo_ventanas.ManejoVentana()
    
    
    def draw(self): 
        self.window.fill((0,0,0,0))

        self.manejo_ventana.draw(self.window)
    
    def update(self,dt):
        self.manejo_ventana.update(dt)
    
    def run(self): 
        dt = 0
        while True:
            self.update(min(1,dt/1000))
            self.draw()

            pygame.display.flip()
            dt = self.clock.tick(definiciones.FPS)


main = Main()

main.run()
    