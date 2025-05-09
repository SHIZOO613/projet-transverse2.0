import pygame
from game_logic import Game
from lava_game import LavaGame
from ice_game import IceGame
from main_menu import MainMenu

def main():
    """Point d'entrée principal du jeu. Initialise et gère la boucle principale entre les modes."""
    # Initialiser pygame
    pygame.init()
    
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
    
    # Quitter proprement pygame
    pygame.quit()

if __name__ == "__main__":
    main()