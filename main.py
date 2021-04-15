import pygame
import sys
import random
import math


def multiples(num1, num2, mult):  # Creates a numbered list with a custom range and multiple jump
    listz = [*range(num1, num2)]
    newlist = listz[::mult]
    return newlist


def rotate_asteroid():  # TODO fix this function lolol
    new_asteroid = pygame.transform.rotate(ASTEROID_SURFACE, VELOCITY * 2.5)
    return new_asteroid


def create_asteroid():  # Creates an asteroid in a random position and places it in the asteroid list
    random_asteroid_pos = random.choice(asteroid_location)
    top_asteroid = ASTEROID_SURFACE.get_rect(midbottom=(random_asteroid_pos, 10))
    return top_asteroid


def move_asteroids(asteroids):  # Moves the asteroids down the screen
    for asteroid in asteroids:
        asteroid.centery += 5
    return asteroids


def draw_asteroids(asteroids):  # Draws the asteroids onto the game screen
    for asteroid in asteroids:
        DUMMY_WINDOW.blit(ASTEROID_SURFACE, asteroid)


def check_asteroid_collision(asteroids, bullets, spaceship):  # Handles the asteroid collision physics
    global red_score, damaged_ship_health
    for asteroid in asteroids:
        if spaceship.colliderect(asteroid):
            pygame.mixer.Channel(1).play(DEATH_SOUND)
            return False
        for bullet in bullets:
            if bullet.colliderect(asteroid):
                red_score += 1
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                pygame.mixer.Channel(2).play(LASER_HIT)
        if asteroid.top > BORDER.bottom:
            pygame.mixer.Channel(3).play(SHIP_DAMAGE)
            damaged_ship_health -= 2
            asteroids.remove(asteroid)
    return True


def handle_bullets(red_bullet, asteroid):  # Handles the bullet collision physics and ammunition count
    for bullet in red_bullet:
        bullet.y -= BULLET_VELOCITY
        if asteroid.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ASTEROID_HIT))
        elif bullet.y < 0:
            red_bullet.remove(bullet)


def red_handle_movement(keys_press, redship):  # Moves the spaceship according to user input
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


def game_quit():  # Quits the game when prompted
    pygame.quit()
    sys.exit()


def instructions_screen_1():  # Displays instructions to game screen
    instruction_state = True
    while instruction_state:
        DUMMY_WINDOW.fill(WHITE)
        for events in pygame.event.get():
            if events.type == pygame.KEYDOWN:
                instruction_state = False
            if events.type == pygame.QUIT:
                game_quit()
        DUMMY_WINDOW.blit(INTRO_1, (0, 0))
        scale_window()


def instructions_screen_2():  # Displays instructions to game screen
    instruction_state = True
    while instruction_state:
        DUMMY_WINDOW.fill(WHITE)
        for events in pygame.event.get():
            if events.type == pygame.KEYDOWN:
                instruction_state = False
            if events.type == pygame.QUIT:
                game_quit()
        DUMMY_WINDOW.blit(INTRO_2, (0, 0))
        scale_window()


def instructions_screen_3():  # Displays instructions to game screen
    instruction_state = True
    while instruction_state:
        DUMMY_WINDOW.fill(WHITE)
        for events in pygame.event.get():
            if events.type == pygame.KEYDOWN:
                instruction_state = False
            if events.type == pygame.QUIT:
                game_quit()
        DUMMY_WINDOW.blit(INTRO_3, (0, 0))
        scale_window()


def start_screen():
    global running
    while not running:
        DUMMY_WINDOW.fill(WHITE)
        for events in pygame.event.get():
            if events.type == pygame.KEYDOWN and events.key == pygame.K_SPACE:
                running = True
            if events.type == pygame.QUIT:
                game_quit()
        draw_stuff(red, red_bullets, red_score, damaged_ship_health)
        DUMMY_WINDOW.blit(SPACEBAR_INSTRUCTIONS, SPACEBAR_INSTRUCTIONS_RECT)
        scale_window()


