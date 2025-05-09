import pygame
import os

# Initialize Pygame
pygame.init()

# Display settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

# Physics settings
GRAVITY = 0.5
MAX_CHARGE = 20
CHARGE_RATE = 0.5

# Platform settings
PLATFORM_HEIGHT = 10
MIN_PLATFORM_WIDTH = 60
MAX_PLATFORM_WIDTH = 120
PLATFORM_SPACING = 100

# Player settings
PLAYER_SIZE = 40  # Increased size to better show the frog sprite
JUMP_HORIZONTAL_FACTOR = 0.05
MAX_HORIZONTAL_DISTANCE = 150

# Animation settings
ANIMATION_SPEED = 0.15  # Seconds per frame for idle animation

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
BG_ASSETS_DIR = os.path.join(ASSETS_DIR, "backgrounds") 