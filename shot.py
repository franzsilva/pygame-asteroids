import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.is_powerup_shot = False
        self.trail_positions = []  # Store previous positions for trail effect
        self.max_trail_length = 8  # Maximum number of trail positions to keep
    
    def draw(self, screen):
        if self.is_powerup_shot:
            # Draw trail for powerup shots
            if len(self.trail_positions) > 1:
                for i, pos in enumerate(self.trail_positions):
                    alpha = int(255 * (i + 1) / len(self.trail_positions))
                    # Create a surface for alpha blending
                    trail_surface = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
                    # Use RGBA color directly (cyan with alpha)
                    color_with_alpha = (0, 255, 255, alpha)  # Cyan with alpha
                    pygame.draw.circle(trail_surface, color_with_alpha, (self.radius * 2, self.radius * 2), self.radius)
                    screen.blit(trail_surface, (pos.x - self.radius * 2, pos.y - self.radius * 2))
            
            # Draw main powerup shot (cyan/electric blue with glow effect)
            # Outer glow
            pygame.draw.circle(screen, "cyan", self.position, self.radius + 2, 0)
            # Inner bright core
            pygame.draw.circle(screen, "white", self.position, self.radius, 0)
        else:
            # Draw normal shot
            pygame.draw.circle(screen, "white", self.position, self.radius, 2)
    
    def update(self, dt):
        # Add current position to trail before moving
        if self.is_powerup_shot:
            self.trail_positions.append(self.position.copy())
            # Keep only the last few positions for the trail
            if len(self.trail_positions) > self.max_trail_length:
                self.trail_positions.pop(0)
        
        self.position += self.velocity * dt