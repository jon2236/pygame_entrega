import pygame
import random
import json
from settings import *
from player import Player
from enemy import Enemy
from coin import Coin
from essentials import *

pygame.init()
pygame.mixer.init()

spawn_enemies(enemy_count)

is_running = True
score = 0
high_scores = load_high_scores_csv()
text = font.render(f"Score: {score}", True, RED)
show_title_screen = True
show_high_score_screen = False

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

def update_high_scores(score):
    global high_scores
    high_scores.append(score)
    for i in range(len(high_scores)):
        for j in range(i + 1, len(high_scores)):
            if high_scores[j] > high_scores[i]:
                high_scores[i], high_scores[j] = high_scores[j], high_scores[i]
    high_scores = high_scores[:10]
    save_high_scores_csv(high_scores)



pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.9)

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if show_title_screen:
                if play_button.collidepoint(event.pos):
                    show_title_screen = False
                    show_high_score_screen = False
                    reset_game()
                if exit_button.collidepoint(event.pos):
                    is_running = False
                if high_score_button.collidepoint(event.pos):
                    show_title_screen = False
                    show_high_score_screen = True
            elif show_high_score_screen:
                if main_menu_button.collidepoint(event.pos):
                    show_title_screen = True
                    show_high_score_screen = False
            else:
                if restart_button.collidepoint(event.pos) and player.alive == False:
                    reset_game()
                if main_menu_button.collidepoint(event.pos) and player.alive == False:
                    show_title_screen = True

    if show_title_screen:
        start_screen()
    elif show_high_score_screen:
        high_score_screen(high_scores)
    else:
        dt = clock.tick(FPS)

        # Actualizar temporizador de spawn de enemigos
        enemy_spawn_timer += dt
        if enemy_spawn_timer >= enemy_spawn_delay:
            enemy_spawn_timer = 0
            enemy_count += 5  # Incrementar la cantidad de enemigos en 5
            spawn_enemies(enemy_count)

        # Actualizo elementos
        for sprite in all_sprites:
            if isinstance(sprite, Player):
                sprite.update(dt)
            elif isinstance(sprite, Enemy):
                sprite.update(player, dt)
            else:
                sprite.update()

        for bullet in player.bullets:
            
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in hit_enemies:
                enemy.hp -= 100
                print(f'Enemy HP after hit: {enemy.hp}')  
                bullet.kill()  
                if enemy.hp <= 0:
                    enemy.kill()  
                    coin = Coin(enemy.rect.centerx, enemy.rect.centery)
                    coins.add(coin)
                    all_sprites.add(coin)

        collected_coins = pygame.sprite.spritecollide(player, coins, True)
        for coin in collected_coins:
            score += 1
            text = font.render(f"Score: {score}", True, RED)
            player.coins += 1
            print(f'Player collected a coin! Total coins: {player.coins}')

        player_death = pygame.sprite.spritecollide(player, enemies, False)
        for enemy in player_death:
            player.hp -= 100
            if player.hp <= 0:
                player.alive = False
                player.kill()
                update_high_scores(score)

        # Dibujo en pantalla
        SCREEN.blit(background, (0, 0))
        all_sprites.draw(SCREEN)
        player.bullets.draw(SCREEN)
        SCREEN.blit(text, (WIDTH / 2, 5))
        if not player.alive:
            SCREEN.blit(gameover, (0, 0))
            pygame.draw.rect(SCREEN, MAGENTA, restart_button)
            pygame.draw.rect(SCREEN, MAGENTA, main_menu_button)
            SCREEN.blit(restart_button_text, (restart_button.x + 50, restart_button.y + 20))
            SCREEN.blit(main_menu_button_text, (main_menu_button.x + 20, restart_button.y + 20))

    pygame.display.flip()

pygame.quit()