import pygame
import random

# Initialize pygame
pygame.init()
pygame.display.set_caption("Alien Aim Trainer")

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Aim Trainer")

# Load the alien and crosshair images
alien_imgs = [pygame.image.load("./assets/alien1.png").convert_alpha(),
                pygame.image.load("./assets/alien2.png").convert_alpha(),
                pygame.image.load("./assets/alien3.png").convert_alpha(),
                pygame.image.load("./assets/alien4.png").convert_alpha(),
                pygame.image.load("./assets/alien5.png").convert_alpha()]

alien_img = random.choice(alien_imgs)
alien_width = alien_img.get_width()
alien_height = alien_img.get_height()

crosshair_img = pygame.image.load("./assets/crosshair.png").convert_alpha()
crosshair_width = crosshair_img.get_width()
crosshair_height = crosshair_img.get_height()

# Set up the aliens
aliens = []
alien_spawn_time = 1000 # milliseconds
last_alien_spawn_time = 0
alien_speed = 1 # pixels per frame


# Set up the game stats
kills = 0
misses = 0

# Set up the game clock
clock = pygame.time.Clock()

# load background image
background_image = pygame.image.load("./assets/space.png")
background_image = pygame.transform.scale(background_image,(window_width, window_height))
background_sound = pygame.mixer.Sound('./assets/background_sound.wav')
# Play the sound in a loop
background_sound.play(loops=-1)

explosion_img = pygame.image.load("./assets/explosion.png").convert_alpha()
explosion_sound = pygame.mixer.Sound("./assets/explosion.wav")

# Hide the default cursor
pygame.mouse.set_visible(False)
# Set the cursor to the crosshair image
pygame.mouse.set_cursor(*pygame.cursors.broken_x)

# Set up the text font and size
font = pygame.font.SysFont(None, 50)
title_font = pygame.font.SysFont(None, 36)
game_title = font.render("Alien Aim Trainer", True, (255, 255, 255))
click_to_play = title_font.render("Click to Play", True, (255, 255, 255))
title_rect = game_title.get_rect(center=(window_width/2, window_height/2))
click_rect = click_to_play.get_rect(center=(window_width/2, title_rect.bottom + 20))

# Set up the game rules
rules = [
    "Rules:",
    "1. Miss 5 aliens, Game Over",
    "2. DIfficulty increases every 5 kills."
]
rules_texts = [title_font.render(rule, True, (255, 255, 255)) for rule in rules]
rules_rects = [text.get_rect(center=(window_width/2, click_rect.bottom + 20 + i*30)) for i, text in enumerate(rules_texts)]

# Show the game title screen
show_title_screen = True
while show_title_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            show_title_screen = False

    window.blit(background_image, (0, 0))
    window.blit(game_title, title_rect)
    window.blit(click_to_play, click_rect)
    for rule_text, rule_rect in zip(rules_texts, rules_rects):
        window.blit(rule_text, rule_rect)
    pygame.display.update()

# Game loop
running = True
while running:
    # blit background image onto window surface
    window.blit(background_image, (0, 0))
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click hit an alien
            for alien in aliens:
                if alien["rect"].collidepoint(pygame.mouse.get_pos()):
                    # Kill the alien
                    aliens.remove(alien)
                    kills += 1
                    misses = 0
                    # Display the explosion image at the position of the hit alien
                    explosion_sound.play()
                    window.blit(explosion_img, alien["rect"])
                    pygame.display.update()
                    pygame.time.wait(200)
                    break
            else:
                # Increment misses if the click missed all aliens
                misses += 1

    # Spawn new aliens
    current_time = pygame.time.get_ticks()
    if current_time - last_alien_spawn_time >= alien_spawn_time:
        alien_x = random.randint(0, window_width - alien_width)
        alien_y = random.randint(0, window_height - alien_height)
        alien_img = random.choice(alien_imgs)
        aliens.append({
            "rect": pygame.Rect(alien_x, alien_y, alien_width, alien_height),
            "speed": alien_speed,
            "img": alien_img
        })
        last_alien_spawn_time = current_time

    # Move the aliens and check for misses
    for alien in aliens:
        alien["rect"].move_ip(0, alien["speed"])
        if alien["rect"].top >= window_height:
            aliens.remove(alien)
            misses += 1
            break

    # Increase alien speed and spawn rate as time goes on
    if kills > 0 and kills % 5 == 0:
        alien_speed = min(alien_speed + 0.2, 5)
        alien_spawn_time = max(alien_spawn_time - 50, 500)

    # End the game if the player misses 5 kills in a row
    if misses >= 5:
        running = False

    # Draw the game
    window.blit(background_image, (0, 0))
    for alien in aliens:
        window.blit(alien["img"], alien["rect"])
    window.blit(crosshair_img, pygame.mouse.get_pos())

    # Update the display
    pygame.display.update()

    # Tick the clock
    clock.tick(60)

# Show the game over screen
font = pygame.font.SysFont(None, 50)
game_over_text = font.render(f"Game Over - Kills: {kills}", True, (255, 255, 255))
text_rect = game_over_text.get_rect(center=(window_width/2, window_height/2))
window.blit(background_image, (0, 0))
window.blit(game_over_text, text_rect)
pygame.display.update()

# Wait for a few seconds before quitting
pygame.time.wait(3000)

# Quit pygame
pygame.quit()
