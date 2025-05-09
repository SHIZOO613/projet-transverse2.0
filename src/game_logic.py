import pygame
import random

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, YELLOW, RED,
    MIN_PLATFORM_WIDTH, MAX_PLATFORM_WIDTH, PLATFORM_SPACING
)
from utils import create_pixel_text
from background import Background
from player import Player
from platform import Platform, MovingPlatform, BreakablePlatform, IcePlatform

class Game:
    """Main game class that manages all game elements and states."""
    
    def __init__(self):
        # Set up display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Cloud Jump")
        self.clock = pygame.time.Clock()
        
        # Create fonts
        self.regular_font = pygame.font.Font(None, 36)
        self.pixel_font_large = pygame.font.Font(None, 64)
        self.pixel_font_small = pygame.font.Font(None, 36)
        
        # Initialize game objects
        self.background = Background()
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
        
        # Taille fixe de plateforme basée sur la première plateforme
        platform_width = 100  # Taille standard pour toutes les plateformes
        
        # Create initial ground platform - toujours normale
        self.platforms.append(Platform(SCREEN_WIDTH//2 - platform_width//2, SCREEN_HEIGHT - 100, platform_width))
        
        # Generate random platforms
        for i in range(12):
            x = random.randint(20, SCREEN_WIDTH - platform_width)
            y = SCREEN_HEIGHT - 200 - i * PLATFORM_SPACING
            
            # Créer des plateformes aléatoires, mais les premières sont normales
            # pour que le joueur puisse s'habituer au jeu
            if i < 3:
                self.platforms.append(Platform(x, y, platform_width))
            else:
                # Utiliser la méthode statique pour créer une plateforme aléatoire
                self.platforms.append(
                    Platform.create_random_platform(x, y, platform_width, self.difficulty)
                )
    
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
            
            # Créer une plateforme aléatoire basée sur la difficulté actuelle
            platform = Platform.create_random_platform(x, y, platform_width, self.difficulty)
            self.platforms.append(platform)
    
    def draw(self):
        """Draw all game elements to the screen."""
        # Draw background
        self.screen.fill(BLACK)
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
        
        # Restart instructions
        restart_text = create_pixel_text("Press SPACE to restart", self.pixel_font_small, WHITE)
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
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset()  # Restart the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.game_over:  # Left mouse button
                    self.player.start_charge()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and not self.game_over:  # Left mouse button
                    mouse_x, _ = pygame.mouse.get_pos()
                    self.player.release_jump(mouse_x)
        return True
    
    def run(self):
        """Main game loop."""
        running = True
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Update display and maintain framerate
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit() 