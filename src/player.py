"""
Module with the player structures.
"""

from typing import Dict
from typing import List

import pygame
from pygame import Rect
from pygame import Surface
from pygame.sprite import AbstractGroup
from pygame.sprite import Group
from pygame.sprite import Sprite
from pygame.sprite import spritecollide

from src.animations import AnimationRepository
from src.animations import Animator
from src.inputs import CapturedInput
from src.scrolling import Scroll
from src.settings import GRAVITY
from src.settings import JUMP_VELOCITY_Y


class Player(Sprite):
    """
    Represents the main player (hero) of the game.
    """

    # movement
    _speed: List[int]
    _moving_right: bool
    _moving_left: bool

    # animation and image
    _animator: Animator
    _image_flip: bool

    def __init__(self, x: float, y: float, animation_repository: AnimationRepository, *groups: AbstractGroup) -> None:
        # animation state
        self._animator = Animator("idle", animation_repository)
        self._image_flip = False
        self.image = self._animator.image  # images always come from the animator

        # collisions and movement
        if self.image is not None:
            self.rect = Rect(x, y, self.image.get_width(), self.image.get_height())

        self._speed = [0, 0]
        self._moving_left = False
        self._moving_right = False

    @property
    def speed(self) -> List[int]:
        return self._speed

    def update(self, *args, **kwargs) -> None:
        """
        Updates the player's state. Called on each frame.
        """
        captured_inputs: CapturedInput = args[0]
        collidables: Group = args[1]

        self._move_and_check_collisions(collidables)

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

        if self._image_flip:
            self.image = pygame.transform.flip(self._animator.image, True, False)
        else:
            self.image = self._animator.image

        self._animator.update()

    def render_on(self, raw_display: Surface, scroll: Scroll) -> None:
        """
        Blits the player image onto the display's surface.
        """
        if self.image and self.rect:
            raw_display.blit(self.image, (self.rect.x - scroll.offset_x, self.rect.y - scroll.offset_y))

    def _move_and_check_collisions(self, collidables_group: Group) -> Dict:
        """
        Updates the player's rect (x, y) position by applying its velocity vectory in (x, y) coordinates.
        After updating the position with the speed, collisions are checked in order to reposition the player.
        """
        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        assert self.rect

        # x axis handling
        self.rect.x += self.speed[0]
        collisions_tiles_x = spritecollide(self, collidables_group, False)

        for collided_tile in collisions_tiles_x:
            if self.speed[0] > 0 and collided_tile.rect is not None:
                self.rect.right = collided_tile.rect.left
                collision_types["right"] = True

            if self.speed[0] < 0 and collided_tile.rect is not None:
                self.rect.left = collided_tile.rect.right
                collision_types["left"] = True

        # y axis handling
        self.rect.y += self.speed[1]
        collisions_tiles_y = spritecollide(self, collidables_group, False)

        for collided_tile in collisions_tiles_y:
            if self.speed[1] > 0 and collided_tile.rect is not None:
                self.rect.bottom = collided_tile.rect.top
                collision_types["bottom"] = True

            if self.speed[1] < 0 and collided_tile.rect is not None:
                self.rect.top = collided_tile.rect.bottom
                collision_types["top"] = True

        return collision_types
