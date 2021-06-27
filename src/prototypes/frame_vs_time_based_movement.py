"""
A quick study regarding frame-based vs time-based movement.
"""
import math
import sys

import pygame
from pygame.constants import QUIT
from pygame.sprite import AbstractGroup
from pygame.sprite import Group
from pygame.sprite import Sprite
from pygame.surface import Surface

# Settings
WIDTH = 600
HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (100, 200, 30)


class FrameRateDependentPlayer(Sprite):
    """
    Player's position is changed in frame-rate dependent way. The more FPS the farther/faster
    the player moves. This is usually a bad design as it introduces hardware dependencies on
    the game.
    """

    _velocity_x: float

    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)

        # add image to the player
        self.image = Surface((50, 50))
        self.image.fill(YELLOW)

        # rect from image for collisions
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 100
        self._velocity_x = 2  # (pixel/frame) - frame-based movement
        # self._velocity_x = 120 # (120 pixels/s) - time-based movement

    def update(self, *args, **kwargs) -> None:
        """
        Update is called once per frame to update the Player's state.
        """
        super().update(*args, **kwargs)

        if self.rect is not None:

            # if the FPS is high: 2 (pixel/frame) * 60 frame = 120 pixels moved
            # if the FPS drops: 2 (pixel/frame) * 20 frame = 40 pixels moved (slower)

            # (pixel/frame) * frame = pixels => unit is frame-rate DEPENDENT => often NOT good, depends on hardware!
            self.rect.x += self._velocity_x  # type: ignore

            if self.rect.left > WIDTH:
                print("Frame Rate Dependent Hit!")
                self.rect.left = 0


class TimeDependentPlayer(Sprite):
    """
    Player's position is changed in time-based (non frame-rate dependent) way. However, here,
    the player's rect (x, y) values are directly updated so the float numbers are floor'd by pygame
    which introduces errors over time.
    """

    _velocity_x: float

    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)

        # add image to the player
        self.image = Surface((50, 50))
        self.image.fill(GREEN)

        # rect from image for collisions
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 300
        self._velocity_x = 120  # (pixel/s) -- notice how bigger this is than 2 (pixels/frame)

    def update(self, *args, **kwargs) -> None:
        """
        Update is called once per frame to update the Player's state.
        """
        super().update(*args, **kwargs)
        dt = args[0]

        if self.rect is not None:
            # (pixels/s) * s = pixels => no more frame-rate dependency!
            self.rect.x += self._velocity_x * dt  # type: ignore

            if self.rect.left > WIDTH:
                self.rect.left = 0


class TimeDependentWithoutDirectUpdatingRectPlayer(Sprite):
    """
    Player's position is changed in time-based (non frame-rate dependent) way. However,
    in this case, a float position is used to store the player's position so that the
    Rect (x, y) values are NOT directly updated with velocity: all calculations use the
    float position and then this float position updates the Rect (x, y) when Pygame floors
    the values.

    Seems the same, but it's not: the game logic/updates now update the FLOAT position
    and not the rect's (x, y) that are always floor'd which accumulates errors over time.
    The game logic remains consistent: floats are applied to floats, and not to floor'd values.
    """

    _position_x: float
    _velocity_x: float

    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)

        # add image to the player
        self.image = Surface((50, 50))
        self.image.fill(GREEN)

        # rect from image for collisions
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 500
        self._position_x = 0
        self._velocity_x = 120  # (pixel/s) -- notice how bigger this is than 2 (pixels/frame)

    def update(self, *args, **kwargs) -> None:
        """
        Update is called once per frame to update the Player's state.
        """
        super().update(*args, **kwargs)
        dt = args[0]

        if self.rect is not None:
            # rectangles positions in pygame are PIXELS! They CANNOT be floats! Hence,
            # pygame FLOORS values before setting rect values, i.e (2.5 -> 2; -2.5 -> -3)

            # to avoid problems: update a float vector, so all logic updates this float value!
            self._position_x += self._velocity_x * dt  # self._position still a float!

            if self._position_x > WIDTH:
                print("Time-based (non frame-rate dependent) Dependent Hit!")
                self._position_x = 0

            # pygame FLOORs the position, but next computations will continue using the FLOAT self._position!
            # in a way that less errors are introduced!
            self.rect.x = math.floor(self._position_x)  # same as what pygame does: math.floor non-int values!


def draw_grid(screen: Surface, grid_size: int) -> None:
    """
    Draws a grid on the screen.
    """
    x = 0
    y = 0

    while y < HEIGHT:
        if y != 0:  # first vertical line is not drawn
            pygame.draw.line(screen, GRAY, start_pos=(0, y), end_pos=(WIDTH, y), width=1)

        y += grid_size

    while x < WIDTH:
        if x != 0:  # first horizontal line is not drawn
            pygame.draw.line(screen, GRAY, start_pos=(x, 0), end_pos=(x, HEIGHT), width=1)

        x += grid_size


def main():
    # init code
    pygame.init()
    screen: Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Time vs Frame Based Movement Prototype")
    clock = pygame.time.Clock()
    dt = 0  # delta time since last frame (seconds)

    all_sprites_group = Group()
    FrameRateDependentPlayer(all_sprites_group)
    TimeDependentPlayer(all_sprites_group)
    TimeDependentWithoutDirectUpdatingRectPlayer(all_sprites_group)

    # main game loop
    while True:
        # clear screen
        screen.fill(BLACK)

        draw_grid(screen, 50)
        all_sprites_group.update(dt)
        all_sprites_group.draw(screen)  # blits the image at rect's position

        # basic events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # flush the whole updated screen
        pygame.display.update()

        # game tick
        dt = clock.tick(FPS) / 1000


if __name__ == "__main__":
    main()
