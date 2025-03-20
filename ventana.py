import pygame
import definiciones
from jugador import Jugador
from laberinto import Laberinto

class Ventana:
    def __init__(self):
        pass
    def draw(self,superficie):
        pass
    def update(self,dt):
        pass




class VentanaJuego(Ventana):
    def __init__(self):
        super().__init__()

        self.jugador = Jugador(0,0)
        self.laberinto = Laberinto()

    def update(self, dt):
        eventos = pygame.event.get()

        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        self.jugador.manejo_entrada(eventos)
        self.jugador.update(dt,self)

    def draw(self,superficie):
        self.laberinto.draw(superficie)
        self.jugador.draw(superficie)