import pygame
from game_logic import Game
from lava_game import LavaGame
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
        mode = menu.run()
        
        # Vérifier le mode choisi
        if mode == "NORMAL":
            # Mode de jeu normal
            game = Game()
            result = game.run()
            
            # Si le résultat est "QUIT", quitter l'application
            if result == "QUIT":
                running = False
            # Si le résultat est "MENU", on continue la boucle pour revenir au menu
        elif mode == "LAVA":
            # Mode de jeu lave
            lava_game = LavaGame()
            result = lava_game.run()
            
            # Si le résultat est "QUIT", quitter l'application
            if result == "QUIT":
                running = False
            # Si le résultat est "MENU", on continue la boucle pour revenir au menu
        else:
            # Si le joueur a quitté depuis le menu ou aucun mode n'a été sélectionné
            running = False
    
    # Quitter proprement pygame
    pygame.quit()

if __name__ == "__main__":
    main()