#!/usr/bin/env python3
"""
Simple test script to verify bouncing ball functionality
"""
import pygame
import sys
import os

# Add the current directory to the path to import game modules
sys.path.insert(0, os.path.dirname(__file__))

from constants import *
from bouncingball import BouncingBall
from bouncingballspawner import BouncingBallSpawner

def test_bouncing_ball():
    """Test bouncing ball creation and basic functionality"""
    pygame.init()
    
    # Test ball creation
    ball = BouncingBall(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    # Test that ball has correct properties
    assert ball.radius == BALL_RADIUS, f"Expected radius {BALL_RADIUS}, got {ball.radius}"
    assert ball.position.x == SCREEN_WIDTH // 2, "Ball not positioned correctly"
    assert ball.position.y == SCREEN_HEIGHT // 2, "Ball not positioned correctly"
    assert ball.velocity.length() > 0, "Ball should have initial velocity"
    
    # Test ball update (movement)
    initial_x = ball.position.x
    initial_y = ball.position.y
    ball.update(0.1)  # Update with 0.1 second
    
    # Ball should have moved
    moved = (ball.position.x != initial_x) or (ball.position.y != initial_y)
    assert moved, "Ball should have moved after update"
    
    print("✓ BouncingBall creation and movement tests passed")

def test_boundary_bouncing():
    """Test that balls bounce off screen boundaries"""
    pygame.init()
    
    # Test ball near left edge
    ball = BouncingBall(5, SCREEN_HEIGHT // 2)
    ball.velocity.x = -100  # Moving left
    ball.update(0.1)
    
    # Should bounce and move right
    assert ball.velocity.x > 0, "Ball should bounce off left edge"
    
    # Test ball near right edge
    ball = BouncingBall(SCREEN_WIDTH - 5, SCREEN_HEIGHT // 2)
    ball.velocity.x = 100  # Moving right
    ball.update(0.1)
    
    # Should bounce and move left
    assert ball.velocity.x < 0, "Ball should bounce off right edge"
    
    print("✓ Boundary bouncing tests passed")

def test_spawner():
    """Test bouncing ball spawner functionality"""
    pygame.init()
    
    # Create sprite groups
    bouncing_balls = pygame.sprite.Group()
    BouncingBall.containers = (bouncing_balls,)
    
    # Create spawner
    spawner = BouncingBallSpawner(bouncing_balls)
    
    # Test that spawner doesn't spawn immediately
    initial_count = len(bouncing_balls)
    
    # Test spawner update
    spawner.spawn_timer = 0  # Force immediate spawn
    spawner.update(0.1)
    
    # Should have spawned one ball
    assert len(bouncing_balls) == initial_count + 1, "Spawner should have created one ball"
    
    print("✓ Spawner tests passed")

def main():
    """Run all tests"""
    print("Running bouncing ball tests...")
    
    try:
        test_bouncing_ball()
        test_boundary_bouncing()
        test_spawner()
        print("\n🎉 All tests passed! Bouncing ball implementation is working correctly.")
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)