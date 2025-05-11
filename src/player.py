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
    
    def __init__(self, skin_path=None):
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
        
        # Store the base path for the skin if provided
        self.skin_base_path = skin_path 

        # Chargement des sprites
        self.sprites = {
            'idle': [],
            'charge': None,
            'jump': None,
            'sliding': None
        }
        
        # Chargement des sprites Idle
        # If a specific skin_path for an idle animation is provided, try to use it and its sequence.
        # Otherwise, fall back to default idle animation.
        if self.skin_base_path and os.path.exists(self.skin_base_path):
            # Assuming skin_base_path is the path to the first idle frame (e.g., .../frog_idle0.png)
            # We need a way to get other frames if it's an animation.
            # For simplicity, let's assume the provided skin_path is the *only* idle frame for now,
            # or that it implies a naming convention we can derive.
            
            # Attempt to load a sequence if the path suggests it (e.g., ends with 0.png)
            base_name, ext = os.path.splitext(os.path.basename(self.skin_base_path))
            dir_name = os.path.dirname(self.skin_base_path)
            
            loaded_idle_sprites = 0
            if base_name.endswith('0'): # Check if it looks like a sequence start (e.g., frog_idle0)
                name_prefix = base_name[:-1] # e.g., frog_idle
                for i in range(4): # Try to load 4 frames like the default
                    frame_path = os.path.join(dir_name, f"{name_prefix}{i}{ext}")
                    if os.path.exists(frame_path):
                        self.sprites['idle'].append(self.load_sprite(frame_path))
                        loaded_idle_sprites += 1
                    else:
                        # If a frame is missing in the sequence, stop for this skin
                        # or we could just load what's available.
                        # For now, if one is missing, we might have an incomplete animation.
                        break 
            
            if not loaded_idle_sprites: # If sequence loading failed or not applicable
                # Load just the single provided skin_path as the only idle sprite
                self.sprites['idle'].append(self.load_sprite(self.skin_base_path))
                self.idle_sequence = [0] # Only one frame in the sequence
            elif loaded_idle_sprites < 4 and loaded_idle_sprites > 0:
                # If we loaded some but not all 4, adjust idle_sequence
                self.idle_sequence = list(range(loaded_idle_sprites)) 
                # Could make a more complex sequence like [0,1,..,n-1, n-2, ..., 1] if more than 1 frame
                if loaded_idle_sprites > 1:
                    self.idle_sequence += list(range(loaded_idle_sprites - 2, 0, -1))
                else: # single frame
                    self.idle_sequence = [0]

            if not self.sprites['idle'] : # Ultimate fallback if all loading failed
                print(f"Warning: Could not load any idle sprites for skin {self.skin_base_path}. Falling back to default idle.")
                self.load_default_idle_sprites()

        else:
            # Fallback to default idle animation if no skin_path or path doesn't exist
            if skin_path: # only print warning if a path was given but not found
                print(f"Warning: Skin path {skin_path} not found. Loading default player idle sprites.")
            self.load_default_idle_sprites()
            
        # Chargement des sprites d'action
        action_sprite_source_files = {
            'charge': "frog_charge.png",
            'jump': "frog_jump.png",
            'sliding': "frog_sliding.png"
        }
        
        actions_folder_path = os.path.join(ASSETS_DIR, "sprites", "frog", "Frog actions") # Default path

        # Check if a specific skin path is provided and try to use its action sprites
        if self.skin_base_path and "Winter_frog_skin" in self.skin_base_path:
            # Try to determine the actions folder for the Winter skin
            winter_skin_root_folder = os.path.dirname(os.path.dirname(self.skin_base_path)) 
            potential_winter_actions_folder = os.path.join(winter_skin_root_folder, "winter_frogactions")
            
            if os.path.isdir(potential_winter_actions_folder):
                actions_folder_path = potential_winter_actions_folder
                action_sprite_source_files['charge'] = "frog_charge_winter.png"
                action_sprite_source_files['jump'] = "frog_jump_winter.png"
                action_sprite_source_files['sliding'] = "frog_sliding_winter.png"
                print(f"Log: Using Winter skin action sprites from {actions_folder_path}")
            else:
                print(f"Warning: Winter skin actions folder not found at {potential_winter_actions_folder}. Using default action sprites.")
        
        elif self.skin_base_path and "Yellow_frog_skin" in self.skin_base_path:
            # Try to determine the actions folder for the Yellow skin
            yellow_skin_root_folder = os.path.dirname(os.path.dirname(self.skin_base_path)) # Path: .../skins/Yellow_frog_skin/
            potential_yellow_actions_folder = os.path.join(yellow_skin_root_folder, "winter_frogactions") # The folder is named winter_frogactions
            
            if os.path.isdir(potential_yellow_actions_folder):
                actions_folder_path = potential_yellow_actions_folder
                action_sprite_source_files['charge'] = "frog_charge_hiver_jaune_clair.png"
                action_sprite_source_files['jump'] = "frog_jump_hiver_jaune_clair.png"
                action_sprite_source_files['sliding'] = "frog_sliding_hiver_jaune_clair.png"
                print(f"Log: Using Yellow skin action sprites from {actions_folder_path}")
            else:
                print(f"Warning: Yellow skin actions folder not found at {potential_yellow_actions_folder}. Using default action sprites.")
        else:
            print(f"Log: Using default action sprites from {actions_folder_path}")

        for action_key, filename in action_sprite_source_files.items():
            sprite_path = os.path.join(actions_folder_path, filename)
            if os.path.exists(sprite_path):
                self.sprites[action_key] = self.load_sprite(sprite_path)
            else:
                print(f"Warning: Action sprite not found: {sprite_path}. Player.{action_key} will be None.")
                # Fallback: if an action sprite is missing, Player.draw will use the fallback color for that action
                self.sprites[action_key] = None # Explicitly set to None
            
        # État d'animation actuel
        self.current_animation = 'idle'
        
    def load_default_idle_sprites(self):
        """Loads the default idle animation sequence."""
        self.sprites['idle'] = [] # Clear any previous attempts
        self.idle_sequence = [0, 1, 2, 3, 2, 1] # Reset to default sequence
        default_idle_folder = os.path.join(ASSETS_DIR, "sprites", "frog", "Idle frog")
        for i in range(4):
            sprite_path = os.path.join(default_idle_folder, f"frog_idle{i}.png")
            loaded_sprite = self.load_sprite(sprite_path)
            if loaded_sprite: # Check if sprite loaded successfully
                 self.sprites['idle'].append(loaded_sprite)
            else:
                print(f"Error: Failed to load default idle sprite: {sprite_path}")
                # Handle error, e.g. by adding a placeholder or stopping
        if not self.sprites['idle']:
            print("CRITICAL: Could not load ANY default idle sprites. Player will be invisible or use fallback color.")
            # Add a colored square as an absolute fallback for idle if all fails
            fallback_sprite = pygame.Surface((self.size, self.size))
            fallback_sprite.fill(self.color)
            self.sprites['idle'].append(fallback_sprite)
            self.idle_sequence = [0]

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
        prev_platform = self.current_platform
        
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Limiter la vitesse maximale de chute pour améliorer les collisions
        max_fall_speed = 15
        if self.vel_y > max_fall_speed:
            self.vel_y = max_fall_speed
        
        # Appliquer la friction lorsque le cube est au sol
        if self.on_ground and self.current_platform:
            # Si on est sur une plateforme mobile, ajuster la vitesse horizontale
            if self.current_platform.platform_type == "moving":
                # Conserver une partie de la vitesse horizontale pour un mouvement plus fluide
                self.vel_x *= 0.95
            else:
                # Pour les autres plateformes, utiliser leur friction normale
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
            if self.vel_y > 0 or (old_on_ground and platform == prev_platform):  # Chute ou déjà sur la plateforme
                # Check if player's bottom is within platform bounds
                if (self.y + self.size >= platform.y and 
                    self.y + self.size <= platform.y + PLATFORM_HEIGHT and
                    self.x + self.size > platform.x and 
                    self.x < platform.x + platform.width):
                    
                    self.on_ground = True
                    self.jumping = False
                    self.current_platform = platform
                    
                    # Gestion spéciale pour les plateformes mobiles
                    if platform.platform_type == "moving":
                        # Calculer le delta de mouvement de la plateforme
                        platform_delta_y = platform.y - platform.prev_y if hasattr(platform, 'prev_y') else 0
                        
                        # Si la plateforme monte, donner un petit boost au joueur
                        if platform_delta_y < 0:
                            self.vel_y = min(platform_delta_y * 1.2, 0)
                        # Si la plateforme descend, suivre son mouvement
                        elif platform_delta_y > 0:
                            self.vel_y = platform_delta_y
                        
                        # Ajuster la position Y pour rester collé à la plateforme
                        self.y = platform.y - self.size
                    else:
                        # Pour les plateformes normales
                        self.y = platform.y - self.size
                        self.vel_y = 0
                    
                    # Si on vient d'atterrir sur la plateforme, déclencher l'événement
                    if not old_on_ground or platform != prev_platform:
                        platform.on_landing(self)
                    
                    break
                
                # Ajout: vérifier si on a traversé une plateforme entre deux frames
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
        
        # Si le joueur charge un saut et qu'il est sur une plateforme mobile
        if self.charging and self.on_ground and self.current_platform and self.current_platform.platform_type == "moving":
            # Assurer que le joueur reste collé à la plateforme pendant qu'il charge
            self.y = self.current_platform.y - self.size
            # Ajuster la vitesse verticale pour suivre la plateforme
            platform_delta_y = self.current_platform.y - (self.current_platform.prev_y if hasattr(self.current_platform, 'prev_y') else self.current_platform.y)
            self.vel_y = platform_delta_y
        
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
        # Déterminer le sprite de base à utiliser
        base_sprite = None
        if self.current_animation == 'idle':
            if self.sprites['idle']: # Check if idle sprites are loaded
                frame_index = self.idle_sequence[self.current_frame % len(self.idle_sequence)] # Ensure index is valid
                if frame_index < len(self.sprites['idle']): # Double check index validity
                    base_sprite = self.sprites['idle'][frame_index]
                else:
                    print(f"Warning: Invalid frame_index {frame_index} for idle animation.")
                    # Fallback to first idle frame or default color if very broken
                    if self.sprites['idle']:
                         base_sprite = self.sprites['idle'][0]
            if not base_sprite: # If still no base_sprite, use fallback color
                 # This case should be rare if load_default_idle_sprites has its own fallback
                pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
                # Draw charge bar and trajectory even with fallback color
                if self.charging and self.on_ground:
                    pygame.draw.rect(screen, WHITE, (self.x, self.y - 15, self.size, 10))
                    charge_width = int(self.size * (self.charge / MAX_CHARGE))
                    pygame.draw.rect(screen, YELLOW, (self.x, self.y - 15, charge_width, 10))
                    points = self.predict_trajectory()
                    if len(points) > 1:
                        pygame.draw.lines(screen, RED, False, points, 1)
                return # Exit early if using fallback color

        else: # For 'charge', 'jump', 'sliding'
            base_sprite = self.sprites[self.current_animation]
        
        # Si base_sprite n'a pas pu être déterminé (même pour les actions), utiliser le fallback
        if not base_sprite:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
            # Draw charge bar and trajectory even with fallback color
            if self.charging and self.on_ground:
                pygame.draw.rect(screen, WHITE, (self.x, self.y - 15, self.size, 10))
                charge_width = int(self.size * (self.charge / MAX_CHARGE))
                pygame.draw.rect(screen, YELLOW, (self.x, self.y - 15, charge_width, 10))
                points = self.predict_trajectory()
                if len(points) > 1:
                    pygame.draw.lines(screen, RED, False, points, 1)
            return # Exit early

        # Déterminer si la grenouille doit être retournée horizontalement
        should_flip = False
        if self.charging:
            mouse_x, _ = pygame.mouse.get_pos()
            if mouse_x < self.x + self.size // 2: # Souris à gauche du joueur
                should_flip = True
        elif self.vel_x != 0: # Si le joueur bouge horizontalement
            if self.vel_x < 0: # Bouge vers la gauche
                should_flip = True
        # Si vel_x est 0 et pas en charge, on garde la dernière orientation (pas de flip ici, sprite est déjà orienté)

        # Appliquer le flip si nécessaire
        sprite_to_draw = base_sprite
        if should_flip:
            sprite_to_draw = pygame.transform.flip(base_sprite, True, False)
            
        screen.blit(sprite_to_draw, (self.x, self.y))
        
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