from circleshape import *
from constants import *
import pygame
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0  # Timer variable for shooting cooldown
        self.powerup_timer = 0  # Timer for powerup duration
    
    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        # Add visual effect when powerup is active
        if self.powerup_timer > 0:
            # Draw a glowing outline when powerup is active
            pygame.draw.polygon(screen, "cyan", self.triangle(), 4)
            pygame.draw.polygon(screen, "white", self.triangle(), 2)
        else:
            pygame.draw.polygon(screen, "white", self.triangle(), 2)
    
    def rotate(self, dt):
        self.rotation += dt * PLAYER_TURN_SPEED

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(-dt)
        if keys[pygame.K_s]:    
            self.move(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        # Add shift key support for rapid fire
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.shoot(rapid_fire=True)
            
        # Decrease the shooting timer by dt
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
            
        # Decrease the powerup timer if active
        if self.powerup_timer > 0:
            self.powerup_timer -= dt
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        
    def shoot(self, rapid_fire=False):
        # Determine the appropriate cooldown
        cooldown = PLAYER_SHOOT_COOLDOWN
        if self.powerup_timer > 0:
            cooldown = POWERUP_SHOOT_COOLDOWN  # Very fast shooting during powerup
        elif rapid_fire:
            cooldown = RAPID_FIRE_COOLDOWN  # Fast shooting with shift key
        
        # Only allow shooting if the timer is 0 or less
        if self.shoot_timer <= 0:
            # Reset the timer to the appropriate cooldown value
            self.shoot_timer = cooldown
            
            # Get the front point of the triangle
            forward = pygame.Vector2(0, -1).rotate(self.rotation)
            front_point = self.position + forward * self.radius
            
            # Create the shot at the front point
            shot = Shot(front_point.x, front_point.y)
            shot.velocity = pygame.Vector2(0, -1).rotate(self.rotation)
            
            # Apply powerup effect if active
            if self.powerup_timer > 0:
                shot.velocity *= PLAYER_SHOOT_SPEED * POWERUP_SHOT_MULTIPLIER
                # Make powerup shots more visible
                shot.is_powerup_shot = True
            else:
                shot.velocity *= PLAYER_SHOOT_SPEED
                shot.is_powerup_shot = False

