import pygame
from definiciones import TILE
import herramientas
import fx
class Interactuable:
    def __init__(self,padre):
        self.padre = padre
    def interactuar(self,juego):
        pass


class AgarrarLLave(Interactuable):
    def interactuar(self,juego):
        if juego.jugador.rect.colliderect(self.padre.rect):
            pygame.mixer.Sound("sonidos/agarrar.wav").play()

            self.padre.puerta.cantidad_de_llaves_necesarias -= 1
            self.padre.kill()

class AbrirPuertas(Interactuable):
    def __init__(self,padre):
        super().__init__(padre)
        # Aumento el area del margen para que el jugador pueda interactuar y que no colicione.
        self.area_interactuable = pygame.Rect(self.padre.rect.x-10,self.padre.rect.y-10,self.padre.rect.width+20,self.padre.rect.height+20)
    def interactuar(self, juego):
        if juego.jugador.rect.colliderect(self.area_interactuable):
            if self.padre.cantidad_de_llaves_necesarias < 1:
                self.padre.kill()
                juego.laberinto.eliminar_bloque_solido((self.padre.rect.x//TILE,self.padre.rect.y//TILE))
                # juego.texto_llaves.text = "Llaves Recogidas: " + str(4 - self.padre.cantidad_de_llaves_necesarias)

class GanarJuego(Interactuable):
    def __init__(self, padre):
        super().__init__(padre)
    def interactuar(self, juego):
        if juego.jugador.rect.colliderect(self.padre.rect):
            pygame.mixer.Sound("sonidos/agarrar.wav").play()
            juego.gano_juego = True

class AgarrarMartillo(Interactuable):
    def __init__(self, padre):
        super().__init__(padre)
    def interactuar(self, juego):
        if juego.jugador.rect.colliderect(self.padre.rect):
            pygame.mixer.Sound("sonidos/agarrar.wav").play()
            juego.jugador.manejo_herramientas.agregar(herramientas.RomperMuro(juego.jugador))
            juego.elementos_actualizables.add(fx.Cartel(self.padre.rect.x,self.padre.rect.y,"Martillo"))
            self.padre.kill()

class AgarrarBotiquin(Interactuable):
    def __init__(self, padre):
        super().__init__(padre)
    def interactuar(self, juego):
        if juego.jugador.rect.colliderect(self.padre.rect):
            pygame.mixer.Sound("sonidos/agarrar.wav").play()
            juego.jugador.manejo_herramientas.agregar(herramientas.Botiquin(juego.jugador))
            juego.elementos_actualizables.add(fx.Cartel(self.padre.rect.x,self.padre.rect.y,"Botiquin"))
            self.padre.kill()

class AgarrarBombaAturdidora(Interactuable):
    def __init__(self, padre):
        super().__init__(padre)
    def interactuar(self, juego):
        if juego.jugador.rect.colliderect(self.padre.rect):
            pygame.mixer.Sound("sonidos/agarrar.wav").play()
            juego.jugador.manejo_herramientas.agregar(herramientas.AturdirMinotauro(juego.jugador))
            juego.elementos_actualizables.add(fx.Cartel(self.padre.rect.x,self.padre.rect.y,"Bomba Aturdidora"))
            self.padre.kill()

class AgarrarBrujula(Interactuable):
    def __init__(self, padre):
        super().__init__(padre)
    def interactuar(self, juego):
        if juego.jugador.rect.colliderect(self.padre.rect):
            pygame.mixer.Sound("sonidos/agarrar.wav").play()
            juego.jugador.manejo_herramientas.agregar(herramientas.Brujula(juego.jugador))
            juego.elementos_actualizables.add(fx.Cartel(self.padre.rect.x,self.padre.rect.y,"Brujula"))
            self.padre.kill()