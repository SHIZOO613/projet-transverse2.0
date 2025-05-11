# Frog Jump - Platform Game

A 2D platform game where the player controls a frog that must jump from platform to platform to climb as high as possible.

## How to Play

1. Launch the game by running:
   ```
   python game.py
   ```

2. In the main menu, you can choose between three modes:
   - **Normal Mode**: Various platforms (normal, moving, icy, breakable)
   - **Lava Mode**: Only breakable platforms with a lava background and fireballs
   - **Ice Mode**: Slippery ice platforms that make movement more challenging

3. Controls:
   - Click and hold the left mouse button to charge a jump
   - Release to jump in the direction of the cursor
   - Press Space to return to the menu after Game Over
   - Press Escape to quit

## Project Structure

The project is organized using an object-oriented architecture with the following files:

```
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
- **pygame**: For graphics rendering and input handling
- **PIL** (Pillow): For some image processing operations

To install the dependencies:
```
pip install pygame pillow
```

## License

This project is distributed under a free license.

## Credits

- Sprites and graphics: Custom resources
- Development: Original project 
