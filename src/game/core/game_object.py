"""
Base class for all game objects.
"""
from typing import Tuple, Optional
import pygame
from ..utils.config import Path

class GameObject:
    """Base class for all game objects providing common functionality."""
    
    def __init__(self, x: float, y: float, width: int, height: int):
        """Initialize the game object with position and dimensions."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self._sprite: Optional[pygame.Surface] = None
        
    def update(self) -> None:
        """Update the object's state. Should be overridden by subclasses."""
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the object on the screen."""
        if self._sprite:
            screen.blit(self._sprite, self.rect)
            
    def load_sprite(self, sprite_path: Path) -> None:
        """Load a sprite from the given path."""
        try:
            self._sprite = pygame.image.load(str(sprite_path)).convert_alpha()
            self._sprite = pygame.transform.scale(self._sprite, (self.width, self.height))
        except pygame.error as e:
            print(f"Error loading sprite {sprite_path}: {e}")
            
    @property
    def position(self) -> Tuple[float, float]:
        """Get the current position of the object."""
        return self.x, self.y
    
    @position.setter
    def position(self, pos: Tuple[float, float]) -> None:
        """Set the position of the object."""
        self.x, self.y = pos
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
    def collides_with(self, other: 'GameObject') -> bool:
        """Check if this object collides with another object."""
        return self.rect.colliderect(other.rect) 