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
            menu_outcome = menu.run() # Attendre un dictionnaire

            if not menu_outcome: # Si l'utilisateur ferme le menu sans choisir
                running = False
                continue

            game_mode = menu_outcome.get("mode")
            selected_skin = menu_outcome.get("skin")

            if not selected_skin:
                print("Error: No skin path received from menu. Exiting.")
                # Fallback to a default skin path if necessary or handle error
                # For now, let's assume a default if None. This should ideally be handled more robustly.
                # default_skin_path = os.path.join("assets", "sprites", "frog", "Idle frog", "frog_idle0.png") # Example default
                # selected_skin = default_skin_path 
                # Better to ensure menu always returns a valid skin or None and game handles None if player can't load without it
                running = False # Or handle as an error state
                continue
            
            # Démarrer le mode de jeu sélectionné
            game_instance = None
            if game_mode == "NORMAL":
                # Mode de jeu normal avec différents types de plateformes
                game_instance = Game(player_skin_path=selected_skin) # Passer le skin
            elif game_mode == "LAVA":
                # Mode de jeu lave avec plateformes cassables et fond de lave
                game_instance = LavaGame(player_skin_path=selected_skin) # Passer le skin
            elif game_mode == "ICE":
                # Mode de jeu glace avec plateformes glissantes et fond de glace
                game_instance = IceGame(player_skin_path=selected_skin) # Passer le skin
            else:
                # Quitter si aucun mode n'est sélectionné ou si l'utilisateur a quitté
                running = False
                continue
            
            if game_instance:
                result = game_instance.run()
            else: # Should not happen if game_mode is one of the above
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