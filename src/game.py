import pygame
from game_logic import Game
from main_menu import MainMenu

def main():
    """Initialize and run the game."""
    # Initialiser pygame
    pygame.init()
    
    # Boucle principale entre le menu et le jeu
    running = True
    
    while running:
        # Afficher le menu principal
        menu = MainMenu()
        start_game = menu.run()
        
        # Si le joueur clique sur "Start", lancer le jeu
        if start_game:
            game = Game()
            result = game.run()
            
            # Si le résultat est "QUIT", quitter l'application
            if result == "QUIT":
                running = False
            # Si le résultat est "MENU", on continue la boucle pour revenir au menu
        else:
            # Si le joueur a quitté depuis le menu
            running = False
    
    # Quitter proprement pygame
    pygame.quit()

if __name__ == "__main__":
    main()