import pygame
import sys
import random
import time
from constants import *
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def draw_ascii_art_background(screen, ascii_asteroids, dt):
    # Update and draw ASCII art asteroids
    for asteroid in ascii_asteroids[:]:
        asteroid['pos'][0] += asteroid['vel'][0] * dt
        asteroid['pos'][1] += asteroid['vel'][1] * dt
        
        # Remove asteroids that go off screen
        if (asteroid['pos'][0] < -50 or asteroid['pos'][0] > SCREEN_WIDTH + 50 or 
            asteroid['pos'][1] < -50 or asteroid['pos'][1] > SCREEN_HEIGHT + 50):
            ascii_asteroids.remove(asteroid)
        else:
            # Draw ASCII asteroid
            font = pygame.font.SysFont('courier', asteroid['size'])
            text = font.render(asteroid['char'], True, (80, 80, 80))  # Dark gray for subtlety
            screen.blit(text, asteroid['pos'])
    
    # Occasionally spawn new ASCII asteroids
    if random.random() < 0.05:  # 5% chance each frame
        # Choose edge to spawn from
        edge = random.randint(0, 3)
        pos = [0, 0]
        vel = [0, 0]
        
        if edge == 0:  # Top
            pos = [random.randint(0, SCREEN_WIDTH), -20]
            vel = [random.uniform(-20, 20), random.uniform(30, 60)]
        elif edge == 1:  # Right
            pos = [SCREEN_WIDTH + 20, random.randint(0, SCREEN_HEIGHT)]
            vel = [random.uniform(-60, -30), random.uniform(-20, 20)]
        elif edge == 2:  # Bottom
            pos = [random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + 20]
            vel = [random.uniform(-20, 20), random.uniform(-60, -30)]
        else:  # Left
            pos = [-20, random.randint(0, SCREEN_HEIGHT)]
            vel = [random.uniform(30, 60), random.uniform(-20, 20)]
            
        ascii_chars = ['*', '#', '+', '.', 'o', 'O', '@']
        ascii_asteroids.append({
            'pos': pos,
            'vel': vel,
            'char': random.choice(ascii_chars),
            'size': random.randint(15, 40)
        })

def show_menu(screen, clock):
    # Initial setup for the menu
    menu_options = ["New Game", "Exit"]
    selected_option = 0
    font_large = pygame.font.SysFont("arial", 72, bold=True)
    font_medium = pygame.font.SysFont("arial", 48)
    
    # ASCII art asteroids for background
    ascii_asteroids = []
    
    # Menu loop
    while True:
        dt = clock.tick(60) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # New Game
                        return GAME
                    elif selected_option == 1:  # Exit
                        pygame.quit()
                        sys.exit()
        
        # Draw background
        screen.fill("black")
        draw_ascii_art_background(screen, ascii_asteroids, dt)
        
        # Draw title
        title = font_large.render("ASTEROIDS", True, "white")
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title, title_rect)
        
        # Draw menu options
        for i, option in enumerate(menu_options):
            if i == selected_option:
                text = font_medium.render(f"> {option} <", True, "yellow")
            else:
                text = font_medium.render(option, True, "white")
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 70))
            screen.blit(text, text_rect)
        
        pygame.display.flip()

def run_game(screen, clock):
    dt = 0
    
    # Initialize counter for destroyed asteroids
    destroyed_asteroids = 0
    
    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable_group, drawable_group)
    Asteroid.containers = (asteroids, updatable_group, drawable_group)
    AsteroidField.containers = updatable_group
    Shot.containers = (shots, updatable_group, drawable_group)
    
    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return MENU
                
        dt = clock.tick(60) / 1000

        screen.fill("black")
        updatable_group.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                # Wait a moment before returning to menu
                time.sleep(1)
                return MENU
        
        # Check collisions between bullets and asteroids
        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    shot.kill()  # Remove the bullet
                    if asteroid.radius <= ASTEROID_MIN_RADIUS:
                        destroyed_asteroids += 1  # Increment counter when smallest asteroids are destroyed
                    asteroid.split()  # Split the asteroid instead of just killing it

        for drawable in drawable_group:
            drawable.draw(screen)
        
        # Draw the asteroid counter in blue at the bottom right
        font = pygame.font.SysFont(None, 36)  # Default font, size 36
        counter_text = font.render(f"{destroyed_asteroids}", True, "blue")
        counter_rect = counter_text.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))
        screen.blit(counter_text, counter_rect)
        
        pygame.display.flip()

def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    # Start with menu state
    current_state = MENU
    
    while True:
        if current_state == MENU:
            current_state = show_menu(screen, clock)
        elif current_state == GAME:
            current_state = run_game(screen, clock)
        else:
            # Should never happen, but just in case
            print("Invalid game state!")
            break
    


if __name__ == "__main__":
    main()