def draw_stuff(redship, red_bullet, redscore, ship_health):  # Draws the relevant assets onscreen
    global MAX_BULLETS, asteroid_spawn_rate
    DUMMY_WINDOW.blit(BACKGROUND_SURFACE, (0, 0))

    red_score_text = SCORE_FONT.render(f"Score: {redscore}", True, WHITE)
    DUMMY_WINDOW.blit(red_score_text, (420, 970))

    def ship_health_colour(colour_choice, health):
        if colour_choice == "Green":
            ship_health_text = SCORE_FONT.render(f"Ship Health: {health}%", True, GREEN)
        elif colour_choice == "Yellow":
            ship_health_text = SCORE_FONT.render(f"Ship Health: {health}%", True, YELLOW)
        elif colour_choice == "Orange":
            ship_health_text = SCORE_FONT.render(f"Ship Health: {health}%", True, ORANGE)
        elif colour_choice == "Red":
            ship_health_text = SCORE_FONT.render(f"Ship Health: {health}%", True, RED)
        return ship_health_text

    if ship_health >= 90:
        DUMMY_WINDOW.blit(ship_health_colour("Green", ship_health), (10, 970))
    elif 89 >= ship_health >= 60:
        DUMMY_WINDOW.blit(ship_health_colour("Yellow", ship_health), (10, 970))
    elif 59 >= ship_health >= 30:
        DUMMY_WINDOW.blit(ship_health_colour("Orange", ship_health), (10, 970))
    else:
        DUMMY_WINDOW.blit(ship_health_colour("Red", ship_health), (10, 970))

    max_bullet_text = SCORE_FONT.render(f"Bullets = {len(red_bullets)}/{MAX_BULLETS}", True, WHITE)
    DUMMY_WINDOW.blit(max_bullet_text, (0, 0))
    
    current_spawn_rate_text = SCORE_FONT.render(
        f"Current Rate: every {asteroid_spawn_rate / 1000} seconds", True, WHITE)
    DUMMY_WINDOW.blit(current_spawn_rate_text, (40, 250))

    DUMMY_WINDOW.blit(RED_SPACESHIP, (redship.x, redship.y))
    DUMMY_WINDOW.blit(LOGO, (60, 25))

    for bullet in red_bullet:
        pygame.draw.rect(DUMMY_WINDOW, WHITE, bullet)
        # DUMMY_WINDOW.blit(LASER_BLAST, RED_SPACESHIP.get_rect().top, bullet)

    pygame.display.update()


def spawn_asteroid(rate):  # Custom User Event that spawns in asteroids at a set rate
    pygame.time.set_timer(SPAWN_ASTEROID, rate)
    return rate


def score_display():  # Writes out high score to the game window
    hi_score_surface = SCORE_FONT.render(f"High Score: {int(high_score)}", True, WHITE)
    hi_score_rect = hi_score_surface.get_rect(center=(288, 960))
    DUMMY_WINDOW.blit(hi_score_surface, hi_score_rect)

    score_surface = SCORE_FONT.render(f"Current Score: {int(red_score)}", True, WHITE)
    score_rect = score_surface.get_rect(center=(288, 920))
    DUMMY_WINDOW.blit(score_surface, score_rect)


def update_score(score, hi_score):  # Handles the logic of updating the high score
    if score > hi_score:
        hi_score = score
    return hi_score


def you_win():  # Displays the victory screen
    global game_active, high_score
    if damaged_ship_health >= 100:
        game_active = False
        DUMMY_WINDOW.blit(BACKGROUND_SURFACE, (0, 0))
        DUMMY_WINDOW.blit(LOGO, (60, 25))
        DUMMY_WINDOW.blit(YOU_WIN_SURFACE, (6, 392))
        DUMMY_WINDOW.blit(SPACEBAR_AGAIN_INSTRUCTIONS, (6, 712))

        high_score = update_score(red_score, high_score)
        score_display()


def scale_window():  # Scales the game window and assets to fit the user's monitor dimensions
    frame = pygame.transform.scale(DUMMY_WINDOW, SCREEN_DIMENSIONS)
    WINDOW.blit(frame, frame.get_rect())
    pygame.display.flip()


def game_over():  # Displays the game over screen
    global red, high_score
    if not game_active:
        DUMMY_WINDOW.blit(BACKGROUND_SURFACE, (0, 0))
        DUMMY_WINDOW.blit(LOGO, (60, 25))
        DUMMY_WINDOW.blit(YOU_LOSE_SURFACE, (6, 292))
        DUMMY_WINDOW.blit(SPACEBAR_AGAIN_INSTRUCTIONS, (6, 712))

        high_score = update_score(red_score, high_score)
        score_display()

        red.center = (288, 900)


def ship_death(health):  # Causes the game session to end once the ship health reaches 0%
    global game_active
    if health <= 0:
        game_active = False
        game_over()


def game_clear():  # Clears the relevant variables to start a new game session
    global game_active, red_score, damaged_ship_health, asteroid_spawn_rate, red_bullets, asteroids_list, running
    game_active = True
    red_score = 0
    damaged_ship_health = 50
    asteroid_spawn_rate = 1200
    red_bullets.clear()
    asteroids_list.clear()
    running = True


