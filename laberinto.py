import pygame,random,time
from definiciones import *
from bloque import *

class Laberinto:

    def __init__(self):
        self.tamanio_mapa = 101
        self.punto_aparicion = (1,1)

        # Guarda las posciones (en coordenadas de grilla) para despues formar el grafo.
        self.bloques_solidos = {
            "colicionables" : {}, # muros, puertas, etc
            "items" : {}, # llaves,etc.
        }
        # Guarda las intancias de los objetos para despues agregarlo al quad-tree.
        self.objetos = {
            "muro" : pygame.sprite.Group(),
            "suelo" : pygame.sprite.Group(),
            "llaves" : pygame.sprite.Group(),
            "puerta" : pygame.sprite.Group(),
            "salida" : pygame.sprite.Group(),
            "limite": pygame.sprite.Group(),
            "items": pygame.sprite.Group(),
        }
        self.id_sprite = {
            1:0, # muro
            2:1, # piso
            3:2, # pared izquierda
            4:3, # pared derecha
                          } # id : pos_sprite
        
        self.mapeo_sprites = {} # pos:id

        self.sprite_sheet = pygame.image.load("sprites/tiles.png").convert_alpha()

        # Inicializo todo el laberinto agregando la posicion de los muros
        for i in range(self.tamanio_mapa):
            for j in range(self.tamanio_mapa):                
                self.mapeo_sprites[(i,j)] = 1
                if i == 0 or i == self.tamanio_mapa-1 or j == 0 or j == self.tamanio_mapa-1:
                    if i == 0 or i == self.tamanio_mapa-1:
                        self.mapeo_sprites[(i,j)] = 3
                    self.bloques_solidos["colicionables"][(i,j)] = LIMITE
                    continue


                self.bloques_solidos["colicionables"][(i,j)] = MURO
                


        self.tamanio_nivel = (self.tamanio_mapa * TILE,self.tamanio_mapa * TILE)
        
        self.generar_laberinto()
        
        self.borrar_paredes()

        self.posicionar_objetos()

        self.instanciar_objetos()


        self.grafo = self.generar_grafo()
        s = pygame.sprite.Group()
        

    def eliminar_bloque_solido(self,pos_en_grilla):
        if pos_en_grilla in self.bloques_solidos["colicionables"]:
            self.bloques_solidos["colicionables"].pop(pos_en_grilla)
            self.actualizar_grafo(pos_en_grilla,"agregar")
    
    def obtener_sprite_sheet(self,Id):
  
        imagen = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
        imagen.blit(self.sprite_sheet, (0, 0), pygame.Rect(TILE * self.id_sprite[Id],0,TILE,TILE))
        return imagen


    def borrar_paredes(self):
        direcciones = [(1,0),(-1,0),(0,-1),(0,1)]
        for i in range(int(self.tamanio_mapa * self.tamanio_mapa * 0.1)):
            pos = (random.randint(2,(self.tamanio_mapa//2)-2) * 2,random.randint(2,(self.tamanio_mapa//2)-2) * 2)
            dire = random.choice(direcciones)
            # Tile intermedio
            intermedio = (pos[0] + dire[0], pos[1] + dire[1])

            if intermedio in self.bloques_solidos["colicionables"]:
                # self.bloques_solidos.discard(intermedio)
                self.bloques_solidos["colicionables"].pop(intermedio)
                self.mapeo_sprites[intermedio] = 2
            
            
        
        centro = (self.tamanio_mapa // 2 ,self.tamanio_mapa // 2)
        # Si el centro tiene pared, se la quito.
        if centro in self.bloques_solidos["colicionables"]:
            # self.bloques_solidos.discard(centro)
            self.bloques_solidos["colicionables"].pop(centro)
            self.mapeo_sprites[intermedio] = 2
        
        # Quito los muros para que al agregar la puerta, se cambien los muros por limites.
        for dx,dy in direcciones:
            pos = (centro[0] + dx,centro[1] + dy)
            if pos in self.bloques_solidos["colicionables"]:
                # self.bloques_solidos.discard(pos)
                self.bloques_solidos["colicionables"].pop(pos)
                self.mapeo_sprites[intermedio] = 2




    def generar_laberinto(self):
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
            # self.bloques_solidos.discard(nodo)
            self.bloques_solidos["colicionables"].pop(nodo,None)
            no_visitados.discard(nodo)

            nodos_vecinos = [(actual[0] + dx,actual[1] + dy) for dx,dy in direcciones 
                             if (actual[0] + dx,actual[1] + dy) in self.bloques_solidos["colicionables"]  and \
                                (actual[0] + dx,actual[1] + dy) in no_visitados]
            


            
            if nodos_vecinos:
                nuevo = random.choice(nodos_vecinos)
                dire = ((nuevo[0] - actual[0]) // dist,(nuevo[1] - actual[1])//dist)

                # Tile intermedio
                intermedio = (actual[0] + dire[0], actual[1] + dire[1])
                # self.bloques_solidos.discard(intermedio)
                self.bloques_solidos["colicionables"].pop(intermedio,None)
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
            pygame.draw.rect(superficie,"blue",(actual[0] * TILE,actual[1] * TILE,TILE,TILE))
        dist = 2
        direcciones = [(dist,0),(-dist,0),(0,-dist),(0,dist)]

        no_visitados = set()
        for i in range(1,self.tamanio_mapa-1,2):
            for j in range(1,self.tamanio_mapa-1,2):
                no_visitados.add((i,j))

        pila    = []
        while no_visitados:
            nodo = actual
            self.bloques_solidos.pop(nodo,None)
            no_visitados.discard(nodo)

            nodos_vecinos = [(actual[0] + dx,actual[1] + dy) for dx,dy in direcciones 
                             if (actual[0] + dx,actual[1] + dy) in self.bloques_solidos  and \
                                (actual[0] + dx,actual[1] + dy) in no_visitados]
            
            
            if nodos_vecinos:
                nuevo = random.choice(nodos_vecinos)
                dire = ((nuevo[0] - actual[0]) // dist,(nuevo[1] - actual[1])//dist)

                # Tile intermedio
                intermedio = (actual[0] + dire[0], actual[1] + dire[1])
                self.bloques_solidos.pop(intermedio,None)
                pila.append(actual)
                actual = nuevo
            else:
                if pila:
                    actual = pila.pop()


            superficie.fill((0,0,0,0))
            self.draw(superficie)

            if actual:
                pygame.draw.rect(superficie,"blue",(actual[0] * TILE,actual[1] * TILE,TILE,TILE))
            time.sleep(0.1)
            pygame.display.flip()



    def generar_grafo(self):
        grafo = {}
        direcciones = [(1,0),(-1,0),(0,1),(0,-1)]
        for i in range(1,self.tamanio_mapa -1):
            for j in range(1,self.tamanio_mapa -1):
                if (i,j) not in self.bloques_solidos["colicionables"].keys():
                    grafo[(i,j)] = []
                    for dx,dy in direcciones:
                        if (i+dx,j+dy) not in self.bloques_solidos["colicionables"].keys() :
                            grafo[(i,j)].append((i+dx,j+dy))
        
        return grafo

    def actualizar_grafo(self,posicion,accion = "quitar"):
        if accion == "quitar":
            adyacentes = self.grafo[posicion]
            for adyacente in adyacentes:
                self.grafo[adyacente].remove(posicion)
            self.grafo.pop(posicion,None)
        
        elif accion == "agregar":
            self.grafo[posicion] = []

            direcciones = [(1,0),(-1,0),(0,1),(0,-1)]
            for dx,dy in direcciones:
                adyacente = (posicion[0] + dx,posicion[1] + dy)
                if adyacente not in self.bloques_solidos["colicionables"]:
                    self.grafo[posicion].append(adyacente)
                    self.grafo[adyacente].append(posicion)
    
    
    def posicionar_objetos(self):

        # Instancio la puerta bloqueando el centro.
        centro = (self.tamanio_mapa // 2,self.tamanio_mapa // 2)
        direcciones = [(1,0),(-1,0),(0,1),(0,-1)]
        agrego_puerta = False
        # Encierro el centro con muro dejando la puerta como unico camino posible.
        for dx,dy in direcciones:
            pos_vecina = (centro[0] + dx,centro[1] + dy)
            
            if not agrego_puerta:
                if not pos_vecina in self.bloques_solidos["colicionables"]:
                    agrego_puerta = True
                    self.bloques_solidos["colicionables"][pos_vecina] = PUERTA
                    # Me aseguro que no halla muros al rededor de la puerta.
                    for dx,dy in direcciones:
                        pos = (pos_vecina[0] + dx,pos_vecina[1] + dy)
                        if pos in self.bloques_solidos["colicionables"]:
                            self.bloques_solidos["colicionables"].pop(pos)

            else:
                if not pos_vecina in self.bloques_solidos["colicionables"]:
                    self.bloques_solidos["colicionables"][pos_vecina] = LIMITE


   


        self.bloques_solidos["items"][centro] = SALIDA
        posiciones_libres = [(i,j) for j in range(self.tamanio_mapa) for i in range(self.tamanio_mapa) if (i,j) not in self.bloques_solidos["colicionables"]]
        random.shuffle(posiciones_libres)
        proporcion = 0.05  # 5% del total de celdas tendrán ítems
        cantidad_items = max(3, int(len(posiciones_libres) * proporcion))  # Mínimo 3 ítems

        tipos = [MARTILLO, BRUJULA, BOTIQUIN]
        distribucion = {MARTILLO: 0.5, BRUJULA: 0.3, BOTIQUIN: 0.2}

        for _ in range(cantidad_items):
            tipo = random.choices(tipos, weights=distribucion.values())[0]
            pos = posiciones_libres.pop(0)
            self.bloques_solidos["items"][pos] = tipo




        # Aplico el sprite correspondiente a cada muro.
        for i in range(self.tamanio_mapa):
            for j in range(self.tamanio_mapa):
                pos = (i,j)


                if pos not in self.bloques_solidos["colicionables"]:
                    self.mapeo_sprites[pos] = 2
                    if pos not in self.bloques_solidos["items"]:
                        self.bloques_solidos["items"][pos] = SUELO
                    for dx,dy in direcciones:
                        pos_vecina = (pos[0] + dx,pos[1] + dy)
                        if pos_vecina in self.bloques_solidos["colicionables"]:
                            if dx != 0:
                                self.mapeo_sprites[pos_vecina] = 3
                            if dy != 0:
                                self.mapeo_sprites[pos_vecina] = 1
                            




    def instanciar_objetos(self):
        for tipo in self.bloques_solidos:
            for posicion,Id in self.bloques_solidos[tipo].items():
                if Id == LIMITE:
                    self.objetos["limite"].add(Muro(posicion[0],posicion[1],self.obtener_sprite_sheet(self.mapeo_sprites[posicion])))
                elif Id == MURO:
                    self.objetos["muro"].add(Muro(posicion[0],posicion[1],self.obtener_sprite_sheet(self.mapeo_sprites[posicion])))
                elif Id == PUERTA:
                    puerta = Puerta(posicion[0],posicion[1])
                    # Intancio las llaves en distintos puntos del mapa.
                    posiciones_libres = [(i,j) for j in range(self.tamanio_mapa) for i in range(self.tamanio_mapa) if (i,j) not in self.bloques_solidos["colicionables"]]
                    random.shuffle(posiciones_libres)
                    cantidad_llaves = puerta.cantidad_de_llaves_necesarias
                    centro = (self.tamanio_mapa // 2,self.tamanio_mapa // 2)
                    while cantidad_llaves > 0:
                        pos = posiciones_libres.pop(0)
                        if abs(pos[0] - centro[0]) + abs(pos[1] - centro[1]) > self.tamanio_mapa // 4:
                            self.objetos["llaves"].add(LLave(pos[0],pos[1],puerta))
                            cantidad_llaves -= 1
                    self.objetos["puerta"].add(puerta)
                
                elif Id == SUELO:
                    self.objetos["suelo"].add(Bloque(posicion[0],posicion[1],self.obtener_sprite_sheet(self.mapeo_sprites[posicion])))
                elif Id == MARTILLO:
                    self.objetos["items"].add(ItemRompeMuro(posicion[0],posicion[1]))
                elif Id == BOTIQUIN:
                    self.objetos["items"].add(ItemBotiquin(posicion[0],posicion[1]))
                elif Id == BOMBAATURDIDORA:
                    self.objetos["items"].add(ItemAturdirMinotauro(posicion[0],posicion[1]))
                elif Id == BRUJULA:
                    self.objetos["items"].add(ItemBrujula(posicion[0],posicion[1]))
                elif Id == SALIDA:
                    self.objetos["salida"].add(Salida(posicion[0],posicion[1]))
                
    def draw(self,superficie:pygame.Surface,offset :tuple[int,int]):
        for m in self.bloques_solidos.values():
            m.draw(superficie,offset)
        pygame.draw.rect(superficie,"red",((self.tamanio_mapa//2 * TILE) - offset[0],(self.tamanio_mapa//2 * TILE )- offset[1],TILE,TILE))






class LaberintoAnimado:
    def __init__(self):
        self.ancho = ANCHO
        self.alto = ALTO
        self.tile_size = 16
        self.grid = [[1 for _ in range(ANCHO // self.tile_size)] for _ in range(ALTO // self.tile_size)]
        self.stack = []
        self.current = (0, 0)
        self.visitados = set()
        self.terminado = False
        self.surface = pygame.Surface((ANCHO, ALTO))
        self.colores = {0: (50,50,50), 1: "white"}  # pared, camino
        self.visitados.add(self.current)
        self.stack.append(self.current)

    def update(self):
        if self.terminado:
            return

        x, y = self.current
        vecinos = self.obtener_vecinos_validos(x, y)

        if vecinos:
            nuevo = random.choice(vecinos)
            self.remover_pared_entre((x, y), nuevo)
            self.visitados.add(nuevo)
            self.stack.append(nuevo)
            self.current = nuevo
        else:
            if self.stack:
                self.current = self.stack.pop()
            else:
                self.terminado = True

        self.redibujar_tile(x,y)
    def obtener_vecinos_validos(self, x, y):
        vecinos = []
        direcciones = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.ancho // self.tile_size and 0 <= ny < self.alto // self.tile_size and (nx, ny) not in self.visitados:
                vecinos.append((nx, ny))
        return vecinos

    def remover_pared_entre(self, actual, siguiente):
        ax, ay = actual
        sx, sy = siguiente
        mx, my = (ax + sx) // 2, (ay + sy) // 2
        self.grid[ay][ax] = 0
        self.grid[sy][sx] = 0
        self.grid[my][mx] = 0
        self.redibujar_tile(sx,sy)
        self.redibujar_tile(mx,my)

    def redibujar_tile(self, x, y):
        valor = self.grid[y][x]
        color = self.colores[valor]
        pygame.draw.rect(
            self.surface,
            color,
            (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
        )

    def draw(self, pantalla):
        pantalla.blit(self.surface, (0, 0))