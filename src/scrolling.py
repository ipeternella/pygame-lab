"""
Module with scrolling utilities.
"""
from src.settings import RAW_DISPLAY_SIZE
from src.settings import SCROLLING_OFFSET_FRACTION
from src.settings import TILE_SIZE


class Scroll:
    """
    Represents an offset that should be applied to blit images on the screen. The offset
    gives the 'screen scrolling' sensation.
    """

    _offset_x: int
    _offset_y: int

    def __init__(self, offset_x: int, offset_y: int) -> None:
        self._offset_x = offset_x
        self._offset_y = offset_y

    @property
    def offset_x(self) -> int:
        return self._offset_x

    @property
    def offset_y(self) -> int:
        return self._offset_y

    def update(self, player_x: int, player_y: int) -> None:
        """
        Adjusts the scroll offset according to the player's position.
        """
        self._offset_x += (
            player_x - RAW_DISPLAY_SIZE[0] // 2 - TILE_SIZE // 2 - self._offset_x
        ) * SCROLLING_OFFSET_FRACTION
        self._offset_y += (
            player_y - RAW_DISPLAY_SIZE[1] // 2 - TILE_SIZE // 2 - self._offset_y
        ) * SCROLLING_OFFSET_FRACTION
