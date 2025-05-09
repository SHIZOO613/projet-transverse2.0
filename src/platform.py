import pygame
import random
import math
import os
from config import GREEN, BLUE, YELLOW, RED, PLATFORM_HEIGHT, ASSETS_DIR

class Platform:
    """Plateforme de base sur laquelle le joueur peut sauter."""
    
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.color = GREEN  # Couleur de secours
        self.platform_type = "normal"
        self.friction = 0.85  # Friction normale
        
        # Charger le sprite
        self.sprite = self.load_sprite("normal_platform.png")
        
    def load_sprite(self, filename):
        """Charge le sprite de la plateforme sans redimensionnement."""
        try:
            sprite_path = os.path.join(ASSETS_DIR, "sprites", "platforms", filename)
            sprite = pygame.image.load(sprite_path).convert_alpha()
            return sprite
        except Exception as e:
            print(f"Erreur lors du chargement du sprite {filename}: {e}")
            return None
        
    def update(self, scroll_speed=0):
        """Update platform position, handling scrolling."""
        # Move platform down for scrolling effect
        self.y += scroll_speed
        
    def draw(self, screen):
        """Draw the platform to the screen."""
        if self.sprite:
            # Redimensionner le sprite pour qu'il corresponde à la largeur de la plateforme
            # tout en conservant ses proportions (ratio d'aspect)
            original_width = self.sprite.get_width()
            original_height = self.sprite.get_height()
            
            # Calculer la nouvelle hauteur pour conserver le ratio d'aspect
            scale_factor = self.width / original_width
            new_height = int(original_height * scale_factor)
            
            # Redimensionner le sprite
            scaled_sprite = pygame.transform.scale(self.sprite, (self.width, new_height))
            
            # Dessiner le sprite redimensionné
            screen.blit(scaled_sprite, (self.x, self.y))
        else:
            # Fallback to rectangle if sprite not available
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, PLATFORM_HEIGHT))
        
    def on_landing(self, player):
        """Appelé quand le joueur atterrit sur la plateforme."""
        # La classe de base ne fait rien de spécial
        pass
    
    @staticmethod
    def create_random_platform(x, y, width, difficulty=1.0):
        """Crée une plateforme aléatoire basée sur la difficulté."""
        # Plus la difficulté est élevée, plus il y a de chances d'avoir une plateforme spéciale
        chance = random.random() * difficulty
        
        # Ajuster les seuils en fonction de la difficulté
        # À mesure que la difficulté augmente, les plateformes normales sont moins fréquentes
        ice_threshold = max(0.7, 0.85 - (difficulty - 1.0) * 0.15)      # Descend de 0.85 à 0.7
        moving_threshold = max(0.5, 0.7 - (difficulty - 1.0) * 0.2)     # Descend de 0.7 à 0.5
        breakable_threshold = max(0.3, 0.55 - (difficulty - 1.0) * 0.25) # Descend de 0.55 à 0.3
        
        if chance > ice_threshold:
            return IcePlatform(x, y, width)
        elif chance > moving_threshold:
            return MovingPlatform(x, y, width)
        elif chance > breakable_threshold:
            return BreakablePlatform(x, y, width)
        else:
            return Platform(x, y, width)


class MovingPlatform(Platform):
    """Plateforme qui se déplace verticalement."""
    
    def __init__(self, x, y, width):
        super().__init__(x, y, width)
        self.color = BLUE
        self.platform_type = "moving"
        self.original_y = y
        self.amplitude = random.randint(30, 60)  # Distance de déplacement
        self.speed = random.uniform(0.02, 0.04)  # Vitesse de déplacement
        self.time = random.uniform(0, 2 * math.pi)  # Phase aléatoire
        self.prev_y = y  # Mémoriser la position précédente pour calculer le mouvement
        
        # Charger le sprite spécifique
        self.sprite = self.load_sprite("sliding_platform.png")
        
    def update(self, scroll_speed=0):
        """Mettre à jour la position avec mouvement vertical + défilement."""
        # Mémoriser la position actuelle
        self.prev_y = self.y
        
        # Mettre à jour le mouvement vertical
        self.time += self.speed
        self.y = self.original_y + math.sin(self.time) * self.amplitude
        
        # Ajouter le défilement de l'écran
        self.original_y += scroll_speed
    
    def on_landing(self, player):
        """Ajuster la position du joueur quand la plateforme se déplace."""
        # Si la plateforme monte (position actuelle plus haute que précédente)
        # on n'a rien à faire car le joueur reste naturellement sur la plateforme
        # Mais si elle descend, on doit ajuster la vitesse du joueur
        if self.y > self.prev_y:
            # Calculer le déplacement vertical de la plateforme
            delta_y = self.y - self.prev_y
            # Ajuster la vitesse verticale du joueur pour suivre la plateforme
            # Mais ne pas l'ajuster si le joueur est en train de charger un saut
            if not player.charging:
                player.vel_y = max(0, delta_y)
        # Si la plateforme monte, la collision standard gère déjà le cas


class BreakablePlatform(Platform):
    """Plateforme qui se casse après qu'on l'ait touchée."""
    
    def __init__(self, x, y, width):
        super().__init__(x, y, width)
        self.color = YELLOW
        self.platform_type = "breakable"
        self.breaking = False
        self.break_timer = 0
        self.break_time = 1.8  # Secondes avant de se casser
        
        # Charger le sprite spécifique
        self.sprite = self.load_sprite("breakable_platform.png")
        
    def update(self, scroll_speed=0):
        """Mettre à jour la plateforme, gérer le timer de destruction."""
        super().update(scroll_speed)
        
        if self.breaking:
            self.break_timer += 1/60  # Incrémenter d'1/60 sec (à 60 FPS)
            
            # Modifier l'opacité du sprite en fonction du temps restant
            if self.sprite:
                alpha = 255 * (1 - self.break_timer / self.break_time)
                self.sprite.set_alpha(max(0, int(alpha)))
            else:
                # Mettre à jour la couleur pour un effet visuel si pas de sprite
                progress = min(self.break_timer / self.break_time, 1.0)
                r = int(YELLOW[0] + (RED[0] - YELLOW[0]) * progress)
                g = int(YELLOW[1] + (RED[1] - YELLOW[1]) * progress)
                b = int(YELLOW[2] + (RED[2] - YELLOW[2]) * progress)
                self.color = (r, g, b)
        
    def on_landing(self, player):
        """Déclencher le compte à rebours de destruction."""
        if not self.breaking:
            self.breaking = True
            
    def should_remove(self):
        """Vérifier si la plateforme doit être supprimée."""
        return self.breaking and self.break_timer >= self.break_time


class IcePlatform(Platform):
    """Plateforme glissante avec moins de friction."""
    
    def __init__(self, x, y, width):
        super().__init__(x, y, width)
        self.color = (150, 230, 250)  # Bleu clair pour la glace
        self.platform_type = "ice"
        self.friction = 0.98  # Beaucoup moins de friction
        
        # Charger le sprite spécifique
        self.sprite = self.load_sprite("ice_platform.png")
                            
    def on_landing(self, player):
        """Appliquer un effet de glisse au joueur."""
        # Le joueur utilisera la friction de cette plateforme
        pass 