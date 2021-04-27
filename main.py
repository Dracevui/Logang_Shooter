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


def update_score(score, hi_score):  # Handles the logic of updating the high score
    if score > hi_score:
        hi_score = score
    return hi_score


def game_quit():  # Quits the game when prompted
    pygame.quit()
    sys.exit()


class Asteroid:
    def __init__(self):
        # Class Imports
        self.game = game
        self.spaceship = spaceship

        # Variables
        self.asteroid_spawn_rate = 2000
        self.increased_spawn_rate = 15000
        self.asteroids_list = []
        self.asteroid_location = multiples(12, 563, 50)

        # User Events
        self.ASTEROID_HIT = pygame.USEREVENT + 1
        self.SPAWN_ASTEROID = pygame.USEREVENT + 2
        self.ASTEROID_SPAWN_RATE_PLUS = pygame.USEREVENT + 4

        # User Event Timers
        pygame.time.set_timer(self.ASTEROID_SPAWN_RATE_PLUS, self.increased_spawn_rate)

        # Asset Files
        self.ASTEROID_SURFACE = pygame.transform.scale(
            (pygame.image.load("assets/asteroid.png")).convert_alpha(), (50, 50))
        self.ASTEROID_RECT = self.ASTEROID_SURFACE.get_rect()

    @staticmethod
    def move_asteroids(asteroids):  # Moves the asteroids down the screen
        for asteroid in asteroids:
            asteroid.centery += 5
        return asteroids

    @staticmethod
    def remove_asteroid(asteroids):  # Removes the asteroids from the game screen
        for asteroid in asteroids:
            asteroids.remove(asteroid)

    @staticmethod
    def rotate_asteroid(surface, angles):  # Rotates the asteroid as they fly down the screen
        rotated_asteroid = pygame.transform.rotozoom(surface, angles, 1)
        return rotated_asteroid

    @staticmethod
    def halve_rate(rate):  # Used to halve the asteroid spawning rate
        rate //= 2
        return rate

    def change_asteroid_pos(self, ast_rect, index):  # Changes the initial starting angle of the created asteroid
        if ast_rect.midbottom > self.game.BACKGROUND_SURFACE.get_rect().midtop:
            changed_asteroid = self.rotate_asteroid(self.ASTEROID_SURFACE, index)
            return changed_asteroid

    def create_asteroid(self):  # Creates an asteroid in a random position and places it in the asteroid list
        random_asteroid_pos = random.choice(self.asteroid_location)
        top_asteroid = self.ASTEROID_SURFACE.get_rect(midbottom=(random_asteroid_pos, -10))
        return top_asteroid

    def spawn_asteroids(self, rate, loop):  # Custom User Event that spawns in asteroids at a set rate
        pygame.time.set_timer(self.SPAWN_ASTEROID, rate, loop)
        return rate

    def draw_asteroids(self, asteroids):  # Draws the asteroids onto the game screen
        for asteroid in asteroids:
            rotated_asteroid = self.rotate_asteroid(self.ASTEROID_SURFACE, self.game.angle)
            self.game.DUMMY_WINDOW.blit(rotated_asteroid, asteroid)

    def check_asteroid_collision(self, asteroids, bullets, spaceship):  # Handles the asteroid collision physics
        for asteroid in asteroids:
            if spaceship.colliderect(asteroid):
                pygame.mixer.Channel(1).play(self.game.DEATH_SOUND)
                return False
            for bullet in bullets:
                if bullet.colliderect(asteroid):
                    self.game.red_score += 1
                    self.game.DUMMY_WINDOW.blit(self.game.EXPLOSION_SURFACE, asteroid)
                    asteroids.remove(asteroid)
                    bullets.remove(bullet)
                    pygame.mixer.Channel(2).play(self.game.LASER_HIT)
            if asteroid.top > 1024:
                pygame.mixer.Channel(3).play(self.game.SHIP_DAMAGE)
                self.spaceship.damaged_ship_health -= 2
                asteroids.remove(asteroid)
        return True


