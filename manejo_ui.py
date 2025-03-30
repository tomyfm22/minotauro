import pygame,pygame_gui
import pygame_gui.ui_manager
from definiciones import *


# Clase que se encarga de mostrar la imagen de la herramienta seleccionada por el jugador.

class InventarioUI:
    def __init__(self):
        self.posicion = [ANCHO//2,ALTO-40]  # Posición donde se mostrarán los ítems

        self.font = pygame.Font("configuracion_ui/font/Perfect.ttf",20)
        self.texto = self.font.render("",False,(255,255,255))
        # Cargar imágenes de herramientas (debes reemplazar con las rutas correctas)
        self.tool_images = {
            -1 : [pygame.image.load("sprites/marco.png").convert_alpha(),""],
            BOTIQUIN : [pygame.image.load("sprites/marco_botiquin.png").convert_alpha(),"botiquin"],
            BOMBAATURDIDORA : [pygame.image.load("sprites/marco_bomba_aturdidora.png").convert_alpha(),"bomba aturdidora"],
            MARTILLO : [pygame.image.load("sprites/marco_martillo.png").convert_alpha(),"martillo"],
            BRUJULA : [pygame.image.load("sprites/marco_brujula.png").convert_alpha(),"brujula"],
        }

        self.delay = 0.5
        self.delay_desaparecer_texto = self.delay #segundos
        self.actualizar_imagen(-1)
  
    def actualizar_imagen(self,Id):
        self.item = self.tool_images[Id]
        self.texto = self.font.render(self.item[1],False,(255,255,255))
        self.delay_desaparecer_texto = self.delay

    def update(self,dt):
        if self.delay_desaparecer_texto > 0:
            self.delay_desaparecer_texto -= dt


    def draw(self,superficie):
        """ Dibuja las imágenes de las herramientas en la pantalla """
        x, y = self.posicion
    
        rect = self.item[0].get_rect()
        superficie.blit(self.item[0],(x - rect.width//2,y-rect.height))

        if self.delay_desaparecer_texto > 0:
            rect_texto = self.texto.get_rect()
            self.texto.set_alpha(255 * (self.delay_desaparecer_texto / self.delay))
            superficie.blit(self.texto,(x - rect_texto.width // 2,y-rect.height - rect_texto.height - 5))




class VidaUI:
    def __init__(self):
        self.font = pygame.font.Font("configuracion_ui/font/Perfect.ttf", 30)
        self.texto = self.font.render("Vida: 3", True, (255, 255, 255))
        self.rect = self.texto.get_rect()
        self.rect.x = 40
        self.rect.y = ALTO-40 - self.rect.height
    def actualizar_texto(self,jugador):
        self.texto = self.font.render("Vida: " + str(jugador.vida), True, (255, 255, 255))
        
    def draw(self,superficie):
        superficie.blit(self.texto,self.rect)