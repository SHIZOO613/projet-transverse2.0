from ice_background import IceBackground
from game_platform import IcePlatform, Platform

class IceGame(GameBase):
    """Mode de jeu avec uniquement des plateformes de glace, sauf la première."""

    def __init__(self, screen, clock, font, menu_callback):
        # Initialiser la classe parente
        super().__init__(screen, clock, font, menu_callback, bg_class=IceBackground)
        # Type de jeu
        self.game_type = "ice"
        # Générer les plateformes initiales
        self.generate_platforms()

    def generate_platforms(self):
        """Génère les plateformes initiales - plateforme de départ normale, puis uniquement des plateformes de glace."""
        # Vider la liste des plateformes
        self.platforms = []

        # Créer la plateforme de départ (normale)
        platform_width = 100
        platform_x = (SCREEN_WIDTH - platform_width) // 2
        platform_y = SCREEN_HEIGHT - 100
        self.platforms.append(Platform(platform_x, platform_y, platform_width))

        # Générer d'autres plateformes (uniquement des plateformes de glace)
        num_platforms = 10
        for i in range(1, num_platforms):
            platform_width = 100
            platform_x = random.randint(50, SCREEN_WIDTH - platform_width - 50)
            platform_y = platform_y - random.randint(100, 140)
            
            # Toutes les plateformes après la première sont des plateformes de glace
            self.platforms.append(IcePlatform(platform_x, platform_y, platform_width))

    def update(self):
        """Mettre à jour l'état du jeu."""
        # Vérifier si le joueur est tombé
        if self.player.rect.top > SCREEN_HEIGHT:
            self.game_over = True
            return

        # Si le score a augmenté, ajouter des plateformes
        if int(self.player.score) > self.last_platform_score:
            self.last_platform_score = int(self.player.score)
            
            # Ajouter une nouvelle plateforme de glace
            platform_width = 100
            platform_x = random.randint(50, SCREEN_WIDTH - platform_width - 50)
            platform_y = self.platforms[0].rect.y - random.randint(100, 140)
            
            # Déterminer le type de plateforme (toujours une plateforme de glace)
            self.platforms.insert(0, IcePlatform(platform_x, platform_y, platform_width))

            # Supprimer la plateforme la plus basse si elle est hors de l'écran
            if self.platforms[-1].rect.y > SCREEN_HEIGHT:
                self.platforms.pop()

        # Appeler la méthode de mise à jour de la classe parente
        super().update() 