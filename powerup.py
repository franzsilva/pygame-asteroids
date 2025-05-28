import pygame
import random
from circleshape import CircleShape
from constants import *


class PowerUp(CircleShape):
    def __init__(self, x, y, color="yellow"):
        super().__init__(x, y, POWERUP_RADIUS)
        self.color = color
        # Set random velocity for the powerup
        self.velocity = pygame.Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        ).normalize() * POWERUP_SPEED
    
    def draw(self, screen):
        # Draw the powerup using its color
        pygame.draw.circle(screen, self.color, self.position, self.radius, 0)
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
    
    def update(self, dt):
        # Update position based on velocity
        self.position += self.velocity * dt
        
        # Bounce off the screen edges
        if self.position.x - self.radius <= 0 or self.position.x + self.radius >= SCREEN_WIDTH:
            self.velocity.x *= -1
        if self.position.y - self.radius <= 0 or self.position.y + self.radius >= SCREEN_HEIGHT:
            self.velocity.y *= -1
        
        # Keep the powerup within the screen bounds
        self.position.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.position.x))
        self.position.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.position.y))

