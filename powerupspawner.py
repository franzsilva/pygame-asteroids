import pygame
import random
from constants import *
from powerup import PowerUp

class PowerUpSpawner(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > POWERUP_SPAWN_RATE:
            self.spawn_timer = 0
            
            # Spawn a new powerup at a random position within the screen (away from edges)
            padding = POWERUP_RADIUS * 2
            x = random.uniform(padding, SCREEN_WIDTH - padding)
            y = random.uniform(padding, SCREEN_HEIGHT - padding)
            
            # Randomly choose a powerup color (yellow or blue)
            color = random.choice(["yellow", "blue"])
            PowerUp(x, y, color=color)  # The PowerUp will add itself to the containers

