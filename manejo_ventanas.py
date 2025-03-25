import pygame

from ventana import *
from transicion import *

# Clase que se encarga de mostrar las distintas escenas del juego y la transicion entre ellas.

class ManejoVentana:
    def __init__(self):
        self.ventana_actual = MenuPrincipal(self)
        self.nueva_ventana = None
    
        self.ventanas = {"juego" : VentanaJuego,
                         "menu" : MenuPrincipal,
                         "fin" : FinDelJuego,}
        self.transicion = Transicion()

    def cambiar_ventana(self,ventana:str):
        self.nueva_ventana = ventana
        self.transicion.iniciar()
    
    def update(self,dt):
        self.transicion.update(dt)
        if self.transicion.estado == TERMINO:
            if not self.nueva_ventana:
                self.ventana_actual.update(dt)
        else:
            # Realizar la transicion y luego cambiar la escena.
            if self.transicion.estado == ESPERANDO and self.nueva_ventana:
                self.ventana_actual = self.ventanas[self.nueva_ventana](self)
                self.nueva_ventana = None

    def draw(self,superficie):
        self.ventana_actual.draw(superficie)
        self.transicion.draw(superficie)