import pygame
from PIL import Image

def scale_image(image_path, target_size, is_pixel_art=True):
    """Scale the image using appropriate algorithm for pixel art or regular images."""
    with Image.open(image_path) as img:
        img = img.convert('RGBA')
        if is_pixel_art:
            # Use nearest neighbor for pixel art to maintain sharp pixels
            img = img.resize(target_size, Image.Resampling.NEAREST)
        else:
            # Use Lanczos for smooth scaling of non-pixel art
            img = img.resize(target_size, Image.Resampling.LANCZOS)
        img_data = img.tobytes()
        return pygame.image.fromstring(img_data, img.size, 'RGBA')


def create_pixel_text(text, font, color, scale_factor=3):
    """Create pixelated text by rendering at small size and scaling up with nearest neighbor."""
    # First render the text at a smaller size
    base_surface = font.render(text, True, color)
    
    # Get the size of the base surface
    width, height = base_surface.get_size()
    
    # Scale it down to create pixelation effect when scaled back up
    small_size = (width // scale_factor, height // scale_factor)
    # Convert to PIL Image for better scaling control
    pil_surface = Image.frombytes('RGBA', (width, height), pygame.image.tostring(base_surface, 'RGBA'))
    pil_surface = pil_surface.resize(small_size, Image.Resampling.NEAREST)
    
    # Scale back up with nearest neighbor sampling for pixelated look
    final_size = (small_size[0] * scale_factor, small_size[1] * scale_factor)
    pil_surface = pil_surface.resize(final_size, Image.Resampling.NEAREST)
    
    # Convert back to Pygame surface
    final_surface = pygame.image.fromstring(pil_surface.tobytes(), final_size, 'RGBA')
    return final_surface 