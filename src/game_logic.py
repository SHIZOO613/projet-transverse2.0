import pygame
import random

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, YELLOW, RED,
    MIN_PLATFORM_WIDTH, MAX_PLATFORM_WIDTH, PLATFORM_SPACING,
    add_coins
)
from utils import create_pixel_text
from game_base import GameBase
from background import Background
from player import Player
from game_platform import Platform, MovingPlatform, BreakablePlatform, IcePlatform  # Import from our renamed game_platform classes
from coin import Coin

class Game(GameBase):
    """Mode de jeu normal avec plateformes variées et fond de nuages."""
    
    def __init__(self, player_skin_path):
        # Appel du constructeur de la classe parente
        super().__init__(title="Cloud Jump")
        
        self.player_skin_path = player_skin_path # Store the skin path

        # Initialiser les objets spécifiques à ce mode
        self.background = Background()
        self.player = Player(skin_path=self.player_skin_path) # Pass skin path to Player
        
        # Initialiser le système de pièces
        self.coins = []
        self.coin_count = 0
        
        # Générer les plateformes initiales
        self.generate_platforms()
        
        # Générer les pièces initiales
        self.generate_coins()
        
    def generate_platforms(self):
        """Générer les plateformes initiales pour le jeu."""
        # Vider les plateformes existantes
        self.platforms = []
        
        # Taille fixe de plateforme
        platform_width = 100  # Taille standard pour toutes les plateformes
        
        # Créer la plateforme de sol initiale
        self.platforms.append(Platform(SCREEN_WIDTH//2 - platform_width//2, SCREEN_HEIGHT - 100, platform_width))
        
        # Générer des plateformes aléatoires
        for i in range(12):
            x = random.randint(20, SCREEN_WIDTH - platform_width)
            y = SCREEN_HEIGHT - 200 - i * PLATFORM_SPACING
            
            # Choisir un type de plateforme au hasard avec probabilités différentes
            platform_type = random.choices(
                ["normal", "moving", "ice", "breakable"],
                weights=[0.6, 0.2, 0.1, 0.1],
                k=1
            )[0]
            
            if platform_type == "normal":
                self.platforms.append(Platform(x, y, platform_width))
            elif platform_type == "moving":
                self.platforms.append(MovingPlatform(x, y, platform_width))
            elif platform_type == "ice":
                self.platforms.append(IcePlatform(x, y, platform_width))
            elif platform_type == "breakable":
                self.platforms.append(BreakablePlatform(x, y, platform_width))
    
    def generate_coins(self):
        """Générer des pièces sur certaines plateformes."""
        # Vider la liste des pièces
        self.coins = []
        
        # Placer des pièces sur certaines plateformes (pas toutes)
        for platform in self.platforms:
            # Ne pas placer de pièces sur les plateformes mobiles
            if hasattr(platform, 'platform_type') and platform.platform_type == "moving":
                continue
                
            # 30% de chance d'avoir une pièce sur une plateforme (si ce n'est pas une plateforme mobile)
            if random.random() < 0.3:
                # Positionner la pièce au-dessus de la plateforme
                coin_x = platform.x + platform.width // 2 - 15  # Centrer la pièce (largeur de pièce = 30)
                coin_y = platform.y - 40  # Positionner au-dessus de la plateforme
                self.coins.append(Coin(coin_x, coin_y))
    
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
            
        # Mettre à jour les pièces et vérifier les collisions
        for coin in self.coins:
            coin.update(self.scroll_speed)
            if coin.check_collision(self.player):
                self.coin_count += 1
                
        # Supprimer les pièces collectées ou hors écran
        self.coins = [c for c in self.coins if not c.collected and c.y < SCREEN_HEIGHT + 50]
            
        # Supprimer les plateformes cassées ou qui sont sorties de l'écran
        self.platforms = [p for p in self.platforms if p.y < SCREEN_HEIGHT + 50 and 
                         (not hasattr(p, 'should_remove') or not p.should_remove())]
        
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
            
            # Avec le score qui augmente, ajouter des plateformes plus difficiles
            platform_type_chances = {
                "normal": max(0.1, 0.7 - self.difficulty * 0.25),  # De 0.7 à 0.1
                "moving": 0.2 + self.difficulty * 0.15,  # De 0.2 à 0.5
                "ice": min(0.25, 0.05 + self.difficulty * 0.1),  # De 0.05 à 0.25
                "breakable": min(0.25, 0.05 + self.difficulty * 0.1)  # De 0.05 à 0.25
            }
            
            # Normaliser les probabilités
            total = sum(platform_type_chances.values())
            normalized_chances = {k: v / total for k, v in platform_type_chances.items()}
            
            platform_type = random.choices(
                list(normalized_chances.keys()),
                weights=list(normalized_chances.values()),
                k=1
            )[0]
            
            # Créer la plateforme en fonction du type
            if platform_type == "normal":
                platform = Platform(x, y, platform_width)
            elif platform_type == "moving":
                platform = MovingPlatform(x, y, platform_width)
            elif platform_type == "ice":
                platform = IcePlatform(x, y, platform_width)
            else:  # "breakable"
                platform = BreakablePlatform(x, y, platform_width)
                
            self.platforms.append(platform)
            
            # 30% de chance de placer une pièce sur cette nouvelle plateforme (sauf si c'est une plateforme mobile)
            if platform_type != "moving" and random.random() < 0.3:
                coin_x = x + platform_width // 2 - 15  # Centrer la pièce
                coin_y = y - 40  # Positionner au-dessus de la plateforme
                self.coins.append(Coin(coin_x, coin_y))
    
    def draw(self):
        """Dessiner tous les éléments du jeu à l'écran."""
        # Dessiner le fond
        self.background.draw(self.screen)
        
        # Dessiner les plateformes
        for platform in self.platforms:
            platform.draw(self.screen)
            
        # Dessiner les pièces
        for coin in self.coins:
            coin.draw(self.screen)
        
        # Dessiner le joueur si le jeu est actif
        if not self.game_over:
            self.player.draw(self.screen)
            
            # Dessiner le score avec style pixel art
            score_text = create_pixel_text(f"Score: {self.score}", self.pixel_font_small, WHITE)
            self.screen.blit(score_text, (10, 10))
            
            # Dessiner le compteur de pièces avec style pixel art
            coin_text = create_pixel_text(f"Coins: {self.coin_count}", self.pixel_font_small, YELLOW)
            self.screen.blit(coin_text, (10, 50))
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
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10))
        self.screen.blit(score_text, score_rect)
        
        # Coin text
        coin_text = create_pixel_text(f"Coins: {self.coin_count}", self.pixel_font_small, YELLOW)
        coin_rect = coin_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
        self.screen.blit(coin_text, coin_rect)
        
        # Instruction pour retourner au menu
        restart_text = create_pixel_text("Press SPACE for menu", self.pixel_font_small, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
        self.screen.blit(restart_text, restart_rect)
    
    def reset(self):
        """Reset the game state to start a new game."""
        # Re-initialize player with the stored skin path
        self.player = Player(skin_path=self.player_skin_path) 
        self.score = 0
        self.coin_count = 0
        self.game_over = False
        self.scroll_speed = 0
        self.difficulty = 1.0
        self.generate_platforms()
        self.generate_coins()
    
    def handle_events(self):
        """Handle all user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "QUIT"
                elif event.key == pygame.K_SPACE and self.game_over:
                    # Ajouter les pièces collectées au compteur total
                    add_coins(self.coin_count)
                    return "MENU"  # Retourner au menu principal
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.game_over:  # Left mouse button
                    self.player.start_charge()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and not self.game_over:  # Relâchement du clic gauche
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