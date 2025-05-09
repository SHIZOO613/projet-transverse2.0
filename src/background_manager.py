import pygame
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, ASSETS_DIR, BG_ASSETS_DIR

class BackgroundBase:
    """Classe de base pour tous les fonds du jeu."""
    
    def __init__(self):
        """Initialiser les propriétés communes."""
        self.bg_x = 0
        self.bg_y = 0
    
    def scale_background(self, image, maintain_aspect_ratio=True):
        """Redimensionner une image de fond pour couvrir l'écran."""
        if not image:
            return None
            
        # Récupérer les dimensions originales
        bg_orig_width = image.get_width()
        bg_orig_height = image.get_height()
        
        if maintain_aspect_ratio:
            # Calculer le facteur d'échelle pour couvrir l'écran sans déformer l'image
            scale_x = SCREEN_WIDTH / bg_orig_width
            scale_y = SCREEN_HEIGHT / bg_orig_height
            scale = max(scale_x, scale_y)  # Prendre le plus grand pour couvrir tout l'écran
            
            # Appliquer l'échelle
            new_width = int(bg_orig_width * scale)
            new_height = int(bg_orig_height * scale)
        else:
            # Redimensionner pour remplir l'écran sans maintenir le ratio
            new_width = SCREEN_WIDTH
            new_height = SCREEN_HEIGHT
        
        # Redimensionner l'image
        scaled_image = pygame.transform.scale(image, (new_width, new_height))
        
        # Calculer les positions pour centrer
        self.bg_x = (SCREEN_WIDTH - new_width) // 2
        self.bg_y = (SCREEN_HEIGHT - new_height) // 2
        
        return scaled_image
    
    def create_fallback_background(self, color=(0, 0, 0)):
        """Créer un fond uni de secours si l'image ne peut pas être chargée."""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill(color)
        self.bg_x = 0
        self.bg_y = 0
        return background
    
    def load_image(self, path, convert_alpha=False):
        """Charger une image avec gestion d'erreur."""
        try:
            if os.path.exists(path):
                if convert_alpha:
                    return pygame.image.load(path).convert_alpha()
                else:
                    return pygame.image.load(path).convert()
            else:
                print(f"Erreur: Fichier introuvable: {path}")
                return None
        except Exception as e:
            print(f"Erreur lors du chargement de l'image {path}: {e}")
            return None
    
    def update(self):
        """Méthode à implémenter dans les classes dérivées."""
        pass
    
    def draw(self, screen):
        """Méthode à implémenter dans les classes dérivées."""
        pass 