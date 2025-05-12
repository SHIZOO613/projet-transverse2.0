import pygame
import os

# Initialize Pygame
pygame.init()

# Display settings
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 750
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

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

# Gestion du nombre total de pièces
TOTAL_COINS = 0

# High scores for each game mode
HIGH_SCORES = {
    "normal": 0
}

# Unlocked skins storage
UNLOCKED_SKINS = []

def add_coins(count):
    """Ajouter des pièces au compteur total"""
    global TOTAL_COINS
    TOTAL_COINS += count

def get_total_coins():
    """Obtenir le nombre total de pièces"""
    return TOTAL_COINS

def spend_coins(amount):
    """Spend coins if available"""
    global TOTAL_COINS
    if TOTAL_COINS >= amount:
        TOTAL_COINS -= amount
        return True
    return False

def unlock_skin(skin_path):
    """Mark a skin as unlocked"""
    global UNLOCKED_SKINS
    if skin_path not in UNLOCKED_SKINS:
        UNLOCKED_SKINS.append(skin_path)
        return True
    return False

def is_skin_unlocked(skin_path):
    """Check if a skin is unlocked"""
    return skin_path in UNLOCKED_SKINS

def update_high_score(mode, score):
    """Update the high score for a specific game mode if the new score is higher"""
    global HIGH_SCORES
    if score > HIGH_SCORES[mode]:
        HIGH_SCORES[mode] = score
        return True
    return False

def get_high_score(mode):
    """Get the high score for a specific game mode"""
    return HIGH_SCORES[mode] 