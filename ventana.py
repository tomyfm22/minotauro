import pygame
from definiciones import *
from jugador import Jugador
from laberinto import Laberinto
from camara import Camara
from minotauro import Minotauro
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
        
        self.laberinto = Laberinto()
        self.jugador = Jugador(self.laberinto.punto_aparicion[0] * TILE,self.laberinto.punto_aparicion[0] * TILE)
        self.minotauro = Minotauro(self.laberinto.punto_aparicion[0] * TILE,self.laberinto.punto_aparicion[0] * TILE)
        self.camara = Camara(0,0,self.jugador)
        self.elementos_en_pantalla = []
        self.grafo = self.laberinto.generar_grafo()
        self.s = "llll"
    
    def obtener_elementos_pantalla(self,offset):
        # Obtengo los tiles que se encuentran mostrando en la patalla.
        self.elementos_en_pantalla = []
        for i in range(offset[0] //TILE,(offset[0] + ANCHO) // TILE + 1):
            for j in range(offset[1] // TILE,(offset[1] + ALTO) // TILE + 1):
                for elemento in self.laberinto.elementos_del_laberinto:
                    if (i,j) in self.laberinto.elementos_del_laberinto[elemento]:
                        self.elementos_en_pantalla.append(self.laberinto.elementos_del_laberinto[elemento][(i,j)])
                        
    def obtener_posicion_jugador_grilla(self):
        return (self.jugador.rect.x // TILE,self.jugador.rect.y // TILE)

        # print(len(self.elementos_en_pantalla))
    def update(self, dt):
        eventos = pygame.event.get()

        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        for tipo in self.laberinto.elementos_del_laberinto:
            if tipo == "muro":
                continue

            for elemento in self.laberinto.elementos_del_laberinto[tipo].copy().values():
                elemento.update(dt,self)

        self.jugador.manejo_entrada(eventos)
        self.jugador.update(dt,self)
        self.minotauro.update(dt,self)
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

        self.obtener_elementos_pantalla(offset)

        for i in self.elementos_en_pantalla:
            i.draw(superficie,offset)
        
        # self.laberinto.rb_visual(superficie)
        self.minotauro.draw(superficie,offset)
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