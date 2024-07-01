import pygame, sys, random
from settings import *


pygame.init()

SCREEN = pygame.display.set_mode((SCREEN_SIZE))
pygame.display.set_caption("test Juego")
clock = pygame.time.Clock()

en_ejecucion = True

ABAJO_DERECHA = 3 # +x +y
ABAJO_IZQUIERDA = 9 #-x +y
ARRIBA_DERECHA = 1 # -x +y
ARRIBA_IZQUIERDA = 7 # 

bloque_width = 100
bloque_height = 100

speed = 3

gravedad = True
gravedad_x = True

bloque = {"rectangulo": pygame.Rect(350, 250, 80, 80),"color": GREEN, "direccion": ABAJO_DERECHA}

#bloque = pygame.draw.rect(SCREEN, VERDE_LIMA, (350, 250, 80, 80))

while en_ejecucion:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_ejecucion = False
    SCREEN.fill(BLUE)

    if bloque["rectangulo"].right >= WIDTH:
        if  bloque["direccion"] == ABAJO_DERECHA:
            bloque["direccion"] = ABAJO_IZQUIERDA
        else:
            bloque["direccion"] = ARRIBA_IZQUIERDA
    elif bloque["rectangulo"].left <= 0:
        if bloque["direccion"] == ABAJO_IZQUIERDA:
            bloque["direccion"] = ABAJO_DERECHA
        else:
            bloque["direccion"] = ARRIBA_DERECHA
    elif bloque["rectangulo"].top <= 0:
        if  bloque["direccion"] == ARRIBA_DERECHA:
            bloque["direccion"] = ABAJO_DERECHA
        else: 
            bloque["direccion"] = ABAJO_IZQUIERDA
    elif bloque["rectangulo"].bottom >= HEIGHT:
        if  bloque["direccion"] == ABAJO_DERECHA:
            bloque["direccion"] = ARRIBA_DERECHA
        else:
            bloque["direccion"] =  ARRIBA_IZQUIERDA
    if bloque["direccion"] == ABAJO_DERECHA:
        bloque["rectangulo"].x += speed
        bloque["rectangulo"].y += speed
    elif bloque["direccion"] == ABAJO_IZQUIERDA:
        bloque["rectangulo"].x -= speed
        bloque["rectangulo"].y += speed
    elif bloque["direccion"] == ARRIBA_DERECHA:
        bloque["rectangulo"].x += speed
        bloque["rectangulo"].y -= speed
    elif bloque["direccion"] == ARRIBA_IZQUIERDA:
        bloque["rectangulo"].x -= speed
        bloque["rectangulo"].y -= speed

    pygame.draw.rect(SCREEN, bloque["color"], bloque["rectangulo"])

    clock.tick(60)
    pygame.display.flip()

pygame.quit()