import pygame


# Componente que hace que un objeto sea rompible.
class Rompible:
    def __init__(self,padre):
        self.padre = padre
    
    def romper(self):
        self.padre.kill()
