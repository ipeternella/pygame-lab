"""
Module with camera implementation used to apply drawing offsets.
"""

from pygame.rect import Rect

from src.player import Player
from src.settings import RAW_DISPLAY_SIZE
from src.settings import SCROLLING_OFFSET_FRACTION


class Camera:
    """
    Models a camera object which is used to apply offsets to sprites' rects in
    order to create a scrolling effect.
    """

    _rect: Rect
    _width: int
    _height: int

    def __init__(self, width: int, height: int) -> None:
        self._rect = Rect(0, 0, width, height)  # stores the offset
        self._width = width
        self._height = height

    @property
    def rect(self) -> Rect:
        return self._rect

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def apply_offset(self, rect: Rect) -> Rect:
        return rect.move(self._rect.topleft)

    def update(self, target_rect: Player) -> None:
        offset_x = (
            self._rect.x + ((-target_rect.rect.x + RAW_DISPLAY_SIZE[0] / 2) - self._rect.x) * SCROLLING_OFFSET_FRACTION
        )
        offset_y = (
            self._rect.y + ((-target_rect.rect.y + RAW_DISPLAY_SIZE[1] / 2) - self._rect.y) * SCROLLING_OFFSET_FRACTION
        )

        # clamp offsets so that nothing beyond the map is shown
        offset_x = min(0, offset_x)  # left
        offset_y = min(0, offset_y)  # top

        offset_x = max(-(self.width - RAW_DISPLAY_SIZE[0]), offset_x)  # right
        offset_y = max(-(self.height - RAW_DISPLAY_SIZE[1]), offset_y)  # bottom

        self._rect = Rect(offset_x, offset_y, self.width, self.height)
