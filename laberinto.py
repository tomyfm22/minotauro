import pygame,random,time
import definiciones



class Celda:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vecinos = set()
        self.esquinas = [((self.x,self.y),(self.x + 1,self.y)), # Arriba
                         ((self.x,self.y),(self.x, self.y + 1)), # Izquierda
                         ((self.x + 1,self.y),(self.x + 1,self.y + 1)), # Derecha
                         ((self.x,self.y + 1),(self.x + 1 ,self.y + 1))] # Abajo
        self.muros  = [True,True,True,True]   
        self.visitada = False
        self.es_muro = True
    
    def abrir_camino(self,dx,dy):
        if dx == 1:
            self.muros[2] = False
        elif dx == -1:
            self.muros[1] = False
        elif dy == -1:
            self.muros[0] = False
        elif dy == 1:
            self.muros[3] = False
            
    
    
    def draw(self,superficie:pygame.Surface):
        # color = "white" if not self.es_muro else "blue"
        # if self.visitada:
            # return
        tamanio_tile = definiciones.TILE
        pygame.draw.rect(superficie,"green",(self.x * definiciones.TILE,self.y * definiciones.TILE,definiciones.TILE,definiciones.TILE))
        
        for i,j in enumerate(self.esquinas):
            if self.muros[i]:
                pygame.draw.line(superficie,"blue",(j[0][0] * tamanio_tile,j[0][1] * tamanio_tile),(j[1][0] * tamanio_tile,j[1][1] * tamanio_tile))

    def hay_muro(self,dx,dy):
        if dx == 2:
            return self.muros[2]
        elif dx == -2:
            return self.muros[1]
        elif dy == 2:
            return self.muros[3]
        elif dy == -2:
            return self.muros[0]



