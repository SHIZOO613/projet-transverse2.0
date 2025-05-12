import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, YELLOW, RED
from utils import create_pixel_text
from player import Player
from audio_manager import audio_manager  # Import the audio manager

class GameBase:
    """Classe de base pour les modes de jeu, contenant la logique commune"""
    
    def __init__(self, title="Cloud Jump", game_mode="normal"):
        """Initialiser la classe de base avec les éléments communs aux différents modes"""
        # Configuration de base
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        
        # Store the game mode for audio
        self.game_mode = game_mode
        
        # Start the appropriate music
        audio_manager.play_music(self.game_mode)
        
        # Polices communes
        self.regular_font = pygame.font.Font(None, 36)
        self.pixel_font_large = pygame.font.Font(None, 64)
        self.pixel_font_small = pygame.font.Font(None, 36)
        
        # Joueur et plateformes (initialisés dans les classes dérivées)
        self.player = None
        self.platforms = []
        
        # États du jeu
        self.score = 0
        self.game_over = False
        self.scroll_speed = 0
        self.difficulty = 1.0
    
    def draw_game_over_screen(self):
        """Afficher l'écran de game over avec texte pixelisé"""
        # Overlay semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Texte Game Over
        game_over_text = create_pixel_text("GAME OVER", self.pixel_font_large, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Texte du score
        score_text = create_pixel_text(f"Score: {self.score}", self.pixel_font_small, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        self.screen.blit(score_text, score_rect)
        
        # Instructions pour retourner au menu
        restart_text = create_pixel_text("Press SPACE for menu", self.pixel_font_small, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
        self.screen.blit(restart_text, restart_rect)
    
    def handle_events(self):
        """Gérer les événements utilisateur"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "QUIT"
                elif event.key == pygame.K_SPACE and self.game_over:
                    return "MENU"  # Retour au menu principal
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.game_over:  # Clic gauche
                    if self.player:
                        self.player.start_charge()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and not self.game_over:  # Relâchement du clic gauche
                    if self.player:
                        mouse_x, _ = pygame.mouse.get_pos()
                        self.player.release_jump(mouse_x)
        return "CONTINUE"
    
    def reset(self):
        """Réinitialiser l'état du jeu pour une nouvelle partie"""
        self.player = Player()
        self.score = 0
        self.game_over = False
        self.scroll_speed = 0
        self.difficulty = 1.0
        self.generate_platforms()  # Cette méthode doit être implémentée dans les classes dérivées
    
    def run(self):
        """Boucle principale du jeu"""
        running = True
        result = "CONTINUE"
        
        while running:
            # Gérer les événements
            result = self.handle_events()
            
            if result == "QUIT":
                running = False
            elif result == "MENU":
                # Switch to menu music when returning to the menu
                audio_manager.play_music("menu")
                return "MENU"  # Signal pour retourner au menu
            
            # Mettre à jour l'état du jeu
            self.update()
            
            # Dessiner tous les éléments
            self.draw()
            
            # Mettre à jour l'affichage et maintenir le framerate
            pygame.display.flip()
            self.clock.tick(FPS)
            
        return "QUIT"  # Le jeu s'est terminé par une demande de sortie 