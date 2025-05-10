# Frog Jump - Jeu de Plateformes

Un jeu de plateformes en 2D où le joueur contrôle une grenouille qui doit sauter de plateforme en plateforme pour monter le plus haut possible.

## Comment jouer

1. Lancez le jeu en exécutant:
   ```
   python game.py
   ```

2. Dans le menu principal, vous pouvez choisir entre deux modes:
   - **Mode Normal**: Plateformes variées (normales, mouvantes, glacées, cassables)
   - **Mode Lave**: Uniquement des plateformes cassables avec un fond de lave et des boules de feu

3. Commandes:
   - Cliquez et maintenez le bouton gauche de la souris pour charger un saut
   - Relâchez pour sauter dans la direction où se trouve le curseur
   - Appuyez sur Espace pour revenir au menu après un Game Over
   - Appuyez sur Échap pour quitter

## Structure du projet

Le projet est organisé selon une architecture orientée objet avec les fichiers suivants:

```
src/
├── assets/               # Ressources du jeu (sprites, images)
├── game.py               # Point d'entrée principal du jeu
├── game_base.py          # Classe de base pour les modes de jeu
├── game_logic.py         # Implémentation du mode de jeu normal
├── lava_game.py          # Implémentation du mode de jeu lave
├── main_menu.py          # Menu principal
├── background_manager.py # Classes de base pour gérer les fonds
├── background.py         # Gestion du fond avec parallaxe
├── lava_background.py    # Gestion du fond de lave
├── platform.py           # Classes pour les différents types de plateformes
├── player.py             # Classe du joueur (grenouille)
├── config.py             # Configuration et constantes du jeu
├── utils.py              # Fonctions utilitaires
└── __init__.py
```

## Dépendances

Le jeu utilise les bibliothèques Python suivantes:
- **pygame**: Pour le rendu graphique et la gestion des entrées
- **PIL** (Pillow): Pour certaines opérations de traitement d'image

Pour installer les dépendances:
```
pip install pygame pillow
```

## Licence

Ce projet est distribué sous licence libre.

## Crédits

- Sprites et graphismes: Ressources personnalisées
- Développement: Projet original 
