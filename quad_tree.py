import pygame

class Quadtree:
    def __init__(self,level : int,rect : pygame.Rect,padre  = None,raiz = True):
        self.level_max      = 5
        self.capacidad      = 25 #mmmmm hay que verlo
        self.raiz           = raiz

        self.level          = level
        self.objetos        = pygame.sprite.Group()
        self.rect           = rect

        self.nodos          = [None] * 4
        self.Padre          = padre
        self.tiles_cargados = {}

    def dividir(self):
        mitadancho          = self.rect.width  // 2
        mitadalto           = self.rect.height // 2
                                                                            
        x                   = self.rect.x   
        y                   = self.rect.y                           
        '''
        La pantalla la divide en cuatro porciones

         1 | 0     
        -- | --   
         2 | 3   
        '''

        
        self.nodos[0]       = Quadtree(self.level + 1,pygame.Rect(x + mitadancho,y,mitadancho,mitadalto),self,False)   # Primer sector.
        self.nodos[1]       = Quadtree(self.level + 1,pygame.Rect(x,y,mitadancho,mitadalto),self, False)                # Segundo sector.            
        self.nodos[2]       = Quadtree(self.level + 1,pygame.Rect(x,y + mitadalto,mitadancho,mitadalto),self, False)    # Tercer sector.
        self.nodos[3]       = Quadtree(self.level + 1,pygame.Rect(x + mitadancho,y + mitadalto,mitadancho,mitadalto),self, False)   # Cuarto sector.




    def insertar(self,elemt,tipo = "colicion"):
        indice = self.obtener_indice(elemt.rect,0)
        if not indice:
            return False
        
            

        if len(self.objetos) < self.capacidad and self.nodos[0] is None:
            self.objetos.add(elemt)
            return True
       
        if self.nodos[0] is None:
            self.dividir()
       
        for elemto in self.objetos:
            for i in self.obtener_indice(elemto.rect,0):
                if self.nodos[i].insertar(elemto,tipo):
                    break
       
        self.objetos.empty()
       
        for i in indice:
            if self.nodos[i].insertar(elemt,tipo):
                return True
       
        return False    


    
    def obtener_indice(self,elemt_rect : pygame.Rect,margen = 32):
        indice              = []
        mitad_ancho         = self.rect.x + self.rect.width  // 2
        mitad_alto          = self.rect.y + self.rect.height // 2
        
        # Divide el espacio en dos partes, superior e inferior.

        cuadrante_top       = elemt_rect.y - margen < mitad_alto
        cuadrante_abajo     = elemt_rect.y + elemt_rect.height + margen > mitad_alto
        cuadrante_este      = elemt_rect.x + elemt_rect.width + margen > mitad_ancho
        cuadrante_oeste     = elemt_rect.x - margen < mitad_ancho



        '''

        1 | 0 --> indices
       -- | --
        2 | 3


        '''
        
        if cuadrante_top:
            if cuadrante_este:
                indice.append(0)
            if cuadrante_oeste:
                indice.append(1)
        
        if cuadrante_abajo:
            if cuadrante_oeste:
                indice.append(2)
            if cuadrante_este:
                indice.append(3)

   

        return indice
    






    def consulta(self, area: pygame.Rect, tipo=None, tiles_encontrados=None) -> list:
        if tiles_encontrados is None:
            tiles_encontrados = set()

        if not self.rect.colliderect(area):
            return list(tiles_encontrados)

        if self.nodos[0] is not None:
            for nodo in self.nodos:
                nodo.consulta(area, tipo, tiles_encontrados)

        for i in self.objetos:
            if i.rect.colliderect(area):
                tiles_encontrados.add(i)

        return list(tiles_encontrados)

   

    def draw(self,superficie,offset):

        pygame.draw.rect(superficie,"grey",(self.rect.x-offset[0],self.rect.y-offset[1],self.rect.width,self.rect.height),32)
        for n in self.nodos:
            if n is not None:
                n.draw(superficie,offset)




