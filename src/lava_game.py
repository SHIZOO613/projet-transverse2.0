import pygame
import random

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, YELLOW, RED,
    PLATFORM_SPACING
)
from utils import create_pixel_text
from lava_background import LavaBackground
from player import Player
from platform import Platform, BreakablePlatform

class LavaGame:
    """Mode de jeu 'lave' avec uniquement des plateformes cassables et un fond de lave."""
    
    def __init__(self):
        # Set up display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cloud Jump - Lava Mode")
        self.clock = pygame.time.Clock()
        
        # Create fonts
        self.regular_font = pygame.font.Font(None, 36)
        self.pixel_font_large = pygame.font.Font(None, 64)
        self.pixel_font_small = pygame.font.Font(None, 36)
        
        # Initialize game objects
        self.background = LavaBackground()
        self.player = Player()
        self.platforms = []
        
        # Game state
        self.score = 0
        self.game_over = False
        self.scroll_speed = 0
        self.difficulty = 1.0  # Niveau de difficulté qui augmente avec le score
        
        # Create initial platforms
        self.generate_platforms()
        
    def generate_platforms(self):
        """Generate the initial platforms for the game."""
        # Clear existing platforms
        self.platforms = []
        
        # Taille fixe de plateforme
        platform_width = 100  # Taille standard pour toutes les plateformes
        
        # Create initial ground platform - la seule plateforme normale en mode lave
        self.platforms.append(Platform(SCREEN_WIDTH//2 - platform_width//2, SCREEN_HEIGHT - 100, platform_width))
        
        # Generate random platforms - toutes cassables
        for i in range(12):
            x = random.randint(20, SCREEN_WIDTH - platform_width)
            y = SCREEN_HEIGHT - 200 - i * PLATFORM_SPACING
            
            # En mode lave, toutes les autres plateformes sont cassables
            self.platforms.append(BreakablePlatform(x, y, platform_width))
    
    def update(self):
        """Update all game elements for one frame."""
        if self.game_over:
            return
            
        # Update background
        self.background.update()
        
        # Update player
        player_update_result = self.player.update(self.platforms)
        
        # Check if player fell off the bottom
        if player_update_result == "GAME_OVER":
            self.game_over = True
            return
        
        # Système de caméra simplifié
        should_scroll = player_update_result  # Le player renvoie directement un booléen
        self.scroll_speed = 5 if should_scroll else 0
        if self.scroll_speed > 0:
            self.score += 1
            
            # Augmenter progressivement la difficulté avec le score
            self.difficulty = 1.0 + (self.score / 500)  # Augmente de 1.0 à 2.0 sur 500 points
            
        # Update platforms with scrolling
        for platform in self.platforms:
            platform.update(self.scroll_speed)
            
        # Supprimer les plateformes cassées ou qui sont sorties de l'écran
        self.platforms = [p for p in self.platforms if p.y < SCREEN_HEIGHT + 50 and 
                         (not hasattr(p, 'should_remove') or not p.should_remove())]
        
        # Ajouter de nouvelles plateformes au fur et à mesure
        while len(self.platforms) < 13:
            # Get y-position of highest platform and add a new one above it
            highest_y = min([p.y for p in self.platforms])
            platform_width = 100  # Taille standard
            
            # Calculer l'espacement vertical en fonction du score
            # Plus le score est élevé, plus l'espacement est grand
            current_spacing = PLATFORM_SPACING + int(self.score / 100) * 5
            # Limiter l'espacement maximum pour éviter que le jeu devienne impossible
            current_spacing = min(current_spacing, PLATFORM_SPACING * 2)
            
            x = random.randint(20, SCREEN_WIDTH - platform_width)
            y = highest_y - current_spacing
            
            # En mode lave, toutes les nouvelles plateformes sont cassables
            platform = BreakablePlatform(x, y, platform_width)
            self.platforms.append(platform)
    
    def draw(self):
        """Draw all game elements to the screen."""
        # Draw background
        self.background.draw(self.screen)
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)
        
        # Draw player if game is active
        if not self.game_over:
            self.player.draw(self.screen)
            
            # Draw score with pixel art style
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
        self.player = Player()
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