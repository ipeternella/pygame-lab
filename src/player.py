"""
Module with the player structures.
"""

from typing import List

import pygame
from pygame import Rect
from pygame.surface import Surface

from src.animations import AnimationRepository
from src.animations import Animator
from src.inputs import CapturedInput
from src.settings import GRAVITY
from src.settings import JUMP_VELOCITY_Y


class Player:
    """
    Represents the main player (hero) of the game.
    """

    _rect: Rect  # contains (x, y) coordinates
    _image: Surface
    _image_flip: bool
    _animator: Animator
    _moving_right: bool
    _moving_left: bool
    _speed: List[int]

    def __init__(self, x: float, y: float, animation_repository: AnimationRepository) -> None:
        # animation state
        self._animator = Animator("idle", animation_repository)
        self._image = self._animator.image  # images always come from the animator
        self._image_flip = False

        # collisions and movement
        self._rect = Rect(x, y, self._image.get_width(), self._image.get_height())
        self._speed = [0, 0]
        self._moving_left = False
        self._moving_right = False

    @property
    def rect(self) -> Rect:
        return self._rect

    @property
    def speed(self) -> List[int]:
        return self._speed

    @property
    def image(self) -> Surface:
        if self._image_flip:
            return pygame.transform.flip(self._animator.image, True, False)

        return self._animator.image

    def update(self, captured_inputs: CapturedInput) -> None:
        """
        Updates the player's state. Called on each frame.
        """
        if captured_inputs.moving_right or captured_inputs.moving_right_stop:
            self._moving_right = not captured_inputs.moving_right_stop

        if captured_inputs.moving_left or captured_inputs.moving_left_stop:
            self._moving_left = not captured_inputs.moving_left_stop

        # speed_x resetting: allows the player to immediately stop once the key is released
        # if not reset: gives the 'sliding on ice' sensation
        # speed_y is not reset: gravity is always ON
        self._speed[0] = 0

        if captured_inputs.has_jumped:
            self._speed[1] -= JUMP_VELOCITY_Y  # negative y

        # x axis
        if self._moving_right:
            self._animator.change_action("run")
            self._image_flip = False
            self._speed[0] += 2

        if self._moving_left:
            self._animator.change_action("run")
            self._image_flip = True
            self._speed[0] -= 2

        if not self._moving_left and not self._moving_right:
            self._animator.change_action("idle")

        # y axis: always updated as gravity always drags down
        self._speed[1] += GRAVITY

        if self._speed[1] > 3:  # clamping
            self._speed[1] = 3

        self._animator.update()
