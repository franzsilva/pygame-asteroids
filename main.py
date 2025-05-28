import pygame
import sys
from constants import *
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from powerup import PowerUp
from powerupspawner import PowerUpSpawner
from explosion import ExplosionParticle, Explosion
from menu_animation import MenuAnimation

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
    
    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    explosion_particles = pygame.sprite.Group()

    Player.containers = (updatable_group, drawable_group)
    Asteroid.containers = (asteroids, updatable_group, drawable_group)
    AsteroidField.containers = updatable_group
    Shot.containers = (shots, updatable_group, drawable_group)
    PowerUp.containers = (powerups, updatable_group, drawable_group)
    PowerUpSpawner.containers = updatable_group
    ExplosionParticle.containers = (explosion_particles, updatable_group, drawable_group)
    
    asteroid_field = AsteroidField()
    powerup_spawner = PowerUpSpawner()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return MENU_STATE  # Return to menu instead of exiting directly
        dt = clock.tick(60) / 1000

        screen.fill("black")
        updatable_group.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                return MENU_STATE  # Return to menu on game over

        # Check for powerup collection
        for powerup in powerups:
            if powerup.collides_with(player):
                # Activate the appropriate powerup
                if getattr(powerup, "color", "yellow") == "blue":
                    player.blue_powerup_timer = POWERUP_DURATION
                else:
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

        if player.blue_powerup_timer > 0:
            timer_text = font.render(f"POWERUP: {int(player.blue_powerup_timer)}", True, "blue")
            timer_rect = timer_text.get_rect(midtop=(SCREEN_WIDTH / 2, 80))
            screen.blit(timer_text, timer_rect)
            stream_text = font.render("TRIANGLE SHOT ACTIVE!", True, "blue")
            stream_rect = stream_text.get_rect(midtop=(SCREEN_WIDTH / 2, 110))
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