class Spaceship:
    def __init__(self):
        # Class Imports
        self.game = game
        self.asteroid = asteroid

        # Constants
        self.VELOCITY = 10
        self.BULLET_VELOCITY = 7
        self.MAX_BULLETS = 10
        self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT = 65, 50

        # Variables
        self.ship_regen_rate = 2000
        self.red_bullets = []
        self.red = pygame.Rect(288, 900, self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)
        self.damaged_ship_health = 50

        # Ship Booleans
        self.ship_regen_1 = False
        self.ship_regen_2 = True
        self.ship_regen_3 = False

        self.ship_health_25 = False
        self.ship_health_50 = True
        self.ship_health_75 = False

        # User Events
        self.INCREASE_SHIP_HEALTH = pygame.USEREVENT + 3

        # Event Timers
        pygame.time.set_timer(self.INCREASE_SHIP_HEALTH, self.ship_regen_rate)

        # Asset Files
        self.RED_SPACESHIP_IMAGE = pygame.transform.scale(
            (pygame.image.load("assets/spaceship.png").convert_alpha()), (500, 413))
        self.RED_SPACESHIP = pygame.transform.rotate(
            pygame.transform.scale(self.RED_SPACESHIP_IMAGE, (self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)), 180
        )
        self.RED_SPACESHIP_RECT = self.RED_SPACESHIP.get_rect(center=(288, 900))

        self.LASER_BLAST = pygame.image.load("assets/laser_blast.png").convert_alpha()
        self.LASER_BLAST_RECT = self.LASER_BLAST.get_rect()

    def ship_death(self, health):  # Causes the game session to end once the ship health reaches 0%
        if health <= 0:
            self.game.game_active = False
            self.game.game_over()

    def ship_health_colour(
            self, colour_choice, health):  # Changes the colour of the ship's health depending on its value
        if colour_choice == "Green":
            ship_health_text = self.game.SCORE_FONT.render(f"Ship Health: {health}%", True, self.game.GREEN)
            return ship_health_text
        elif colour_choice == "Yellow":
            ship_health_text = self.game.SCORE_FONT.render(f"Ship Health: {health}%", True, self.game.YELLOW)
            return ship_health_text
        elif colour_choice == "Orange":
            ship_health_text = self.game.SCORE_FONT.render(f"Ship Health: {health}%", True, self.game.ORANGE)
            return ship_health_text
        elif colour_choice == "Red":
            ship_health_text = self.game.SCORE_FONT.render(f"Ship Health: {health}%", True, self.game.RED)
            return ship_health_text

    def red_handle_movement(self, keys_press, redship):  # Moves the spaceship according to user input
        if self.game.game_active:
            if keys_press[pygame.K_LEFT] and redship.left - self.VELOCITY > 20:  # LEFT
                redship.x -= self.VELOCITY
            if keys_press[pygame.K_RIGHT] and redship.right - self.VELOCITY < 596:  # RIGHT
                redship.x += self.VELOCITY
            if keys_press[pygame.K_UP] and redship.top - self.VELOCITY > 0:  # UP
                redship.y -= self.VELOCITY
            if keys_press[pygame.K_DOWN] and redship.bottom + self.VELOCITY < 1024:  # DOWN
                redship.y += self.VELOCITY

    def handle_bullets(self, red_bullet, asteroid):  # Handles the bullet collision physics and ammunition count
        for bullet in red_bullet:
            bullet.y -= self.BULLET_VELOCITY
            if asteroid.colliderect(bullet):
                pygame.event.post(pygame.event.Event(self.asteroid.ASTEROID_HIT))
            elif bullet.y < 0:
                red_bullet.remove(bullet)


