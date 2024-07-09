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
font_high_score = pygame.font.Font("src/assets/fonts/Metroid-Fusion.ttf", 50)
font_restart = pygame.font.Font("src/assets/fonts/Metroid-Fusion.ttf", 50)
font_main_menu = pygame.font.Font("src/assets/fonts/Metroid-Fusion.ttf", 50)

play_button = pygame.Rect(WIDTH / 2 - 400, HEIGHT / 2 - 150, 600, 200)
exit_button = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 + 150, 600, 200)
high_score_button = pygame.Rect(WIDTH / 2 + 600, HEIGHT / 2 + 400, 300, 100)
restart_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 300, 300, 100)
main_menu_button = pygame.Rect(WIDTH / 2 + 400, HEIGHT / 2 + 300, 300, 100)



play_button_text = font_start.render("play", True, WHITE)
exit_button_text = font_start.render("exit", True, WHITE)
high_score_button_text = font_high_score.render("high score", True, WHITE)
restart_button_text = font_restart.render("restart", True, WHITE)
main_menu_button_text = font_main_menu.render("main menu", True, WHITE)



background = pygame.image.load("./src/assets/imagenes/ori_ara.jpg")
gameover = pygame.image.load("./src/assets/imagenes/gameover.jpg")
start_screen_bg = pygame.image.load("./src/assets/imagenes/samus.jpg")

clock = pygame.time.Clock()

# Crear un grupo de sprites y añadir al jugador
all_sprites = pygame.sprite.Group()
player = Player(clock)
all_sprites.add(player)

enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()


enemy_spawn_timer = 0
enemy_spawn_delay = 7000
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
    SCREEN.blit(start_screen_bg, (0, 0))
    draw_text(SCREEN, "Utroid", font_title, (WIDTH / 2 + 200, HEIGHT / 2 - 400), WHITE)
    pygame.draw.rect(SCREEN, BLUE, play_button)
    pygame.draw.rect(SCREEN, BLUE, exit_button)
    pygame.draw.rect(SCREEN, BLUE, high_score_button)
    SCREEN.blit(play_button_text, (play_button.x, play_button.y))
    SCREEN.blit(exit_button_text, (exit_button.x + 50, exit_button.y - 10))
    SCREEN.blit(high_score_button_text, (high_score_button.x + 15, high_score_button.y + 30))
    pygame.display.update()


def reset_game():
    global score, enemy_spawn_timer, enemy_count, player, all_sprites, enemies, coins, text
    score = 0
    text = font.render(f"Score: {score}", True, RED)
    enemy_spawn_timer = 0
    enemy_count = initial_enemy_count
    all_sprites.empty()
    enemies.empty()
    coins.empty()
    player = Player(clock)
    all_sprites.add(player)
    spawn_enemies(enemy_count)


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
