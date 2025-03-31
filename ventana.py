import pygame,pygame_gui
import pygame_gui.ui_manager
from definiciones import *
from jugador import Jugador
from laberinto import *
from camara import Camara
from minotauro import Minotauro
from quad_tree import Quadtree
from manejo_ui import *

# Clase vase de una ventana, se va a encargar de actualizar y mostrar las distintas escenas del juego.
class Ventana:
    def __init__(self,manejo_venanta):
        self.manejo_ventana = manejo_venanta
        pass
    def draw(self,superficie):
        pass
    def update(self,dt):
        pass



# Clase que se encarga de mostrar el juego, es la ventana principal del juego
class VentanaJuego(Ventana):
    def __init__(self,manejo_venanta):
        super().__init__(manejo_venanta)
        
        self.laberinto  = Laberinto()
        self.quad_tree  = Quadtree(0,pygame.Rect(0,0,self.laberinto.tamanio_nivel[0],self.laberinto.tamanio_nivel[1]))
        self.jugador    = Jugador(self.laberinto.punto_aparicion[0] * TILE,self.laberinto.punto_aparicion[0] * TILE)
        self.minotauro  = Minotauro(self.laberinto.punto_aparicion_minotauro[0] * TILE,self.laberinto.punto_aparicion_minotauro[1] * TILE)
        self.camara     = Camara(0,0,self.laberinto.tamanio_nivel,self.jugador)
        self.manejo_gui = pygame_gui.UIManager((ANCHO, ALTO))
        self.elementos_en_pantalla = []

        self.gano_juego = False
        self.inventario_ui = InventarioUI()
        self.vida_ui        = VidaUI()


        # lista de elementos que se actualizan sin importar si estan o no el la pantalla(particulas,efectos,etc)
        self.elementos_actualizables = pygame.sprite.Group()

        for tipo in self.laberinto.objetos:
            for elemento in self.laberinto.objetos[tipo]:
                self.quad_tree.insertar(elemento)


        self.obtener_elementos_pantalla()

    
        self.texto_vida  =  pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((40,ALTO-30-40), (200, 30)),
            text='Vida: 3',
            manager=self.manejo_gui
        )


    

    def obtener_elementos_pantalla(self):
        offset = self.camara.obtener_offset()
        self.elementos_en_pantalla = []

        # Obtengo los tiles que se encuentran mostrando en la patalla.
        self.elementos_en_pantalla =  self.quad_tree.consulta(pygame.Rect(offset[0]-TILE,offset[1]-TILE,ANCHO + 2 * TILE,ALTO + 2 * TILE))
        self.elementos_en_pantalla.sort(key=lambda x: x.z_index) # ordeno los elementos por su z_index para dibujarlos en el orden correcto.

    def obtener_posicion_jugador_grilla(self):
        return (self.jugador.rect.centerx // TILE,self.jugador.rect.centery // TILE)

    def update(self, dt):
        eventos = pygame.event.get()

        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            self.manejo_gui.process_events(event)
        
        self.obtener_elementos_pantalla()
        self.manejo_gui.update(dt)
        for i in self.elementos_en_pantalla:
            i.update(dt,self)

        for i in self.elementos_actualizables:
            i.update(dt,self)
        self.jugador.manejo_entrada(eventos)
        self.jugador.update(dt,self)
        self.minotauro.update(dt,self)
        self.camara.update(dt)
        self.inventario_ui.update(dt)

        if self.gano_juego or self.jugador.vida <= 0:
            self.manejo_ventana.cambiar_ventana("menu")

    
    def generar_mascara_vision(self,superficie, offset, radio):
        # Crear una superficie negra con transparencia
        mascara = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)
        mascara.fill((0, 0, 0, 200))  # Negro semi-transparente

        # Obtener la posición del jugador en la pantalla
        centro_x, centro_y = self.jugador.rect.center

        # Dibujar un círculo transparente en la máscara
        pygame.draw.circle(mascara, (0, 0, 0, 0), (centro_x -offset[0], centro_y-offset[1]), radio)

        return mascara

    def draw(self,superficie):
        offset = self.camara.obtener_offset()


        for i in self.elementos_en_pantalla:
            i.draw(superficie,offset)
        

        # self.laberinto.rb_visual(superficie)
        self.minotauro.draw(superficie,offset)
        self.jugador.draw(superficie,offset)
        
        for i in self.elementos_actualizables:
            i.draw(superficie,offset)
        # Generar la máscara de visión
        mascara = self.generar_mascara_vision(superficie, offset, radio=150)
        superficie.blit(mascara, (0, 0))  # Superponer la máscara

        self.inventario_ui.draw(superficie)
        self.vida_ui.draw(superficie)
        # for i in self.grafo:
            # pygame.draw.circle(superficie,"yellow",(i[0] * TILE + TILE//2 - offset[0],i[1] * TILE + TILE // 2 - offset[1]),5)
            # for j in self.grafo[i]:
                # pygame.draw.line(superficie,"blue",(i[0] * TILE + TILE // 2 - offset[0],i[1] * TILE + TILE // 2 - offset[1]),(j[0] * TILE + TILE // 2 - offset[0],j[1] * TILE + TILE // 2 - offset[1]))

        # self.quad_tree.draw(superficie,offset)


