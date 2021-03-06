import pygame
import sys
import random
import math


def multiples(num1, num2, mult):  # Creates a numbered list with a custom range and multiple jump
    listz = [*range(num1, num2)]
    newlist = listz[::mult]
    return newlist


def angle_choice(angle_listicle):  # Randomly chooses a new starting angle from a list of values
    angle_dex = random.choice(angle_listicle)
    return angle_dex


def change_asteroid_pos(ast_rect, index):  # Changes the initial starting angle of the created asteroid
    if ast_rect.midbottom > BACKGROUND_SURFACE.get_rect().midtop:
        changed_asteroid = rotate_asteroid(ASTEROID_SURFACE, index)
        return changed_asteroid


def rotate_asteroid(surface, angles):  # Rotates the asteroid as they fly down the screen
    rotated_asteroid = pygame.transform.rotozoom(surface, angles, 1)
    return rotated_asteroid


def create_asteroid():  # Creates an asteroid in a random position and places it in the asteroid list
    random_asteroid_pos = random.choice(asteroid_location)
    top_asteroid = ASTEROID_SURFACE.get_rect(midbottom=(random_asteroid_pos, -10))
    return top_asteroid


def spawn_asteroid(rate, loop):  # Custom User Event that spawns in asteroids at a set rate
    pygame.time.set_timer(SPAWN_ASTEROID, rate, loop)
    return rate


def move_asteroids(asteroids):  # Moves the asteroids down the screen
    for asteroid in asteroids:
        asteroid.centery += 5
    return asteroids


def draw_asteroids(asteroids):  # Draws the asteroids onto the game screen
    for asteroid in asteroids:
        rotated_asteroid = rotate_asteroid(ASTEROID_SURFACE, angle)
        DUMMY_WINDOW.blit(rotated_asteroid, asteroid)


def remove_asteroid(asteroids):  # Removes the asteroids from the game screen
    for asteroid in asteroids:
        asteroids.remove(asteroid)


def check_asteroid_collision(asteroids, bullets, spaceship):  # Handles the asteroid collision physics
    global red_score, damaged_ship_health
    for asteroid in asteroids:
        if spaceship.colliderect(asteroid):
            pygame.mixer.Channel(1).play(DEATH_SOUND)
            return False
        for bullet in bullets:
            if bullet.colliderect(asteroid):
                red_score += 1
                DUMMY_WINDOW.blit(EXPLOSION_SURFACE, asteroid)
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                pygame.mixer.Channel(2).play(LASER_HIT)
        if asteroid.top > 1024:
            pygame.mixer.Channel(3).play(SHIP_DAMAGE)
            damaged_ship_health -= 2
            asteroids.remove(asteroid)
    return True


def halve_rate(rate):  # Used to halve the asteroid spawning rate
    rate //= 2
    return rate


def red_handle_movement(keys_press, redship):  # Moves the spaceship according to user input
    if game_active:
        if keys_press[pygame.K_LEFT] and redship.left - VELOCITY > 20:  # LEFT
            redship.x -= VELOCITY
        if keys_press[pygame.K_RIGHT] and redship.right - VELOCITY < 596:  # RIGHT
            redship.x += VELOCITY
        if keys_press[pygame.K_UP] and redship.top - VELOCITY > 0:  # UP
            redship.y -= VELOCITY
        if keys_press[pygame.K_DOWN] and redship.bottom + VELOCITY < 1024:  # DOWN
            redship.y += VELOCITY


def handle_bullets(red_bullet, asteroid):  # Handles the bullet collision physics and ammunition count
    for bullet in red_bullet:
        bullet.y -= BULLET_VELOCITY
        if asteroid.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ASTEROID_HIT))
        elif bullet.y < 0:
            red_bullet.remove(bullet)


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


def instructions_screen_4():  # Displays instructions to game screen
    instruction_state = True
    while instruction_state:
        DUMMY_WINDOW.fill(WHITE)
        for events in pygame.event.get():
            if events.type == pygame.KEYDOWN:
                instruction_state = False
            if events.type == pygame.QUIT:
                game_quit()
        DUMMY_WINDOW.blit(INTRO_4, (0, 0))
        scale_window()


