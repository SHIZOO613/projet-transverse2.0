import pygame
import os
import sys
from utils import create_pixel_text
from background import Background
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, ASSETS_DIR, WHITE

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
        
        # Créer le bouton de démarrage
        button_width = 250  # Taille plus grande pour le bouton
        button_x = SCREEN_WIDTH//2
        
        # Ajuster les positions verticales pour les deux boutons
        start_button_y = SCREEN_HEIGHT//2 + 150
        lava_button_y = SCREEN_HEIGHT//2 + 250
        
        # Créer les boutons
        self.start_button = Button(button_x, start_button_y, button_width, 0)
        
        # Créer le bouton pour le mode lave avec le même style
        self.lava_button = Button(button_x, lava_button_y, button_width, 0)
        
        # Modifier le texte du bouton lava mode
        self.lava_button.text = create_pixel_text("LAVA MODE", self.lava_button.font, (0, 0, 0))
        self.lava_button.text_rect = self.lava_button.text.get_rect(center=self.lava_button.rect.center)
        self.lava_button.text_rect_pressed = self.lava_button.text.get_rect(center=(self.lava_button.rect.centerx, self.lava_button.rect.centery + 3))
        
        # Créer le fond
        self.background = Background()
        
    def run(self):
        running = True
        result = None  # Pour stocker le résultat de l'action du menu
        
        while running and result is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        self.start_button.check_press(event.pos)
                        self.lava_button.check_press(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Relâchement du clic gauche
                        if self.start_button.check_release(event.pos):
                            # Démarrer le jeu normal au relâchement du bouton
                            result = "NORMAL"
                        elif self.lava_button.check_release(event.pos):
                            # Démarrer le mode lave
                            result = "LAVA"
                            
            # Mettre à jour le fond
            self.background.update()
            
            # Dessiner
            self.screen.fill((0, 0, 0))
            self.background.draw(self.screen)
            
            # Dessiner le logo
            self.screen.blit(self.logo, self.logo_rect)
            
            # Dessiner les boutons
            self.start_button.draw(self.screen)
            self.lava_button.draw(self.screen)
            
            # Mettre à jour l'affichage
            pygame.display.flip()
            self.clock.tick(FPS)
            
        return result 