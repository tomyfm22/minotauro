import pygame
from definiciones import *
from jugador import Jugador
from laberinto import Laberinto
from camara import Camara
from minotauro import Minotauro
from quad_tree import Quadtree


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
        
        self.laberinto  = Laberinto()
        self.quad_tree  = Quadtree(0,pygame.Rect(0,0,self.laberinto.tamanio_nivel[0],self.laberinto.tamanio_nivel[1]))
        self.jugador    = Jugador(self.laberinto.punto_aparicion[0] * TILE,self.laberinto.punto_aparicion[0] * TILE)
        # self.minotauro  = Minotauro(self.laberinto.punto_aparicion[0] * TILE,self.laberinto.punto_aparicion[0] * TILE)
        self.camara     = Camara(0,0,self.jugador)
        self.elementos_en_pantalla = []
        self.grafo      = self.laberinto.generar_grafo()

        for tipo in self.laberinto.objetos:
            for elemento in self.laberinto.objetos[tipo]:
                self.quad_tree.insertar(elemento,tipo)

        self.cantidad_llaves = len(self.laberinto.objetos["llaves"])



        

    def obtener_elementos_pantalla(self):
        offset = self.camara.obtener_offset()
        self.elementos_en_pantalla = []

        # Obtengo los tiles que se encuentran mostrando en la patalla.
        self.elementos_en_pantalla =  self.quad_tree.consulta(pygame.Rect(offset[0]-TILE,offset[1]-TILE,ANCHO + 2 * TILE,ALTO + 2 * TILE))
                        
    def obtener_posicion_jugador_grilla(self):
        return (self.jugador.rect.x // TILE,self.jugador.rect.y // TILE)

        # print(len(self.elementos_en_pantalla))
    def update(self, dt):
        eventos = pygame.event.get()

        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        self.obtener_elementos_pantalla()
        
        for i in self.elementos_en_pantalla:
            i[0].update(dt,self)


        self.jugador.manejo_entrada(eventos)
        self.jugador.update(dt,self)
        # self.minotauro.update(dt,self)
        self.camara.update(dt)


    
    def generar_mascara_vision(self,superficie, offset, radio):
        # Crear una superficie negra con transparencia
        mascara = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)
        mascara.fill((0, 0, 0, 150))  # Negro semi-transparente

        # Obtener la posición del jugador en la pantalla
        centro_x, centro_y = self.jugador.rect.center

        # Dibujar un círculo transparente en la máscara
        pygame.draw.circle(mascara, (0, 0, 0, 0), (centro_x -offset[0], centro_y-offset[1]), radio)

        return mascara

    def draw(self,superficie):
        offset = self.camara.obtener_offset()


        for i in self.elementos_en_pantalla:
            i[0].draw(superficie,offset)
        
        # self.laberinto.rb_visual(superficie)
        # self.minotauro.draw(superficie,offset)
        self.jugador.draw(superficie,offset)
        
        # Generar la máscara de visión
        mascara = self.generar_mascara_vision(superficie, offset, radio=150)
        superficie.blit(mascara, (0, 0))  # Superponer la máscara

        # for i in self.grafo:
            # pygame.draw.circle(superficie,"yellow",(i[0] * TILE + TILE//2 - offset[0],i[1] * TILE + TILE // 2 - offset[1]),5)
            # for j in self.grafo[i]:
                # pygame.draw.line(superficie,"blue",(i[0] * TILE + TILE // 2 - offset[0],i[1] * TILE + TILE // 2 - offset[1]),(j[0] * TILE + TILE // 2 - offset[0],j[1] * TILE + TILE // 2 - offset[1]))
        centro = (self.laberinto.tamanio_mapa // 2 * TILE,self.laberinto.tamanio_mapa // 2 * TILE)
        pygame.draw.rect(superficie,"blue",(centro[0] - offset[0],centro[1] - offset[1],TILE,TILE))

        # self.quad_tree.draw(superficie,offset)