def instructions_screen():  # Displays all the instructions to the game screen
    instructions_screen_1()

    instructions_screen_2()

    instructions_screen_3()

    instructions_screen_4()


def start_screen():  # The start screen of the game
    global running, game_active
    while not running:
        DUMMY_WINDOW.fill(WHITE)
        for events in pygame.event.get():
            if events.type == pygame.KEYDOWN and events.key == pygame.K_SPACE:
                running = True
                game_active = True
                spawn_asteroid(2000, 7)
            if events.type == pygame.QUIT:
                game_quit()
        draw_stuff(red, red_bullets, red_score, damaged_ship_health)
        DUMMY_WINDOW.blit(SPACEBAR_INSTRUCTIONS, SPACEBAR_INSTRUCTIONS_RECT)
        scale_window()


def draw_stuff(redship, red_bullet, redscore, ship_health):  # Draws the relevant assets onscreen
    # Background
    DUMMY_WINDOW.blit(BACKGROUND_SURFACE, (0, 0))

    # Current Score
    red_score_text = SCORE_FONT.render(f"Score: {redscore}", True, WHITE)
    DUMMY_WINDOW.blit(red_score_text, (420, 970))

    # Ship Health
    if ship_health >= 90:
        DUMMY_WINDOW.blit(ship_health_colour("Green", ship_health), (10, 970))
    elif 89 >= ship_health >= 60:
        DUMMY_WINDOW.blit(ship_health_colour("Yellow", ship_health), (10, 970))
    elif 59 >= ship_health >= 30:
        DUMMY_WINDOW.blit(ship_health_colour("Orange", ship_health), (10, 970))
    else:
        DUMMY_WINDOW.blit(ship_health_colour("Red", ship_health), (10, 970))

    # Bullets
    for bullet in red_bullet:
        DUMMY_WINDOW.blit(LASER_BLAST, bullet)
    max_bullet_text = SCORE_FONT.render(f"Bullets = {len(red_bullets)}/{MAX_BULLETS}", True, WHITE)
    DUMMY_WINDOW.blit(max_bullet_text, (0, 0))

    current_spawn_rate_text = SCORE_FONT.render(
        f"Current Rate: every {asteroid_spawn_rate / 1000} seconds", True, WHITE)
    DUMMY_WINDOW.blit(current_spawn_rate_text, (40, 250))

    DUMMY_WINDOW.blit(RED_SPACESHIP, (redship.x - (redship.w // 2), redship.y))
    DUMMY_WINDOW.blit(LOGO, (60, 25))

    pygame.display.update()


def ship_health_colour(colour_choice, health):  # Changes the colour of the ship's health depending on its value
    if colour_choice == "Green":
        ship_health_text = SCORE_FONT.render(f"Ship Health: {health}%", True, GREEN)
        return ship_health_text
    elif colour_choice == "Yellow":
        ship_health_text = SCORE_FONT.render(f"Ship Health: {health}%", True, YELLOW)
        return ship_health_text
    elif colour_choice == "Orange":
        ship_health_text = SCORE_FONT.render(f"Ship Health: {health}%", True, ORANGE)
        return ship_health_text
    elif colour_choice == "Red":
        ship_health_text = SCORE_FONT.render(f"Ship Health: {health}%", True, RED)
        return ship_health_text


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


def ship_regeneration_screen(regen_rate):  # Draws the relevant ship regeneration buttons onscreen
    DUMMY_WINDOW.blit(SHIP_REGENERATION_SCREEN, (0, 0))
    DUMMY_WINDOW.blit(ONE_SECOND_SURFACE, (189, 598))
    DUMMY_WINDOW.blit(TWO_SECOND_SURFACE, (160, 748))
    DUMMY_WINDOW.blit(THREE_SECOND_SURFACE, (180, 898))

    if ship_regen_1:
        regen_text = REGEN_FONT.render(f"Current Regeneration Rate: {regen_rate // 1000} seconds", True, EASY)
        regen_rect = regen_text.get_rect(center=(288, 980))
        DUMMY_WINDOW.blit(regen_text, regen_rect)
    elif ship_regen_2:
        regen_text = REGEN_FONT.render(f"Current Regeneration Rate: {regen_rate // 1000} seconds", True, YELLOW)
        regen_rect = regen_text.get_rect(center=(288, 980))
        DUMMY_WINDOW.blit(regen_text, regen_rect)
    elif ship_regen_3:
        regen_text = REGEN_FONT.render(f"Current Regeneration Rate: {regen_rate // 1000} seconds", True, HARD)
        regen_rect = regen_text.get_rect(center=(288, 980))
        DUMMY_WINDOW.blit(regen_text, regen_rect)


def regen_button_click(x, y, click):  # Handles the button clicks in the ship regeneration settings page
    global ship_regen_1, ship_regen_2, ship_regen_3, ship_regen_rate
    if ONE_SECOND_RECT.collidepoint(x, y) and click:
        ship_regen_rate = 1000
        ship_regen_1 = True
        ship_regen_2 = False
        ship_regen_3 = False

    if TWO_SECOND_RECT.collidepoint(x, y) and click:
        ship_regen_rate = 2000
        ship_regen_1 = False
        ship_regen_2 = True
        ship_regen_3 = False

    if THREE_SECOND_RECT.collidepoint(x, y) and click:
        ship_regen_rate = 3000
        ship_regen_1 = False
        ship_regen_2 = False
        ship_regen_3 = True


def ship_regeneration_settings():  # Handles the ship regeneration settings page logic
    global ship_regen_rate, ship_regen_1, ship_regen_2, ship_regen_3
    ship_regeneration_state = True
    while ship_regeneration_state:
        ship_regeneration_screen(ship_regen_rate)

        mx, my = pygame.mouse.get_pos()

        click = False

        for event in pygame.event.get():
            click = True if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 else False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                settings()
                ship_regeneration_state = False

            if event.type == pygame.QUIT:
                game_quit()

        regen_button_click(mx, my, click)

        scale_window()
        CLOCK.tick(FPS)


def ship_health_screen(ship_health):  # Draws the relevant ship health variables onto the settings page
    DUMMY_WINDOW.blit(SHIP_HEALTH_SCREEN, (0, 0))
    DUMMY_WINDOW.blit(TWENTY_FIVE_SURFACE, (170, 418))
    DUMMY_WINDOW.blit(FIFTY_SURFACE, (136, 618))
    DUMMY_WINDOW.blit(SEVENTY_FIVE_SURFACE, (172, 818))

    if ship_health_25:
        health_text = REGEN_FONT.render(f"Current Ship Health: {ship_health}%", True, HARD)
        health_rect = health_text.get_rect(center=(288, 960))
        DUMMY_WINDOW.blit(health_text, health_rect)

    elif ship_health_50:
        health_text = REGEN_FONT.render(f"Current Ship Health: {ship_health}%", True, YELLOW)
        health_rect = health_text.get_rect(center=(288, 960))
        DUMMY_WINDOW.blit(health_text, health_rect)

    elif ship_health_75:
        health_text = REGEN_FONT.render(f"Current Ship Health: {ship_health}%", True, EASY)
        health_rect = health_text.get_rect(center=(288, 960))
        DUMMY_WINDOW.blit(health_text, health_rect)


def health_button_click(x, y, click):  # Handles the button clicks in the health settings page
    global damaged_ship_health, ship_health_25, ship_health_50, ship_health_75
    if TWENTY_FIVE_RECT.collidepoint(x, y) and click:
        damaged_ship_health = 25
        ship_health_25 = True
        ship_health_50 = False
        ship_health_75 = False

    if FIFTY_RECT.collidepoint(x, y) and click:
        damaged_ship_health = 50
        ship_health_25 = False
        ship_health_50 = True
        ship_health_75 = False

    if SEVENTY_FIVE_RECT.collidepoint(x, y) and click:
        damaged_ship_health = 75
        ship_health_25 = False
        ship_health_50 = False
        ship_health_75 = True


def ship_health_settings():  # Handles the ship health settings logic
    global damaged_ship_health, ship_health_25, ship_health_50, ship_health_75
    ship_health_state = True
    while ship_health_state:
        ship_health_screen(damaged_ship_health)

        mx, my = pygame.mouse.get_pos()

        click = False

        for event in pygame.event.get():
            click = True if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 else False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                settings()
                ship_health_state = False

            if event.type == pygame.QUIT:
                game_quit()

        health_button_click(mx, my, click)

        scale_window()
        CLOCK.tick(FPS)


def settings_screen():  # Shows the options screen to the player
    DUMMY_WINDOW.blit(SETTINGS_SCREEN_SURFACE, (0, 0))
    DUMMY_WINDOW.blit(SHIP_HEALTH_BUTTON, (165, 418))
    DUMMY_WINDOW.blit(SHIP_REGENERATION_BUTTON, (96, 718))


def settings_button_click(x, y, click):  # Handles the button clicks in the settings page
    if SHIP_REGENERATION_RECT.collidepoint(x, y) and click:
        ship_regeneration_settings()

    if SHIP_HEALTH_RECT.collidepoint(x, y) and click:
        ship_health_settings()


def settings():  # Handles the settings logic in the settings page
    global settings_state
    settings_state = True
    while settings_state:
        settings_screen()

        mx, my = pygame.mouse.get_pos()

        click = False

        for event in pygame.event.get():
            click = True if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 else False
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_game()
                settings_state = False

        settings_button_click(mx, my, click)

        scale_window()
        CLOCK.tick(FPS)


def pause_game_screen():  # Draws the paused screen assets
    draw_stuff(red, red_bullets, red_score, damaged_ship_health)
    draw_asteroids(asteroids_list)
    DUMMY_WINDOW.blit(RESUME_BUTTON_SURFACE, (82, 442))
    DUMMY_WINDOW.blit(OPTIONS_BUTTON_SURFACE, (365, 10))


def pause_button_click(x, y, click):  # Handles the button clicks in the paused screen
    if OPTIONS_BUTTON_RECT.collidepoint((x, y)) and click:
        settings()


def pause_game():  # Handles the paused screen logic
    global paused, settings_state
    paused = True
    while paused:
        pause_game_screen()

        mx, my = pygame.mouse.get_pos()

        click = False

        for event in pygame.event.get():
            click = True if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 else False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or \
                    RESUME_BUTTON_RECT.collidepoint((mx, my)) and click:
                paused = False
                settings_state = False

            if event.type == pygame.QUIT:
                game_quit()

        pause_button_click(mx, my, click)

        scale_window()
        CLOCK.tick(FPS)


def game_clear():  # Clears the relevant variables to start a new game session
    global game_active, red_score, damaged_ship_health, asteroid_spawn_rate, red_bullets, asteroids_list, running, \
        ship_regen_rate
    asteroid_spawn_rate = 2000

    spawn_asteroid(2000, 7)

    if ship_health_25:
        damaged_ship_health = 25
    elif ship_health_50:
        damaged_ship_health = 50
    elif ship_health_75:
        damaged_ship_health = 75

    if ship_regen_1:
        ship_regen_rate = 1000
    elif ship_regen_2:
        ship_regen_rate = 2000
    elif ship_regen_3:
        ship_regen_rate = 3000

    red_score = 0
    red_bullets.clear()
    asteroids_list.clear()
    game_active = True
    running = True


def active_game():  # Handles the relevant variables when a game is in session
    global game_active, asteroids_list
    if game_active:
        # Spaceship
        game_active = check_asteroid_collision(asteroids_list, red_bullets, red)

        # Asteroids
        asteroids_list = move_asteroids(asteroids_list)
        draw_asteroids(asteroids_list)


def game_over():  # Displays the game over screen
    global red, high_score
    if not game_active:
        DUMMY_WINDOW.blit(BACKGROUND_SURFACE, (0, 0))
        DUMMY_WINDOW.blit(LOGO, (60, 25))
        DUMMY_WINDOW.blit(YOU_LOSE_SURFACE, (6, 292))
        DUMMY_WINDOW.blit(SPACEBAR_AGAIN_INSTRUCTIONS, (6, 670))

        high_score = update_score(red_score, high_score)
        score_display()

        red.center = (308, 900)


def ship_death(health):  # Causes the game session to end once the ship health reaches 0%
    global game_active
    if health <= 0:
        game_active = False
        game_over()


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


def running_loop():  # The main running loop that handles asteroid creation and collision among others
    global angle, asteroid_spawn_rate, damaged_ship_health
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_quit()

        if event.type == ASTEROID_HIT:
            remove_asteroid(asteroids_list)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and not game_active:
            game_clear()

        if game_active and not paused:
            angle -= 15
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(red.x - 9, red.y - 20, 17, 70)
                red_bullets.append(bullet)
                LASER_SOUND.play()

            if event.type == ASTEROID_SPAWN_RATE_PLUS:
                asteroid_spawn_rate = halve_rate(asteroid_spawn_rate)
                spawn_asteroid(asteroid_spawn_rate, 0)

            if event.type == SPAWN_ASTEROID:
                asteroids_list.append(create_asteroid())

            if event.type == INCREASE_SHIP_HEALTH:
                damaged_ship_health += 1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_game()


def main():  # The main game loop that handles the majority of the game logic
    global damaged_ship_health, asteroid_spawn_rate, angle
    asteroid = ASTEROID_RECT

    while running:
        running_loop()

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


def game_quit():  # Quits the game when prompted
    pygame.quit()
    sys.exit()


def scale_window():  # Scales the game window and assets to fit the user's monitor dimensions
    frame = pygame.transform.scale(DUMMY_WINDOW, SCREEN_DIMENSIONS)
    WINDOW.blit(frame, frame.get_rect())
    pygame.display.flip()


# Constants
pygame.init()
MONITOR = pygame.display.Info()
SCREEN_DIMENSIONS = (math.floor(MONITOR.current_w * 0.3), math.ceil(MONITOR.current_h * 0.948))
WINDOW = pygame.display.set_mode(SCREEN_DIMENSIONS)
DUMMY_WINDOW = pygame.Surface((576, 1024))
WIDTH, HEIGHT = SCREEN_DIMENSIONS
WINDOW_WIDTH = WINDOW.get_width()
WINDOW_HEIGHT = WINDOW.get_height()

# Colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 102, 39)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
EASY, MEDIUM, HARD = (98, 255, 183), (97, 174, 255), (255, 116, 123)

# Miscellaneous
FPS = 60
VELOCITY = 10
BULLET_VELOCITY = 7
MAX_BULLETS = 10

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 65, 50
CLOCK = pygame.time.Clock()

SCORE_FONT = pygame.font.SysFont("comic_sans", 40, True)
REGEN_FONT = pygame.font.SysFont("Impact", 30)

pygame.display.set_caption("Logang Shooter")
asteroid_spawn_rate = 2000
increased_spawn_rate = 15000
ship_regen_rate = 2000

# User Events
ASTEROID_HIT = pygame.USEREVENT + 1
SPAWN_ASTEROID = pygame.USEREVENT + 2
INCREASE_SHIP_HEALTH = pygame.USEREVENT + 3
ASTEROID_SPAWN_RATE_PLUS = pygame.USEREVENT + 4

# User Event Timers
pygame.time.set_timer(INCREASE_SHIP_HEALTH, ship_regen_rate)
pygame.time.set_timer(ASTEROID_SPAWN_RATE_PLUS, increased_spawn_rate)

# Asset Files
BACKGROUND_SURFACE = pygame.transform.scale((pygame.image.load("assets/space.png")), (576, 1024))
RED_SPACESHIP_IMAGE = pygame.transform.scale((pygame.image.load("assets/spaceship.png").convert_alpha()), (500, 413))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180
)
RED_SPACESHIP_RECT = RED_SPACESHIP.get_rect(center=(288, 900))

ASTEROID_SURFACE = pygame.transform.scale((pygame.image.load("assets/asteroid.png")).convert_alpha(), (50, 50))
ASTEROID_RECT = ASTEROID_SURFACE.get_rect()

LASER_BLAST = pygame.image.load("assets/laser_blast.png").convert_alpha()
LASER_BLAST_RECT = LASER_BLAST.get_rect()

EXPLOSION_SURFACE = pygame.image.load("assets/boom.png").convert_alpha()

LOGO = pygame.image.load("assets/logo.png")
YOU_WIN_SURFACE = pygame.image.load("assets/you_win.png")
YOU_LOSE_SURFACE = pygame.image.load("assets/game_over.png")
SPACEBAR_AGAIN_INSTRUCTIONS = pygame.image.load("assets/press_spacebar.png")

# Buttons
RESUME_BUTTON_SURFACE = pygame.image.load("assets/resume_button.png")
RESUME_BUTTON_RECT = RESUME_BUTTON_SURFACE.get_rect(center=WINDOW.get_rect().center)

RESUME_HOVER_SURFACE = pygame.image.load("assets/resume_hover.png")
RESUME_HOVER_RECT = RESUME_HOVER_SURFACE.get_rect(center=(288, 512))

OPTIONS_BUTTON_SURFACE = pygame.image.load("assets/button_options.png")
OPTIONS_BUTTON_RECT = OPTIONS_BUTTON_SURFACE.get_rect(
    topright=WINDOW.get_rect().topright)

SHIP_HEALTH_BUTTON = pygame.image.load("assets/button_ship-health.png")
SHIP_HEALTH_RECT = SHIP_HEALTH_BUTTON.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.44))

