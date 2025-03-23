import pygame

# Componenete que hace que un objeto colicione con el jugador.
class Colicionable:
    # Recibe como parametro el rect de la instacia que utiliza el componente.
    def __init__(self,rect):
        self.rect = rect
    
    def chequear_colicion_x(self,rect:pygame.Rect,direccion:pygame.math.Vector2):
        if rect.colliderect(self.rect):
            if direccion.x > 0:
                rect.right = self.rect.left
            if direccion.x < 0:
                rect.left = self.rect.right
            
        return rect.x

    def chequear_colicion_y(self,rect:pygame.Rect,direccion:pygame.math.Vector2):
        if rect.colliderect(self.rect):
            if direccion.y > 0:
                rect.bottom = self.rect.top
            if direccion.y < 0:
                rect.top = self.rect.bottom
            
        return rect.y