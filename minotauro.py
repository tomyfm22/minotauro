import pygame
import heapq
from definiciones import TILE
class Minotauro(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.imagen = pygame.Surface((50,50))
        self.imagen.fill("brown")
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 9

        self.delay_generar_camino_max = 0.5
        self.delay_generar_camino = 0
        self.camino = []
        self.muros_cercano = []
    
    def obtener_muros_cercanos(self,laberinto):
        
        self.muros_cercano = []
        pos = (self.rect.x//TILE,self.rect.y//TILE)
        direcciones = [(1,0),(-1,0),(1,1),(-1,1),(-1,-1),(0,1),(0,-1),(1,-1)]
        
        
        for direccion in direcciones:
            muro_vecino = (pos[0] + direccion[0],pos[1] + direccion[1])
            if muro_vecino in laberinto.muros:
                self.muros_cercano.append(laberinto.muros[muro_vecino])
         

    
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
            actual = padre[actual]
        camino.reverse()
        camino.pop(0) # descarto la posicion en la que ya estoy.
        return camino

    def seguir_jugador(self):
        if not self.camino:
            return

        nodo = self.camino[0]
        nodo = (nodo[0] * TILE + TILE // 2, nodo[1] * TILE + TILE // 2)

        direccion = pygame.math.Vector2(nodo[0] - self.rect.centerx, nodo[1] - self.rect.centery)
        distancia_total = direccion.length()

        if distancia_total < TILE // 2:  # Distancia mínima para eliminar el nodo
            self.camino.pop(0)
        else:


            direccion = direccion.normalize()

            tamanio = 50
            self.rect.x += direccion.x * self.velocidad
            rect = pygame.Rect(self.rect.x,self.rect.y,tamanio,tamanio)
            for i in self.muros_cercano:
                if rect.colliderect(i.rect):
                    if direccion.x > 0:
                        rect.right = i.rect.left
                    if direccion.x < 0:
                        rect.left = i.rect.right
                    
                    self.rect.x = rect.x



            self.rect.y += direccion.y * self.velocidad
            rect = pygame.Rect(self.rect.x,self.rect.y,tamanio,tamanio)
            for i in self.muros_cercano:
                if rect.colliderect(i.rect):
                    if direccion.y > 0:
                        rect.bottom = i.rect.top
                    if direccion.y < 0:
                        rect.top = i.rect.bottom
                    
                    self.rect.y = rect.y
            

    def update(self,dt,juego):
        self.delay_generar_camino -= dt
        if self.delay_generar_camino < 0:
            self.camino = self.generar_camino(juego.grafo,juego.obtener_posicion_jugador_grilla())
            self.delay_generar_camino = self.delay_generar_camino_max
        self.obtener_muros_cercanos(juego.laberinto)
        self.seguir_jugador()


    def draw(self,superficie,offset):
        superficie.blit(self.imagen,(self.rect.x - offset[0],self.rect.y - offset[1]))

