import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, velocity, bullet_velocity, max_bullets, spaceship_image):
        super().__init__()
        self.image = spaceship_image
        self.rect = self.image.get_rect(center=pos)
        self.velocity = velocity
        self.bullet_velocity = bullet_velocity
        self.max_bullets = max_bullets
        self.bullets = pygame.sprite.Group()
        self.health = 50
        self.score = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left - self.velocity > 20:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right + self.velocity < 596:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top - self.velocity > 0:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom + self.velocity < 1024:
            self.rect.y += self.velocity

    def shoot(self, laser_blast_image, laser_sound):
        if len(self.bullets) < self.max_bullets:
            bullet = Bullet(self.rect.centerx, self.rect.top, self.bullet_velocity, laser_blast_image)
            self.bullets.add(bullet)
            laser_sound.play()

    def update(self):
        self.bullets.update()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.bullets.draw(surface)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, asteroid_image):
        super().__init__()
        self.image = asteroid_image
        self.rect = self.image.get_rect(center=pos)
        self.angle = 0
        self.rotation_speed = random.randint(-5, 5)

    def update(self):
        self.rect.y += 5
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotozoom(self.image, self.angle, 1)
        if self.rect.top > 1024:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = velocity

    def update(self):
        self.rect.y -= self.velocity
        if self.rect.bottom < 0:
            self.kill()
