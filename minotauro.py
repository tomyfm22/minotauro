import pygame
import heapq
from definiciones import TILE, FPS
# Clase del minotauro, se encarga de seguir al jugador y de generar un camino hacia el.
class Minotauro(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.imagen = pygame.image.load("sprites/minotauro.png").convert_alpha()
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 13

        self.delay_generar_camino_max = 0.2
        self.delay_generar_camino = 0
        self.camino = []
        self.muros_cercano = []
        self.aturdido = False
        self.delay_aturdido = 5 # segundos
        self.delay_ataque = 2 # segundos
        self.ataco = False

    def aturdir(self):
        self.aturdido = True
        self.delay_aturdido = 5
    
     

    
    def generar_camino(self,grafo,pos_jugador):
        #bfs
        visitados = set()
        padre = {}
        cola = [(self.rect.x // TILE,self.rect.y // TILE)]

        padre[(self.rect.x // TILE,self.rect.y // TILE)] = None
        visitados.add((self.rect.x // TILE,self.rect.y // TILE))
        while cola:
            actual = cola.pop(0)
            if pos_jugador == actual:
                break

            visitados.add(actual)
            for vecino in grafo[actual]:
                if vecino not in visitados:
                    cola.append(vecino)
                    padre[vecino] = actual
                    visitados.add(vecino)

        return self.armar_camino(padre,pos_jugador)
    
    def armar_camino(self,padre,pos_jugador):
        camino =[]
        actual = pos_jugador
        while actual:
            camino.append(actual)
            if actual in padre:
                actual = padre[actual]
            else:
                actual = None
        camino.reverse()
        camino.pop(0) # descarto la posicion en la que ya estoy.
        return camino

    def seguir_jugador(self,dt,juego):
        tamanio = 50
        jugador = juego.jugador
        # Si me encuentro en el mismo tile que el jugador, los sigo 
        pos_jugador_grilla = (jugador.rect.centerx // TILE,jugador.rect.centery // TILE)
        if pos_jugador_grilla == (self.rect.centerx // TILE,self.rect.centery // TILE):

            direccion = pygame.math.Vector2(jugador.rect.centerx - self.rect.centerx ,jugador.rect.centery - self.rect.centery)
            if direccion.length() > 20:
                direccion = direccion.normalize()

                self.rect.x += self.velocidad * direccion.x * dt * FPS
                rect = pygame.Rect(self.rect.x,self.rect.y,self.rect.width,self.rect.height)
                for i in self.muros_cercano:
                    if "colicion" in i.__dict__:
                        self.rect.x = i.colicion.chequear_colicion_x(rect,direccion)


                self.rect.y += self.velocidad * direccion.y * dt * FPS
                rect = pygame.Rect(self.rect.x,self.rect.y,self.rect.width,self.rect.height)
                for i in self.muros_cercano:
                    if "colicion" in i.__dict__:
                        self.rect.y = i.colicion.chequear_colicion_y(rect,direccion)
                return
            else:
                if not self.ataco:
                    # Si esta cerca del jugador, este recibe danio.
                    juego.camara.sacudir_camara(20,5)
                    jugador.recibir_danio()
                    juego.vida_ui.actualizar_texto(juego.jugador)
                    self.ataco = True

        

        if not self.camino:
            return



        nodo = self.camino[0]
        nodo = (nodo[0] * TILE + TILE // 2, nodo[1] * TILE + TILE // 2)

        direccion = pygame.math.Vector2(nodo[0] - self.rect.centerx, nodo[1] - self.rect.centery)
        distancia_total = direccion.length()

        if distancia_total < TILE // 4:  # Distancia mínima para eliminar el nodo
            self.camino.pop(0)
        else:


            direccion = direccion.normalize()

            self.rect.x += direccion.x * self.velocidad * dt * FPS
            rect = pygame.Rect(self.rect.x,self.rect.y,self.rect.width,self.rect.height)
            for i in self.muros_cercano:
                if "colicion" in i.__dict__:
                    self.rect.x = i.colicion.chequear_colicion_x(rect,direccion)


            self.rect.y += direccion.y * self.velocidad * dt * FPS
            rect = pygame.Rect(self.rect.x,self.rect.y,self.rect.width,self.rect.height)
            for i in self.muros_cercano:
                if "colicion" in i.__dict__:
                    self.rect.y = i.colicion.chequear_colicion_y(rect,direccion)

            

    def update(self,dt,juego):
        if self.aturdido:
            self.delay_aturdido -= dt
            if self.delay_aturdido < 0:
                self.aturdido = False
            return

        if self.ataco:
            self.delay_ataque -= dt
            if self.delay_ataque <= 0:
                self.ataco = False
                self.delay_ataque = 2

        
        self.delay_generar_camino -= dt
        if self.delay_generar_camino < 0:
            self.camino = self.generar_camino(juego.laberinto.grafo,juego.obtener_posicion_jugador_grilla())
            self.delay_generar_camino = self.delay_generar_camino_max
        self.muros_cercano = []
        self.muros_cercano = juego.quad_tree.consulta(pygame.Rect(self.rect.x - TILE * 2,self.rect.y - TILE * 2,self.rect.width + TILE * 4,self.rect.height + TILE * 4))
        
        
        self.seguir_jugador(dt,juego)




    def draw(self,superficie,offset):
        superficie.blit(self.imagen,(self.rect.x - offset[0],self.rect.y - offset[1]))

