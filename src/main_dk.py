import pygame
from settings import *

pygame.init()
pygame.mixer.init()

SCREEN = pygame.display.set_mode((SCREEN_SIZE))
pygame.display.set_caption("mi juego")

clock = pygame.time.Clock()

# rect_1 = pygame.Rect(100, 400, 200, 100)

# rect_1.center = SCREEN_CENTER
background = pygame.image.load("dk.jpg")

image = pygame.image.load("nint.jpg")
image_rect = image.get_rect()
image_rect.center = SCREEN_CENTER

speed_x = 2
speed_y = 2

pygame.mixer.music.load("aquatic ambience.mp3")
pygame.mixer.music.play(-1)
# gravedad = True




is_running = True
frames_contador = 0

while is_running:
    clock.tick(FPS)
    frames_contador += 1
    # analizo eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    # actualizo elementos

    image_rect.x += speed_x
    image_rect.y += speed_y

    if image_rect.right >= WIDTH or image_rect.left <= 0:
        speed_x = -speed_x
    if image_rect.bottom >= HEIGHT or image_rect.top <= 0:
        speed_y = -speed_y

    rgb_image = mod_rgb(image, frames_contador)

    #-------------------------------------------- rectangulo rebotando estilo dvd
    # rect_1.x += speed_x
    # rect_1.y += speed_y

    # if rect_1.right >= WIDTH or rect_1.left <= 0:
    #     speed_x = -speed_x
    # if rect_1.bottom >= HEIGHT or rect_1.top <= 0:
    #     speed_y = -speed_y
    #-------------------------------------------- rebote solo eje y
    # if gravedad:
    #     if rect_1.bottom <= HEIGHT:
    #         rect_1.y += speed

    #     else:
    #         gravedad = False
    # else:        
    #     if rect_1.top >= 0:
    #         rect_1.y -= speed


    #     else:
    #         gravedad = True


    # print(rect_1.y)
#--------------------------------------------------
    #dibujo en pantalla
    SCREEN.blit(background, (0, 0))
    #pygame.draw.rect(SCREEN, GREEN, rect_1)
    SCREEN.blit(rgb_image, image_rect)


    pygame.display.flip()


pygame.quit()