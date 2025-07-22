import pygame
import sys
from DataValues import Constants, Assets
from Player import Player

# Initialize Pygame
pygame.init()

# Set up the display
screen: pygame.Surface = pygame.display.set_mode(Constants.SCREEN_SIZE)
pygame.display.set_caption("Platformer")

# Clock for controlling frame rate
clock: pygame.time.Clock = pygame.time.Clock()

# --- Game Setup ---
player: Player = Player(100, Constants.SCREEN_HEIGHT - 100) # Starting position

all_sprites: pygame.sprite.Group = pygame.sprite.Group()
platforms: pygame.sprite.Group = pygame.sprite.Group() # Define the platforms sprite group

def reset(): # Resets the screen based on stage switching
    all_sprites.empty()
    all_sprites.add(player)
    # Add all platforms from the platforms group to the all_sprites group for drawing
    for platform in platforms:
        all_sprites.add(platform)

reset()

# --- Game Loop ---
running: bool = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                player.jump()
            elif event.key == pygame.K_ESCAPE:
                # PAUSE MENU
                ...

    keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
    player.stop()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.go_left()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.go_right()

    """
    x = 0
    
    if right:
        x += 5
    if left:
        x -= 5
    
    player.x_speed = x * delta_time
    """

    # Update game elements
    player.update(platforms) # Pass platforms to player for collision detection

    # Drawing
    screen.fill(Assets.BLACK) # Fill background

    all_sprites.draw(screen) # Draw all sprites

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(Constants.FPS)

pygame.quit()
sys.exit()