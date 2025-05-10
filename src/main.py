"""
Main entry point for the game.
"""
import sys
import pygame
from game.utils.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game.ui.main_menu import MainMenu

def initialize_game() -> pygame.Surface:
    """Initialize pygame and create the game window."""
    pygame.init()
    pygame.display.set_caption("Platformer Game")
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def main() -> None:
    """Main game loop."""
    try:
        screen = initialize_game()
        clock = pygame.time.Clock()
        game_menu = MainMenu()
        
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                game_menu.handle_event(event)
            
            # Update game state
            game_menu.update()
            
            # Draw everything
            screen.fill((0, 0, 0))  # Clear screen
            game_menu.draw(screen)
            pygame.display.flip()
            
            # Control frame rate
            clock.tick(FPS)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main() 