from DataValues import Constants, Assets
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface(Constants.PLAYER_SIZE)
        self.image.fill(Assets.BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.change_x = 0
        self.change_y = 0
        self.death = False
        self.on_ground = False
        self.coyote_timer = 0.0 # New: Timer to track time since leaving ground

    def update(self, platforms):
        # Apply gravity
        self.change_y += Constants.GRAVITY
        if self.change_y > 10: # Cap falling speed
            self.change_y = 10

        # Move left/right
        self.rect.x += self.change_x

        # Check for horizontal collisions with platforms
        self.collide_horizontal(platforms)

        # Move up/down
        self.rect.y += self.change_y

        # Check for vertical collisions with platforms
        self.collide_vertical(platforms)

        # Coyote time logic:
        # If the player is currently on the ground, reset the coyote timer.
        if self.on_ground:
            self.coyote_timer = 0.0
        # If the player is in the air, increment the coyote timer.
        else:
            self.coyote_timer += (1.0 / Constants.FPS) # Increment by time per frame


        # Keep player within screen bounds horizontally
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Constants.SCREEN_WIDTH:
            self.rect.right = Constants.SCREEN_WIDTH

    def collide_horizontal(self, platforms):
        # Check for collisions after horizontal movement
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if platform.color == Assets.RED:
                    self.death = True
                if self.change_x > 0: # Moving right
                    self.rect.right = platform.rect.left
                elif self.change_x < 0: # Moving left
                    self.rect.left = platform.rect.right

    def collide_vertical(self, platforms):
        # Check for collisions after vertical movement
        # Temporarily set on_ground to False; it will be set to True if a collision occurs below.
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if platform.color == Assets.RED:
                    self.death = True
                elif self.change_y > 0: # Falling down, hit top of platform
                    self.rect.bottom = platform.rect.top
                    self.change_y = 0
                    self.on_ground = True # Player is now on ground
                elif self.change_y < 0: # Jumping up, hit bottom of platform
                    self.rect.top = platform.rect.bottom
                    self.change_y = 0

        # If player falls off screen, reset position (simple death/reset)
        if self.rect.top > Constants.SCREEN_HEIGHT or self.death:
            self.rect.x = 100
            self.rect.y = 100
            self.change_y = 0
            self.on_ground = False # Player is no longer on ground after reset
            self.death = False # Player doesn't get stuck in a death loop
            self.coyote_timer = 0.0 # Reset coyote timer on death/reset

    def go_left(self):
        self.change_x = -Constants.PLAYER_SPEED

    def go_right(self):
        self.change_x = Constants.PLAYER_SPEED

    def stop(self):
        self.change_x = 0

    def jump(self):
        # Allow jumping if on the ground OR within the coyote time window
        if self.on_ground or (self.coyote_timer < Constants.COYOTE_TIME_LIMIT):
            self.change_y = Constants.JUMP_STRENGTH
            self.on_ground = False # Player is now in the air
            self.coyote_timer = Constants.COYOTE_TIME_LIMIT # Consume coyote time after jumping to prevent multiple jumps