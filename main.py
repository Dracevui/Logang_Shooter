import pygame
import sys
import random
import math


def multiples(num1, num2, mult):
    listz = [*range(num1, num2)]
    newlist = listz[::mult]
    return newlist


def rotate_asteroid(asteroids):
    pass


def create_asteroid():
    random_asteroid_pos = random.choice(asteroid_location)
    bottom_asteroid = ASTEROID_SURFACE.get_rect(midtop=(random_asteroid_pos, -200))
    top_asteroid = ASTEROID_SURFACE.get_rect(midbottom=(random_asteroid_pos, 10))
    return bottom_asteroid, top_asteroid


def move_asteroids(asteroids):
    for asteroid in asteroids:
        asteroid.centery += 5
    # visible_asteroids = [asteroid for asteroid in asteroids if asteroid.top > 1126]
    return asteroids


def draw_asteroids(asteroids):
    for asteroid in asteroids:
        DUMMY_WINDOW.blit(ASTEROID_SURFACE, asteroid)


def check_asteroid_collision(asteroids, bullets):
    for asteroid in asteroids:
        if RED_SPACESHIP_RECT.colliderect(asteroid):
            DEATH_SOUND.play()
            return False
    for bullet in bullets:
        if bullet.colliderect(asteroid):
            asteroids.remove(asteroid)
    return True


def handle_bullets(red_bullet, asteroid):
    for bullet in red_bullet:
        bullet.y -= BULLET_VELOCITY
        if asteroid.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ASTEROID_HIT))
            red_bullet.remove(bullet)
        elif bullet.y < 0:
            red_bullet.remove(bullet)


def red_handle_movement(keys_press, red):
    if keys_press[pygame.K_LEFT] and red.x + VELOCITY > 0:  # LEFT
        red.x -= VELOCITY
    if keys_press[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH:  # RIGHT
        red.x += VELOCITY
    if keys_press[pygame.K_UP] and red.y - VELOCITY > 0:  # UP
        red.y -= VELOCITY
    if keys_press[pygame.K_DOWN] and red.y + VELOCITY + red.width < HEIGHT:  # DOWN
        red.y += VELOCITY


def game_quit():
    pygame.quit()
    sys.exit()


def draw_stuff(red, red_bullet):
    DUMMY_WINDOW.blit(BACKGROUND_SURFACE, (0, 0))
    DUMMY_WINDOW.blit(RED_SPACESHIP, (red.x, red.y))
    DUMMY_WINDOW.blit(LOGO, (60, 0))

    for bullet in red_bullet:
        pygame.draw.rect(DUMMY_WINDOW, (255, 255, 255), bullet)
        # DUMMY_WINDOW.blit(LASER_BLAST, RED_SPACESHIP.get_rect().top, bullet)

    draw_asteroids(asteroids_list)

    pygame.display.update()


def scale_window():
    frame = pygame.transform.scale(DUMMY_WINDOW, SCREEN_DIMENSIONS)
    WINDOW.blit(frame, frame.get_rect())
    pygame.display.flip()


def game_over():
    global game_active
    if not game_active:
        DUMMY_WINDOW.blit(BACKGROUND_SURFACE, (0, 0))


def game_clear():
    global game_active
    game_active = True
    asteroids_list.clear()
    RED_SPACESHIP_RECT.center = (250, 900)


def active_game():
    global game_active, asteroids_list
    if game_active:
        # Spaceship
        game_active = check_asteroid_collision(asteroids_list, red_bullets)

        # Asteroids
        asteroids_list = move_asteroids(asteroids_list)


def main():
    red = pygame.Rect(250, 900, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_health = 10

    asteroid = pygame.Rect(250, 20, 50, 50)

    while running:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                game_quit()

            if events.type == pygame.KEYDOWN and events.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(red.x + red.width // 2, red.y, 5, 10)
                red_bullets.append(bullet)

            if events.type == SPAWN_ASTEROID:
                asteroids_list.extend(create_asteroid())
                print(asteroids_list)

            if events.type == ASTEROID_HIT:
                for asteroid in asteroids_list:
                    asteroids_list.remove(asteroid)

            if events.type == pygame.KEYDOWN and not game_active:
                game_clear()

            game_over()

        draw_stuff(red, red_bullets)

        active_game()

        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        
        handle_bullets(red_bullets, asteroid)

        scale_window()

        CLOCK.tick(FPS)


# Constants
pygame.init()
MONITOR = pygame.display.Info()
SCREEN_DIMENSIONS = (math.floor(MONITOR.current_w * 0.3), math.ceil(MONITOR.current_h * 0.948))
WINDOW = pygame.display.set_mode(SCREEN_DIMENSIONS)
DUMMY_WINDOW = pygame.Surface((576, 1024))
WIDTH, HEIGHT = SCREEN_DIMENSIONS
BORDER = pygame.Rect(0, 0, WIDTH, HEIGHT)
FPS = 60
VELOCITY = 10
BULLET_VELOCITY = 7
MAX_BULLETS = 50
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 65, 50
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Logang Shooter")
ICON = pygame.image.load("assets/icon.png")
pygame.display.set_icon(ICON)


# User Events
ASTEROID_HIT = pygame.USEREVENT + 1
SPAWN_ASTEROID = pygame.USEREVENT + 2


# Game Variables
running = True
game_active = True
red_bullets = []

asteroids_list = []
asteroid_location = multiples(12, 563, 50)
pygame.time.set_timer(SPAWN_ASTEROID, 1200)


# Asset Files
BACKGROUND_SURFACE = pygame.transform.scale((pygame.image.load("assets/space.png")), (576, 1024))
RED_SPACESHIP_IMAGE = pygame.image.load("assets/spaceship_red.png").convert_alpha()
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180
)
RED_SPACESHIP_RECT = RED_SPACESHIP.get_rect()

ASTEROID_SURFACE = pygame.transform.scale((pygame.image.load("assets/asteroid.png")).convert_alpha(), (50, 50))
ASTEROID_RECT = ASTEROID_SURFACE.get_rect()

LASER_BLAST = pygame.transform.scale((pygame.image.load("assets/laser_blast.png")).convert_alpha(), (50, 50))
LASER_BLAST_RECT = LASER_BLAST.get_rect()
LASER_SOUND = pygame.mixer.Sound("assets/Gun+Silencer.mp3")
LASER_HIT = pygame.mixer.Sound("assets/Grenade+1.mp3")
DEATH_SOUND = pygame.mixer.Sound("assets/sfx_hit.wav")

LOGO = pygame.image.load("assets/logo.png")

# Start of the main game...
main()

if __name__ == '__main__':
    main()
