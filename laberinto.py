import pygame,random,time
import definiciones



class Muro(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x # coordenadas en grilla.
        self.y = y # coordenadas en grilla.
        self.rect = pygame.Rect(x * definiciones.TILE,y *definiciones.TILE,definiciones.TILE,definiciones.TILE) # coordenadas en el mundo.

    def draw(self,superficie,offset:tuple[int,int]):
        pygame.draw.rect(superficie,"green",((self.rect.x) - offset[0],(self.rect.y) - offset[1],definiciones.TILE,definiciones.TILE))

class Laberinto: 
    def __init__(self):
        self.tamanio_mapa = 101
        self.muros = {} # pos:Muro
        self.punto_aparicion = (1,1)

        for i in range(self.tamanio_mapa):
            for j in range(self.tamanio_mapa):
                self.muros[(i,j)] = Muro(i,j)
        self.rb()

        self.borrar_paredes()

    def borrar_paredes(self):
        direcciones = [(1,0),(-1,0),(0,-1),(0,1)]
        for i in range(int(self.tamanio_mapa * self.tamanio_mapa * 0.1)):
            pos = (random.randint(2,(self.tamanio_mapa//2)-2) * 2,random.randint(2,(self.tamanio_mapa//2)-2) * 2)
            dire = random.choice(direcciones)
            # Tile intermedio
            intermedio = (pos[0] + dire[0], pos[1] + dire[1])

            if intermedio in self.muros:
                self.muros.pop(intermedio)
        
        #borro las 4 paredes del centro.
        centro = (self.tamanio_mapa // 2 ,self.tamanio_mapa // 2)
        for i in direcciones:
            posible_muro = (centro[0] + i[0],centro[1] + i[1])
            if posible_muro in self.muros:
                self.muros.pop(posible_muro)


    def rb(self):
        dist = 2
        direcciones = [(dist,0),(-dist,0),(0,-dist),(0,dist)]

        no_visitados = set()
        for i in range(self.punto_aparicion[0],self.tamanio_mapa -1,2):
            for j in range(self.punto_aparicion[1],self.tamanio_mapa -1,2):
                no_visitados.add((i,j))

        actual = self.punto_aparicion
        pila    = []
        while no_visitados:
            nodo = actual
            self.muros.pop(nodo,None)
            no_visitados.discard(nodo)

            nodos_vecinos = [(actual[0] + dx,actual[1] + dy) for dx,dy in direcciones 
                             if (actual[0] + dx,actual[1] + dy) in self.muros and \
                                (actual[0] + dx,actual[1] + dy) in no_visitados]
            
            
            if nodos_vecinos:
                nuevo = random.choice(nodos_vecinos)
                dire = ((nuevo[0] - actual[0]) // dist,(nuevo[1] - actual[1])//dist)

                # Tile intermedio
                intermedio = (actual[0] + dire[0], actual[1] + dire[1])
                self.muros.pop(intermedio,None)
                pila.append(actual)
                actual = nuevo
            else:
                if pila:
                    actual = pila.pop()

    

    def rb_visual(self,superficie):
        superficie.fill((0,0,0,0))
        self.draw(superficie)


        actual = (1,1)
        if actual:
            pygame.draw.rect(superficie,"blue",(actual[0] * definiciones.TILE,actual[1] * definiciones.TILE,definiciones.TILE,definiciones.TILE))
        dist = 2
        direcciones = [(dist,0),(-dist,0),(0,-dist),(0,dist)]

        no_visitados = set()
        for i in range(1,self.tamanio_mapa-1,2):
            for j in range(1,self.tamanio_mapa-1,2):
                no_visitados.add((i,j))

        pila    = []
        while no_visitados:
            nodo = actual
            self.muros.pop(nodo,None)
            no_visitados.discard(nodo)

            nodos_vecinos = [(actual[0] + dx,actual[1] + dy) for dx,dy in direcciones 
                             if (actual[0] + dx,actual[1] + dy) in self.muros and \
                                (actual[0] + dx,actual[1] + dy) in no_visitados]
            
            
            if nodos_vecinos:
                nuevo = random.choice(nodos_vecinos)
                dire = ((nuevo[0] - actual[0]) // dist,(nuevo[1] - actual[1])//dist)

                # Tile intermedio
                intermedio = (actual[0] + dire[0], actual[1] + dire[1])
                self.muros.pop(intermedio,None)
                pila.append(actual)
                actual = nuevo
            else:
                if pila:
                    actual = pila.pop()


            superficie.fill((0,0,0,0))
            self.draw(superficie)

            if actual:
                pygame.draw.rect(superficie,"blue",(actual[0] * definiciones.TILE,actual[1] * definiciones.TILE,definiciones.TILE,definiciones.TILE))
            time.sleep(0.1)
            pygame.display.flip()



    def generar_grafo(self):
        grafo = {}
        direcciones = [(1,0),(-1,0),(0,1),(0,-1)]
        for i in range(1,self.tamanio_mapa -1):
            for j in range(1,self.tamanio_mapa -1):
                if (i,j) not in self.muros:
                    grafo[(i,j)] = []
                    for dx,dy in direcciones:
                        if (i+dx,j+dy) not in self.muros:
                            grafo[(i,j)].append((i+dx,j+dy))
        
        return grafo

    def draw(self,superficie:pygame.Surface,offset :tuple[int,int]):
        for m in self.muros.values():
            m.draw(superficie,offset)
        pygame.draw.rect(superficie,"red",((self.tamanio_mapa//2 * definiciones.TILE) - offset[0],(self.tamanio_mapa//2 * definiciones.TILE )- offset[1],definiciones.TILE,definiciones.TILE))