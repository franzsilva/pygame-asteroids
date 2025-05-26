# Pygame Asteroids

A classic arcade-style Asteroids game implemented in Python using Pygame. Navigate your spaceship through an asteroid field, shoot asteroids to destroy them, and collect powerups to enhance your firepower.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Setup

### Creating a Virtual Environment

It's recommended to use a virtual environment to isolate the game's dependencies.

#### On Windows:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

#### On macOS and Linux:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### Installing Dependencies

Once your virtual environment is activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Game

After installing the dependencies, you can run the game with:

```bash
python main.py
```

## Game Controls

- **W** - Move forward
- **S** - Move backward
- **A** - Rotate left
- **D** - Rotate right
- **SPACE** - Shoot

## Game Features

- Navigate a spaceship through an asteroid field
- Shoot asteroids to break them into smaller pieces
- Smaller asteroids yield points when destroyed
- Collect powerups to temporarily enhance your shooting capabilities
- Try to achieve the highest score by destroying as many asteroids as possible

## Game Over

The game ends when your spaceship collides with an asteroid.

## Credits

Created by franzsilva