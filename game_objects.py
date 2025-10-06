import pygame
import random


class Player:
    """Manages the player's spaceship, including movement, shooting, and health."""
    
    def __init__(self, x, y, width, height, image, max_bullets=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.velocity = 10
        self.bullet_velocity = 7
        self.max_bullets = max_bullets
        self.bullets = []
        self.score = 0
        self.health = 50
        
    def move(self, keys_pressed, game_active):
        """Moves the spaceship according to user input."""
        if game_active:
            if keys_pressed[pygame.K_LEFT] and self.rect.left - self.velocity > 20:
                self.rect.x -= self.velocity
            if keys_pressed[pygame.K_RIGHT] and self.rect.right - self.velocity < 596:
                self.rect.x += self.velocity
            if keys_pressed[pygame.K_UP] and self.rect.top - self.velocity > 0:
                self.rect.y -= self.velocity
            if keys_pressed[pygame.K_DOWN] and self.rect.bottom + self.velocity < 1024:
                self.rect.y += self.velocity
    
    def shoot(self, laser_sound):
        """Creates a bullet if the player can shoot."""
        if len(self.bullets) < self.max_bullets:
            bullet = Bullet(self.rect.x - 9, self.rect.y - 20, 17, 70)
            self.bullets.append(bullet)
            laser_sound.play()
    
    def update_bullets(self):
        """Updates all bullets and removes those that are off-screen."""
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.rect.y < 0:
                self.bullets.remove(bullet)
    
    def draw(self, surface):
        """Draws the player on the screen."""
        surface.blit(self.image, (self.rect.x - (self.rect.w // 2), self.rect.y))
    
    def draw_bullets(self, surface, bullet_image):
        """Draws all bullets on the screen."""
        for bullet in self.bullets:
            bullet.draw(surface, bullet_image)
    
    def reset(self):
        """Resets the player's position."""
        self.rect.center = (308, 900)


class Asteroid:
    """Manages individual asteroids, including movement and rotation."""
    
    def __init__(self, x, y, surface):
        self.surface = surface
        self.rect = surface.get_rect(midbottom=(x, y))
        self.angle = 0
        
    def move(self):
        """Moves the asteroid down the screen."""
        self.rect.centery += 5
    
    def rotate(self):
        """Rotates the asteroid."""
        self.angle -= 15
        rotated = pygame.transform.rotozoom(self.surface, self.angle, 1)
        return rotated
    
    def draw(self, surface):
        """Draws the asteroid on the screen."""
        rotated_surface = self.rotate()
        surface.blit(rotated_surface, self.rect)
    
    def is_off_screen(self):
        """Checks if the asteroid is off the bottom of the screen."""
        return self.rect.top > 1024


class Bullet:
    """Manages individual bullets."""
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def move(self):
        """Moves the bullet upward."""
        self.rect.y -= 7
    
    def draw(self, surface, image):
        """Draws the bullet on the screen."""
        surface.blit(image, self.rect)
