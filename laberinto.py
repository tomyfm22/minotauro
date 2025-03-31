import pygame,random,time
from definiciones import *
from bloque import *


# Clase que se encarga de generar el laberinto y de instanciar los objetos.

class Laberinto:

    def __init__(self):
        self.tamanio_mapa = 75
        self.punto_aparicion = (1,1)
        self.punto_aparicion_minotauro = (1,1)
        # Guarda las posciones (en coordenadas de grilla) para formar despues el grafo con los elementos colicionables.
        self.elementos_del_laberinto = {
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
            3:2, # pared
            4:3,              } # id : pos_sprite
        
        self.mapeo_sprites = {} # pos:id

        self.sprite_sheet = pygame.image.load("sprites/tiles.png").convert_alpha()

        # Inicializo todo el laberinto agregando la posicion de los muros
        for i in range(self.tamanio_mapa):
            for j in range(self.tamanio_mapa):                
                self.mapeo_sprites[(i,j)] = 1
                if i == 0 or i == self.tamanio_mapa-1 or j == 0 or j == self.tamanio_mapa-1:
                    # if i == 0 or i == self.tamanio_mapa-1:
                        # self.mapeo_sprites[(i,j)] = 3
                    
                    self.mapeo_sprites[(i,j)] = 4
                    self.elementos_del_laberinto["colicionables"][(i,j)] = LIMITE
                    continue


                self.elementos_del_laberinto["colicionables"][(i,j)] = MURO
                


        self.tamanio_nivel = (self.tamanio_mapa * TILE,self.tamanio_mapa * TILE)
        
        self.generar_laberinto()
        
        self.borrar_paredes()

        self.posicionar_objetos()

        self.instanciar_objetos()


        self.grafo = self.generar_grafo()
        

    # Cada vez que se quita un bloque solido, se actualiza el grafo.
    def eliminar_bloque_solido(self,pos_en_grilla):
        if pos_en_grilla in self.elementos_del_laberinto["colicionables"]:
            self.elementos_del_laberinto["colicionables"].pop(pos_en_grilla)
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

            if intermedio in self.elementos_del_laberinto["colicionables"]:
                # self.elementos_del_laberinto.discard(intermedio)
                self.elementos_del_laberinto["colicionables"].pop(intermedio)
                self.mapeo_sprites[intermedio] = 2
            
            
        
        centro = (self.tamanio_mapa // 2 ,self.tamanio_mapa // 2)
        # Si el centro tiene pared, se la quito.
        if centro in self.elementos_del_laberinto["colicionables"]:
            # self.elementos_del_laberinto.discard(centro)
            self.elementos_del_laberinto["colicionables"].pop(centro)
            self.mapeo_sprites[intermedio] = 2
        
        # Quito los muros para que al agregar la puerta, se cambien los muros por limites.
        for dx,dy in direcciones:
            pos = (centro[0] + dx,centro[1] + dy)
            if pos in self.elementos_del_laberinto["colicionables"]:
                # self.elementos_del_laberinto.discard(pos)
                self.elementos_del_laberinto["colicionables"].pop(pos)
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
            self.elementos_del_laberinto["colicionables"].pop(nodo,None)
            no_visitados.discard(nodo)

            nodos_vecinos = [(actual[0] + dx,actual[1] + dy) for dx,dy in direcciones 
                             if (actual[0] + dx,actual[1] + dy) in self.elementos_del_laberinto["colicionables"]  and \
                                (actual[0] + dx,actual[1] + dy) in no_visitados]
            


            
            if nodos_vecinos:
                nuevo = random.choice(nodos_vecinos)
                dire = ((nuevo[0] - actual[0]) // dist,(nuevo[1] - actual[1])//dist)

                # Tile intermedio
                intermedio = (actual[0] + dire[0], actual[1] + dire[1])
                # self.elementos_del_laberinto.discard(intermedio)
                self.elementos_del_laberinto["colicionables"].pop(intermedio,None)
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
            self.elementos_del_laberinto.pop(nodo,None)
            no_visitados.discard(nodo)

            nodos_vecinos = [(actual[0] + dx,actual[1] + dy) for dx,dy in direcciones 
                             if (actual[0] + dx,actual[1] + dy) in self.elementos_del_laberinto  and \
                                (actual[0] + dx,actual[1] + dy) in no_visitados]
            
            
            if nodos_vecinos:
                nuevo = random.choice(nodos_vecinos)
                dire = ((nuevo[0] - actual[0]) // dist,(nuevo[1] - actual[1])//dist)

                # Tile intermedio
                intermedio = (actual[0] + dire[0], actual[1] + dire[1])
                self.elementos_del_laberinto.pop(intermedio,None)
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
                if (i,j) not in self.elementos_del_laberinto["colicionables"].keys():
                    grafo[(i,j)] = []
                    for dx,dy in direcciones:
                        if (i+dx,j+dy) not in self.elementos_del_laberinto["colicionables"].keys() :
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
                if adyacente not in self.elementos_del_laberinto["colicionables"]:
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
                if not pos_vecina in self.elementos_del_laberinto["colicionables"]:
                    agrego_puerta = True
                    self.elementos_del_laberinto["colicionables"][pos_vecina] = PUERTA
                    # Me aseguro que no halla muros al rededor de la puerta.
                    for dx,dy in direcciones:
                        pos = (pos_vecina[0] + dx,pos_vecina[1] + dy)
                        if pos in self.elementos_del_laberinto["colicionables"]:
                            self.elementos_del_laberinto["colicionables"].pop(pos)

            else:
                if not pos_vecina in self.elementos_del_laberinto["colicionables"]:
                    self.elementos_del_laberinto["colicionables"][pos_vecina] = LIMITE


   

        self.elementos_del_laberinto["items"][centro] = SALIDA

        posiciones_libres = [(i,j) for j in range(self.tamanio_mapa) for i in range(self.tamanio_mapa) if ((i,j) not in self.elementos_del_laberinto["colicionables"] and (i,j) != centro)]
        random.shuffle(posiciones_libres)
        proporcion = 0.01  # 5% del total de celdas tendrán ítems
        cantidad_items = max(3, int(len(posiciones_libres) * proporcion))  # Mínimo 3 ítems

        tipos = [MARTILLO, BOMBAATURDIDORA, BOTIQUIN ,BRUJULA]
        distribucion = {MARTILLO: 0.5, BOMBAATURDIDORA: 0.3, BOTIQUIN: 0.2 ,BRUJULA : 0.1}

        for _ in range(cantidad_items):
            tipo = random.choices(tipos, weights=distribucion.values())[0]
            pos = posiciones_libres.pop(0)
            self.elementos_del_laberinto["items"][pos] = tipo

        
        # Busco en que posicion agrego al minotaruo.
        for i in range(self.tamanio_mapa//2 + 5,self.tamanio_mapa//2 + self.tamanio_mapa//2):
            agrego = False
            for j in range(self.tamanio_mapa//2 + 5,self.tamanio_mapa//2 + self.tamanio_mapa//2):
                
                if (i,j) not in self.elementos_del_laberinto["colicionables"] and random.random() > 0.5:
                    self.punto_aparicion_minotauro = (i,j)
                    agrego = True
                    break
            if agrego:
                break

        # Aplico el sprite correspondiente a cada muro.
        for i in range(self.tamanio_mapa):
            for j in range(self.tamanio_mapa):
                pos = (i,j)


                if pos not in self.elementos_del_laberinto["colicionables"]:
                    self.mapeo_sprites[pos] = 2
                    if pos not in self.elementos_del_laberinto["items"]:
                        self.elementos_del_laberinto["items"][pos] = SUELO
                    for dx,dy in direcciones:
                        pos_vecina = (pos[0] + dx,pos[1] + dy)
                        if pos_vecina in self.elementos_del_laberinto["colicionables"]:
                            if self.elementos_del_laberinto["colicionables"][pos_vecina] == LIMITE:
                                self.mapeo_sprites[pos_vecina] = 4
                                continue

                            if dx != 0:
                                self.mapeo_sprites[pos_vecina] = 3
                            if dy != 0:
                                self.mapeo_sprites[pos_vecina] = 1
                            




    def instanciar_objetos(self):
        for tipo in self.elementos_del_laberinto:
            for posicion,Id in self.elementos_del_laberinto[tipo].items():
                if Id == LIMITE:
                    self.objetos["limite"].add(Limite(posicion[0],posicion[1],self.obtener_sprite_sheet(self.mapeo_sprites[posicion])))
                elif Id == MURO:
                    self.objetos["muro"].add(Muro(posicion[0],posicion[1],self.obtener_sprite_sheet(self.mapeo_sprites[posicion])))
                elif Id == PUERTA:
                    puerta = Puerta(posicion[0],posicion[1])
                    # Intancio las llaves en distintos puntos del mapa.
                    posiciones_libres = [(i,j) for j in range(self.tamanio_mapa) for i in range(self.tamanio_mapa) if (i,j) not in self.elementos_del_laberinto["colicionables"]]
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





# Clase simplificada del laberinto que sirve para visualizar la generacion en el menu principal
class LaberintoAnimado:
    def __init__(self):
        self.ancho = ANCHO
        self.alto = ALTO
        self.tamanio_tile = 16
        self.grilla = [[1 for _ in range(ANCHO // self.tamanio_tile)] for _ in range(ALTO // self.tamanio_tile)]
        self.pila = []
        self.actual = (0, 0)
        self.visitados = set()
        self.terminado = False
        self.surface = pygame.Surface((ANCHO, ALTO))
        self.colores = {0: (50,50,50), 1: "white"}  # pared, camino
        self.visitados.add(self.actual)
        self.pila.append(self.actual)

    def update(self):
        if self.terminado:
            return

        x, y = self.actual
        vecinos = self.obtener_vecinos_validos(x, y)

        if vecinos:
            nuevo = random.choice(vecinos)
            self.remover_pared_entre((x, y), nuevo)
            self.visitados.add(nuevo)
            self.pila.append(nuevo)
            self.actual = nuevo
        else:
            if self.pila:
                self.actual = self.pila.pop()
            else:
                self.terminado = True

        self.redibujar_tile(x,y)
    def obtener_vecinos_validos(self, x, y):
        vecinos = []
        direcciones = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.ancho // self.tamanio_tile and 0 <= ny < self.alto // self.tamanio_tile and (nx, ny) not in self.visitados:
                vecinos.append((nx, ny))
        return vecinos

    def remover_pared_entre(self, actual, siguiente):
        ax, ay = actual
        sx, sy = siguiente
        mx, my = (ax + sx) // 2, (ay + sy) // 2
        self.grilla[ay][ax] = 0
        self.grilla[sy][sx] = 0
        self.grilla[my][mx] = 0
        self.redibujar_tile(sx,sy)
        self.redibujar_tile(mx,my)

    def redibujar_tile(self, x, y):
        valor = self.grilla[y][x]
        color = self.colores[valor]
        pygame.draw.rect(
            self.surface,
            color,
            (x * self.tamanio_tile, y * self.tamanio_tile, self.tamanio_tile, self.tamanio_tile)
        )

    def draw(self, pantalla):
        pantalla.blit(self.surface, (0, 0))