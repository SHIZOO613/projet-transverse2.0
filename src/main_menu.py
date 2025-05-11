import pygame
import os
import sys
from utils import create_pixel_text
from background import Background
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, ASSETS_DIR, WHITE, YELLOW, get_total_coins, BLACK

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


        original_img_width = self.original_image.get_width()
        original_img_height = self.original_image.get_height()
        aspect_ratio = original_img_width / original_img_height if original_img_height > 0 else 1

        self.width = width
        self.height = int(width / aspect_ratio) if aspect_ratio > 0 else height
        
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))
        
        self.x = x - self.width // 2
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_pressed = False
        self.is_selected = False # To indicate if this skin is currently selected

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.is_selected:
            pygame.draw.rect(screen, YELLOW, self.rect, 3) # Highlight selected skin with a yellow border
        elif self.is_pressed:
            pygame.draw.rect(screen, WHITE, self.rect, 3) # Highlight pressed skin with a white border (optional)
        else:
            pygame.draw.rect(screen, BLACK, self.rect, 1) # Default border

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
        
        # Charger le logo
        logo_path = os.path.join(ASSETS_DIR, "Main menu", "Logo", "Main Logo.png")
        self.logo = pygame.image.load(logo_path)
        
        # Redimensionner le logo pour qu'il ait une taille maximale
        logo_width = min(SCREEN_WIDTH * 0.99, self.logo.get_width() * 6.5)  # Augmenté à 6.5x
        logo_height = logo_width * (self.logo.get_height() / self.logo.get_width())
        self.logo = pygame.transform.scale(self.logo, (int(logo_width), int(logo_height)))
        
        # Positionner le logo
        self.logo_rect = self.logo.get_rect(centerx=SCREEN_WIDTH//2, top=SCREEN_HEIGHT//30)
        
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
        
        skin_button_width = button_width // 2
        skin_button_height = skin_button_width

        skin_button_y_pos = ice_button_y + self.ice_button.height + 20

        num_skins = 3 # Changed from 2 to 3
        total_skin_buttons_width = num_skins * skin_button_width + (num_skins - 1) * 20 if num_skins > 0 else 0
        start_x_skins = SCREEN_WIDTH // 2 - total_skin_buttons_width // 2

        # Updated paths for skin images - adding a placeholder for the 3rd skin
        self.skin_image_paths = [
            os.path.join(ASSETS_DIR, "sprites", "frog", "skins", "Winter_frog_skin", "idle_winterfrog", "frog_idle0_winter.png"),
            os.path.join(ASSETS_DIR, "sprites", "frog", "Idle frog", "frog_idle0.png"),
            os.path.join(ASSETS_DIR, "sprites", "frog", "skins", "Yellow_frog_skin", "idle_winterfrog", "frog_idle0_hiver_jauen_clair.png") # Path for Yellow Skin
        ]
        
        for i in range(num_skins):
            skin_path = self.skin_image_paths[i]
            button = SkinButton(
                start_x_skins + i * (skin_button_width + 20) + skin_button_width // 2,
                skin_button_y_pos,
                skin_button_width,
                skin_button_height,
                skin_path,
                SCREEN_WIDTH 
            )
            self.skin_buttons.append(button)

        # Skin Choice Text
        self.skin_choice_font = pygame.font.Font(None, 30) # Smaller font for this label
        self.skin_choice_text_surface = create_pixel_text("SKIN CHOICE", self.skin_choice_font, WHITE)
        # Position above the skin buttons
        text_y_pos = skin_button_y_pos - self.skin_choice_text_surface.get_height() - 10 # 10px padding above
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
                            
            self.background.update()
            
            self.screen.fill((0, 0, 0))
            self.background.draw(self.screen)
            
            self.screen.blit(self.logo, self.logo_rect)
            
            total_coins = get_total_coins()
            coin_text = create_pixel_text(f"Total Coins: {total_coins}", self.font, YELLOW)
            coin_rect = coin_text.get_rect(centerx=SCREEN_WIDTH//2, top=self.logo_rect.bottom + 10)
            self.screen.blit(coin_text, coin_rect)
            
            self.start_button.draw(self.screen)
            self.lava_button.draw(self.screen)
            self.ice_button.draw(self.screen)

            # Dessiner le texte "SKIN CHOICE"
            if hasattr(self, 'skin_choice_text_surface'): # Check if it's initialized
                self.screen.blit(self.skin_choice_text_surface, self.skin_choice_text_rect)

            for skin_button in self.skin_buttons:
                skin_button.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
        return menu_outcome # Return the dictionary 