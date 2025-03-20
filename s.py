import random
import pygame
import numpy as np

def generar_laberinto(ancho, alto):
    laberinto = np.ones((alto, ancho), dtype=int)  # 1 es pared, 0 es camino
     
    def generar():
        inicio_x, inicio_y = 1, 1  # Comenzar desde la esquina superior izquierda
        laberinto[inicio_y][inicio_x] = 0
        paredes = [(inicio_x + dx // 2, inicio_y + dy // 2, inicio_x + dx, inicio_y + dy) 
                   for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]
                   if 0 < inicio_x + dx < ancho-1 and 0 < inicio_y + dy < alto-1]
        random.shuffle(paredes)
        
        while paredes:
            px, py, nx, ny = paredes.pop()
            if laberinto[ny][nx] == 1:
                laberinto[py][px] = 0
                laberinto[ny][nx] = 0
                nuevos_vecinos = [(nx + dx // 2, ny + dy // 2, nx + dx, ny + dy)
                                  for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]
                                  if 0 < nx + dx < ancho-1 and 0 < ny + dy < alto-1]
                random.shuffle(nuevos_vecinos)
                paredes.extend(nuevos_vecinos)
    
    generar()
    
    # Asegurar que el centro sea accesible
    centro_x, centro_y = ancho // 2, alto // 2
    laberinto[centro_y][centro_x] = 0
    caminos = [(centro_x + dx, centro_y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
               if 0 < centro_x + dx < ancho-1 and 0 < centro_y + dy < alto-1]
    if caminos:
        cx, cy = random.choice(caminos)
        laberinto[cy][cx] = 0
    
    return laberinto

def mostrar_laberinto_pygame(laberinto, tamaño_celda=20):
    pygame.init()
    ancho, alto = len(laberinto[0]) * tamaño_celda, len(laberinto) * tamaño_celda
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Laberinto")
    
    negro = (0, 0, 0)
    blanco = (255, 255, 255)
    
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        
        pantalla.fill(negro)
        for y, fila in enumerate(laberinto):
            for x, celda in enumerate(fila):
                color = blanco if celda == 0 else negro
                pygame.draw.rect(pantalla, color, (x * tamaño_celda, y * tamaño_celda, tamaño_celda, tamaño_celda))
        
        pygame.display.flip()
    
    pygame.quit()

# Generar y mostrar un laberinto de 21x21
laberinto = generar_laberinto(30, 30)
mostrar_laberinto_pygame(laberinto,29)
