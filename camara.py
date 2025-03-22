from definiciones import *
import pygame,random


class Camara:
    def __init__(self,posx,posy,objetivo = None):
        self.posx = posx
        self.posy = posy
        self.objetivo = objetivo

        self.offsetx,self.offsety = 0,0

        self.cam_box = pygame.Rect(0,0,ANCHO,ALTO)

        self.centro_cam_box = [self.cam_box.center[0],self.cam_box.center[1]]

        self.shake_duracion     = 1
        self.shake_remain       = 0
        self.shake_magnitud     = 0

        self.factor_zoom        = 2
    
    def update(self,dt):
        
        self.centro_cam_box[0] += (self.objetivo.rect.center[0] - self.centro_cam_box[0])  #* dt
        self.centro_cam_box[1] += (self.objetivo.rect.center[1] - self.centro_cam_box[1])  #* dt
        
        self.posx = self.centro_cam_box[0] - self.cam_box.width // 2
        self.posy = self.centro_cam_box[1] - self.cam_box.height // 2
  
        # if self.posx + self.cam_box.width > TAMANIO_MAPA[0]:
        #     self.posx = TAMANIO_MAPA[0] - self.cam_box.width 
        # if self.posy + self.cam_box.height > TAMANIO_MAPA[1]:
        #     self.posy = TAMANIO_MAPA[1] - self.cam_box.height 

        # # Efecto sacudon.
        # self.posx += random.uniform(-self.shake_remain,self.shake_remain)
        # self.posy += random.uniform(-self.shake_remain,self.shake_remain)
        
        if self.posx < 0:
            self.posx = 0
        if self.posy < 0:
            self.posy = 0



        # self.shake_remain = max(0,self.shake_remain - (1 / self.shake_duracion) * self.shake_magnitud)

    def sacudircamara(self,mag,dur):
        self.shake_magnitud = mag
        self.shake_remain = mag
        self.shake_duracion = dur

    def obtener_offset(self):
        return (int(self.posx),int(self.posy))

