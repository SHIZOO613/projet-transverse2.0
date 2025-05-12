import pygame
import os
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLUE, WHITE, YELLOW, RED,
    GRAVITY, MAX_CHARGE, CHARGE_RATE, 
    PLAYER_SIZE, JUMP_HORIZONTAL_FACTOR, MAX_HORIZONTAL_DISTANCE,
    PLATFORM_HEIGHT, PROJECT_ROOT, ASSETS_DIR, ANIMATION_SPEED
)

# Physics constants for projectile motion
# GRAVITY = acceleration due to gravity (pixels/frame²)
# DELTA_T = time step per frame (implicit = 1)
# JUMP_HORIZONTAL_FACTOR = scaling factor for horizontal velocity
# MAX_HORIZONTAL_DISTANCE = constraint on input direction magnitude

# In this simulation, we use a discrete-time approximation to the continuous
# equations of motion, with each frame representing one time step (DELTA_T = 1).
# 
# The full projectile motion equations are:
#  x(t) = x₀ + v₀ₓ·t
#  y(t) = y₀ + v₀ᵧ·t + (1/2)·GRAVITY·t²
#
# For our discrete time steps:
#  x[n+1] = x[n] + vₓ[n]·DELTA_T
#  y[n+1] = y[n] + vᵧ[n]·DELTA_T
#  vᵧ[n+1] = vᵧ[n] + GRAVITY·DELTA_T

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
        
        # Chargement des sprites Idle basé sur le skin sélectionné
        if self.skin_base_path and os.path.exists(self.skin_base_path):
            # Si le skin est le Winter Frog
            if "Winter_frog_skin" in self.skin_base_path:
                self.load_winter_skin_idle()
            # Si le skin est le Yellow Frog
            elif "Yellow_frog_skin" in self.skin_base_path:
                self.load_yellow_skin_idle()
            # Pour le skin par défaut ou autre
            else:
                self.load_idle_animation_from_path(self.skin_base_path)
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
        """
        Calculate and return points along predicted jump trajectory using projectile motion equations.
        
        The trajectory follows classical kinematics equations for projectile motion:
        x(t) = x₀ + v₀ₓ·t
        y(t) = y₀ + v₀ᵧ·t + (1/2)·g·t²
        
        Where:
        - (x₀, y₀) is the initial position
        - (v₀ₓ, v₀ᵧ) are the initial velocity components
        - g is the gravitational acceleration (positive downward)
        - t is time
        """
        if not self.charging or not self.on_ground:
            return []
            
        # Get mouse position for direction vector calculation
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Initial position (x₀, y₀)
        x_0 = self.x + self.size // 2
        y_0 = self.y + self.size // 2
        
        # Calculate direction vector Δx = mouse_x - x₀ (constraint to max horizontal distance)
        delta_x = mouse_x - x_0
        delta_x = max(min(delta_x, MAX_HORIZONTAL_DISTANCE), -MAX_HORIZONTAL_DISTANCE)
        
        # Initial velocity components (v₀ₓ, v₀ᵧ)
        # v₀ₓ = Δx × JUMP_HORIZONTAL_FACTOR
        v_0x = delta_x * JUMP_HORIZONTAL_FACTOR
        
        # v₀ᵧ = -jump_power (negative because y-axis is inverted in screen coordinates)
        jump_power = self.charge
        v_0y = -jump_power
        
        # Trajectory points array for visualization
        points = []
        
        # Simulate projectile motion over discrete time steps
        # x(t) = x₀ + v₀ₓ·t
        # y(t) = y₀ + v₀ᵧ·t + (1/2)·g·t²
        # Discretized as:
        # x[i+1] = x[i] + vₓ[i]
        # y[i+1] = y[i] + vᵧ[i]
        # vᵧ[i+1] = vᵧ[i] + g
        x_t = x_0
        y_t = y_0
        v_x = v_0x
        v_y = v_0y
        
        # Compute trajectory for multiple time steps
        # Using t = 0, Δt, 2Δt, ..., 49Δt
        for t_step in range(50):  # 50 discrete time steps
            # Update velocity due to gravity: vᵧ[i+1] = vᵧ[i] + g
            v_y += GRAVITY
            
            # Update position: x[i+1] = x[i] + vₓ[i], y[i+1] = y[i] + vᵧ[i]
            x_t += v_x
            y_t += v_y
            
            # Bounds checking: only add points within visible area plus some margin
            # for showing complete parabolic arcs
            if 0 <= x_t <= SCREEN_WIDTH and y_t <= SCREEN_HEIGHT + 400:
                points.append((int(x_t), int(y_t)))
            
            # Break if trajectory goes too far outside visible bounds
            if x_t < 0 or x_t > SCREEN_WIDTH or y_t > SCREEN_HEIGHT + 500:
                break
            
        return points
            
    def draw(self, screen, debug=False):
        """Dessine le joueur sur l'écran"""
        # Détermine le sprite à utiliser en fonction de l'animation en cours
        sprite = None
        if self.current_animation == 'idle':
            if self.sprites['idle'] and self.current_frame < len(self.idle_sequence) and self.idle_sequence[self.current_frame] < len(self.sprites['idle']):
                frame_index = self.idle_sequence[self.current_frame]
                sprite = self.sprites['idle'][frame_index]
        elif self.current_animation in self.sprites and self.sprites[self.current_animation]:
            sprite = self.sprites[self.current_animation]
            
        # Dessine le sprite ou un rectangle de couleur si pas de sprite
        if sprite:
            # IMPORTANT: Default sprite orientation is facing RIGHT
            # We need to flip when facing LEFT
            
            # Determine if we should flip the sprite based on direction
            flip_sprite = False
            
            # When jumping, base flipping on horizontal velocity
            if self.jumping and self.vel_x != 0:
                # INVERTED: Flip if moving RIGHT (positive velocity) to match game logic
                flip_sprite = self.vel_x > 0
            # When charging, face toward mouse cursor
            elif self.charging:
                mouse_x, _ = pygame.mouse.get_pos()
                # INVERTED: Flip if cursor is to the RIGHT of player
                flip_sprite = mouse_x > self.x + self.size // 2
            # When sliding or idle, determine based on recent movement
            elif self.current_animation == 'sliding':
                # INVERTED: When sliding, flip if moving RIGHT
                flip_sprite = self.vel_x > 0
            # For idle, we'd ideally remember the last direction
            # Since we don't track that yet, we'll default to facing right
            
            # Create a copy of the sprite so we can flip it if needed
            display_sprite = sprite
            if flip_sprite:
                display_sprite = pygame.transform.flip(sprite, True, False)
                
            # Position the sprite centered on player's position
            sprite_rect = display_sprite.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
            screen.blit(display_sprite, sprite_rect)
        else:
            # Fallback to rectangle if sprite is missing
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
    
        # Draw charge bar when charging
        if self.charging and self.on_ground:
            # Draw charge bar background
            pygame.draw.rect(screen, WHITE, (self.x, self.y - 15, self.size, 10))
            # Draw charge level
            charge_width = int(self.size * (self.charge / MAX_CHARGE))
            pygame.draw.rect(screen, YELLOW, (self.x, self.y - 15, charge_width, 10))
            
            # Draw predicted trajectory
            points = self.predict_trajectory()
            if len(points) > 1:
                # Draw points along trajectory to visualize the discrete time steps
                # of the parametric equation (x(t), y(t))
                for i, point in enumerate(points):
                    # Draw larger points at key positions (start, apex, end)
                    if i == 0:  # Initial position (t = 0)
                        pygame.draw.circle(screen, (255, 0, 0), point, 3)  # Red
                    elif i == len(points) - 1:  # Final position
                        pygame.draw.circle(screen, (255, 0, 0), point, 3)  # Red
                    elif i > 0 and points[i-1][1] > point[1] and i < len(points)-1 and points[i+1][1] > point[1]:
                        # Apex of the parabola (where dy/dt = 0)
                        pygame.draw.circle(screen, (255, 255, 0), point, 3)  # Yellow
                    else:
                        # Regular points along the trajectory
                        pygame.draw.circle(screen, (255, 100, 100), point, 2)  # Light red
                
                # Draw the parametric curve representing the trajectory
                # This visualizes the continuous function (x(t), y(t)) for t ∈ [0, t_max]
                pygame.draw.lines(screen, (255, 0, 0), False, points, 2)
        
        # Affichage du debug
        if debug:
            # Contour du joueur
            pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size), 1)
            
            # Affichage de la charge
            if self.charging:
                charge_height = 5
                charge_width = (self.charge / MAX_CHARGE) * 50
                pygame.draw.rect(screen, RED, (self.x, self.y - 10, charge_width, charge_height))
                
            # Affichage du vecteur de saut
            if self.jump_target:
                points = [
                    (self.x + self.size // 2, self.y + self.size // 2),
                    self.jump_target
                ]
                if len(points) >= 2:
                    pygame.draw.lines(screen, RED, False, points, 1)

    def load_winter_skin_idle(self):
        """Load the Winter frog skin idle animation"""
        self.sprites['idle'] = []
        winter_idle_folder = os.path.dirname(self.skin_base_path)
        
        # Try to load all 4 idle frames
        for i in range(4):
            sprite_path = os.path.join(winter_idle_folder, f"frog_idle{i}_winter.png")
            loaded_sprite = self.load_sprite(sprite_path)
            if loaded_sprite:
                self.sprites['idle'].append(loaded_sprite)
            else:
                print(f"Warning: Failed to load Winter idle sprite: {sprite_path}")
        
        # If we loaded any sprites, update the sequence
        if self.sprites['idle']:
            if len(self.sprites['idle']) >= 4:
                self.idle_sequence = [0, 1, 2, 3, 2, 1]
            else:
                self.idle_sequence = list(range(len(self.sprites['idle'])))
                if len(self.sprites['idle']) > 1:
                    self.idle_sequence += list(range(len(self.sprites['idle']) - 2, 0, -1))
        else:
            print("Warning: Could not load any Winter skin idle sprites. Falling back to default.")
            self.load_default_idle_sprites()
    
    def load_yellow_skin_idle(self):
        """Load the Yellow frog skin idle animation"""
        self.sprites['idle'] = []
        yellow_idle_folder = os.path.dirname(self.skin_base_path)
        
        # Keep track if we successfully loaded any frames
        frames_loaded = 0
        
        # Try to load all 4 idle frames with correct naming
        for i in range(4):
            # First try with the correct spelling
            sprite_path = os.path.join(yellow_idle_folder, f"frog_idle{i}_hiver_jaune_clair.png")
            
            # If the file doesn't exist, try alternative spelling
            if not os.path.exists(sprite_path):
                sprite_path = os.path.join(yellow_idle_folder, f"frog_idle{i}_hiver_jauen_clair.png")
            
            if os.path.exists(sprite_path):
                loaded_sprite = self.load_sprite(sprite_path)
                if loaded_sprite:
                    self.sprites['idle'].append(loaded_sprite)
                    frames_loaded += 1
                else:
                    print(f"Warning: Failed to load Yellow idle sprite: {sprite_path}")
            else:
                print(f"Warning: Could not find Yellow idle sprite with index {i}")
        
        # If we loaded at least one frame, make sure we have something for the animation
        if frames_loaded > 0:
            print(f"Loaded {frames_loaded} frames for Yellow frog idle animation")
            # If we have fewer than 4 frames, duplicate the last frame until we have at least 4
            while len(self.sprites['idle']) < 4:
                self.sprites['idle'].append(self.sprites['idle'][frames_loaded - 1])
            
            # Use the standard idle sequence now that we have 4 frames
            self.idle_sequence = [0, 1, 2, 3, 2, 1]
        else:
            print("Warning: Could not load any Yellow skin idle sprites. Falling back to default.")
            self.load_default_idle_sprites()
    
    def load_idle_animation_from_path(self, path):
        """Load idle animation from a given path, assuming a naming convention"""
        self.sprites['idle'] = []
        base_name, ext = os.path.splitext(os.path.basename(path))
        dir_name = os.path.dirname(path)
        
        loaded_idle_sprites = 0
        if base_name.endswith('0'):  # Check if it looks like a sequence start (e.g., frog_idle0)
            name_prefix = base_name[:-1]  # e.g., frog_idle
            for i in range(4):  # Try to load 4 frames
                frame_path = os.path.join(dir_name, f"{name_prefix}{i}{ext}")
                if os.path.exists(frame_path):
                    self.sprites['idle'].append(self.load_sprite(frame_path))
                    loaded_idle_sprites += 1
                else:
                    break
        
        if not loaded_idle_sprites:  # If sequence loading failed
            # Load just the single provided path as the only idle sprite
            self.sprites['idle'].append(self.load_sprite(path))
            self.idle_sequence = [0]  # Only one frame
        elif loaded_idle_sprites < 4 and loaded_idle_sprites > 0:
            # Adjust sequence for partial frames
            self.idle_sequence = list(range(loaded_idle_sprites))
            if loaded_idle_sprites > 1:
                self.idle_sequence += list(range(loaded_idle_sprites - 2, 0, -1))
        
        if not self.sprites['idle']:  # Ultimate fallback
            print(f"Warning: Could not load any idle sprites from {path}. Falling back to default.")
            self.load_default_idle_sprites() 