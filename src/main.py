import pygame
import random
from settings import *
from enemy import Enemy
from player import Player

pygame.init()
pygame.mixer.init()

SCREEN = pygame.display.set_mode((SCREEN_SIZE))
pygame.display.set_caption("mi juego")

icono = pygame.image.load("imagenes/juego icono ventana.png")
pygame.display.set_icon(icono)

background = pygame.image.load("imagenes/ori_ara.jpg")

clock = pygame.time.Clock()

# Crear un grupo de sprites y añadir al jugador
all_sprites = pygame.sprite.Group()
player = Player(clock)
all_sprites.add(player)

# Crear un grupo de enemigos
enemies = pygame.sprite.Group()

# Temporizador para agregar enemigos
enemy_spawn_timer = 0
enemy_spawn_delay = 10000  # 10 segundos
initial_enemy_count = 3
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

# Inicialmente generar enemigos
spawn_enemies(enemy_count)

is_running = True

while is_running:
    dt = clock.tick(FPS)

    # Analizo eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    # Actualizar temporizador de spawn de enemigos
    enemy_spawn_timer += dt
    if enemy_spawn_timer >= enemy_spawn_delay:
        enemy_spawn_timer = 0
        enemy_count += 2  # Incrementar la cantidad de enemigos en 2
        spawn_enemies(enemy_count)

    # Actualizo elementos
    player.update(dt)
    for enemy in enemies:
        enemy.update(player, dt)
    player.bullets.update()

    # Verificar colisiones entre proyectiles y enemigos
    for bullet in player.bullets:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
        for enemy in hit_enemies:
            enemy.hp -= 20  # Reducir HP del enemigo
            print(f'Enemy HP after hit: {enemy.hp}')  # Imprimir HP del enemigo en la consola
            bullet.kill()  # Eliminar el proyectil
            if enemy.hp <= 0:
                enemy.kill()  # Eliminar al enemigo si su HP es 0 o menor

    # Dibujo en pantalla
    SCREEN.blit(background, (0, 0))
    all_sprites.draw(SCREEN)
    player.bullets.draw(SCREEN)

    pygame.display.flip()

pygame.quit()
