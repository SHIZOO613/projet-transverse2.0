import pygame
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, ASSETS_DIR, BG_ASSETS_DIR

class LavaBackground:
    """Classe pour gérer le fond de lave simple sans animations"""
    def __init__(self):
        # Charger l'image de fond de lave
        try:
            # Utiliser spécifiquement le fichier background_lava_mode.jpg dans le dossier Lava_background
            bg_path = os.path.join(BG_ASSETS_DIR, "Lava_background", "background_lava_mode.jpg")
            print(f"Chargement du fond spécifique: {bg_path}")
            
            if os.path.exists(bg_path):
                print(f"Fond trouvé à {bg_path}")
                self.background = pygame.image.load(bg_path).convert()
            else:
                raise FileNotFoundError(f"Fichier background_lava_mode.jpg introuvable dans {BG_ASSETS_DIR}/Lava_background")
            
            # Conserver l'échelle originale et centrer l'image
            bg_orig_width = self.background.get_width()
            bg_orig_height = self.background.get_height()
            
            # Calculer le facteur d'échelle pour couvrir l'écran sans déformer l'image
            scale_x = SCREEN_WIDTH / bg_orig_width
            scale_y = SCREEN_HEIGHT / bg_orig_height
            scale = max(scale_x, scale_y)  # Prendre le plus grand pour couvrir tout l'écran
            
            # Appliquer l'échelle
            new_width = int(bg_orig_width * scale)
            new_height = int(bg_orig_height * scale)
            self.background = pygame.transform.scale(self.background, (new_width, new_height))
            
            # Calculer les positions pour centrer
            self.bg_x = (SCREEN_WIDTH - new_width) // 2
            self.bg_y = (SCREEN_HEIGHT - new_height) // 2
                
        except Exception as e:
            print(f"Erreur lors du chargement du fond: {e}")
            # Fallback: créer un fond rouge foncé si l'image ne peut pas être chargée
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((100, 0, 0))  # Rouge foncé pour indiquer un mode lave
            self.bg_x = 0
            self.bg_y = 0
    
    def update(self):
        """Aucune mise à jour nécessaire pour un fond statique"""
        pass
    
    def draw(self, screen):
        """Dessiner uniquement le fond"""
        screen.blit(self.background, (self.bg_x, self.bg_y))
        
    def draw_foreground(self, screen):
        """Dessiner le fond en premier plan (après les autres éléments)"""
        # Créer un effet de premier plan de lave semi-transparent
        foreground = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        foreground.fill((180, 20, 0, 80))  # Rouge semi-transparent
        screen.blit(foreground, (0, 0)) 