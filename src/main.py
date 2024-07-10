import pygame
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
life_count = 3
high_scores = load_high_scores_csv()
text = font.render(f"Score: {score}", True, RED)
show_title_screen = True
show_high_score_screen = False
active_shield = False
shield_timer = 0
is_paused = False
quit = False
heart_size = (30, 30)
heart_spacing = 10

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

def swap_lista(lista:list, valor1, valor2):
    aux = lista[valor1]
    lista[valor1] = lista[valor2]
    lista[valor2] = aux

def update_high_scores(score):
    global high_scores
    high_scores.append(score)
    for i in range(len(high_scores) - 1):
        for j in range(i + 1, len(high_scores)):
            if high_scores[j] > high_scores[i]:
                swap_lista(high_scores, i, j)
    high_scores = high_scores[:10]
    save_high_scores_csv(high_scores)

def draw_hearts(surface):
    x = WIDTH - 200
    y = 10
    for _ in range(life_count):
        surface.blit(heart_image, (x, y))
        x -= heart_size[0] + heart_spacing

pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)




while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                is_paused = not is_paused
                if is_paused:
                    result = pause_screen()
                    if result == 'main_menu':
                        show_title_screen = True
                        is_paused = False
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

    if is_paused:
        continue
    if show_title_screen:
        start_screen()
    elif show_high_score_screen:
        high_score_screen(high_scores)
    else:
        dt = clock.tick(FPS)


        enemy_spawn_timer += dt
        if enemy_spawn_timer >= enemy_spawn_delay:
            enemy_spawn_timer = 0
            enemy_count += 5  # incremento mis enemigos
            spawn_enemies(enemy_count)


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
                pygame.mixer.Sound("./src/assets/sounds/enemy_death.wav").play()
                bullet.kill()  
                if enemy.hp <= 0:
                    enemy.kill()  
                    coin = Coin(enemy.rect.centerx, enemy.rect.centery)
                    coins.add(coin)
                    all_sprites.add(coin)

        collected_coins = pygame.sprite.spritecollide(player, coins, True)
        for coin in collected_coins:
            pygame.mixer.Sound("./src/assets/sounds/coin_up.wav").play()
            score += 1
            text = font.render(f"Score: {score}", True, RED)
            player.coins += 1
            print(f"moneyyyyyyyyyy Total coins: {player.coins}")

        player_death = pygame.sprite.spritecollide(player, enemies, False)
        shield_timer += 1
        if not active_shield:
            for enemy in player_death:
                shield_timer = 0
                active_shield = True
                life_count -= 1
                player.hp -= 100
                if life_count <= 0:
                    player.alive = False
                    player.kill()
                    life_count = 3
                    update_high_scores(score)
        else:
            if shield_timer == 180:
                active_shield = False


        SCREEN.blit(background, (0, 0))
        all_sprites.draw(SCREEN)
        SCREEN.blit(text, (WIDTH / 2, 5))
        draw_hearts(SCREEN)
        player.bullets.draw(SCREEN)
        SCREEN.blit(text, (WIDTH / 2, 5))
        if active_shield:
            pygame.draw.circle(SCREEN, YELLOW, player.rect.center, 100, 1)
        if not player.alive:
            SCREEN.blit(gameover, (0, 0))
            pygame.draw.rect(SCREEN, MAGENTA, restart_button)
            pygame.draw.rect(SCREEN, MAGENTA, main_menu_button)
            SCREEN.blit(restart_button_text, (restart_button.x + 50, restart_button.y + 20))
            SCREEN.blit(main_menu_button_text, (main_menu_button.x + 20, restart_button.y + 20))

    pygame.display.flip()

pygame.quit()