class Settings:
    def __init__(self):
        # Class Imports
        self.game = game
        self.spaceship = spaceship
        self.asteroid = asteroid

        # Variables
        self.paused = False
        self.settings_state = False

        # Backgrounds
        self.SETTINGS_SCREEN_SURFACE = pygame.image.load("assets/settings_screen.png")
        self.SHIP_HEALTH_SURFACE = pygame.image.load("assets/ship_health_screen.png")
        self.SHIP_REGENERATION_SURFACE = pygame.image.load("assets/ship_regeneration_screen.png")

        # Asset Files: Buttons
        self.RESUME_BUTTON_SURFACE = pygame.image.load("assets/resume_button.png")
        self.RESUME_BUTTON_RECT = self.RESUME_BUTTON_SURFACE.get_rect(center=self.game.WINDOW.get_rect().center)

        self.RESUME_HOVER_SURFACE = pygame.image.load("assets/resume_hover.png")
        self.RESUME_HOVER_RECT = self.RESUME_HOVER_SURFACE.get_rect(center=(288, 512))

        self.OPTIONS_BUTTON_SURFACE = pygame.image.load("assets/button_options.png")
        self.OPTIONS_BUTTON_RECT = self.OPTIONS_BUTTON_SURFACE.get_rect(
            topright=self.game.WINDOW.get_rect().topright)

        self.SHIP_HEALTH_BUTTON = pygame.image.load("assets/button_ship-health.png")
        self.SHIP_HEALTH_RECT = self.SHIP_HEALTH_BUTTON.get_rect(
            center=(self.game.WINDOW_WIDTH // 2, self.game.WINDOW_HEIGHT * 0.44))

        self.SHIP_REGENERATION_BUTTON = pygame.image.load("assets/button_ship-regeneration.png")
        self.SHIP_REGENERATION_RECT = self.SHIP_REGENERATION_BUTTON.get_rect(
            center=(self.game.WINDOW_WIDTH // 2, self.game.WINDOW_HEIGHT * 0.73))

        self.ONE_SECOND_SURFACE = pygame.image.load("assets/button_1s.png")
        self.ONE_SECOND_RECT = self.ONE_SECOND_SURFACE.get_rect(
            center=(self.game.WINDOW_WIDTH // 2, self.game.WINDOW_HEIGHT * 0.605))

        self.TWO_SECOND_SURFACE = pygame.image.load("assets/button_2s.png")
        self.TWO_SECOND_RECT = self.TWO_SECOND_SURFACE.get_rect(
            center=(self.game.WINDOW_WIDTH // 2, self.game.WINDOW_HEIGHT * 0.75))

        self.THREE_SECOND_SURFACE = pygame.image.load("assets/button_3s.png")
        self.THREE_SECOND_RECT = self.THREE_SECOND_SURFACE.get_rect(
            center=(self.game.WINDOW_WIDTH // 2, self.game.WINDOW_HEIGHT * 0.9))

        self.TWENTY_FIVE_SURFACE = pygame.image.load("assets/button_25.png")
        self.TWENTY_FIVE_RECT = self.TWENTY_FIVE_SURFACE.get_rect(center=(
            self.game.WINDOW_WIDTH // 2, self.game.WINDOW_HEIGHT * 0.44))

        self.FIFTY_SURFACE = pygame.image.load("assets/button_50.png")
        self.FIFTY_RECT = self.FIFTY_SURFACE.get_rect(
            center=(self.game.WINDOW_WIDTH // 2, self.game.WINDOW_HEIGHT * 0.63))

        self.SEVENTY_FIVE_SURFACE = pygame.image.load("assets/button_75.png")
        self.SEVENTY_FIVE_RECT = self.SEVENTY_FIVE_SURFACE.get_rect(
            center=(self.game.WINDOW_WIDTH // 2, self.game.WINDOW_HEIGHT * 0.83))

    def pause_game(self):  # Handles the paused screen logic
        paused = True
        while paused:
            self.pause_game_screen()

            mx, my = pygame.mouse.get_pos()

            click = False

            for event in pygame.event.get():
                click = True if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 else False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or \
                        self.RESUME_BUTTON_RECT.collidepoint((mx, my)) and click:
                    paused = False
                    self.settings_state = False

                if event.type == pygame.QUIT:
                    game_quit()

            self.pause_button_click(mx, my, click)

            self.game.scale_window()
            self.game.CLOCK.tick(self.game.FPS)

    def ship_regeneration_screen(self, regen_rate):  # Draws the relevant ship regeneration buttons onscreen
        self.game.DUMMY_WINDOW.blit(self.SHIP_REGENERATION_SURFACE, (0, 0))
        self.game.DUMMY_WINDOW.blit(self.ONE_SECOND_SURFACE, (189, 598))
        self.game.DUMMY_WINDOW.blit(self.TWO_SECOND_SURFACE, (160, 748))
        self.game.DUMMY_WINDOW.blit(self.THREE_SECOND_SURFACE, (180, 898))

        if self.spaceship.ship_regen_1:
            regen_text = self.game.REGEN_FONT.render(
                f"Current Regeneration Rate: {regen_rate // 1000} seconds", True, self.game.EASY)
            regen_rect = regen_text.get_rect(center=(288, 980))
            self.game.DUMMY_WINDOW.blit(regen_text, regen_rect)
        elif self.spaceship.ship_regen_2:
            regen_text = self.game.REGEN_FONT.render(
                f"Current Regeneration Rate: {regen_rate // 1000} seconds", True, self.game.YELLOW)
            regen_rect = regen_text.get_rect(center=(288, 980))
            self.game.DUMMY_WINDOW.blit(regen_text, regen_rect)
        elif self.spaceship.ship_regen_3:
            regen_text = self.game.REGEN_FONT.render(
                f"Current Regeneration Rate: {regen_rate // 1000} seconds", True, self.game.HARD)
            regen_rect = regen_text.get_rect(center=(288, 980))
            self.game.DUMMY_WINDOW.blit(regen_text, regen_rect)

    def regen_button_click(self, x, y, click):  # Handles the button clicks in the ship regeneration settings page
        if self.ONE_SECOND_RECT.collidepoint(x, y) and click:
            self.spaceship.ship_regen_rate = 1000
            self.spaceship.ship_regen_1 = True
            self.spaceship.ship_regen_2 = False
            self.spaceship.ship_regen_3 = False

        if self.TWO_SECOND_RECT.collidepoint(x, y) and click:
            self.spaceship.ship_regen_rate = 2000
            self.spaceship.ship_regen_1 = False
            self.spaceship.ship_regen_2 = True
            self.spaceship.ship_regen_3 = False

        if self.THREE_SECOND_RECT.collidepoint(x, y) and click:
            self.spaceship.ship_regen_rate = 3000
            self.spaceship.ship_regen_1 = False
            self.spaceship.ship_regen_2 = False
            self.spaceship.ship_regen_3 = True

    def ship_regeneration_settings(self):  # Handles the ship regeneration settings page logic
        ship_regeneration_state = True
        while ship_regeneration_state:
            self.ship_regeneration_screen(self.spaceship.ship_regen_rate)

            mx, my = pygame.mouse.get_pos()

            click = False

            for event in pygame.event.get():
                click = True if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 else False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.settings_logic()
                    ship_regeneration_state = False

                if event.type == pygame.QUIT:
                    game_quit()

            self.regen_button_click(mx, my, click)

            self.game.scale_window()
            self.game.CLOCK.tick(self.game.FPS)

    def ship_health_screen(self, ship_health):  # Draws the relevant ship health variables onto the settings page
        self.game.DUMMY_WINDOW.blit(self.SHIP_HEALTH_SURFACE, (0, 0))
        self.game.DUMMY_WINDOW.blit(self.TWENTY_FIVE_SURFACE, (170, 418))
        self.game.DUMMY_WINDOW.blit(self.FIFTY_SURFACE, (136, 618))
        self.game.DUMMY_WINDOW.blit(self.SEVENTY_FIVE_SURFACE, (172, 818))

        if self.spaceship.ship_health_25:
            health_text = self.game.REGEN_FONT.render(f"Current Ship Health: {ship_health}%", True, self.game.HARD)
            health_rect = health_text.get_rect(center=(288, 960))
            self.game.DUMMY_WINDOW.blit(health_text, health_rect)

        elif self.spaceship.ship_health_50:
            health_text = self.game.REGEN_FONT.render(f"Current Ship Health: {ship_health}%", True, self.game.YELLOW)
            health_rect = health_text.get_rect(center=(288, 960))
            self.game.DUMMY_WINDOW.blit(health_text, health_rect)

        elif self.spaceship.ship_health_75:
            health_text = self.game.REGEN_FONT.render(f"Current Ship Health: {ship_health}%", True, self.game.EASY)
            health_rect = health_text.get_rect(center=(288, 960))
            self.game.DUMMY_WINDOW.blit(health_text, health_rect)

    def health_button_click(self, x, y, click):  # Handles the button clicks in the health settings page
        if self.TWENTY_FIVE_RECT.collidepoint(x, y) and click:
            self.spaceship.damaged_ship_health = 25
            self.spaceship.ship_health_25 = True
            self.spaceship.ship_health_50 = False
            self.spaceship.ship_health_75 = False

        if self.FIFTY_RECT.collidepoint(x, y) and click:
            self.spaceship.damaged_ship_health = 50
            self.spaceship.ship_health_25 = False
            self.spaceship.ship_health_50 = True
            self.spaceship.ship_health_75 = False

        if self.SEVENTY_FIVE_RECT.collidepoint(x, y) and click:
            self.spaceship.damaged_ship_health = 75
            self.spaceship.ship_health_25 = False
            self.spaceship.ship_health_50 = False
            self.spaceship.ship_health_75 = True

    def ship_health_settings(self):  # Handles the ship health settings logic
        ship_health_state = True
        while ship_health_state:
            self.ship_health_screen(self.spaceship.damaged_ship_health)

            mx, my = pygame.mouse.get_pos()

            click = False

            for event in pygame.event.get():
                click = True if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 else False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.settings_logic()
                    ship_health_state = False

                if event.type == pygame.QUIT:
                    game_quit()

            self.health_button_click(mx, my, click)

            self.game.scale_window()
            self.game.CLOCK.tick(self.game.FPS)

    def settings_screen(self):  # Shows the options screen to the player
        self.game.DUMMY_WINDOW.blit(self.SETTINGS_SCREEN_SURFACE, (0, 0))
        self.game.DUMMY_WINDOW.blit(self.SHIP_HEALTH_BUTTON, (165, 418))
        self.game.DUMMY_WINDOW.blit(self.SHIP_REGENERATION_BUTTON, (96, 718))

    def settings_button_click(self, x, y, click):  # Handles the button clicks in the settings page
        if self.SHIP_REGENERATION_RECT.collidepoint(x, y) and click:
            self.ship_regeneration_settings()

        if self.SHIP_HEALTH_RECT.collidepoint(x, y) and click:
            self.ship_health_settings()

    def settings_logic(self):  # Handles the settings logic in the settings page
        settings_state = True
        while settings_state:
            self.settings_screen()

            mx, my = pygame.mouse.get_pos()

            click = False

            for event in pygame.event.get():
                click = True if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 else False
                if event.type == pygame.QUIT:
                    game_quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pause_game()
                    settings_state = False

            self.settings_button_click(mx, my, click)

            self.game.scale_window()
            self.game.CLOCK.tick(self.game.FPS)

    def pause_game_screen(self):  # Draws the paused screen assets
        self.game.draw_stuff(
            self.spaceship.red, self.spaceship.red_bullets, self.game.red_score, self.spaceship.damaged_ship_health)
        self.asteroid.draw_asteroids(self.asteroid.asteroids_list)
        self.game.DUMMY_WINDOW.blit(self.RESUME_BUTTON_SURFACE, (82, 442))
        self.game.DUMMY_WINDOW.blit(self.OPTIONS_BUTTON_SURFACE, (365, 10))

    def pause_button_click(self, x, y, click):  # Handles the button clicks in the paused screen
        if self.OPTIONS_BUTTON_RECT.collidepoint((x, y)) and click:
            self.settings_logic()


class Game:
    def __init__(self):
        # Game Initialisation
        pygame.init()
        pygame.display.set_caption("Logang Shooter")
        self.ICON = pygame.image.load("assets/icon.png")
        pygame.display.set_icon(self.ICON)

        # Class Imports
        self.spaceship = spaceship
        self.asteroid = asteroid
        self.settings = settings

        # Game Constants
        self.MONITOR = pygame.display.Info()
        self.SCREEN_DIMENSIONS = (math.floor(self.MONITOR.current_w * 0.3), math.ceil(self.MONITOR.current_h * 0.948))
        self.WINDOW = pygame.display.set_mode(self.SCREEN_DIMENSIONS)
        self.DUMMY_WINDOW = pygame.Surface((576, 1024))
        self.WIDTH, HEIGHT = self.SCREEN_DIMENSIONS
        self.WINDOW_WIDTH = self.WINDOW.get_width()
        self.WINDOW_HEIGHT = self.WINDOW.get_height()
        self.FPS = 60
        self.CLOCK = pygame.time.Clock()

        # Game Variables
        self.running = False
        self.game_active = False
        self.red_score = 0
        self.high_score = 0
        self.angle = 0
        self.angle_list = multiples(0, 360, 20)
        self.angle_index = angle_choice(self.angle_list)

        # Colours
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 102, 39)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)
        self.EASY, self.MEDIUM, self.HARD = (98, 255, 183), (97, 174, 255), (255, 116, 123)

        # Fonts
        self.SCORE_FONT = pygame.font.SysFont("comic_sans", 40, True)
        self.REGEN_FONT = pygame.font.SysFont("Impact", 30)

        # Asset Files
        self.BACKGROUND_SURFACE = pygame.transform.scale((pygame.image.load("assets/space.png")), (576, 1024))
        self.EXPLOSION_SURFACE = pygame.image.load("assets/boom.png").convert_alpha()
        self.LOGO = pygame.image.load("assets/logo.png")
        self.YOU_WIN_SURFACE = pygame.image.load("assets/you_win.png")
        self.YOU_LOSE_SURFACE = pygame.image.load("assets/game_over.png")
        self.SPACEBAR_AGAIN_INSTRUCTIONS = pygame.image.load("assets/press_spacebar.png")

        # Instruction Files
        self.INTRO_1 = pygame.image.load("assets/intro_1.png")
        self.INTRO_2 = pygame.image.load("assets/intro_2.png")
        self.INTRO_3 = pygame.image.load("assets/intro_3.png")
        self.INTRO_4 = pygame.image.load("assets/intro_4.png")
        self.SPACEBAR_INSTRUCTIONS = pygame.image.load("assets/spacebar_instructions.png")
        self.SPACEBAR_INSTRUCTIONS_RECT = self.SPACEBAR_INSTRUCTIONS.get_rect(center=(288, 560))

        # Audio Files
        self.LASER_SOUND = pygame.mixer.Sound("assets/Gun+Silencer.mp3")
        pygame.mixer.Sound.set_volume(self.LASER_SOUND, 0.2)
        self.LASER_HIT = pygame.mixer.Sound("assets/Grenade+1.mp3")
        pygame.mixer.Sound.set_volume(self.LASER_HIT, 0.3)

        self.SHIP_DAMAGE = pygame.mixer.Sound("assets/ship_damage.wav")
        pygame.mixer.Sound.set_volume(self.SHIP_DAMAGE, 0.3)
        self.DEATH_SOUND = pygame.mixer.Sound("assets/dead.wav")
        pygame.mixer.Sound.set_volume(self.DEATH_SOUND, 0.3)

        self.GAME_MUSIC = pygame.mixer.Sound("assets/bgm.wav")
        pygame.mixer.Sound.set_volume(self.GAME_MUSIC, 0.1)
        self.GAME_MUSIC.play(-1)

    def scale_window(self):  # Scales the game window and assets to fit the user's monitor dimensions
        frame = pygame.transform.scale(self.DUMMY_WINDOW, self.SCREEN_DIMENSIONS)
        self.WINDOW.blit(frame, frame.get_rect())
        pygame.display.flip()

    def main(self):  # The main game loop that handles the majority of the game logic
        self.instructions_screen()

        self.start_screen()

        asteroid = self.asteroid.ASTEROID_RECT

        while self.running:
            self.running_loop()

            self.draw_stuff(
                self.spaceship.red, self.spaceship.red_bullets, self.red_score, self.spaceship.damaged_ship_health)

            self.spaceship.ship_death(self.spaceship.damaged_ship_health)

            self.game_over()

            self.active_game()

            self.you_win()

            keys_pressed = pygame.key.get_pressed()
            self.spaceship.red_handle_movement(keys_pressed, self.spaceship.red)

            self.spaceship.handle_bullets(self.spaceship.red_bullets, asteroid)

            self.scale_window()

            self.CLOCK.tick(self.FPS)

    def running_loop(self):  # The main running loop that handles asteroid creation and collision among others
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

            if event.type == self.asteroid.ASTEROID_HIT:
                self.asteroid.remove_asteroid(self.asteroid.asteroids_list)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and not self.game_active:
                self.game_clear()

            if self.game_active and not self.settings.paused:
                self.angle -= 15
                self.other_running_loop(event)

    def other_running_loop(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE \
                and len(self.spaceship.red_bullets) < self.spaceship.MAX_BULLETS:
            bullet = pygame.Rect(self.spaceship.red.x - 9, self.spaceship.red.y - 20, 17, 70)
            self.spaceship.red_bullets.append(bullet)
            self.LASER_SOUND.play()

        if event.type == self.asteroid.ASTEROID_SPAWN_RATE_PLUS:
            asteroid_spawn_rate = self.asteroid.halve_rate(self.asteroid.asteroid_spawn_rate)
            self.asteroid.spawn_asteroids(asteroid_spawn_rate, 0)

        if event.type == self.asteroid.SPAWN_ASTEROID:
            self.asteroid.asteroids_list.append(self.asteroid.create_asteroid())

        if event.type == self.spaceship.INCREASE_SHIP_HEALTH:
            self.spaceship.damaged_ship_health += 1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.settings.pause_game()

    def you_win(self):  # Displays the victory screen
        if self.spaceship.damaged_ship_health >= 100:
            self.game_active = False
            self.DUMMY_WINDOW.blit(self.BACKGROUND_SURFACE, (0, 0))
            self.DUMMY_WINDOW.blit(self.LOGO, (60, 25))
            self.DUMMY_WINDOW.blit(self.YOU_WIN_SURFACE, (6, 392))
            self.DUMMY_WINDOW.blit(self.SPACEBAR_AGAIN_INSTRUCTIONS, (6, 712))

            self.high_score = update_score(self.red_score, self.high_score)
            self.score_display()

    def game_over(self):  # Displays the game over screen
        if not self.game_active:
            self.DUMMY_WINDOW.blit(self.BACKGROUND_SURFACE, (0, 0))
            self.DUMMY_WINDOW.blit(self.LOGO, (60, 25))
            self.DUMMY_WINDOW.blit(self.YOU_LOSE_SURFACE, (6, 292))
            self.DUMMY_WINDOW.blit(self.SPACEBAR_AGAIN_INSTRUCTIONS, (6, 670))

            self.high_score = update_score(self.red_score, self.high_score)
            self.score_display()

            self.spaceship.red.center = (308, 900)

    def active_game(self):  # Handles the relevant variables when a game is in session
        if self.game_active:
            # Spaceship
            self.game_active = self.asteroid.check_asteroid_collision(
                self.asteroid.asteroids_list, self.spaceship.red_bullets, self.spaceship.red)

            # Asteroids
            self.asteroid.asteroids_list = self.asteroid.move_asteroids(self.asteroid.asteroids_list)
            self.asteroid.draw_asteroids(self.asteroid.asteroids_list)

    def game_clear(self):  # Clears the relevant variables to start a new game session
        self.asteroid.asteroid_spawn_rate = 2000

        self.asteroid.spawn_asteroids(2000, 7)

        if self.spaceship.ship_health_25:
            self.spaceship.damaged_ship_health = 25
        elif self.spaceship.ship_health_50:
            self.spaceship.damaged_ship_health = 50
        elif self.spaceship.ship_health_75:
            self.spaceship.damaged_ship_health = 75

        if self.spaceship.ship_regen_1:
            self.spaceship.ship_regen_rate = 1000
        elif self.spaceship.ship_regen_2:
            self.spaceship.ship_regen_rate = 2000
        elif self.spaceship.ship_regen_3:
            self.spaceship.ship_regen_rate = 3000

        self.spaceship.red_score = 0
        self.spaceship.red_bullets.clear()
        self.asteroid.asteroids_list.clear()
        self.game_active = True
        self.running = True

    def score_display(self):  # Writes out high score to the game window
        hi_score_surface = self.SCORE_FONT.render(f"High Score: {int(self.high_score)}", True, self.WHITE)
        hi_score_rect = hi_score_surface.get_rect(center=(288, 960))
        self.DUMMY_WINDOW.blit(hi_score_surface, hi_score_rect)

        score_surface = self.SCORE_FONT.render(f"Current Score: {int(self.red_score)}", True, self.WHITE)
        score_rect = score_surface.get_rect(center=(288, 920))
        self.DUMMY_WINDOW.blit(score_surface, score_rect)

    def draw_stuff(self, redship, red_bullet, redscore, ship_health):  # Draws the relevant assets onscreen
        # Background
        self.DUMMY_WINDOW.blit(self.BACKGROUND_SURFACE, (0, 0))

        # Current Score
        red_score_text = self.SCORE_FONT.render(f"Score: {redscore}", True, self.WHITE)
        self.DUMMY_WINDOW.blit(red_score_text, (420, 970))

        # Ship Health
        if ship_health >= 90:
            self.DUMMY_WINDOW.blit(self.spaceship.ship_health_colour("Green", ship_health), (10, 970))
        elif 89 >= ship_health >= 60:
            self.DUMMY_WINDOW.blit(self.spaceship.ship_health_colour("Yellow", ship_health), (10, 970))
        elif 59 >= ship_health >= 30:
            self.DUMMY_WINDOW.blit(self.spaceship.ship_health_colour("Orange", ship_health), (10, 970))
        else:
            self.DUMMY_WINDOW.blit(self.spaceship.ship_health_colour("Red", ship_health), (10, 970))

        # Bullets
        for bullet in red_bullet:
            self.DUMMY_WINDOW.blit(self.spaceship.LASER_BLAST, bullet)
        max_bullet_text = self.SCORE_FONT.render(
            f"Bullets = {len(self.spaceship.red_bullets)}/{self.spaceship.MAX_BULLETS}", True, self.WHITE)
        self.DUMMY_WINDOW.blit(max_bullet_text, (0, 0))

        current_spawn_rate_text = self.SCORE_FONT.render(
            f"Current Rate: every {self.asteroid.asteroid_spawn_rate / 1000} seconds", True, self.WHITE)
        self.DUMMY_WINDOW.blit(current_spawn_rate_text, (40, 250))

        self.DUMMY_WINDOW.blit(self.spaceship.RED_SPACESHIP, (redship.x - (redship.w // 2), redship.y))
        self.DUMMY_WINDOW.blit(self.LOGO, (60, 25))

        pygame.display.update()

    def instructions_screen_1(self):  # Displays instructions to game screen
        instruction_state = True
        while instruction_state:
            self.DUMMY_WINDOW.fill(self.WHITE)
            for events in pygame.event.get():
                if events.type == pygame.KEYDOWN:
                    instruction_state = False
                if events.type == pygame.QUIT:
                    game_quit()
            self.DUMMY_WINDOW.blit(self.INTRO_1, (0, 0))
            self.scale_window()

    def instructions_screen_2(self):  # Displays instructions to game screen
        instruction_state = True
        while instruction_state:
            self.DUMMY_WINDOW.fill(self.WHITE)
            for events in pygame.event.get():
                if events.type == pygame.KEYDOWN:
                    instruction_state = False
                if events.type == pygame.QUIT:
                    game_quit()
            self.DUMMY_WINDOW.blit(self.INTRO_2, (0, 0))
            self.scale_window()

    def instructions_screen_3(self):  # Displays instructions to game screen
        instruction_state = True
        while instruction_state:
            self.DUMMY_WINDOW.fill(self.WHITE)
            for events in pygame.event.get():
                if events.type == pygame.KEYDOWN:
                    instruction_state = False
                if events.type == pygame.QUIT:
                    game_quit()
            self.DUMMY_WINDOW.blit(self.INTRO_3, (0, 0))
            self.scale_window()

    def instructions_screen_4(self):  # Displays instructions to game screen
        instruction_state = True
        while instruction_state:
            self.DUMMY_WINDOW.fill(self.WHITE)
            for events in pygame.event.get():
                if events.type == pygame.KEYDOWN:
                    instruction_state = False
                if events.type == pygame.QUIT:
                    game_quit()
            self.DUMMY_WINDOW.blit(self.INTRO_4, (0, 0))
            self.scale_window()

    def instructions_screen(self):  # Displays all the instructions to the game screen
        self.instructions_screen_1()

        self.instructions_screen_2()

        self.instructions_screen_3()

        self.instructions_screen_4()

    def start_screen(self):  # The start screen of the game
        while not self.running:
            self.DUMMY_WINDOW.fill(self.WHITE)
            for events in pygame.event.get():
                if events.type == pygame.KEYDOWN and events.key == pygame.K_SPACE:
                    self.running = True
                    self.game_active = True
                    self.asteroid.spawn_asteroids(2000, 7)
                if events.type == pygame.QUIT:
                    game_quit()
            self.draw_stuff(
                self.spaceship.red, self.spaceship.red_bullets, self.red_score, self.spaceship.damaged_ship_health)
            self.DUMMY_WINDOW.blit(self.SPACEBAR_INSTRUCTIONS, self.SPACEBAR_INSTRUCTIONS_RECT)
            self.scale_window()


spaceship = Spaceship()
game = Game()
asteroid = Asteroid()
settings = Settings()


if __name__ == '__main__':
    game = Game()
    game.main()
