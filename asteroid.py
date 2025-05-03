import pygame
from constants import *
from circleshape import CircleShape
import math
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
    
    def split(self):
        # Call kill() to destroy this asteroid
        self.kill()
        
        # If the radius is less than or equal to the minimum, don't spawn new asteroids
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        # Compute the new radius using the formula old_radius - ASTEROID_MIN_RADIUS
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        # Generate a random angle between 20 and 50 degrees
        random_angle = random.uniform(20, 50)
        # Convert to radians
        random_angle_rad = math.radians(random_angle)
        
        # Create first asteroid with velocity rotated by +random_angle
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        # Use the velocity's rotate method to create the new vector
        first_vector = self.velocity.copy().rotate(random_angle)
        # Set the first asteroid's velocity to the first new vector, but make it move faster by scaling it up
        asteroid1.velocity = first_vector * 1.2
        
        # Create second asteroid with velocity rotated by -random_angle
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        # Use the velocity's rotate method to create the new vector in the opposite direction
        second_vector = self.velocity.copy().rotate(-random_angle)
        # Set the second asteroid's velocity to the second new vector, but make it move faster by scaling it up
        asteroid2.velocity = second_vector * 1.2