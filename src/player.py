import pygame
from settings import *
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, clock):
        super().__init__()
        self.idle_sprites = []
        self.idle_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/idle1.png").convert_alpha())
        self.idle_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/idle2.png").convert_alpha())
        self.idle_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/idle3.png").convert_alpha())
        self.idle_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/idle4.png").convert_alpha())
        self.idle_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/idle5.png").convert_alpha())
        self.run_sprites = []
        self.run_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/run1.png").convert_alpha())
        self.run_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/run2.png").convert_alpha())
        self.run_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/run3.png").convert_alpha())
        self.run_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/run4.png").convert_alpha())
        self.run_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/run5.png").convert_alpha())
        self.run_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/run6.png").convert_alpha())
        self.run_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/run7.png").convert_alpha())
        self.run_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/run8.png").convert_alpha())
        self.run_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/run9.png").convert_alpha())
        self.run_sprites.append(pygame.image.load("./src/assets/imagenes/player movement/run10.png").convert_alpha())
        self.current_sprite = 0
        self.image = self.idle_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 7
        self.hp = 100
        self.alive = True

        self.animation_timer = 0
        self.animation_speed = 0.1
        self.bullets = pygame.sprite.Group()
        self.last_direction = "right"
        
        self.shoot_timer = 0
        self.shoot_delay = 500  # milisegundos
        self.clock = clock  # Guardar clock

        self.coins = 0  # Añadir atributo para contar las monedas

        

    def update(self, dt):
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
            moving = True
            self.last_direction = "left"
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
            moving = True
            self.last_direction = "right"
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
            moving = True
            self.last_direction = "up"
        if keys[pygame.K_s]and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            moving = True
            self.last_direction = "down"

        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_sprite += 1
            if moving:
                if self.current_sprite >= len(self.run_sprites):
                    self.current_sprite = 0
                self.image = self.run_sprites[self.current_sprite]
                if self.last_direction == "right":
                    self.image = pygame.transform.flip(self.image, True, False)
            else:
                if self.current_sprite >= len(self.idle_sprites):
                    self.current_sprite = 0
                self.image = self.idle_sprites[self.current_sprite]
                if self.last_direction == "right":
                    self.image = pygame.transform.flip(self.image, True, False)

        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            self.shoot(self.last_direction)

        self.bullets.update()

    def shoot(self, direction):
        bullet = Bullet(self.rect.centerx, self.rect.centery, direction)
        self.bullets.add(bullet)
        

    