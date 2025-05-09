import math
import os
from PIL import Image

from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_ASSETS_DIR
from utils import scale_image

class Background:
    """Manages the parallax scrolling background with multiple layers."""
    
    def __init__(self):
        # Load background layers
        self.layers = []

        # Define the image files in order (from back to front)
        image_files = ["bg_1.png", "bg_2.png", "bg_3.png", "bg_4.png"]

        # Define custom parameters for each layer
        layer_params = [
            {'speed': 0, 'amplitude': 0, 'scale': 1.0, 'y_offset': 0, 'x_offset': 0, 'is_pixel_art': False},
            # Full background, smooth scaling
            {'speed': 0.15, 'amplitude': 4, 'scale': 0.25, 'y_offset': 50, 'x_offset': -100, 'is_pixel_art': True},
            # Cloud silhouette, left side
            {'speed': 0.18, 'amplitude': 5, 'scale': 0.2, 'y_offset': 170, 'x_offset': 120, 'is_pixel_art': True},
            # Thin line, more to the right
            {'speed': 0.2, 'amplitude': 6, 'scale': 0.15, 'y_offset': 250, 'x_offset': -110, 'is_pixel_art': True}
            # Detailed clouds, more to the left
        ]

        for i, (filename, params) in enumerate(zip(image_files, layer_params)):
            image_path = os.path.join(BG_ASSETS_DIR, filename)
            try:
                # Get original image dimensions
                with Image.open(image_path) as img:
                    orig_width, orig_height = img.size

                if i == 0:  # For bg_1.png
                    # Scale to full screen height
                    scale_factor = SCREEN_HEIGHT / orig_height
                else:
                    # For other images, use reduced scale while maintaining aspect ratio
                    base_scale = SCREEN_HEIGHT / orig_height
                    scale_factor = base_scale * params['scale']

                # Calculate new dimensions
                new_width = int(orig_width * scale_factor)
                new_height = int(orig_height * scale_factor)

                # Scale the image with appropriate algorithm
                scaled_image = scale_image(image_path, (new_width, new_height), params['is_pixel_art'])

                # Calculate position with offset from center
                center_x = (SCREEN_WIDTH - new_width) // 2
                x = center_x + params['x_offset']

                # Ensure the image doesn't go completely off screen
                x = max(min(x, SCREEN_WIDTH - new_width // 2), -new_width // 2)

                self.layers.append({
                    'image': scaled_image,
                    'x': x,
                    'y': params['y_offset'],
                    'speed': params['speed'],
                    'amplitude': params['amplitude'],
                    'time': i * 0.5,  # Different phase for each layer
                    'base_y': params['y_offset']  # Store the base y position
                })
            except Exception as e:
                print(f"Couldn't load image {image_path}: {e}")

    def update(self):
        """Update each layer's position for the animated effect."""
        for layer in self.layers:
            if layer['speed'] > 0:  # Only move layers with speed > 0
                layer['time'] += 0.02
                layer['y'] = layer['base_y'] + math.sin(layer['time']) * layer['amplitude']

    def draw(self, screen):
        """Draw all background layers to the screen."""
        for layer in self.layers:
            screen.blit(layer['image'], (layer['x'], layer['y'])) 