import pygame
import os
from config import ASSETS_DIR, ANIMATION_SPEED

class Coin:
    """Classe pour les pièces que le joueur peut collecter"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Charger l'animation de la pièce
        self.frames = []
        self.load_animation()
        
        # État de l'animation
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = ANIMATION_SPEED  # Temps en secondes entre chaque frame
        
        # État de la pièce
        self.collected = False
        
    def load_animation(self):
        """Charger les frames d'animation de la pièce à partir des images individuelles"""
        try:
            # Charger chaque image individuellement
            for i in range(5):  # 5 images: coin0, coin1, coin2, coin3, coin4
                sprite_path = os.path.join(ASSETS_DIR, "sprites", "coins", f"coin{i}.png")
                original_image = pygame.image.load(sprite_path).convert_alpha()
                
                # Récupérer les dimensions originales
                orig_width, orig_height = original_image.get_size()
                
                # Calculer le facteur d'échelle pour préserver le ratio d'aspect
                # Utiliser la plus petite dimension pour éviter l'étirement
                scale_factor = min(self.width / orig_width, self.height / orig_height)
                
                # Calculer les nouvelles dimensions
                new_width = int(orig_width * scale_factor)
                new_height = int(orig_height * scale_factor)
                
                # Redimensionner l'image en préservant le ratio d'aspect
                scaled_image = pygame.transform.scale(original_image, (new_width, new_height))
                
                # Créer une surface transparente pour centrer l'image
                frame = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                
                # Dessiner l'image redimensionnée au centre de la surface
                x_offset = (self.width - new_width) // 2
                y_offset = (self.height - new_height) // 2
                frame.blit(scaled_image, (x_offset, y_offset))
                
                self.frames.append(frame)
                
        except Exception as e:
            print(f"Erreur lors du chargement de l'animation de la pièce: {e}")
            # Créer une image par défaut si le chargement échoue
            self.frames = [self.create_fallback_image() for _ in range(5)]
            
    def create_fallback_image(self):
        """Créer une image par défaut pour la pièce en cas d'erreur"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 215, 0), (self.width//2, self.height//2), self.width//2)
        return surface
            
    def update(self, scroll_speed=0):
        """Mettre à jour l'animation de la pièce et sa position"""
        if self.collected:
            return
            
        # Faire défiler la pièce avec le reste du jeu
        self.y += scroll_speed
        self.rect.y = int(self.y)
        
        # Mettre à jour l'animation
        self.animation_timer += 1/60  # Basé sur 60 FPS
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            
    def draw(self, screen):
        """Dessiner la pièce à l'écran"""
        if not self.collected:
            screen.blit(self.frames[self.current_frame], self.rect)
    
    def check_collision(self, player):
        """Vérifier si le joueur a collecté la pièce"""
        if self.collected:
            return False
            
        # Créer un rectangle pour le joueur à partir de ses attributs
        player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
        
        # Vérifier la collision
        if self.rect.colliderect(player_rect):
            self.collected = True
            return True
            
        return False 