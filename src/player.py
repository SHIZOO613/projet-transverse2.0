import pygame
import os
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLUE, WHITE, YELLOW, RED,
    GRAVITY, MAX_CHARGE, CHARGE_RATE, 
    PLAYER_SIZE, JUMP_HORIZONTAL_FACTOR, MAX_HORIZONTAL_DISTANCE,
    PLATFORM_HEIGHT, PROJECT_ROOT, ASSETS_DIR, ANIMATION_SPEED
)

class Player:
    """Player character (frog) with jumping mechanics."""
    
    def __init__(self):
        self.size = PLAYER_SIZE
        self.x = SCREEN_WIDTH // 2 - self.size // 2
        self.y = SCREEN_HEIGHT - 150
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        self.charge = 0
        self.charging = False
        self.color = BLUE  # Gardé comme fallback
        self.jump_target = None
        self.jumping = False
        # Constante de friction par défaut
        self.friction = 0.85
        # Plateforme actuelle sur laquelle le joueur se trouve
        self.current_platform = None
        
        # Animation properties
        self.animation_timer = 0
        self.animation_speed = ANIMATION_SPEED  # Use the constant from config
        self.current_frame = 0
        self.idle_sequence = [0, 1, 2, 3, 2, 1]  # Séquence d'animation idle
        
        # Chargement des sprites
        self.sprites = {
            'idle': [],
            'charge': None,
            'jump': None,
            'sliding': None
        }
        
        # Chargement des sprites Idle
        for i in range(4):
            sprite_path = os.path.join(ASSETS_DIR, "sprites", "frog", "Idle frog", f"frog_idle{i}.png")
            self.sprites['idle'].append(self.load_sprite(sprite_path))
            
        # Chargement des sprites d'action
        action_sprites = {
            'charge': "frog_charge.png",
            'jump': "frog_jump.png",
            'sliding': "frog_sliding.png"
        }
        
        for action, filename in action_sprites.items():
            sprite_path = os.path.join(ASSETS_DIR, "sprites", "frog", "Frog actions", filename)
            self.sprites[action] = self.load_sprite(sprite_path)
            
        # État d'animation actuel
        self.current_animation = 'idle'
        
    def load_sprite(self, path):
        """Charger un sprite et le redimensionner à la taille du joueur en préservant le ratio d'aspect."""
        try:
            sprite = pygame.image.load(path).convert_alpha()
            
            # Récupérer les dimensions originales
            orig_width, orig_height = sprite.get_size()
            aspect_ratio = orig_width / orig_height
            
            # Déterminer la nouvelle taille en préservant le ratio
            if aspect_ratio > 1:  # Plus large que haut
                new_width = self.size
                new_height = int(self.size / aspect_ratio)
            else:  # Plus haut que large ou carré
                new_height = self.size
                new_width = int(self.size * aspect_ratio)
                
            # Créer une surface avec de la transparence pour le sprite
            scaled_sprite = pygame.transform.scale(sprite, (new_width, new_height))
            
            # Créer une surface carrée pour positionner le sprite centré
            final_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            
            # Positionner le sprite centré horizontalement, mais au bas de la surface
            # pour qu'il touche bien la plateforme
            x_offset = (self.size - new_width) // 2
            y_offset = self.size - new_height  # Aligner en bas plutôt que centrer
            final_surface.blit(scaled_sprite, (x_offset, y_offset))
            
            return final_surface
            
        except Exception as e:
            print(f"Erreur lors du chargement du sprite {path}: {e}")
            # Créer une surface de fallback
            surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            surface.fill(self.color)
            return surface
        
    def update(self, platforms):
        """Update player position and state based on physics and collisions."""
        # Mise à jour de l'animation
        self.update_animation()
        
        # Sauvegarder la position précédente pour détecter les franchissements
        prev_y = self.y
        
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Limiter la vitesse maximale de chute pour améliorer les collisions
        # tout en préservant la dynamique du jeu
        max_fall_speed = 15
        if self.vel_y > max_fall_speed:
            self.vel_y = max_fall_speed
        
        # Appliquer la friction lorsque le cube est au sol
        # Utiliser la friction de la plateforme actuelle si elle existe
        if self.on_ground and self.current_platform:
            self.vel_x *= self.current_platform.friction
            
            # Arrêter complètement le mouvement si la vitesse est très faible
            if abs(self.vel_x) < 0.1:
                self.vel_x = 0
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Keep player in bounds horizontally
        if self.x < 0:
            self.x = 0
            self.vel_x = 0
        elif self.x + self.size > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.size
            self.vel_x = 0
            
        # Check for landing on platforms
        old_on_ground = self.on_ground
        self.on_ground = False
        self.current_platform = None
        
        for platform in platforms:
            # Méthode standard de détection de collision
            if self.vel_y > 0:  # Seulement en chute
                # Check if player's bottom is within platform bounds
                if (self.y + self.size >= platform.y and 
                    self.y + self.size <= platform.y + PLATFORM_HEIGHT and
                    self.x + self.size > platform.x and 
                    self.x < platform.x + platform.width):
                    self.on_ground = True
                    self.jumping = False
                    self.y = platform.y - self.size
                    self.vel_y = 0
                    self.current_platform = platform
                    
                    # Si on vient d'atterrir sur la plateforme, déclencher l'événement
                    if not old_on_ground:
                        platform.on_landing(self)
                    
                    break
                    
                # Ajout: vérifier si on a traversé une plateforme entre deux frames
                # C'est-à-dire si la position précédente était au-dessus de la plateforme
                # et la position actuelle est en-dessous
                elif (prev_y + self.size <= platform.y and 
                     self.y + self.size >= platform.y + PLATFORM_HEIGHT and
                     self.x + self.size > platform.x and 
                     self.x < platform.x + platform.width):
                    # On a traversé la plateforme, replacer le joueur au-dessus
                    self.on_ground = True
                    self.jumping = False
                    self.y = platform.y - self.size
                    self.vel_y = 0
                    self.current_platform = platform
                    
                    # Déclencher l'événement d'atterrissage
                    if not old_on_ground:
                        platform.on_landing(self)
                    
                    break
                
        # Charging jump
        if self.charging and self.on_ground:
            self.charge = min(self.charge + CHARGE_RATE, MAX_CHARGE)
            
        # Check if falling off the bottom of the screen -> game over
        if self.y > SCREEN_HEIGHT:
            return "GAME_OVER"
            
        # Camera follow - simplifier le système de caméra pour plus de stabilité
        should_scroll = self.y < SCREEN_HEIGHT // 2 - 50
        return should_scroll
    
    def update_animation(self):
        """Mise à jour de l'animation en fonction de l'état du joueur."""
        # Déterminer l'animation actuelle en fonction de l'état
        if self.charging:
            self.current_animation = 'charge'
        elif self.jumping:
            self.current_animation = 'jump'
        elif abs(self.vel_x) > 1.0 and self.on_ground:
            self.current_animation = 'sliding'
        else:
            self.current_animation = 'idle'
            
        # Mettre à jour le timer d'animation uniquement pour l'animation idle
        if self.current_animation == 'idle':
            self.animation_timer += 1/60  # Assume 60 FPS
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.idle_sequence)
    
    def start_charge(self):
        """Begin charging a jump (when mouse button is pressed)."""
        if self.on_ground:
            self.charging = True
            self.charge = 0
            
    def release_jump(self, target_x):
        """Release a charged jump toward the target x position."""
        if self.charging and self.on_ground:
            self.charging = False
            self.jumping = True
            
            # Calculate initial velocity based on charge
            jump_power = self.charge
            
            # Calculate angle based on target position
            dx = target_x - (self.x + self.size // 2)
            # Limit horizontal distance
            dx = max(min(dx, MAX_HORIZONTAL_DISTANCE), -MAX_HORIZONTAL_DISTANCE)
            
            # Set velocity components
            self.vel_y = -jump_power
            self.vel_x = dx * JUMP_HORIZONTAL_FACTOR
            
            self.jump_target = (target_x, self.y - jump_power * 5)
            self.charge = 0
            
    def predict_trajectory(self):
        """Calculate and return points along predicted jump trajectory."""
        if not self.charging or not self.on_ground:
            return []
            
        # Get mouse position for direction
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - (self.x + self.size // 2)
        # Limit horizontal distance for prediction
        dx = max(min(dx, MAX_HORIZONTAL_DISTANCE), -MAX_HORIZONTAL_DISTANCE)
        
        # Calculate predicted trajectory points
        points = []
        jump_power = self.charge
        pred_x = self.x + self.size // 2
        pred_y = self.y + self.size // 2
        pred_vel_x = dx * JUMP_HORIZONTAL_FACTOR
        pred_vel_y = -jump_power
        
        # Augmenter le nombre de points pour voir une parabole plus complète
        # et tracer la parabole complète sans se soucier des collisions
        for _ in range(50):  # Augmenter pour une trajectoire plus longue
            pred_vel_y += GRAVITY
            pred_x += pred_vel_x
            pred_y += pred_vel_y
            
            # Vérifier uniquement que le point est dans les limites horizontales de l'écran
            # mais continuer à tracer même en dessous de l'écran pour la parabole complète
            if 0 <= pred_x <= SCREEN_WIDTH and pred_y <= SCREEN_HEIGHT + 400:
                points.append((int(pred_x), int(pred_y)))
            
            # Si on sort horizontalement de l'écran ou si on descend trop bas, arrêter
            if pred_x < 0 or pred_x > SCREEN_WIDTH or pred_y > SCREEN_HEIGHT + 500:
                break
            
        return points
            
    def draw(self, screen):
        """Draw the player and related UI elements (charge bar, trajectory)."""
        # Déterminer le sprite à utiliser
        sprite = None
        if self.current_animation == 'idle':
            frame_index = self.idle_sequence[self.current_frame]
            sprite = self.sprites['idle'][frame_index]
        else:
            sprite = self.sprites[self.current_animation]
        
        # Dessiner le sprite
        if sprite:
            # Déterminer si la grenouille doit être retournée horizontalement
            facing_left = False
            
            if self.charging:
                # Pendant la charge, orienter la grenouille vers la position de la souris
                mouse_x, _ = pygame.mouse.get_pos()
                facing_left = mouse_x < self.x + self.size // 2
            else:
                # Sinon, orienter selon la vitesse horizontale
                facing_left = self.vel_x < 0
            
            # Inverser la logique pour corriger l'orientation
            # La grenouille doit regarder dans la direction opposée à celle déterminée précédemment
            if not facing_left:
                sprite = pygame.transform.flip(sprite, True, False)
                
            screen.blit(sprite, (self.x, self.y))
        else:
            # Fallback au rectangle coloré si le sprite n'est pas disponible
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        
        # Draw charge meter if charging
        if self.charging and self.on_ground:
            # Draw charge bar background
            pygame.draw.rect(screen, WHITE, (self.x, self.y - 15, self.size, 10))
            # Draw charge level
            charge_width = int(self.size * (self.charge / MAX_CHARGE))
            pygame.draw.rect(screen, YELLOW, (self.x, self.y - 15, charge_width, 10))
            
            # Draw predicted trajectory
            points = self.predict_trajectory()
            if len(points) > 1:
                # Dessiner des points sur la trajectoire
                for point in points:
                    pygame.draw.circle(screen, RED, point, 2)
                
                # Ajouter une ligne entre les points pour une trajectoire plus visible
                if len(points) >= 2:
                    pygame.draw.lines(screen, RED, False, points, 1) 