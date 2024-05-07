import pygame
import sys
from random import randint

pygame.init()
game_font = pygame.font.Font(None, 30)
screen_width, screen_height = 800, 600
screen_fill_color = (32, 52, 71)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Awesome Shooter Game")

# Reduce the FIGHTER_STEP value to decrease the movement speed
FIGHTER_STEP = 0.6  # Change this value to adjust the movement speed

fighter_image = pygame.image.load('python/87-pygame-shooter-oop/shooter/images/fighter.png')
fighter_width, fighter_height = fighter_image.get_size()
fighter_x = screen_width / 2 - fighter_width / 2
fighter_y = screen_height - fighter_height
fighter_is_moving_left, fighter_is_moving_right = False, False

BALL_STEP = 0.5
ball_image = pygame.image.load('python/87-pygame-shooter-oop/shooter/images/ball.png')
ball_width, ball_height = ball_image.get_size()
ball_x, ball_y = 0, 0
ball_was_fired = False

ALIEN_STEP = 0.1
alien_speed = ALIEN_STEP
alien_image = pygame.image.load('python\\87-pygame-shooter-oop\\shooter\\images\\alien.png')
alien_width, alien_height = alien_image.get_size()
alien_x = randint(0, screen_width - alien_width)
alien_y = 0

game_score = 0
game_is_running = True
game_is_paused = False
game_state = 'playing'  # New game state variable
game_over = False  # Flag to track game over

# Sample options
difficulty_level = 'easy'
sound_enabled = True

def reset_game():
    global fighter_x, fighter_y, ball_x, ball_y, ball_was_fired, alien_x, alien_y, alien_speed, game_score, game_over
    fighter_x = screen_width / 2 - fighter_width / 2
    fighter_y = screen_height - fighter_height
    ball_x, ball_y = 0, 0
    ball_was_fired = False
    alien_x = randint(0, screen_width - alien_width)
    alien_y = 0
    alien_speed = ALIEN_STEP
    game_score = 0
    game_over = False

while game_is_running:
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                fighter_is_moving_left = True
            if event.key == pygame.K_RIGHT:
                fighter_is_moving_right = True
            if event.key == pygame.K_SPACE:
                ball_was_fired = True
                ball_x = fighter_x + fighter_width / 2 - ball_width / 2
                ball_y = fighter_y - ball_height
            if event.key == pygame.K_p:  # Pause/Unpause
                game_is_paused = not game_is_paused
            if event.key == pygame.K_r:  # Restart
                reset_game()
                game_state = 'playing'
            if event.key == pygame.K_q:  # Exit
                game_is_running = False
            if event.key == pygame.K_o:  # Open Options
                game_state = 'options'
            if game_over:
                if event.key == pygame.K_r:  # Restart game after game over
                    reset_game()
                    game_state = 'playing'
                if event.key == pygame.K_q:  # Exit game after game over
                    game_is_running = False
            if game_state == 'options':
                if event.key == pygame.K_d:  # Change difficulty level
                    if difficulty_level == 'easy':
                        difficulty_level = 'hard'
                    else:
                        difficulty_level = 'easy'
                if event.key == pygame.K_s:  # Toggle sound
                    sound_enabled = not sound_enabled
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                fighter_is_moving_left = False
            if event.key == pygame.K_RIGHT:
                fighter_is_moving_right = False

    if game_state == 'playing':
        if not game_is_paused:
            if fighter_is_moving_left and fighter_x >= FIGHTER_STEP:
                fighter_x -= FIGHTER_STEP
            if fighter_is_moving_right and fighter_x <= screen_width - fighter_width - FIGHTER_STEP:
                fighter_x += FIGHTER_STEP

            if ball_was_fired and ball_y + ball_height < 0:
                ball_was_fired = False
            if ball_was_fired:
                ball_y -= BALL_STEP

            alien_y += alien_speed

        screen.fill(screen_fill_color)
        screen.blit(fighter_image, (fighter_x, fighter_y))
        screen.blit(alien_image, (alien_x, alien_y))
        if ball_was_fired:
            screen.blit(ball_image, (ball_x, ball_y))

        game_score_text = game_font.render(f"Your Score is: {game_score}", True, 'white')
        screen.blit(game_score_text, (20, 20))

        if game_is_paused:
            pause_text = game_font.render("Game Paused", True, 'white')
            pause_rect = pause_text.get_rect()
            pause_rect.center = (screen_width // 2, screen_height // 2)
            screen.blit(pause_text, pause_rect)

        pygame.display.update()

        if not game_is_paused:
            if alien_y + alien_height > fighter_y:
                game_over = True

            if ball_was_fired and \
                    alien_x < ball_x < alien_x + alien_width - ball_width and \
                    alien_y < ball_y < alien_y + alien_height - ball_height:
                ball_was_fired = False
                alien_x = randint(0, screen_width - alien_width)
                alien_y = 0
                alien_speed += ALIEN_STEP / 2
                game_score += 1

    elif game_state == 'options':
        screen.fill(screen_fill_color)
        options_text = game_font.render("Options Menu", True, 'white')
        options_rect = options_text.get_rect()
        options_rect.center = (screen_width // 2, screen_height // 3)
        screen.blit(options_text, options_rect)

        # Display current options
        difficulty_text = game_font.render(f"Difficulty: {difficulty_level.upper()}", True, 'white')
        difficulty_rect = difficulty_text.get_rect()
        difficulty_rect.center = (screen_width // 2, screen_height // 2)
        screen.blit(difficulty_text, difficulty_rect)

        sound_text = game_font.render(f"Sound: {'ON' if sound_enabled else 'OFF'}", True, 'white')
        sound_rect = sound_text.get_rect()
        sound_rect.center = (screen_width // 2, screen_height // 2 + 50)
        screen.blit(sound_text, sound_rect)

        # Display key controls
        controls_text = game_font.render("Controls:", True, 'white')
        controls_rect = controls_text.get_rect()
        controls_rect.topleft = (20, screen_height - 150)
        screen.blit(controls_text, controls_rect)

        control_texts = [
            "D: Change difficulty level",
            "S: Toggle sound",
            "O: Back to game"
        ]
        for i, text in enumerate(control_texts):
            control_text = game_font.render(text, True, 'white')
            control_rect = control_text.get_rect()
            control_rect.topleft = (40, screen_height - 120 + i * 30)
            screen.blit(control_text, control_rect)

        pygame.display.update()

    if game_over:
        game_over_text = game_font.render("Game Over", True, 'white')
        game_over_rectangle = game_over_text.get_rect()
        game_over_rectangle.center = (screen_width / 2, screen_height / 2 - 50)
        screen.blit(game_over_text, game_over_rectangle)

        restart_text = game_font.render("Press 'R' to restart", True, 'white')
        restart_rect = restart_text.get_rect()
        restart_rect.center = (screen_width / 2, screen_height / 2)
        screen.blit(restart_text, restart_rect)

        exit_text = game_font.render("Press 'Q' to exit", True, 'white')
        exit_rect = exit_text.get_rect()
        exit_rect.center = (screen_width / 2, screen_height / 2 + 50)
        screen.blit(exit_text, exit_rect)

        pygame.display.update()

pygame.quit()