import pygame,random
import definiciones



class Celda:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vecinos = set()
        self.esquinas = [((self.x,self.y),(self.x + 1,self.y)),
                         ((self.x,self.y),(self.x, self.y + 1)),
                         ((self.x + 1,self.y),(self.x + 1,self.y + 1)),
                         ((self.x,self.y + 1),(self.x + 1 ,self.y + 1))]
        self.muros  = [True,True,True,True]   
        self.visitada = False
    
    
    def abrir_camino(self,dx,dy):
        if (dx == 1 and dy == 0):
            self.muros[2] = False
        elif (dx == 0 and dy == 1):
            self.muros[3]= False
        elif (dx == 0 and dy == -1):
            self.muros[0] = False
        else:
            self.muros[1] = False
    
    
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

        for i in range(self.tamanio_mapa):
            for j in range(self.tamanio_mapa):
                self.laberinto[(i,j)] = Celda(i,j)

        self.generar_laberinto()    

    def generar_laberinto(self):
        # empieza en una posicion random
        actual = (random.randint(0,self.tamanio_mapa-1),random.randint(0,self.tamanio_mapa-1))
        direcciones = [(1,0),(-1,0),(0,-1),(0,1)]
        while actual:
            
            vecinos = []
            for dx,dy in direcciones:
                pos_vecina = (actual[0] + dx,actual[1] + dy)
                vecinos.append(pos_vecina)
            
            random.shuffle(vecinos)
            sin_vecinos = True
            for pos_vecina in vecinos:
                if pos_vecina in self.laberinto and not (pos_vecina in self.laberinto[(actual[0],actual[1])].vecinos):
                    celda = self.laberinto[(actual[0],actual[1])]
                    celda.abrir_camino((pos_vecina[0] - actual[0]),(pos_vecina[1] - actual[1]))
                    celda.vecinos.add(pos_vecina)
                    celda.visitada = True
                    self.laberinto[(pos_vecina[0],pos_vecina[1])].vecinos.add(actual)
                    actual = pos_vecina
                    sin_vecinos = False
                    break

            if sin_vecinos:
                actual = (0,0)
                encontro = False
                for i in range(self.tamanio_mapa):
                    if encontro:
                        break
                    for j in range(self.tamanio_mapa):
                        
                        celda = self.laberinto[(i,j)]
                        if celda.visitada:
                            continue

                        vecinos = []
                        for dx,dy in direcciones:
                            pos_vecina = (i + dx,j + dy)
                            if pos_vecina in self.laberinto and self.laberinto[(pos_vecina[0],pos_vecina[1])].visitada:
                                vecinos.append(pos_vecina)
                        if vecinos:
                            actual = random.choice(vecinos)
                            encontro = True
                            break
                        # actual = (i,j)
                
                if actual[0] == 0 and actual[1] == 0:
                    actual = None






    
    def draw(self,superficie:pygame.Surface):
        for celda in self.laberinto.values():
            celda.draw(superficie)