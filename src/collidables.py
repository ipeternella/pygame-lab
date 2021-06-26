"""
Module with sprites definitions.
"""
from pygame.rect import Rect
from pygame.sprite import AbstractGroup
from pygame.sprite import Sprite


class Collidable(Sprite):
    """
    Represents a collidable game object with an image an rect.
    """

    def __init__(self, x: int, y: int, width: int, height: int, *groups: AbstractGroup) -> None:
        super().__init__(*groups)

        self.rect = Rect(x, y, width, height)
        self.image = None
