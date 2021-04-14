import pygame
import sys
import random
import math


def multiples(num1, num2, mult):
    listz = [*range(num1, num2)]
    newlist = listz[::mult]
    return newlist


def rotate_asteroid(asteroids):  # Haven't finished it yet
    pass


def create_asteroid():
    random_asteroid_pos = random.choice(asteroid_location)
    top_asteroid = ASTEROID_SURFACE.get_rect(midbottom=(random_asteroid_pos, 10))
    return top_asteroid


def move_asteroids(asteroids):
    for asteroid in asteroids:
        asteroid.centery += 5
    return asteroids


def draw_asteroids(asteroids):
    for asteroid in asteroids:
        DUMMY_WINDOW.blit(ASTEROID_SURFACE, asteroid)


def check_asteroid_collision(asteroids, bullets, spaceship):
    global red_score, damaged_ship_health
    for asteroid in asteroids:
        if spaceship.colliderect(asteroid):
            DEATH_SOUND.play()
            return False
        for bullet in bullets:
            if bullet.colliderect(asteroid):
                red_score += 1
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                LASER_HIT.play()
        if asteroid.top > BORDER.bottom:
            damaged_ship_health -= 2
            asteroids.remove(asteroid)
    return True


def handle_bullets(red_bullet, asteroid):
    for bullet in red_bullet:
        bullet.y -= BULLET_VELOCITY
        if asteroid.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ASTEROID_HIT))
        elif bullet.y < 0:
            red_bullet.remove(bullet)


def red_handle_movement(keys_press, redship):
    global game_active
    if game_active:
        if keys_press[pygame.K_LEFT] and redship.x + VELOCITY > 0:  # LEFT
            redship.x -= VELOCITY
        if keys_press[pygame.K_RIGHT] and redship.x + VELOCITY + redship.width < WIDTH:  # RIGHT
            redship.x += VELOCITY
        if keys_press[pygame.K_UP] and redship.y - VELOCITY > 0:  # UP
            redship.y -= VELOCITY
        if keys_press[pygame.K_DOWN] and redship.y + VELOCITY + redship.width < HEIGHT:  # DOWN
            redship.y += VELOCITY


def game_quit():
    pygame.quit()
    sys.exit()


def draw_stuff(redship, red_bullet, redscore, ship_health):
    global MAX_BULLETS
    DUMMY_WINDOW.blit(BACKGROUND_SURFACE, (0, 0))

    red_score_text = SCORE_FONT.render(f"Score: {redscore}", True, WHITE)
    DUMMY_WINDOW.blit(red_score_text, (420, 970))

    def ship_health_colour(colour_choice, health):
        if colour_choice == "Green":
            ship_health_text = SCORE_FONT.render(f"Ship Health: {health}", True, GREEN)
        elif colour_choice == "Yellow":
            ship_health_text = SCORE_FONT.render(f"Ship Health: {health}", True, YELLOW)
        elif colour_choice == "Orange":
            ship_health_text = SCORE_FONT.render(f"Ship Health: {health}", True, ORANGE)
        elif colour_choice == "Red":
            ship_health_text = SCORE_FONT.render(f"Ship Health: {health}", True, RED)
        return ship_health_text

    if ship_health >= 90:
        DUMMY_WINDOW.blit(ship_health_colour("Green", ship_health), (10, 970))
    elif 89 > ship_health < 60:
        DUMMY_WINDOW.blit(ship_health_colour("Yellow", ship_health), (10, 970))
    elif 59 > ship_health < 30:
        DUMMY_WINDOW.blit(ship_health_colour("Orange", ship_health), (10, 970))
    else:
        DUMMY_WINDOW.blit(ship_health_colour("Red", ship_health), (10, 970))

    max_bullet_text = SCORE_FONT.render(f"Bullets = {len(red_bullets)}/{MAX_BULLETS}", True, WHITE)
    DUMMY_WINDOW.blit(max_bullet_text, (0, 0))

    DUMMY_WINDOW.blit(RED_SPACESHIP, (redship.x, redship.y))
    DUMMY_WINDOW.blit(LOGO, (60, 0))

    for bullet in red_bullet:
        pygame.draw.rect(DUMMY_WINDOW, WHITE, bullet)
        # DUMMY_WINDOW.blit(LASER_BLAST, RED_SPACESHIP.get_rect().top, bullet)

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
    global game_active, red, red_score, damaged_ship_health, asteroid_spawn_rate
    game_active = True
    red.center = (288, 900)
    red_score = 0
    damaged_ship_health = 50
    asteroid_spawn_rate = 1200
    asteroids_list.clear()


def active_game():
    global game_active, asteroids_list, red
    if game_active:
        # Spaceship
        game_active = check_asteroid_collision(asteroids_list, red_bullets, red)

        # Asteroids
        asteroids_list = move_asteroids(asteroids_list)
        draw_asteroids(asteroids_list)


def main():
    global damaged_ship_health, asteroid_spawn_rate
    asteroid = pygame.Rect(250, 20, 50, 50)

    while running:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                game_quit()

            if events.type == pygame.KEYDOWN and events.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(red.x + red.width // 2, red.y, 5, 10)
                red_bullets.append(bullet)

            if events.type == SPAWN_ASTEROID:
                asteroids_list.append(create_asteroid())
                print(asteroids_list)

            if events.type == ASTEROID_HIT:
                for asteroid in asteroids_list:
                    asteroids_list.remove(asteroid)

            if events.type == INCREASE_SHIP_HEALTH:
                damaged_ship_health += 1

            if events.type == ASTEROID_SPAWN_RATE_PLUS:
                asteroid_spawn_rate //= 2
                pygame.time.set_timer(SPAWN_ASTEROID, asteroid_spawn_rate)

            if events.type == pygame.KEYDOWN and events.key == pygame.K_SPACE and not game_active:
                game_clear()

            game_over()

        draw_stuff(red, red_bullets, red_score, damaged_ship_health)

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

WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 102, 39)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

FPS = 60
VELOCITY = 10
BULLET_VELOCITY = 7
MAX_BULLETS = 10

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 65, 50
CLOCK = pygame.time.Clock()

SCORE_FONT = pygame.font.SysFont("comic_sans", 40, True)

pygame.display.set_caption("Logang Shooter")
ICON = pygame.image.load("assets/icon.png")
pygame.display.set_icon(ICON)


# User Events
ASTEROID_HIT = pygame.USEREVENT + 1
SPAWN_ASTEROID = pygame.USEREVENT + 2
INCREASE_SHIP_HEALTH = pygame.USEREVENT + 3
ASTEROID_SPAWN_RATE_PLUS = pygame.USEREVENT + 4


# Game Variables
running = True
game_active = True
red_bullets = []
red = pygame.Rect(288, 900, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
red_score = 0

asteroid_spawn_rate = 1200

damaged_ship_health = 50

asteroids_list = []
asteroid_location = multiples(12, 563, 50)

# User Event Timers
pygame.time.set_timer(SPAWN_ASTEROID, asteroid_spawn_rate)
pygame.time.set_timer(INCREASE_SHIP_HEALTH, 2500)
pygame.time.set_timer(ASTEROID_SPAWN_RATE_PLUS, 15000)


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
