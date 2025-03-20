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
        tamanio_tile = definiciones.TILE
        pygame.draw.rect(superficie,"white",(self.x * definiciones.TILE,self.y * definiciones.TILE,definiciones.TILE,definiciones.TILE))
        
        for i,j in enumerate(self.esquinas):
            if self.muros[i]:
                pygame.draw.line(superficie,"blue",(j[0][0] * tamanio_tile,j[0][1] * tamanio_tile),(j[1][0] * tamanio_tile,j[1][1] * tamanio_tile))






class Laberinto: 
    def __init__(self):
        self.laberinto = {} # (x,y) : Celda
        self.tamanio_mapa = 10
        self.muros = []

        for i in range(self.tamanio_mapa):
            for j in range(self.tamanio_mapa):
                self.laberinto[(i,j)] = Celda(i,j)

        self.generar_laberinto()    

    def crear_camino_entre_celdas(self,celda1:Celda,celda2:Celda,dx:int,dy:int):
        celda1.abrir_camino(dx,dy)
        celda2.abrir_camino(-dx,-dy)

        celda1.vecinos.add((celda2.x,celda2.y))
        celda2.vecinos.add((celda1.x,celda1.y))


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


    def draw(self,superficie:pygame.Surface):
        for celda in self.laberinto.values():
            celda.draw(superficie)
        
        pygame.draw.rect(superficie,"red",(self.tamanio_mapa//2 * definiciones.TILE,self.tamanio_mapa//2 * definiciones.TILE,definiciones.TILE,definiciones.TILE))