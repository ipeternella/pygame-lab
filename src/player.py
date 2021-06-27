"""
Module with the player structures.
"""
from typing import Dict

import pygame
from pygame import Rect
from pygame import Surface
from pygame.math import Vector2
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
from src.settings import MAX_VELOCITY_Y
from src.settings import VELOCITY_X


class Player(Sprite):
    """
    Represents the main player (hero) of the game.
    """

    _position: Vector2
    _velocity: Vector2

    _moving_right: bool
    _moving_left: bool

    _animator: Animator
    _image_flip: bool

    def __init__(self, x: float, y: float, animation_repository: AnimationRepository, *groups: AbstractGroup) -> None:
        super().__init__(*groups)

        self._velocity = Vector2(0, 0)
        self._position = Vector2(x, y)

        self._moving_left = False
        self._moving_right = False

        # animation state
        self._animator = Animator("idle", animation_repository)
        self._image_flip = False
        self.image = self._animator.image  # images always come from the animator

        # collisions and movement
        if self.image is not None:
            self.rect = Rect(x, y, self.image.get_width(), self.image.get_height())

    @property
    def velocity(self) -> Vector2:
        return self._velocity

    def update(self, *args, **kwargs) -> None:
        """
        Updates the player's state. Called on each frame.
        """
        captured_input: CapturedInput = args[0]
        dt = args[1]
        collidables: Group = args[2]

        self._update_with_inputs(captured_input, dt)
        self._move(collidables)
        self._animate()

    def render_on(self, display: Surface, scroll: Scroll) -> None:
        """
        Blits the player image onto the display's surface.
        """
        if self.image and self.rect:
            display.blit(self.image, (self.rect.x - scroll.offset_x, self.rect.y - scroll.offset_y))

    def _update_with_inputs(self, captured_input: CapturedInput, dt: int) -> None:
        """
        Updates the player state according to the player inputs. This updates only self._velocity and
        self._position. The final self.rect is finally moved in self._move in which collisions are taken
        into account.
        """
        self._velocity.x = 0  # self._velocity.y is not reset: player can be jumping

        if captured_input.moving_right or captured_input.moving_right_stop:
            self._moving_right = not captured_input.moving_right_stop

        if captured_input.moving_left or captured_input.moving_left_stop:
            self._moving_left = not captured_input.moving_left_stop

        # x axis
        if self._moving_right:
            self._animator.change_action("run")
            self._image_flip = False
            self._velocity.x += VELOCITY_X * dt  # pixel/s * s = pixel (position unit) (dx/dt * dt = dx)

        if self._moving_left:
            self._animator.change_action("run")
            self._image_flip = True
            self._velocity.x -= VELOCITY_X * dt

        if not self._moving_left and not self._moving_right:
            self._animator.change_action("idle")

        # y axis
        if captured_input.has_jumped:
            self._velocity.y -= JUMP_VELOCITY_Y * dt
        else:
            self._velocity.y += GRAVITY * dt  # if not jumping: gravity always drags down

        # clamp velocity on y to avoid absurd values (self._velocity.y is not reset every frame!)
        if self._velocity.y > MAX_VELOCITY_Y:
            self._velocity.y = MAX_VELOCITY_Y

        # update the position vector which will update the sprite's rect
        self._position += self._velocity

    def _move(self, collidables_group: Group) -> Dict:
        """
        Updates the player's rect (x, y) position by applying its velocity vectory in (x, y) coordinates.
        After updating the position with the velocity, collisions are checked in order to reposition the player.
        """
        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        assert self.rect

        # x axis handling
        self.rect.x = self._position.x  # type: ignore
        collisions_tiles_x = spritecollide(self, collidables_group, False)

        for collided_tile in collisions_tiles_x:
            if self._velocity.x > 0 and collided_tile.rect is not None:
                self._position.x = collided_tile.rect.left - self.rect.width
                collision_types["right"] = True

            if self._velocity.x < 0 and collided_tile.rect is not None:
                self._position.x = collided_tile.rect.right
                collision_types["left"] = True

            self.rect.x = self._position.x  # type: ignore

        # y axis handling
        self.rect.y = self._position.y  # type: ignore
        collisions_tiles_y = spritecollide(self, collidables_group, False)

        for collided_tile in collisions_tiles_y:
            if self._velocity.y > 0 and collided_tile.rect is not None:
                # self.rect.bottom = collided_tile.rect.top
                self._position.y = collided_tile.rect.top - self.rect.height
                collision_types["bottom"] = True

            if self._velocity.y < 0 and collided_tile.rect is not None:
                self._position.y = collided_tile.rect.bottom
                collision_types["top"] = True

            self.rect.y = self._position.y  # type: ignore

        return collision_types

    def _animate(self) -> None:
        """
        Updates the animator and changes the sprite's image according to the current animation action.
        """
        self._animator.update()

        if self._image_flip:
            self.image = pygame.transform.flip(self._animator.image, True, False)
        else:
            self.image = self._animator.image
