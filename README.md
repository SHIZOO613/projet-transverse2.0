# Frog Jump - Platform Game

A 2D platform game where the player controls a frog that must jump from platform to platform to climb as high as possible.

## How to Play

1. Launch the game by running:
   ```bash
   python game.py
   ```

2. Game Modes:
   - **Normal Mode**: Various platforms (normal, moving, icy, breakable) with a cloud background.
   - **Lava Mode**: Only breakable platforms with a lava background and fireball obstacles.
   - **Ice Mode**: Slippery ice platforms that make movement more challenging.

3. Controls:
   - Click and hold the left mouse button to charge a jump.
   - Release to jump in the direction of the cursor.
   - Press **Space** to return to the menu after Game Over.
   - Press **Escape** to quit.

## Features

### Game Mechanics
- **Dynamic Difficulty**: The difficulty increases as the player's score rises, introducing more challenging platforms.
- **Platform Types**:
  - Normal Platforms: Standard platforms.
  - Moving Platforms: Platforms that move horizontally.
  - Ice Platforms: Slippery platforms that affect movement.
  - Breakable Platforms: Fragile platforms that break after being stepped on.
- **Coin Collection**: Coins appear on certain platforms and can be collected to add to the player's total coin count.

### Visual Customization
- **Player Skins**: Players can select different skins for their frog character.
- **Dynamic Backgrounds**: Backgrounds change depending on the game mode (e.g., clouds, lava, ice).

### Scoring and Rewards
- **Pixel-Art Score Display**: The player's score is displayed in pixel-art style during gameplay.
- **Coin Counter**: Tracks the number of coins collected during the game.
- **High Scores**: Keeps track of the highest scores achieved in each mode.

### Game Menus
- **Main Menu**: Allows players to select game modes and access settings.
- **Game Over Screen**: Displays the player's score and coin count with options to return to the menu.

### Shop 
- **Item Shop**: Use collected coins to purchase new skins or other in-game items.

### Core Game Components
- **Object-Oriented Design**: The game uses a modular design with reusable components for platforms, backgrounds, and the player.
- **Collision Detection**: Accurate collision handling for platforms, coins, and other game objects.

### Graphics and Animation
- **Sprite Management**: Each game object (player, platforms, coins) uses custom sprites for a polished look.
- **Parallax Backgrounds**: Smooth-scrolling backgrounds for an immersive experience.

## Project Structure

The project is organized with the following files:

```plaintext
src/
├── assets/               # Game resources (sprites, images)
├── game.py               # Main game entry point
├── game_base.py          # Base class for game modes
├── game_logic.py         # Normal game mode implementation
├── lava_game.py          # Lava game mode implementation
├── ice_game.py           # Ice game mode implementation
├── main_menu.py          # Main menu
├── background_manager.py # Base classes for background management
├── background.py         # Parallax background management
├── lava_background.py    # Lava background management
├── ice_background.py     # Ice background management
├── platform.py           # Classes for different platform types
├── player.py             # Player class (frog)
├── config.py             # Game configuration and constants
├── utils.py              # Utility functions
└── __init__.py
```

## Dependencies

The game uses the following Python libraries:
- **pygame**: For graphics rendering and input handling.
- **PIL** (Pillow): For some image processing operations.

To install the dependencies:
```bash
pip install pygame pillow
```

## Credits

- **Sprites and Graphics**: Custom resources.
- **Development**: Original project.
