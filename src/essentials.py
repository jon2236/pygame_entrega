import pygame
import random
from player import Player
from enemy import Enemy
from settings import *

pygame.init()

SCREEN = pygame.display.set_mode((SCREEN_SIZE))
pygame.display.set_caption("mi juego")

icono = pygame.image.load("./src/assets/imagenes/juego icono ventana.png")
pygame.display.set_icon(icono)

font = pygame.font.SysFont(None, 60)
font_start = pygame.font.Font("src/assets/fonts/Metroid-Fusion.ttf", 240)
font_title = pygame.font.Font("src/assets/fonts/Metroid-Fusion.ttf", 400)

play_button = pygame.Rect(WIDTH / 2 - 400, HEIGHT / 2 - 150, 600, 200)
exit_button = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 + 150, 600, 200)

play_button_text = font_start.render("play", True, WHITE)
exit_button_text = font_start.render("exit", True, WHITE)



background = pygame.image.load("./src/assets/imagenes/ori_ara.jpg")

clock = pygame.time.Clock()

# Crear un grupo de sprites y añadir al jugador
all_sprites = pygame.sprite.Group()
player = Player(clock) 
all_sprites.add(player)


enemies = pygame.sprite.Group()


coins = pygame.sprite.Group()


enemy_spawn_timer = 0
enemy_spawn_delay = 7000  # 7 segundos
initial_enemy_count = 5
enemy_count = initial_enemy_count

def spawn_enemies(count):
    for _ in range(count):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x = random.randint(0, WIDTH)
            y = 0
        elif side == "bottom":
            x = random.randint(0, WIDTH)
            y = HEIGHT
        elif side == "left":
            x = 0
            y = random.randint(0, HEIGHT)
        elif side == "right":
            x = WIDTH
            y = random.randint(0, HEIGHT)
        enemy = Enemy(x, y)
        enemies.add(enemy)
        all_sprites.add(enemy)

def draw_text(superficie, texto, fuente, coordenada, color = WHITE, color_fondo = BLACK) :
    sticker = fuente.render(texto, True, color, color_fondo)
    rect = sticker.get_rect()
    rect.center = coordenada
    superficie.blit(sticker, rect)


def start_screen():
    SCREEN.fill(BLACK)
    draw_text(SCREEN, "Utroid", font_title, (WIDTH / 2 + 200, HEIGHT / 2 - 400), WHITE)
    pygame.draw.rect(SCREEN, BLUE, play_button)
    pygame.draw.rect(SCREEN, BLUE, exit_button)
    SCREEN.blit(play_button_text, (play_button.x, play_button.y))
    SCREEN.blit(exit_button_text, (exit_button.x + 50, exit_button.y - 10))
    pygame.display.update()


def mod_rgb(imagen, frames):
    """Cambia el color de la imagen en rgb basado en frames"""
    imagen_copy = imagen.copy()
    width, height = imagen_copy.get_size()
    for x in range(width):
        for y in range(height):
            r, g, b, a = imagen_copy.get_at((x, y))
            r = (r + frames) % 256
            g = (g + frames * 2) % 256  # Ajusta la velocidad de cambio para el canal G
            b = (b + frames * 3) % 256  # Ajusta la velocidad de cambio para el canal B
            imagen_copy.set_at((x, y), (r, g, b, a))
    return imagen_copy
