import math
import os
from PIL import Image

from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_ASSETS_DIR
from utils import scale_image
from background_manager import BackgroundBase

class Background(BackgroundBase):
    """Gère le fond avec défilement parallaxe à plusieurs couches."""
    
    def __init__(self):
        # Initialiser la classe parente
        super().__init__()
        
        # Charger les couches du fond
        self.layers = []

        # Définir les fichiers image dans l'ordre (arrière-plan à premier plan)
        image_files = ["bg_1.png", "bg_2.png", "bg_3.png", "bg_4.png"]

        # Définir les paramètres personnalisés pour chaque couche
        layer_params = [
            {'speed': 0, 'amplitude': 0, 'scale': 1.0, 'y_offset': 0, 'x_offset': 0, 'is_pixel_art': False},
            # Fond complet, échelle lisse
            {'speed': 0.15, 'amplitude': 4, 'scale': 0.25, 'y_offset': 50, 'x_offset': -100, 'is_pixel_art': True},
            # Silhouette de nuage, côté gauche
            {'speed': 0.18, 'amplitude': 5, 'scale': 0.2, 'y_offset': 170, 'x_offset': 120, 'is_pixel_art': True},
            # Ligne fine, plus à droite
            {'speed': 0.2, 'amplitude': 6, 'scale': 0.15, 'y_offset': 250, 'x_offset': -110, 'is_pixel_art': True}
            # Nuages détaillés, plus à gauche
        ]

        for i, (filename, params) in enumerate(zip(image_files, layer_params)):
            image_path = os.path.join(BG_ASSETS_DIR, filename)
            try:
                # Obtenir les dimensions originales de l'image
                with Image.open(image_path) as img:
                    orig_width, orig_height = img.size

                if i == 0:  # Pour bg_1.png
                    # Échelle à la hauteur d'écran complète
                    scale_factor = SCREEN_HEIGHT / orig_height
                else:
                    # Pour les autres images, utiliser une échelle réduite tout en maintenant le ratio d'aspect
                    base_scale = SCREEN_HEIGHT / orig_height
                    scale_factor = base_scale * params['scale']

                # Calculer les nouvelles dimensions
                new_width = int(orig_width * scale_factor)
                new_height = int(orig_height * scale_factor)

                # Redimensionner l'image avec l'algorithme approprié
                scaled_image = scale_image(image_path, (new_width, new_height), params['is_pixel_art'])

                # Calculer la position avec décalage depuis le centre
                center_x = (SCREEN_WIDTH - new_width) // 2
                x = center_x + params['x_offset']

                # S'assurer que l'image ne sort pas complètement de l'écran
                x = max(min(x, SCREEN_WIDTH - new_width // 2), -new_width // 2)

                self.layers.append({
                    'image': scaled_image,
                    'x': x,
                    'y': params['y_offset'],
                    'speed': params['speed'],
                    'amplitude': params['amplitude'],
                    'time': i * 0.5,  # Phase différente pour chaque couche
                    'base_y': params['y_offset']  # Stocker la position y de base
                })
            except Exception as e:
                print(f"Impossible de charger l'image {image_path}: {e}")

    def update(self):
        """Mettre à jour la position de chaque couche pour l'effet animé."""
        for layer in self.layers:
            if layer['speed'] > 0:  # Ne déplacer que les couches avec vitesse > 0
                layer['time'] += 0.02
                layer['y'] = layer['base_y'] + math.sin(layer['time']) * layer['amplitude']

    def draw(self, screen):
        """Dessiner toutes les couches de fond à l'écran."""
        for layer in self.layers:
            screen.blit(layer['image'], (layer['x'], layer['y'])) 