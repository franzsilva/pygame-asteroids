import pygame
import random
from constants import *
from bouncingball import BouncingBall


class BouncingBallSpawner(pygame.sprite.Sprite):
    def __init__(self, bouncing_balls_group):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        self.spawn_timer = BALL_SPAWN_RATE
        self.bouncing_balls_group = bouncing_balls_group
        
    def update(self, dt):
        self.spawn_timer -= dt
        
        if self.spawn_timer <= 0:
            self.spawn_timer = BALL_SPAWN_RATE
            self.spawn_ball()
    
    def spawn_ball(self):
        # Count current balls to enforce maximum
        if len(self.bouncing_balls_group) >= BALL_MAX_COUNT:
            return  # Don't spawn if we're at max capacity
            
        # Spawn ball at a random edge of the screen
        edge = random.randint(0, 3)  # 0=top, 1=right, 2=bottom, 3=left
        
        if edge == 0:  # top
            x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
            y = BALL_RADIUS
        elif edge == 1:  # right
            x = SCREEN_WIDTH - BALL_RADIUS
            y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
        elif edge == 2:  # bottom
            x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
            y = SCREEN_HEIGHT - BALL_RADIUS
        else:  # left
            x = BALL_RADIUS
            y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
            
        BouncingBall(x, y)