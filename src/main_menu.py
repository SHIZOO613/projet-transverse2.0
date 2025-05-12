import pygame
import os
import sys
from utils import create_pixel_text
from background import Background
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, ASSETS_DIR, WHITE, YELLOW, get_total_coins, BLACK, get_high_score, ORANGE

class Button:
    def __init__(self, x, y, width, height):
        # Charger les images des boutons
        button_path = os.path.join(ASSETS_DIR, "Main menu", "Buttons")
        self.normal_img = pygame.image.load(os.path.join(button_path, "Button_basic.png"))
        self.pressed_img = pygame.image.load(os.path.join(button_path, "Button_pushed.png"))
        
        # Conserver le ratio d'aspect original mais redimensionner à la taille demandée
        original_width = self.normal_img.get_width()
        original_height = self.normal_img.get_height()
        aspect_ratio = original_width / original_height
        
        # Redimensionner en conservant le ratio
        self.width = width
        self.height = int(width / aspect_ratio) if width > 0 else original_height
        
        # Redimensionner les deux sprites
        self.normal_img = pygame.transform.scale(self.normal_img, (self.width, self.height))
        self.pressed_img = pygame.transform.scale(self.pressed_img, (self.width, self.height))
        
        # Centrer le bouton à la position demandée
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_pressed = False
        
        # Créer le texte "START" en style pixel art
        self.font = pygame.font.Font(None, 36)
        self.text = create_pixel_text("START", self.font, (0, 0, 0))
        
        # Centrer le texte sur le bouton
        self.text_rect = self.text.get_rect(center=self.rect.center)
        
        # Position du texte pour l'état pressé (légèrement plus bas)
        self.text_rect_pressed = self.text.get_rect(center=(self.rect.centerx, self.rect.centery + 3))
        
    def draw(self, screen):
        # Dessiner le bouton (normal ou pressé)
        if self.is_pressed:
            screen.blit(self.pressed_img, self.rect)
            # Utiliser la position ajustée pour le texte pressé
            screen.blit(self.text, self.text_rect_pressed)
        else:
            screen.blit(self.normal_img, self.rect)
            # Utiliser la position normale pour le texte
            screen.blit(self.text, self.text_rect)
        
    def check_press(self, pos):
        """Vérifie si le bouton est pressé."""
        if self.rect.collidepoint(pos):
            self.is_pressed = True
            return True
        return False
    
    def check_release(self, pos):
        """Vérifie si le bouton est relâché et était pressé auparavant."""
        was_pressed = self.is_pressed
        if self.is_pressed:
            self.is_pressed = False
            # Vérifier si la souris est toujours sur le bouton lors du relâchement
            if self.rect.collidepoint(pos):
                return True
        return False
        
    def reset(self):
        self.is_pressed = False

