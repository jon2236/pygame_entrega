import pygame
import random
import json
import csv
from player import Player
from enemy import Enemy
from settings import *

pygame.init()

pygame.init()


with open('./src/resources.json') as f:
    resources = json.load(f)


pygame.mixer.music.load(resources["music"]["start_screen_music"])
pygame.mixer.Sound(resources["sounds"]["lazer_sound"])
pygame.mixer.Sound(resources["sounds"]["coin_up"])
pygame.mixer.Sound(resources["sounds"]["enemy_death"])


SCREEN = pygame.display.set_mode((SCREEN_SIZE))
pygame.display.set_caption("mi juego")

icon = pygame.image.load("./src/assets/imagenes/juego icono ventana.png")
pygame.display.set_icon(icon)

font = pygame.font.SysFont(None, 60)
font_start = pygame.font.Font("src/assets/fonts/Metroid-Fusion.ttf", 240)
font_title = pygame.font.Font("src/assets/fonts/Metroid-Fusion.ttf", 400)
font_high_score = pygame.font.Font("src/assets/fonts/Metroid-Fusion.ttf", 50)
font_high_score_inside_menu = pygame.font.Font("src/assets/fonts/Metroid-Fusion.ttf", 100)
font_restart = pygame.font.Font("src/assets/fonts/Metroid-Fusion.ttf", 50)
font_main_menu = pygame.font.Font("src/assets/fonts/Metroid-Fusion.ttf", 50)


play_button = pygame.Rect(WIDTH / 2 - 400, HEIGHT / 2 - 150, 600, 200)
exit_button = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 + 150, 600, 200)
high_score_button = pygame.Rect(WIDTH / 2 + 600, HEIGHT / 2 + 400, 300, 100)
restart_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 300, 300, 100)
main_menu_button = pygame.Rect(WIDTH / 2 + 400, HEIGHT / 2 + 300, 300, 100)
high_score_corner_menu_button = pygame.Rect(WIDTH / 2 + 400, HEIGHT / 2 + 300, 300, 100)


play_button_text = font_start.render("play", True, WHITE)
exit_button_text = font_start.render("exit", True, WHITE)
high_score_button_text = font_high_score.render("high score", True, WHITE)
restart_button_text = font_restart.render("restart", True, WHITE)
main_menu_button_text = font_main_menu.render("main menu", True, WHITE)
high_score_corner_menu_text = font_high_score.render("main menu", True, WHITE)


background = pygame.image.load("./src/assets/imagenes/ori_ara.jpg")
gameover = pygame.image.load("./src/assets/imagenes/gameover.jpg")
start_screen_bg = pygame.image.load("./src/assets/imagenes/samus.jpg")
bg_score = pygame.image.load("./src/assets/imagenes/bg_score.jpg")
heart_image = pygame.image.load("./src/assets/imagenes/hearts.png")

clock = pygame.time.Clock()

#mis sprites
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


def draw_text(surface, text, font, position, color=WHITE, background_color=BLACK):
    rendered_text = font.render(text, True, color, background_color)
    rect = rendered_text.get_rect()
    rect.center = position
    surface.blit(rendered_text, rect)


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


def high_score_screen(high_scores):
    SCREEN.blit(bg_score, (0, 0))
    draw_text(SCREEN, "best scores", font_high_score_inside_menu, (WIDTH / 2 + 100, HEIGHT / 2 - 400), WHITE)
    for i, score in enumerate(high_scores):
        score_text = font.render(f"{i + 1}. {score}", True, WHITE)
        SCREEN.blit(score_text, (WIDTH / 2, HEIGHT / 2 - 200 + i * 50))
    pygame.draw.rect(SCREEN, MAGENTA, high_score_corner_menu_button)
    SCREEN.blit(high_score_corner_menu_text, (high_score_corner_menu_button.x + 20, high_score_corner_menu_button.y + 20))
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


def load_high_scores_csv(filename="high_scores.csv"):
    high_scores = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                high_scores.append(int(row[0]))
    except FileNotFoundError:
        pass
    return high_scores


def save_high_scores_csv(high_scores, filename="high_scores.csv"):
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for score in high_scores:
            writer.writerow([score])

def pause_screen():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_q:  
                    return 'main_menu'
        SCREEN.fill(BLACK)
        draw_text(SCREEN, "Paused", font_title, (WIDTH / 2, HEIGHT / 2 - 100), WHITE)
        draw_text(SCREEN, "Press P to continue", font_restart, (WIDTH / 2, HEIGHT / 2 + 100), WHITE)
        draw_text(SCREEN, "Press Q to quit", font_restart, (WIDTH / 2, HEIGHT / 2 + 200), WHITE)
        
        pygame.display.update()
        clock.tick(15)

