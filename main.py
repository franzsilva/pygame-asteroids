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

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    
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
                return
        dt = clock.tick(60) / 1000

        screen.fill("black")
        updatable_group.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                sys.exit()
        
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
            timer_text = font.render(f"POWERUP: {int(player.powerup_timer)}", True, "yellow")
            timer_rect = timer_text.get_rect(midtop=(SCREEN_WIDTH / 2, 20))
            screen.blit(timer_text, timer_rect)
        
        pygame.display.flip()

    


if __name__ == "__main__":
    main()