class SkinButton:
    def __init__(self, x, y, width, height, image_path, screen_width_for_aspect):
        self.image_path = image_path
        
        # Load character skin image
        try:
            self.original_image = pygame.image.load(image_path)
        except pygame.error as e:
            print(f"Warning: Could not load skin image at {image_path}: {e}")
            # Fallback to a placeholder surface if image loading fails
            self.original_image = pygame.Surface((50, 50)) # Default placeholder size
            self.original_image.fill(WHITE) # Fill with white
            pygame.draw.rect(self.original_image, BLACK, self.original_image.get_rect(), 1) # Add a border
            text_surface = create_pixel_text("?", pygame.font.Font(None, 30), BLACK)
            text_rect = text_surface.get_rect(center=self.original_image.get_rect().center)
            self.original_image.blit(text_surface, text_rect)

        # Load cadre images
        cadre_path = os.path.join(ASSETS_DIR, "sprites", "frog", "cadre")
        try:
            self.normal_cadre = pygame.image.load(os.path.join(cadre_path, "cadre_skins.png"))
            self.pushed_cadre = pygame.image.load(os.path.join(cadre_path, "cadre_skins_pushed.png"))
        except pygame.error as e:
            print(f"Warning: Could not load cadre images: {e}")
            # Fallback to simple rectangles if cadre images fail to load
            self.normal_cadre = None
            self.pushed_cadre = None

        # Store original dimensions for skin sizing
        self.original_width = width
        self.original_height = height
        
        # Preserve aspect ratio of the original skin image
        orig_width = self.original_image.get_width()
        orig_height = self.original_image.get_height()
        img_aspect_ratio = orig_width / orig_height
        
        # Keep skin size relative to original dimensions
        scale_factor = 0.6  # This is for skin sizing
        max_width = self.original_width * scale_factor
        max_height = self.original_height * scale_factor
        
        # Calculate the dimensions that preserve aspect ratio
        if max_width / img_aspect_ratio <= max_height:
            # Width is the limiting factor
            img_width = max_width
            img_height = img_width / img_aspect_ratio
        else:
            # Height is the limiting factor
            img_height = max_height
            img_width = img_height * img_aspect_ratio
        
        # Scale the character image to the calculated dimensions
        self.image = pygame.transform.scale(self.original_image, (int(img_width), int(img_height)))
        
        # For the cadre, make it larger (135% of original size)
        cadre_scale = 1.35  # Increased from 1.25 to 1.35
        cadre_target_width = int(width * cadre_scale)
        cadre_target_height = int(height * cadre_scale)
        
        # For the cadre, use its native aspect ratio but scale to fit the target dimensions
        if self.normal_cadre and self.pushed_cadre:
            cadre_orig_width = self.normal_cadre.get_width()
            cadre_orig_height = self.normal_cadre.get_height()
            cadre_aspect = cadre_orig_width / cadre_orig_height
            
            # Calculate dimensions that preserve the cadre's aspect ratio
            if cadre_target_width / cadre_aspect <= cadre_target_height:
                # Width is the limiting factor
                cadre_width = cadre_target_width
                cadre_height = cadre_width / cadre_aspect
            else:
                # Height is the limiting factor
                cadre_height = cadre_target_height
                cadre_width = cadre_height * cadre_aspect
            
            # Scale the cadre images while preserving aspect ratio
            self.normal_cadre = pygame.transform.scale(self.normal_cadre, (int(cadre_width), int(cadre_height)))
            self.pushed_cadre = pygame.transform.scale(self.pushed_cadre, (int(cadre_width), int(cadre_height)))
            
            # Update dimensions to match cadre size
            self.width = int(cadre_width)
            self.height = int(cadre_height)
        else:
            # If no cadre, use original dimensions
            self.width = width
            self.height = height
        
        # Center the button horizontally at x
        self.x = x - self.width // 2
        # Adjust y to keep the bottom of the button at the same position
        self.y = y - (self.height - height)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_pressed = False
        self.is_selected = False # To indicate if this skin is currently selected
        
        # Create green dot for selection indicator
        self.dot_radius = 6
        self.dot_color = (0, 255, 0)  # Bright green
        # Position the dot centered below the button
        self.dot_pos = (self.x + self.width // 2, self.y + self.height + self.dot_radius + 2)

    def draw(self, screen):
        # First draw the appropriate cadre
        if self.is_selected:
            if self.pushed_cadre:
                screen.blit(self.pushed_cadre, self.rect)
            else:
                pygame.draw.rect(screen, YELLOW, self.rect, 3)
            
            # Draw green dot instead of "SELECTED" text
            pygame.draw.circle(screen, self.dot_color, self.dot_pos, self.dot_radius)
            
        elif self.is_pressed:
            if self.pushed_cadre:
                screen.blit(self.pushed_cadre, self.rect)
            else:
                pygame.draw.rect(screen, WHITE, self.rect, 3)
        else:
            if self.normal_cadre:
                screen.blit(self.normal_cadre, self.rect)
            else:
                pygame.draw.rect(screen, BLACK, self.rect, 1)
                
        # Calculate the exact center position for the skin image
        char_x = self.x + (self.width - self.image.get_width()) // 2
        char_y = self.y + (self.height - self.image.get_height()) // 2
        
        # Draw the character image precisely centered on the cadre
        screen.blit(self.image, (char_x, char_y))

    def check_press(self, pos):
        if self.rect.collidepoint(pos):
            self.is_pressed = True
            return True
        return False
    
    def check_release(self, pos):
        was_pressed = self.is_pressed
        self.is_pressed = False # Reset pressed state on release, regardless of where mouse is
        if was_pressed and self.rect.collidepoint(pos):
            return True
        return False
        
    def reset(self):
        self.is_pressed = False
        # self.is_selected = False # Do not reset selection on general reset, only on new selection

class MainMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cloud Jump - Main Menu")
        self.clock = pygame.time.Clock()
        
        # Charger les deux frames du logo pour l'animation
        logo_path = os.path.join(ASSETS_DIR, "Main menu", "Logo", "Main Logo.png")
        logo_second_frame_path = os.path.join(ASSETS_DIR, "Main menu", "Logo", "Main_ Logo_secondframe.png")
        
        # Charger les deux images
        self.logo_frames = []
        self.logo_frames.append(pygame.image.load(logo_path))
        
        try:
            self.logo_frames.append(pygame.image.load(logo_second_frame_path))
        except pygame.error as e:
            print(f"Warning: Could not load second logo frame: {e}")
            # En cas d'erreur, dupliquer le premier frame comme fallback
            self.logo_frames.append(self.logo_frames[0])
        
        # Variables d'animation
        self.logo_animation_speed = 0.5  # Secondes par frame
        self.logo_animation_timer = 0
        self.current_logo_frame = 0
        
        # Redimensionner les frames du logo
        for i in range(len(self.logo_frames)):
            logo_width = min(SCREEN_WIDTH * 0.99, self.logo_frames[i].get_width() * 6.5)
            logo_height = logo_width * (self.logo_frames[i].get_height() / self.logo_frames[i].get_width())
            self.logo_frames[i] = pygame.transform.scale(self.logo_frames[i], (int(logo_width), int(logo_height)))
        
        # Positionner le logo
        self.logo_rect = self.logo_frames[0].get_rect(centerx=SCREEN_WIDTH//2, top=SCREEN_HEIGHT//30)
        
        # Police pour le compteur de pièces
        self.font = pygame.font.Font(None, 36)
        
        # Créer le bouton de démarrage
        button_width = 250  # Taille plus grande pour le bouton
        button_x = SCREEN_WIDTH//2
        
        # Ajuster les positions verticales pour les trois boutons
        start_button_y = SCREEN_HEIGHT//2 - 60  # Encore plus remonté
        lava_button_y = SCREEN_HEIGHT//2 + 20   # Encore plus remonté
        ice_button_y = SCREEN_HEIGHT//2 + 100   # Encore plus remonté
        
        # Créer les boutons
        self.start_button = Button(button_x, start_button_y, button_width, 0)
        
        # Créer le bouton pour le mode lave avec le même style
        self.lava_button = Button(button_x, lava_button_y, button_width, 0)
        
        # Modifier le texte du bouton lava mode
        self.lava_button.text = create_pixel_text("LAVA MODE", self.lava_button.font, (0, 0, 0))
        self.lava_button.text_rect = self.lava_button.text.get_rect(center=self.lava_button.rect.center)
        self.lava_button.text_rect_pressed = self.lava_button.text.get_rect(center=(self.lava_button.rect.centerx, self.lava_button.rect.centery + 3))
        
        # Créer le bouton pour le mode glace
        self.ice_button = Button(button_x, ice_button_y, button_width, 0)
        
        # Modifier le texte du bouton ice mode
        self.ice_button.text = create_pixel_text("ICE MODE", self.ice_button.font, (0, 0, 0))
        self.ice_button.text_rect = self.ice_button.text.get_rect(center=self.ice_button.rect.center)
        self.ice_button.text_rect_pressed = self.ice_button.text.get_rect(center=(self.ice_button.rect.centerx, self.ice_button.rect.centery + 3))
        
        # Créer le fond
        self.background = Background()

        # Skin selection
        self.selected_skin_path = None # To store the path of the selected skin
        self.skin_buttons = []
        
        # Make skin buttons smaller
        skin_button_width = int(button_width // 2 * 0.8)
        skin_button_height = skin_button_width

        # Position at bottom of screen
        skin_button_y_pos = SCREEN_HEIGHT - skin_button_height - 30
        
        # Adjust spacing
        button_spacing = 40
        num_skins = 3
        total_skin_buttons_width = num_skins * skin_button_width + (num_skins - 1) * button_spacing
        
        # Center horizontally
        start_x_skins = (SCREEN_WIDTH // 2) - (total_skin_buttons_width // 2) + (skin_button_width // 2)

        # Updated paths for skin images
        self.skin_image_paths = [
            os.path.join(ASSETS_DIR, "sprites", "frog", "skins", "Winter_frog_skin", "idle_winterfrog", "frog_idle0_winter.png"),
            os.path.join(ASSETS_DIR, "sprites", "frog", "Idle frog", "frog_idle0.png"),
            os.path.join(ASSETS_DIR, "sprites", "frog", "skins", "Yellow_frog_skin", "idle_winterfrog", "frog_idle0_hiver_jauen_clair.png")
        ]
        
        for i in range(num_skins):
            skin_path = self.skin_image_paths[i]
            button = SkinButton(
                start_x_skins + i * (skin_button_width + button_spacing),
                skin_button_y_pos,
                skin_button_width,
                skin_button_height,
                skin_path,
                SCREEN_WIDTH 
            )
            self.skin_buttons.append(button)

        # Skin Choice Text - Positioned above the skin buttons at the bottom
        self.skin_choice_font = pygame.font.Font(None, 30)  # Smaller font
        self.skin_choice_text_surface = create_pixel_text("SKIN CHOICE", self.skin_choice_font, WHITE)
        # Position above the skin buttons
        text_y_pos = skin_button_y_pos - self.skin_choice_text_surface.get_height() - 10
        self.skin_choice_text_rect = self.skin_choice_text_surface.get_rect(centerx=SCREEN_WIDTH // 2, y=text_y_pos)

        if self.skin_buttons:
            first_skin_button = self.skin_buttons[0]
            if os.path.exists(first_skin_button.image_path):
                 first_skin_button.is_selected = True
                 self.selected_skin_path = first_skin_button.image_path
            else:
                for sb_idx, sb in enumerate(self.skin_buttons):
                    if os.path.exists(sb.image_path):
                        sb.is_selected = True
                        self.selected_skin_path = sb.image_path
                        for other_sb_idx, other_sb in enumerate(self.skin_buttons):
                            if sb_idx != other_sb_idx:
                                other_sb.is_selected = False
                        break 
                if not self.selected_skin_path:
                     print("Warning: No valid skin images found for default selection.")
        else: # Handle case with no skins
            print("Warning: No skin buttons created.")

    def run(self):
        running = True
        # result will now be a dictionary: {"mode": "MODE_NAME", "skin": "path/to/skin.png"}
        # Initialize to None or a structure indicating no selection yet
        menu_outcome = None 
        
        while running and menu_outcome is None: # Loop until an outcome is determined
            # Get the time elapsed since last frame for animation timing
            delta_time = self.clock.tick(FPS) / 1000.0  # Convert to seconds
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.start_button.check_press(event.pos)
                        self.lava_button.check_press(event.pos)
                        self.ice_button.check_press(event.pos)
                        for skin_button in self.skin_buttons:
                            skin_button.check_press(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        action_taken = False
                        if self.start_button.check_release(event.pos):
                            if self.selected_skin_path: # Ensure a skin is selected
                                menu_outcome = {"mode": "NORMAL", "skin": self.selected_skin_path}
                            else:
                                print("Warning: No skin selected for NORMAL mode start.")
                                # Potentially assign a default skin or prevent start
                                menu_outcome = {"mode": "NORMAL", "skin": self.skin_image_paths[0] if self.skin_image_paths else None} # Fallback
                            action_taken = True
                        elif self.lava_button.check_release(event.pos):
                            if self.selected_skin_path:
                                menu_outcome = {"mode": "LAVA", "skin": self.selected_skin_path}
                            else:
                                print("Warning: No skin selected for LAVA mode start.")
                                menu_outcome = {"mode": "LAVA", "skin": self.skin_image_paths[0] if self.skin_image_paths else None} # Fallback
                            action_taken = True
                        elif self.ice_button.check_release(event.pos):
                            if self.selected_skin_path:
                                menu_outcome = {"mode": "ICE", "skin": self.selected_skin_path}
                            else:
                                print("Warning: No skin selected for ICE mode start.")
                                menu_outcome = {"mode": "ICE", "skin": self.skin_image_paths[0] if self.skin_image_paths else None} # Fallback
                            action_taken = True
                        
                        if not action_taken:
                            for skin_button in self.skin_buttons:
                                if skin_button.check_release(event.pos):
                                    for sb in self.skin_buttons:
                                        sb.is_selected = False
                                    skin_button.is_selected = True
                                    self.selected_skin_path = skin_button.image_path
                                    print(f"Skin selected: {self.selected_skin_path}")
                                    break
            
            # Update the logo animation
            self.logo_animation_timer += delta_time
            if self.logo_animation_timer >= self.logo_animation_speed:
                self.current_logo_frame = (self.current_logo_frame + 1) % len(self.logo_frames)
                self.logo_animation_timer = 0
                
            self.background.update()
            
            self.screen.fill((0, 0, 0))
            self.background.draw(self.screen)
            
            # Draw the current logo frame
            self.screen.blit(self.logo_frames[self.current_logo_frame], self.logo_rect)
            
            # Display total coins
            total_coins = get_total_coins()
            coin_text = create_pixel_text(f"Total Coins: {total_coins}", self.font, YELLOW)
            coin_rect = coin_text.get_rect(centerx=SCREEN_WIDTH//2, top=self.logo_rect.bottom + 10)
            self.screen.blit(coin_text, coin_rect)
            
            # Display high scores
            high_scores_y = coin_rect.bottom + 5  # Reduced from 10 to 5
            high_score = get_high_score("normal")
            score_text = create_pixel_text(f"High Score: {high_score}", self.font, ORANGE)
            score_rect = score_text.get_rect(centerx=SCREEN_WIDTH//2, top=high_scores_y)
            self.screen.blit(score_text, score_rect)
            
            self.start_button.draw(self.screen)
            self.lava_button.draw(self.screen)
            self.ice_button.draw(self.screen)

            # Disp"SKIN CHOICE"
            if hasattr(self, 'skin_choice_text_surface'): # Check if it's initialized
                self.screen.blit(self.skin_choice_text_surface, self.skin_choice_text_rect)

            for skin_button in self.skin_buttons:
                skin_button.draw(self.screen)
            
            pygame.display.flip()
            
        return menu_outcome # Return the dictionary 