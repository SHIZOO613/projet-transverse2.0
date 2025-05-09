import pygame
import os
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, ASSETS_DIR, BG_ASSETS_DIR
from background_manager import BackgroundBase

class IceParticle:
    """Classe pour les particules de neige qui tombent en arrière-plan"""
    def __init__(self, x, y, scale=1.0):
        self.x = x
        self.y = y
        self.scale = scale
        self.fall_speed = 1 + scale  # Les particules plus grandes tombent plus vite
        self.drift_speed = 0.2 + 0.2 * scale  # Dérive horizontale
        self.drift_offset = 0
        self.drift_direction = 1 if pygame.time.get_ticks() % 2 == 0 else -1
        self.size = int(3 * scale)
        self.alpha = min(255, int(150 + scale * 100))
        
        # Créer l'image de la particule
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255, self.alpha), (self.size//2, self.size//2), self.size//2)
    
    def update(self):
        """Mettre à jour la position de la particule"""
        # Faire tomber la particule
        self.y += self.fall_speed
        
        # Appliquer une dérive horizontale
        self.drift_offset += 0.05
        self.x += self.drift_direction * self.drift_speed * math.sin(self.drift_offset)
        
        # Si la particule sort de l'écran, la replacer en haut
        if self.y > SCREEN_HEIGHT:
            self.y = -10
            self.x = pygame.time.get_ticks() % SCREEN_WIDTH
    
    def draw(self, screen):
        """Dessiner la particule"""
        screen.blit(self.image, (int(self.x), int(self.y)))

class IceBackground(BackgroundBase):
    """Classe pour gérer le fond de glace avec des particules de neige"""
    def __init__(self):
        # Initialiser la classe parente
        super().__init__()
        
        # Charger l'image de fond de glace
        try:
            # Utiliser l'image spécifique pour le mode glace
            bg_path = os.path.join(BG_ASSETS_DIR, "Ice_background", "ice_background.jpg")
            print(f"Chargement du fond spécifique: {bg_path}")
            
            # Utiliser la méthode de la classe de base pour charger l'image
            bg_image = self.load_image(bg_path)
            
            if bg_image:
                # Utiliser directement l'image de fond de glace sans teinte additionnelle
                # Utiliser la méthode de la classe de base pour redimensionner l'image
                self.background = self.scale_background(bg_image)
            else:
                raise FileNotFoundError(f"Fichier ice_background.jpg introuvable dans {BG_ASSETS_DIR}/Ice_background")
                
        except Exception as e:
            print(f"Erreur lors du chargement du fond: {e}")
            # Utiliser la méthode de la classe de base pour créer un fond de secours
            self.background = self.create_fallback_background((200, 230, 255))  # Bleu très clair pour indiquer un mode glace
        
        # Créer des particules de neige
        self.snow_particles = []
        for _ in range(50):  # Nombre de particules
            x = pygame.time.get_ticks() % SCREEN_WIDTH
            y = pygame.time.get_ticks() % SCREEN_HEIGHT
            scale = 0.5 + 1.5 * pygame.time.get_ticks() % 100 / 100  # Taille aléatoire entre 0.5 et 2.0
            self.snow_particles.append(IceParticle(x, y, scale))
    
    def add_blue_tint(self, surface):
        """Ajouter une teinte bleue à une surface pour l'effet de glace"""
        tinted = surface.copy()
        # Créer un overlay bleu semi-transparent
        blue_overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        blue_overlay.fill((100, 180, 255, 50))  # Bleu clair semi-transparent
        # Appliquer l'overlay
        tinted.blit(blue_overlay, (0, 0))
        return tinted
    
    def update(self):
        """Mettre à jour les particules de neige"""
        for particle in self.snow_particles:
            particle.update()
    
    def draw(self, screen):
        """Dessiner le fond et les particules de neige"""
        # Dessiner le fond
        screen.blit(self.background, (self.bg_x, self.bg_y))
        
        # Ajouter un léger overlay de brouillard
        fog = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        fog.fill((220, 235, 255, 20))  # Bleu très clair presque blanc
        screen.blit(fog, (0, 0))
        
        # Dessiner les particules de neige
        for particle in self.snow_particles:
            particle.draw(screen) 