"""
This module contains the base for pygames prototypes.
"""
import sys

import pygame
from pygame.constants import QUIT
from pygame.sprite import AbstractGroup
from pygame.sprite import Group
from pygame.sprite import Sprite
from pygame.surface import Surface

# settings
WIDTH = 600
HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
GREEN = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)


class Player(Sprite):

    _velocity_x: float

    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)

        # add image to the player
        self.image = Surface((50, 50))
        self.image.fill(YELLOW)

        # rect from image for collisions
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)


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
    pygame.display.set_caption("Prototype Name Goes Here")
    clock = pygame.time.Clock()

    all_sprites_group = Group()
    Player(all_sprites_group)

    # main game loop
    while True:
        screen.fill(BLACK)
        draw_grid(screen, 50)

        all_sprites_group.update()
        all_sprites_group.draw(screen)  # blits the image at rect's position

        # basic events handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # flush the whole updated screen
        pygame.display.update()

        # game tick
        clock.tick(FPS)


if __name__ == "__main__":
    main()
