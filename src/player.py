"""
Module with the player structures.
"""

from pygame import Rect
from pygame import Surface

from src.inputs import CapturedInput


class Player:

    _rect: Rect  # contains (x, y) coordinates
    _image: Surface
    _moving_right: bool
    _moving_left: bool

    def __init__(self, x: float, y: float, image: Surface) -> None:
        self._rect = Rect(x, y, image.get_width(), image.get_height())
        self._image = image
        self._moving_left = False
        self._moving_right = False

    @property
    def rect(self) -> Rect:
        return self._rect

    @property
    def image(self) -> Surface:
        return self._image

    def update(self, captured_inputs: CapturedInput) -> None:
        if captured_inputs.moving_right or captured_inputs.moving_right_stop:
            self._moving_right = not captured_inputs.moving_right_stop

        if captured_inputs.moving_left or captured_inputs.moving_left_stop:
            self._moving_left = not captured_inputs.moving_left_stop

        if self._moving_right:
            self._rect.x += 4

        if self._moving_left:
            self._rect.x -= 4
