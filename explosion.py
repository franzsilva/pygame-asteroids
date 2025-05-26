import pygame
import random
from constants import *
from circleshape import CircleShape

class ExplosionParticle(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, EXPLOSION_PARTICLE_SIZE)
        # Random velocity for the particle
        speed = random.uniform(50, EXPLOSION_MAX_SPEED)
        direction = pygame.Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        ).normalize()
        self.velocity = direction * speed
        
        # Random bright color for the particle
        self.color = random.choice([
            "red", "orange", "yellow", "lime", "cyan", "magenta", "white"
        ])
        
        # Set lifetime for the particle
        self.lifetime = EXPLOSION_DURATION
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, 0)
    
    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

class Explosion:
    def __init__(self, x, y, size):
        # Create explosion particles
        particle_count = int(EXPLOSION_PARTICLE_COUNT * (size / ASTEROID_MIN_RADIUS))
        
        for _ in range(particle_count):
            # Create a particle at the explosion position with a small random offset
            offset_x = random.uniform(-5, 5)
            offset_y = random.uniform(-5, 5)
            # The ExplosionParticle constructor will add the particle to its containers
            ExplosionParticle(x + offset_x, y + offset_y)