SHIP_REGENERATION_BUTTON = pygame.image.load("assets/button_ship-regeneration.png")
SHIP_REGENERATION_RECT = SHIP_REGENERATION_BUTTON.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.73))

ONE_SECOND_SURFACE = pygame.image.load("assets/button_1s.png")
ONE_SECOND_RECT = ONE_SECOND_SURFACE.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.605))

TWO_SECOND_SURFACE = pygame.image.load("assets/button_2s.png")
TWO_SECOND_RECT = TWO_SECOND_SURFACE.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.75))

THREE_SECOND_SURFACE = pygame.image.load("assets/button_3s.png")
THREE_SECOND_RECT = THREE_SECOND_SURFACE.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.9))

TWENTY_FIVE_SURFACE = pygame.image.load("assets/button_25.png")
TWENTY_FIVE_RECT = TWENTY_FIVE_SURFACE.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.44))

FIFTY_SURFACE = pygame.image.load("assets/button_50.png")
FIFTY_RECT = FIFTY_SURFACE.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.63))

SEVENTY_FIVE_SURFACE = pygame.image.load("assets/button_75.png")
SEVENTY_FIVE_RECT = SEVENTY_FIVE_SURFACE.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.83))

# Backgrounds
SETTINGS_SCREEN_SURFACE = pygame.image.load("assets/settings_screen.png")
SHIP_HEALTH_SCREEN = pygame.image.load("assets/ship_health_screen.png")
SHIP_REGENERATION_SCREEN = pygame.image.load("assets/ship_regeneration_screen.png")

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

# Instruction Files
INTRO_1 = pygame.image.load("assets/intro_1.png")
INTRO_2 = pygame.image.load("assets/intro_2.png")
INTRO_3 = pygame.image.load("assets/intro_3.png")
INTRO_4 = pygame.image.load("assets/intro_4.png")
SPACEBAR_INSTRUCTIONS = pygame.image.load("assets/spacebar_instructions.png")
SPACEBAR_INSTRUCTIONS_RECT = SPACEBAR_INSTRUCTIONS.get_rect(center=(288, 560))

ICON = pygame.image.load("assets/icon.png")
pygame.display.set_icon(ICON)

# Game Variables
running = False
game_active = False
paused = False
settings_state = False
red_bullets = []
red = pygame.Rect(288, 900, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
red_score = 0
high_score = 0
angle = 0
angle_list = multiples(0, 360, 20)
angle_index = angle_choice(angle_list)

damaged_ship_health = 50

asteroids_list = []
asteroid_location = multiples(12, 563, 50)

ship_regen_1 = False
ship_regen_2 = True
ship_regen_3 = False

ship_health_25 = False
ship_health_50 = True
ship_health_75 = False


# Start of the main game...
instructions_screen()

start_screen()

main()

if __name__ == '__main__':
    main()
