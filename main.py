import pygame
import sys
import math
from constants import *
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from powerup import PowerUp
from powerupspawner import PowerUpSpawner
from explosion import ExplosionParticle, Explosion
from menu_animation import MenuAnimation
from bouncingball import BouncingBall
from bouncingballspawner import BouncingBallSpawner

def draw_psychedelic_background(screen, time_elapsed):
    """Draw a psychedelic background with rainbow colors and patterns."""
    # Create a time-based color cycle
    time_factor = time_elapsed * 2  # Speed up the effect
    
    # Fill with base gradient
    for y in range(SCREEN_HEIGHT):
        # Create a rainbow gradient that shifts over time
        hue = (y / SCREEN_HEIGHT + time_factor) % 1.0
        # Convert HSV to RGB for rainbow effect
        rgb = hsv_to_rgb(hue, 0.8, 0.6)  # Lower brightness for better readability
        color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))
    
    # Add moving wave patterns
    wave_offset = time_factor * 100
    for x in range(0, SCREEN_WIDTH, 20):
        wave_y = SCREEN_HEIGHT // 2 + int(math.sin((x + wave_offset) * 0.01) * 100)
        hue = (x / SCREEN_WIDTH + time_factor * 2) % 1.0
        rgb = hsv_to_rgb(hue, 1.0, 1.0)
        color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        pygame.draw.circle(screen, color, (x, wave_y), 10, 2)
    
    # Add spiraling patterns
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    for i in range(0, 360, 10):
        angle = math.radians(i + time_factor * 50)
        radius = 50 + 30 * math.sin(time_factor + i * 0.1)
        x = center_x + int(radius * math.cos(angle))
        y = center_y + int(radius * math.sin(angle))
        hue = (i / 360 + time_factor) % 1.0
        rgb = hsv_to_rgb(hue, 1.0, 0.8)
        color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        pygame.draw.circle(screen, color, (x, y), 8, 0)

def hsv_to_rgb(h, s, v):
    """Convert HSV color to RGB. h should be in [0,1], s in [0,1], v in [0,1]."""
    if s == 0.0:
        return (v, v, v)
    i = int(h * 6.)
    f = (h * 6.) - i
    p, q, t = v * (1. - s), v * (1. - s * f), v * (1. - s * (1. - f))
    i %= 6
    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)

def show_menu(screen, clock):
    """Show the game menu with options and handle selection."""
    # Create menu animation
    menu_animation = MenuAnimation()
    
    # Menu options
    menu_options = ["New Game", "Quit"]
    selected_option = 0
    
    # Font setup
    title_font = pygame.font.SysFont(None, 100)
    option_font = pygame.font.SysFont(None, 50)
    
    while True:
        dt = clock.tick(60) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if selected_option == 0:  # New Game
                        return GAME_STATE
                    elif selected_option == 1:  # Quit
                        sys.exit()
        
        # Update animation
        menu_animation.update(dt)
        
        # Clear screen
        screen.fill("black")
        
        # Draw animation
        menu_animation.draw(screen)
        
        # Draw title
        title_text = title_font.render("ASTEROIDS", True, "white")
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
        screen.blit(title_text, title_rect)
        
        # Draw menu options
        for i, option in enumerate(menu_options):
            color = "yellow" if i == selected_option else "white"
            option_text = option_font.render(option, True, color)
            option_rect = option_text.get_rect(
                center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + i * 60)
            )
            screen.blit(option_text, option_rect)
        
        pygame.display.flip()

def run_game(screen, clock):
    """Run the actual game loop."""
    # Initialize counter for destroyed asteroids
    destroyed_asteroids = 0
    # Track elapsed time for psychedelic background
    total_time = 0
    
    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    explosion_particles = pygame.sprite.Group()
    bouncing_balls = pygame.sprite.Group()

    Player.containers = (updatable_group, drawable_group)
    Asteroid.containers = (asteroids, updatable_group, drawable_group)
    AsteroidField.containers = updatable_group
    Shot.containers = (shots, updatable_group, drawable_group)
    PowerUp.containers = (powerups, updatable_group, drawable_group)
    PowerUpSpawner.containers = updatable_group
    ExplosionParticle.containers = (explosion_particles, updatable_group, drawable_group)
    BouncingBall.containers = (bouncing_balls, updatable_group, drawable_group)
    BouncingBallSpawner.containers = updatable_group
    
    asteroid_field = AsteroidField()
    powerup_spawner = PowerUpSpawner()
    ball_spawner = BouncingBallSpawner(bouncing_balls)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return MENU_STATE  # Return to menu instead of exiting directly
        dt = clock.tick(60) / 1000
        total_time += dt

        # Draw background based on powerup status
        if player.powerup_timer > 0:
            draw_psychedelic_background(screen, total_time)
        else:
            screen.fill("black")
            
        updatable_group.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                return MENU_STATE  # Return to menu on game over

        # Check for powerup collection
        for powerup in powerups:
            if powerup.collides_with(player):
                # Activate powerup
                player.powerup_timer = POWERUP_DURATION
                powerup.kill()  # Remove the powerup
        
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
        
        # Draw the powerup timer if active
        if player.powerup_timer > 0:
            timer_text = font.render(f"POWERUP: {int(player.powerup_timer)}", True, "cyan")
            timer_rect = timer_text.get_rect(midtop=(SCREEN_WIDTH / 2, 20))
            screen.blit(timer_text, timer_rect)
            # Add stream mode indicator
            stream_text = font.render("STREAM MODE ACTIVE!", True, "yellow")
            stream_rect = stream_text.get_rect(midtop=(SCREEN_WIDTH / 2, 50))
            screen.blit(stream_text, stream_rect)
        
        pygame.display.flip()

def main():
    """Main function handling game states."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    
    # Start with menu state
    game_state = MENU_STATE
    
    while True:
        if game_state == MENU_STATE:
            game_state = show_menu(screen, clock)
        elif game_state == GAME_STATE:
            game_state = run_game(screen, clock)


if __name__ == "__main__":
    main()    


if __name__ == "__main__":
    main()
