import pygame
from definiciones import *
class Herramientas:
    def __init__(self,jugador,Id):
        self.jugador = jugador
        self.id     = Id
    def usar(self,juego):
        pass


class RomperMuro(Herramientas):
    def __init__(self, jugador):
        super().__init__(jugador,MARTILLO)
        self.usos = 1
    def usar(self, juego):
        
        posicion_bloque = (self.jugador.rect.centerx // TILE * TILE + self.jugador.direccion_mirando.x * TILE,self.jugador.rect.centery // TILE * TILE + self.jugador.direccion_mirando.y * TILE)
        bloques = juego.quad_tree.consulta(pygame.rect.Rect(posicion_bloque[0],posicion_bloque[1],TILE,TILE),"muro")
        if bloques:
            bloques[0].kill()
            juego.laberinto.eliminar_bloque_solido((posicion_bloque[0]//TILE,posicion_bloque[1]//TILE))
            self.usos -= 1


class Botiquin(Herramientas):
    def __init__(self, jugador):
        super().__init__(jugador,BOTIQUIN)
        self.usos = 1
    def usar(self, juego):
        if self.jugador.vida < 3:
            self.jugador.vida += 1
            self.usos -= 1

class AturdirMinotauro(Herramientas):
    def __init__(self, jugador):
        super().__init__(jugador,BOMBAATURDIDORA)
        self.usos = 1
    def usar(self, juego):
        pos_minotauro = (juego.minotauro.rect.centerx // TILE,juego.minotauro.rect.centery // TILE)
        posicion_jugador_mirando = (self.jugador.rect.centerx // TILE + self.jugador.direccion_mirando.x ,self.jugador.rect.centery // TILE + self.jugador.direccion_mirando.y)
        posicion_jugador = (self.jugador.rect.centerx // TILE,self.jugador.rect.centery // TILE)
        if pos_minotauro == posicion_jugador or pos_minotauro == posicion_jugador_mirando:
            juego.minotauro.aturdir()
            juego.camara.sacudir_camara(10,2)
            self.usos -= 1
            






class ManenjoHerramientas:
    def __init__(self):
        self.indice = -1 #-1 porque no hay herramientas al principio.
        self.herramientas = []
    def agregar(self,herramienta:Herramientas):
        self.herramientas.append(herramienta)
        # self.indice = len(self.herramientas) - 1
    def usar_herramienta(self,juego,teclas):
        if self.indice == -1 and len(self.herramientas) > 0:
            self.indice = 0
            juego.manejo_ui.actualizar_imagen(self.herramientas[self.indice].id)
            

            
        if len(self.herramientas) > 0:
            if teclas[pygame.K_SPACE]:
                self.herramientas[self.indice].usar(juego)
                if self.herramientas[self.indice].usos <= 0:
                    self.herramientas.pop(self.indice)
                    if len(self.herramientas) == 0:
                        self.indice = -1
                        juego.manejo_ui.actualizar_imagen(self.indice)

                    else:
                        self.indice = len(self.herramientas) - 1
                        juego.manejo_ui.actualizar_imagen(self.herramientas[self.indice].id)
                    

            if teclas[pygame.K_z]:
                self.indice -= 1
                if self.indice < 0:
                    self.indice = len(self.herramientas)-1
                juego.manejo_ui.actualizar_imagen(self.herramientas[self.indice].id)
                

            if teclas[pygame.K_x]:
                self.indice += 1
                if self.indice == len(self.herramientas):
                    self.indice = 0
                juego.manejo_ui.actualizar_imagen(self.herramientas[self.indice].id)
        
        # if len(self.herramientas) == 0:
        #     juego.manejo_ui.item = juego.manejo_ui.actualizar_imagen(-1)