class Muro(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        

    def draw(self,superficie):
        pygame.draw.rect(superficie,"green",(self.x * definiciones.TILE,self.y * definiciones.TILE,definiciones.TILE,definiciones.TILE))

class Laberinto: 
    def __init__(self):
        self.laberinto = {} # (x,y) : Celda
        self.tamanio_mapa = 31
        self.muros = {}
        self.punto_aparicion = (1,1)

        for i in range(self.tamanio_mapa):
            for j in range(self.tamanio_mapa):
                self.laberinto[(i,j)] = Celda(i,j)
                self.muros[(i,j)] = Muro(i,j)
        # self.generar_laberinto()    
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

    def generar_laberinto(self):
        # empieza en el centro.
        actual = (self.tamanio_mapa // 2 ,self.tamanio_mapa // 2)
        direcciones = [(1,0),(-1,0),(0,-1),(0,1)]
        while actual:
            celda = self.laberinto[actual]
            celda.visitada = True
            
            vecinos = []
            for dx,dy in direcciones:
                pos_vecina = (actual[0] + dx,actual[1] + dy)
                if pos_vecina in self.laberinto and not self.laberinto[(pos_vecina[0],pos_vecina[1])].visitada:
                    vecinos.append(pos_vecina)
            
            if vecinos:
                nueva_pos = random.choice(vecinos)
                dire = (nueva_pos[0] - actual[0],nueva_pos[1] - actual[1])
                self.crear_camino_entre_celdas(celda, self.laberinto[nueva_pos],dire[0],dire[1])
                actual = nueva_pos
            else:

                actual = None
                for pos in self.laberinto.keys():                
                    celda = self.laberinto[pos]
                    if celda.visitada:
                        continue

                    vecinos = []
                    for dx,dy in direcciones:
                        pos_vecina = (pos[0] + dx,pos[1] + dy)
                        if pos_vecina in self.laberinto and self.laberinto[(pos_vecina[0],pos_vecina[1])].visitada:
                            vecinos.append(pos_vecina)
                    if vecinos:
                        nueva_pos = random.choice(vecinos)
                        dire = (nueva_pos[0] - pos[0],nueva_pos[1] - pos[1])
                        self.crear_camino_entre_celdas(self.laberinto[pos], self.laberinto[nueva_pos],dire[0],dire[1])
                        actual = nueva_pos
                        break        
            

    def generar_laberinto_visual(self,superficie):
        # empieza en el centro.
        actual = (self.tamanio_mapa // 2 ,self.tamanio_mapa // 2)
        dist = 2
        direcciones = [(dist,0),(-dist,0),(0,-dist),(0,dist)]

              
        superficie.fill((0,0,0,0))
        self.draw(superficie)
        if actual:
            pygame.draw.rect(superficie,"blue",(actual[0] * definiciones.TILE,actual[1] * definiciones.TILE,definiciones.TILE,definiciones.TILE))
        time.sleep(2)
        pygame.display.flip()
        while actual:
            celda = self.laberinto[actual]
            celda.visitada = True
            celda.es_muro   = False
            
            vecinos = []
            for dx,dy in direcciones:
                pos_vecina = (actual[0] + dx,actual[1] + dy)
                if pos_vecina in self.laberinto and not self.laberinto[(pos_vecina[0],pos_vecina[1])].visitada:
                    vecinos.append(pos_vecina)
            
            if vecinos:
                nueva_pos = random.choice(vecinos)
                dire = ((nueva_pos[0] - actual[0]) // dist,(nueva_pos[1] - actual[1])//dist)
                
                # Tile intermedio
                intermedio = (actual[0] + dire[0], actual[1] + dire[1])

                if intermedio in self.laberinto:
                    self.laberinto[intermedio].visitada = True
                    self.laberinto[intermedio].es_muro = False
                    self.crear_camino_entre_celdas(self.laberinto[actual], self.laberinto[intermedio], dire[0], dire[1])
                    self.crear_camino_entre_celdas(self.laberinto[intermedio], self.laberinto[nueva_pos], dire[0] , dire[1])
                else:
                    self.crear_camino_entre_celdas(self.laberinto[actual], self.laberinto[nueva_pos], dire[0], dire[1])

                actual = nueva_pos
            else:

                actual = None
                for pos in self.laberinto.keys():                
                    celda = self.laberinto[pos]
                    if celda.visitada or  celda.es_muro:
                        continue

                    vecinos = []
                    for dx,dy in direcciones:
                        pos_vecina = (pos[0] + dx,pos[1] + dy)
                        if pos_vecina in self.laberinto and self.laberinto[(pos_vecina[0],pos_vecina[1])].visitada:
                            vecinos.append(pos_vecina)
                    if vecinos:
                        nueva_pos = random.choice(vecinos)
                        dire = ((nueva_pos[0] - pos[0]) // dist,(nueva_pos[1] - pos[1])//dist)
                                
                        # Tile intermedio
                        intermedio = (pos[0] + dire[0], pos[1] + dire[1])

                        if intermedio in self.laberinto:
                            self.laberinto[intermedio].visitada = True
                            self.laberinto[intermedio].es_muro = False
                            self.crear_camino_entre_celdas(self.laberinto[pos], self.laberinto[intermedio], dire[0], dire[1])
                            self.crear_camino_entre_celdas(self.laberinto[intermedio], self.laberinto[nueva_pos], dire[0] , dire[1])
                        else:
                            self.crear_camino_entre_celdas(self.laberinto[pos], self.laberinto[nueva_pos], dire[0], dire[1])


                        actual = nueva_pos
                        break        
            
            superficie.fill((0,0,0,0))
            self.draw(superficie)
            if actual:
                pygame.draw.rect(superficie,"blue",(actual[0] * definiciones.TILE,actual[1] * definiciones.TILE,definiciones.TILE,definiciones.TILE))
            time.sleep(0.1)
            pygame.display.flip()


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

    def draw(self,superficie:pygame.Surface):
        # for celda in self.laberinto.values():
            # celda.draw(superficie)
        for m in self.muros.values():
            m.draw(superficie)
        pygame.draw.rect(superficie,"red",(self.tamanio_mapa//2 * definiciones.TILE,self.tamanio_mapa//2 * definiciones.TILE,definiciones.TILE,definiciones.TILE))