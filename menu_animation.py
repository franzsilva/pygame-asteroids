import pygame
import random
from constants import *

class ASCIIChar:
    """A single ASCII character for menu background animation"""
    def __init__(self):
        self.char = random.choice(["*", ".", "+", "o", "O", "x", "X"])
        self.position = pygame.Vector2(
            random.uniform(0, SCREEN_WIDTH),
            random.uniform(0, SCREEN_HEIGHT)
        )
        self.velocity = pygame.Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        ).normalize() * random.uniform(MENU_ASCII_SPEED_MIN, MENU_ASCII_SPEED_MAX)
        self.color = random.choice(["white", "gray", "lightgray"])
        self.size = random.randint(10, 20)

    def update(self, dt):
        # Update position based on velocity
        self.position += self.velocity * dt

        # Wrap around screen edges
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def draw(self, screen):
        font = pygame.font.SysFont(None, self.size)
        text = font.render(self.char, True, self.color)
        screen.blit(text, self.position)


class MenuAnimation:
    """Background ASCII animation for the menu"""
    def __init__(self):
        self.chars = [ASCIIChar() for _ in range(MENU_ASCII_CHAR_COUNT)]

    def update(self, dt):
        for char in self.chars:
            char.update(dt)

    def draw(self, screen):
        for char in self.chars:
            char.draw(screen)