def active_game():  # Handles the relevant variables when a game is in session
    global game_active, asteroids_list, red
    if game_active:
        # Spaceship
        game_active = check_asteroid_collision(asteroids_list, red_bullets, red)

        # Asteroids
        asteroids_list = move_asteroids(asteroids_list)
        draw_asteroids(asteroids_list)


def main():  # The main game loop that handles the majority of the game logic
    global damaged_ship_health, asteroid_spawn_rate, game_active
    asteroid = ASTEROID_RECT

    while running:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                game_quit()

            if events.type == pygame.KEYDOWN and events.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(red.x + red.width // 2, red.y, 5, 10)
                red_bullets.append(bullet)
                LASER_SOUND.play()

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
                spawn_asteroid(asteroid_spawn_rate)

            if events.type == pygame.KEYDOWN and events.key == pygame.K_SPACE and not game_active:
                game_clear()

        draw_stuff(red, red_bullets, red_score, damaged_ship_health)

        ship_death(damaged_ship_health)

        game_over()

        active_game()

        you_win()

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

# Colours
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

# User Events
ASTEROID_HIT = pygame.USEREVENT + 1
SPAWN_ASTEROID = pygame.USEREVENT + 2
INCREASE_SHIP_HEALTH = pygame.USEREVENT + 3
ASTEROID_SPAWN_RATE_PLUS = pygame.USEREVENT + 4

# Game Variables
running = False
game_active = True
red_bullets = []
red = pygame.Rect(288, 900, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
red_score = 0
high_score = 0

asteroid_spawn_rate = 1200
increased_spawn_rate = 15000

damaged_ship_health = 50

asteroids_list = []
asteroid_location = multiples(12, 563, 50)

# User Event Timers
spawn_asteroid(asteroid_spawn_rate)
pygame.time.set_timer(INCREASE_SHIP_HEALTH, 2500)
pygame.time.set_timer(ASTEROID_SPAWN_RATE_PLUS, increased_spawn_rate)

# Asset Files
BACKGROUND_SURFACE = pygame.transform.scale((pygame.image.load("assets/space.png")), (576, 1024))
RED_SPACESHIP_IMAGE = pygame.image.load("assets/spaceship_red.png").convert_alpha()
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180
)
RED_SPACESHIP_RECT = RED_SPACESHIP.get_rect(center=(288, 900))

ASTEROID_SURFACE = pygame.transform.scale((pygame.image.load("assets/asteroid.png")).convert_alpha(), (50, 50))
ASTEROID_RECT = ASTEROID_SURFACE.get_rect()

LASER_BLAST = pygame.transform.scale((pygame.image.load("assets/laser_blast.png")).convert_alpha(), (50, 50))
LASER_BLAST_RECT = LASER_BLAST.get_rect()

# Audio files
LASER_SOUND = pygame.mixer.Sound("assets/Gun+Silencer.mp3")
pygame.mixer.Sound.set_volume(LASER_SOUND, 0.2)
LASER_HIT = pygame.mixer.Sound("assets/Grenade+1.mp3")
pygame.mixer.Sound.set_volume(LASER_HIT, 0.3)

SHIP_DAMAGE = pygame.mixer.Sound("assets/ship_damage.wav")
pygame.mixer.Sound.set_volume(SHIP_DAMAGE, 0.3)
DEATH_SOUND = pygame.mixer.Sound("assets/dead.wav")
pygame.mixer.Sound.set_volume(DEATH_SOUND, 0.3)

GAME_MUSIC = pygame.mixer.Sound("assets/bgm.wav")
pygame.mixer.Sound.set_volume(GAME_MUSIC, 0.1)
GAME_MUSIC.play(-1)

LOGO = pygame.image.load("assets/logo.png")
YOU_WIN_SURFACE = pygame.image.load("assets/you_win.png")
YOU_LOSE_SURFACE = pygame.image.load("assets/game_over.png")
SPACEBAR_AGAIN_INSTRUCTIONS = pygame.image.load("assets/press_spacebar.png")

# Instruction Files
INTRO_1 = pygame.image.load("assets/intro_1.png")
INTRO_2 = pygame.image.load("assets/intro_2.png")
INTRO_3 = pygame.image.load("assets/intro_3.png")
SPACEBAR_INSTRUCTIONS = pygame.image.load("assets/spacebar_instructions.png")
SPACEBAR_INSTRUCTIONS_RECT = SPACEBAR_INSTRUCTIONS.get_rect(center=(288, 560))

ICON = pygame.image.load("assets/icon.png")
pygame.display.set_icon(ICON)

# Start of the main game...
instructions_screen_1()

instructions_screen_2()

instructions_screen_3()

start_screen()

main()

if __name__ == '__main__':
    main()
