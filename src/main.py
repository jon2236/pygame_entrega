import pygame
import random
from settings import *
from player import Player
from enemy import Enemy
from coin import Coin

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
player = Player(clock)  # Pasar clock al constructor del jugador
all_sprites.add(player)

# Crear un grupo de enemigos
enemies = pygame.sprite.Group()

# Crear un grupo de monedas
coins = pygame.sprite.Group()

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
    for sprite in all_sprites:
        if isinstance(sprite, Player):
            sprite.update(dt)
        elif isinstance(sprite, Enemy):
            sprite.update(player, dt)
        else:
            sprite.update()
    
    # Verificar colisiones entre proyectiles y enemigos
    for bullet in player.bullets:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
        for enemy in hit_enemies:
            enemy.hp -= 30  # Reducir HP del enemigo
            print(f'Enemy HP after hit: {enemy.hp}')  
            bullet.kill()  
            if enemy.hp <= 0:
                enemy.kill()  
                coin = Coin(enemy.rect.centerx, enemy.rect.centery)
                coins.add(coin)
                all_sprites.add(coin)

    # Verificar colisiones entre el jugador y las monedas
    collected_coins = pygame.sprite.spritecollide(player, coins, True)
    for coin in collected_coins:
        player.coins += 1
        print(f'Player collected a coin! Total coins: {player.coins}')

    # Dibujo en pantalla
    SCREEN.blit(background, (0, 0))
    all_sprites.draw(SCREEN)
    player.bullets.draw(SCREEN)

    pygame.display.flip()

pygame.quit()