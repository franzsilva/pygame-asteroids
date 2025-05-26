SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN = 0.3  # seconds between shots

# Powerup constants
POWERUP_RADIUS = 15
POWERUP_SPAWN_RATE = 15.0  # seconds
POWERUP_SPEED = 150
POWERUP_DURATION = 10.0  # seconds
POWERUP_SHOT_MULTIPLIER = 2.5  # Shot speed multiplier (reduced from 10 for visibility)
POWERUP_SHOOT_COOLDOWN = 0.05  # Rapid fire cooldown during powerup
RAPID_FIRE_COOLDOWN = 0.08  # Rapid fire cooldown when holding shift

# Explosion constants
EXPLOSION_DURATION = 0.8  # seconds
EXPLOSION_PARTICLE_COUNT = 15  # number of particles per explosion
EXPLOSION_PARTICLE_SIZE = 3  # size of explosion particles
EXPLOSION_MAX_SPEED = 150  # maximum speed of explosion particles