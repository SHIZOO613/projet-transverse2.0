import sys
import os
import pygame
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"System path: {sys.path}")

# Make sure the current directory is in the path
if '.' not in sys.path:
    sys.path.append('.')
    print("Added current directory to sys.path")

try:
    from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
    from game_logic import Game
    from lava_game import LavaGame
    from ice_game import IceGame
    from main_menu import MainMenu
    print("All modules imported successfully")
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def main():
    """Point d'entrée principal du jeu. Initialise et gère la boucle principale entre les modes."""
    try:
        # Initialiser pygame
        pygame.init()
        print("Pygame initialized successfully.")
        
        # Créer la fenêtre de jeu
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Game")
        clock = pygame.time.Clock()
        print("Game window created successfully.")
        
        # Boucle principale entre les différents modes de jeu
        running = True
        
        while running:
            # Afficher le menu principal et récupérer le mode sélectionné
            menu = MainMenu()
            selected_mode = menu.run()
            
            # Démarrer le mode de jeu sélectionné
            if selected_mode == "NORMAL":
                # Mode de jeu normal avec différents types de plateformes
                game = Game()
                result = game.run()
            elif selected_mode == "LAVA":
                # Mode de jeu lave avec plateformes cassables et fond de lave
                game = LavaGame()
                result = game.run()
            elif selected_mode == "ICE":
                # Mode de jeu glace avec plateformes glissantes et fond de glace
                game = IceGame()
                result = game.run()
            else:
                # Quitter si aucun mode n'est sélectionné ou si l'utilisateur a quitté
                running = False
                continue
                
            # Traiter le résultat du jeu
            if result == "QUIT":
                running = False
            # Si le résultat est "MENU", on continue la boucle pour revenir au menu
            
            # Contrôler la fréquence d'images
            clock.tick(FPS)
        
        # Quitter proprement pygame
        pygame.quit()
        sys.exit(0)
    except Exception as e:
        print(f"Error in main: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()