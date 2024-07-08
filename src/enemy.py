import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.idle_sprites = []
        self.idle_sprites.append(pygame.image.load("./src/assets/imagenes/ghost1.png").convert_alpha())
        self.idle_sprites.append(pygame.image.load("./src/assets/imagenes/ghost2.png").convert_alpha())
        self.idle_sprites.append(pygame.image.load("./src/assets/imagenes/ghost3.png").convert_alpha())
        self.idle_sprites.append(pygame.image.load("./src/assets/imagenes/ghost4.png").convert_alpha())
        self.current_sprite = 0
        self.image = self.idle_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.hp = 100  # Añadir HP al enemigo
        self.animation_timer = 0
        self.animation_speed = 0.1

    def update(self, player, dt):
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        if self.rect.y > player.rect.y:
            self.rect.y -= self.speed

        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_sprite += 1
            if self.current_sprite >= len(self.idle_sprites):
                self.current_sprite = 0
            self.image = self.idle_sprites[self.current_sprite]