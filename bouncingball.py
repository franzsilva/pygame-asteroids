import pygame
import random
import math
from constants import *
from circleshape import CircleShape


class BouncingBall(CircleShape):
    def __init__(self, x, y):
        # Use a smaller radius for the bouncing ball
        super().__init__(x, y, BALL_RADIUS)
        
        # Random initial velocity with both x and y components
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(BALL_MIN_SPEED, BALL_MAX_SPEED)
        self.velocity = pygame.Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )
        
        # Visual properties for distraction
        self.color_phase = random.uniform(0, 2 * math.pi)
        self.color_speed = random.uniform(2, 5)
        
    def draw(self, screen):
        # Create a pulsing, colorful ball for maximum distraction
        time_factor = pygame.time.get_ticks() / 1000.0
        
        # Calculate pulsing radius
        pulse_factor = 1 + 0.3 * math.sin(time_factor * 3 + self.color_phase)
        current_radius = int(self.radius * pulse_factor)
        
        # Calculate rainbow colors that change over time
        hue = (time_factor * self.color_speed + self.color_phase) % (2 * math.pi)
        red = int(127 * (1 + math.sin(hue)))
        green = int(127 * (1 + math.sin(hue + 2.09)))  # 120 degrees phase shift
        blue = int(127 * (1 + math.sin(hue + 4.18)))   # 240 degrees phase shift
        
        color = (red, green, blue)
        
        # Draw main ball with pulsing effect
        pygame.draw.circle(screen, color, self.position, current_radius)
        # Draw bright outline for extra visibility
        pygame.draw.circle(screen, "white", self.position, current_radius, 2)
        
    def update(self, dt):
        # Move the ball
        self.position += self.velocity * dt
        
        # Bounce off screen edges
        if self.position.x - self.radius <= 0 or self.position.x + self.radius >= SCREEN_WIDTH:
            self.velocity.x = -self.velocity.x
            # Keep ball within bounds
            self.position.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.position.x))
            
        if self.position.y - self.radius <= 0 or self.position.y + self.radius >= SCREEN_HEIGHT:
            self.velocity.y = -self.velocity.y
            # Keep ball within bounds  
            self.position.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.position.y))