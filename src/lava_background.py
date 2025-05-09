import pygame
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, ASSETS_DIR, BG_ASSETS_DIR
from background_manager import BackgroundBase

class FireBall:
    """Classe pour les boules de feu dans les coins en utilisant le sprite IdleLoop-Sheet.png"""
    def __init__(self, x, y, scale=1.0):
        self.x = x
        self.y = y
        self.scale = scale
        self.frame = 0
        self.animation_speed = 0.1  # Animation un peu plus rapide
        self.animation_timer = 0
        self.frames = []
        
        try:
            # Charger le sprite IdleLoop-Sheet.png
            sprite_path = os.path.join(BG_ASSETS_DIR, "Lava_background", "IdleLoop-Sheet.png")
            if os.path.exists(sprite_path):
                # Charger l'image
                spritesheet = pygame.image.load(sprite_path).convert_alpha()
                
                # IdleLoop-Sheet.png contient 4 frames pour l'animation de fireball
                # Taille de chaque frame dans la spritesheet
                num_frames = 4  # Nombre de frames dans la spritesheet
                frame_width = spritesheet.get_width() // num_frames
                frame_height = spritesheet.get_height()
                
                # Découper chaque frame de la spritesheet
                for i in range(num_frames):
                    frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
                    frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                    frame.blit(spritesheet, (0, 0), frame_rect)
                    
                    # Redimensionner la frame selon l'échelle
                    scaled_width = int(frame_width * self.scale)
                    scaled_height = int(frame_height * self.scale)
                    scaled_frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
                    
                    # Ajouter à la liste des frames
                    self.frames.append(scaled_frame)
                
                print(f"Animation de fireball chargée avec succès: {num_frames} frames de {frame_width}x{frame_height}, échelle: {self.scale}")
            else:
                raise FileNotFoundError(f"Fichier IdleLoop-Sheet.png introuvable dans {BG_ASSETS_DIR}/Lava_background")
        except Exception as e:
            print(f"Erreur lors du chargement du sprite fireball: {e}")
            # Créer un sprite de secours rouge
            fallback_size = 50
            fallback = pygame.Surface((fallback_size, fallback_size), pygame.SRCALPHA)
            fallback.fill((255, 50, 0))
            scaled_fallback = pygame.transform.scale(fallback, (int(fallback_size * self.scale), int(fallback_size * self.scale)))
            self.frames.append(scaled_fallback)
    
    def update(self):
        """Mettre à jour l'animation"""
        # Si nous avons plusieurs frames, faire l'animation
        if len(self.frames) > 1:
            self.animation_timer += 1/60  # 60 FPS
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.frame = (self.frame + 1) % len(self.frames)
    
    def draw(self, screen):
        """Dessiner la boule de feu"""
        if self.frames:
            screen.blit(self.frames[self.frame], (self.x, self.y))

class LavaBackground(BackgroundBase):
    """Classe pour gérer le fond de lave avec des boules de feu dans les coins"""
    def __init__(self):
        # Initialiser la classe parente
        super().__init__()
        
        # Charger l'image de fond de lave
        try:
            # Utiliser spécifiquement le fichier background_lava_mode.jpg dans le dossier Lava_background
            bg_path = os.path.join(BG_ASSETS_DIR, "Lava_background", "background_lava_mode.jpg")
            print(f"Chargement du fond spécifique: {bg_path}")
            
            # Utiliser la méthode de la classe de base pour charger l'image
            bg_image = self.load_image(bg_path)
            
            if bg_image:
                # Utiliser la méthode de la classe de base pour redimensionner l'image
                self.background = self.scale_background(bg_image)
            else:
                raise FileNotFoundError(f"Fichier background_lava_mode.jpg introuvable dans {BG_ASSETS_DIR}/Lava_background")
                
        except Exception as e:
            print(f"Erreur lors du chargement du fond: {e}")
            # Utiliser la méthode de la classe de base pour créer un fond de secours
            self.background = self.create_fallback_background((100, 0, 0))  # Rouge foncé pour indiquer un mode lave
        
        # Créer les 4 boules de feu dans les 4 coins
        fireball_scale = 3.0  # Échelle plus grande pour le sprite IdleLoop
        
        # Charger la taille du sprite pour positionner correctement
        temp_fireball = FireBall(0, 0, fireball_scale)
        if temp_fireball.frames:
            fb_width = temp_fireball.frames[0].get_width()
            fb_height = temp_fireball.frames[0].get_height()
        else:
            # Valeurs par défaut si le sprite ne charge pas
            fb_width = int(50 * fireball_scale)
            fb_height = int(50 * fireball_scale)
        
        self.fireballs = [
            # Coin supérieur gauche - positionné exactement à (0,0)
            FireBall(0, 0, fireball_scale),
            # Coin supérieur droit - positionné pour que le bord droit soit aligné avec SCREEN_WIDTH
            FireBall(SCREEN_WIDTH - fb_width, 0, fireball_scale),
            # Coin inférieur gauche - positionné pour que le bord inférieur soit aligné avec SCREEN_HEIGHT
            FireBall(0, SCREEN_HEIGHT - fb_height, fireball_scale),
            # Coin inférieur droit - positionné pour que les deux bords soient alignés
            FireBall(SCREEN_WIDTH - fb_width, SCREEN_HEIGHT - fb_height, fireball_scale)
        ]
    
    def update(self):
        """Mettre à jour les animations des boules de feu"""
        for fireball in self.fireballs:
            fireball.update()
    
    def draw(self, screen):
        """Dessiner le fond et les boules de feu"""
        # Dessiner le fond
        screen.blit(self.background, (self.bg_x, self.bg_y))
        
        # Dessiner les boules de feu
        for fireball in self.fireballs:
            fireball.draw(screen)
    
    def draw_foreground(self, screen):
        """Méthode maintenue pour compatibilité, mais non utilisée"""
        pass 