class FinDelJuego(Ventana):
    def __init__(self, manejo_venanta):
        super().__init__(manejo_venanta)

        self.manejo_gui = pygame_gui.UIManager((ANCHO, ALTO),theme_path="configuracion_ui/menu.json")
        self.fondo = pygame.Surface((ANCHO,ALTO))
        self.fondo.fill("brown")

        # # Texto del resultado
        # self.texto_resultado = pygame_gui.elements.UILabel(
        #     relative_rect=pygame.Rect((self.ANCHO//2 - 150, 150), (300, 50)),
        #     text=f"¡Has {resultado}!" if resultado == "ganado" else "¡Has perdido!",
        #     manager=self.manejo_gui,
        #     object_id="#titulo"
        # )

        

        self.boton_menu = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((ANCHO//2 - 100, 320), (200, 50)),
            text="Volver al Menú",
            manager=self.manejo_gui
        )

        self.boton_reintentar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((ANCHO//2 - 100, 250), (200, 50)),
            text="Reintentar",
            manager=self.manejo_gui
        )

        self.manejo_gui.update(1/FPS)

    def update(self, dt):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.boton_menu:
                        self.manejo_ventana.cambiar_ventana("menu")
                    if event.ui_element == self.boton_reintentar:
                        self.manejo_ventana.cambiar_ventana("juego")

            self.manejo_gui.process_events(event)
        self.manejo_gui.update(dt)

    def draw(self, superficie):
        self.fondo.fill("brown")
        superficie.blit(self.fondo,(0,0))

        # Dibujar el menú
        self.manejo_gui.draw_ui(superficie)


# Clase que se encarga de mostrar el menú principal del juego.
class MenuPrincipal(Ventana):
    def __init__(self, manejo_venanta):
        super().__init__(manejo_venanta)
        self.fondo = pygame.Surface((ANCHO,ALTO))
        self.fondo.fill("black")
        self.laberinto_animado = LaberintoAnimado()

        self.manejo_gui = pygame_gui.ui_manager.UIManager((ANCHO,ALTO),theme_path="configuracion_ui/menu.json")
        self.titulo = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0,ALTO//4,-1,-1),
            text = "El Laberinto",
            manager = self.manejo_gui,
            object_id="#Titulo",
            anchors={"centerx":"centerx"}
        )

        # Crear botones
        self.boton_iniciar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(ANCHO // 2 - 100,ALTO // 2 + 50 + 5,200,50),
            text="Iniciar Juego",
            manager=self.manejo_gui
        )

        self.boton_salir = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(ANCHO // 2 - 100,ALTO // 2 + 100 + 5,200,50),
            text="Salir",
            manager=self.manejo_gui
        )

        self.manejo_gui.update(1/FPS)


    def update(self, dt):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.boton_iniciar:
                    self.manejo_ventana.cambiar_ventana("juego")

                if event.ui_element == self.boton_salir:
                    pygame.quit()
                    exit()


            self.manejo_gui.process_events(event)
        self.laberinto_animado.update()
        self.manejo_gui.update(dt)

    def draw(self, superficie):
        self.fondo.fill("black")
        superficie.blit(self.fondo,(0,0))
        self.laberinto_animado.draw(superficie)

        # Dibujar el menú
        self.manejo_gui.draw_ui(superficie)