import pygame
import random

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, YELLOW, RED,
    PLATFORM_SPACING, MIN_PLATFORM_WIDTH, MAX_PLATFORM_WIDTH,
    add_coins, update_high_score
)
from utils import create_pixel_text
from game_base import GameBase
from ice_background import IceBackground
from player import Player
from game_platform import Platform, IcePlatform

class IceGame(GameBase):
    """Mode de jeu 'glace' avec uniquement des plateformes de glace, sauf la première."""
    
    def __init__(self, player_skin_path):
        # Appel du constructeur de la classe parente
        super().__init__(title="Cloud Jump - Ice Mode")
        
        self.player_skin_path = player_skin_path # Store the skin path

        # Initialiser les objets spécifiques à ce mode
        self.background = IceBackground()
        self.player = Player(skin_path=self.player_skin_path) # Pass skin path to Player
        
        # Générer les plateformes initiales
        self.generate_platforms()
        
    def generate_platforms(self):
        """Générer les plateformes initiales pour le jeu."""
        # Vider les plateformes existantes
        self.platforms = []
        
        # Taille fixe de plateforme
        platform_width = 100  # Taille standard pour toutes les plateformes
        
        # Créer la plateforme de sol initiale - la seule plateforme normale en mode glace
        self.platforms.append(Platform(SCREEN_WIDTH//2 - platform_width//2, SCREEN_HEIGHT - 100, platform_width))
        
        # Générer des plateformes aléatoires - toutes glissantes (ice)
        for i in range(12):
            x = random.randint(20, SCREEN_WIDTH - platform_width)
            y = SCREEN_HEIGHT - 200 - i * PLATFORM_SPACING
            
            # En mode glace, toutes les autres plateformes sont des plateformes de glace
            self.platforms.append(IcePlatform(x, y, platform_width))
    
    def update(self):
        """Mettre à jour tous les éléments du jeu pour une frame."""
        if self.game_over:
            return
            
        # Mettre à jour le fond
        self.background.update()
        
        # Mettre à jour le joueur
        player_update_result = self.player.update(self.platforms)
        
        # Vérifier si le joueur est tombé en bas
        if player_update_result == "GAME_OVER":
            self.game_over = True
            return
        
        # Système de caméra simplifié
        should_scroll = player_update_result  # Le joueur renvoie directement un booléen
        self.scroll_speed = 5 if should_scroll else 0
        if self.scroll_speed > 0:
            self.score += 1
            
            # Augmenter progressivement la difficulté avec le score
            self.difficulty = 1.0 + (self.score / 500)  # Augmente de 1.0 à 2.0 sur 500 points
            
        # Mettre à jour les plateformes avec le défilement
        for platform in self.platforms:
            platform.update(self.scroll_speed)
            
        # Supprimer les plateformes qui sont sorties de l'écran
        self.platforms = [p for p in self.platforms if p.y < SCREEN_HEIGHT + 50]
        
        # Ajouter de nouvelles plateformes au fur et à mesure
        while len(self.platforms) < 13:
            # Obtenir la position Y de la plateforme la plus haute et ajouter une nouvelle au-dessus
            highest_y = min([p.y for p in self.platforms])
            platform_width = 100  # Taille standard
            
            # Calculer l'espacement vertical en fonction du score
            # Plus le score est élevé, plus l'espacement est grand
            current_spacing = PLATFORM_SPACING + int(self.score / 100) * 5
            # Limiter l'espacement maximum pour éviter que le jeu devienne impossible
            current_spacing = min(current_spacing, PLATFORM_SPACING * 2)
            
            x = random.randint(20, SCREEN_WIDTH - platform_width)
            y = highest_y - current_spacing
            
            # En mode glace, toutes les nouvelles plateformes sont des plateformes de glace
            platform = IcePlatform(x, y, platform_width)
            self.platforms.append(platform)
    
    def draw(self):
        """Dessiner tous les éléments du jeu à l'écran."""
        # Dessiner le fond
        self.background.draw(self.screen)
        
        # Dessiner les plateformes
        for platform in self.platforms:
            platform.draw(self.screen)
        
        # Dessiner le joueur si le jeu est actif
        if not self.game_over:
            self.player.draw(self.screen)
            
            # Dessiner le score avec style pixel art
            score_text = create_pixel_text(f"Score: {self.score}", self.pixel_font_small, WHITE)
            self.screen.blit(score_text, (10, 10))
        else:
            self.draw_game_over_screen()
    
    def draw_game_over_screen(self):
        """Draw the game over screen with pixelated text."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with 70% opacity
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = create_pixel_text("GAME OVER", self.pixel_font_large, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Score text
        score_text = create_pixel_text(f"Score: {self.score}", self.pixel_font_small, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        self.screen.blit(score_text, score_rect)
        
        # Instruction pour retourner au menu
        restart_text = create_pixel_text("Press SPACE for menu", self.pixel_font_small, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
        self.screen.blit(restart_text, restart_rect)
    
    def reset(self):
        """Reset the game state to start a new game."""
        self.player = Player(skin_path=self.player_skin_path) # Re-initialize player with the stored skin path
        self.score = 0
        self.game_over = False
        self.scroll_speed = 0
        self.difficulty = 1.0
        self.generate_platforms()
    
    def handle_events(self):
        """Handle all user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "QUIT"
                elif event.key == pygame.K_SPACE and self.game_over:
                    # Update high score before returning to menu
                    update_high_score("ice", self.score)
                    return "MENU"  # Retourner au menu principal
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.game_over:  # Left mouse button
                    self.player.start_charge()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and not self.game_over:  # Left mouse button
                    mouse_x, _ = pygame.mouse.get_pos()
                    self.player.release_jump(mouse_x)
        return "CONTINUE"
    
    def run(self):
        """Main game loop."""
        running = True
        result = "CONTINUE"
        
        while running:
            # Handle events
            result = self.handle_events()
            
            if result == "QUIT":
                running = False
            elif result == "MENU":
                return "MENU"  # Signal to return to the menu
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Update display and maintain framerate
            pygame.display.flip()
            self.clock.tick(FPS)
            
        return "QUIT"  # Le jeu s'est terminé par une demande de sortie 