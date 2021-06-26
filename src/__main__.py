"""
Module with the main game loop.
"""

import pygame
from pygame.sprite import Group
from pygame.surface import Surface
from pygame.time import Clock
from pytmx.pytmx import TiledObjectGroup

from src.animations import SpriteSheetParser
from src.collidables import Collidable
from src.exit import exit_if_captured_quit
from src.inputs import capture_player_inputs
from src.maps import TiledMap
from src.player import Player
from src.scrolling import Scroll
from src.settings import CLEAR_DISPLAY_RGB
from src.settings import GAME_FPS
from src.settings import RAW_DISPLAY_SIZE
from src.settings import TMX_OBJECT_COLLIDABLE_NAME
from src.settings import TMX_OBJECT_PLAYER_NAME
from src.settings import WINDOW_SIZE
from src.settings import WINDOW_TITLE


def main():
    """
    Entry point which runs the main game loop.
    """

    pygame.init()
    game_clock = Clock()

    # main screen
    game_screen: Surface = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    pygame.display.set_caption(WINDOW_TITLE)

    # raw_display is the main blit Surface which is scaled later
    raw_display = pygame.Surface(RAW_DISPLAY_SIZE)

    # maps
    level_01 = TiledMap("tiled-level-01.tmx")

    # other spritesheets and animations
    spritesheet_parser = SpriteSheetParser()

    spritesheet_parser.load_spritesheet("hero")
    player_animations = spritesheet_parser.build_animation_repository()

    # sprites and groups
    scroll_offset = Scroll(0.0, 0.0)
    collidables = Group()

    # objects in objects layer: map parsing
    tile_object: TiledObjectGroup

    for tile_object in level_01.tmx_map.objects:
        if tile_object.name == TMX_OBJECT_PLAYER_NAME:
            player = Player(tile_object.x, tile_object.y, player_animations)

        if tile_object.name == TMX_OBJECT_COLLIDABLE_NAME:
            Collidable(tile_object.x, tile_object.y, tile_object.width, tile_object.height, collidables)

    # main game loop
    while True:
        raw_display.fill(CLEAR_DISPLAY_RGB)  # clears the display
        scroll_offset.update(player.rect.x, player.rect.y)  # update scrolling according player

        # input handling and state update
        captured_input = capture_player_inputs()
        exit_if_captured_quit(captured_input)

        player.update(captured_input, collidables)

        # rendering
        player.render_on(raw_display, scroll_offset)
        level_01.render_on(raw_display, scroll_offset)

        # scale display is what is blit on the game screen
        scaled_display = pygame.transform.scale(raw_display, WINDOW_SIZE)
        game_screen.blit(scaled_display, (0, 0))

        pygame.display.update()
        game_clock.tick(GAME_FPS)


if __name__ == "__main__":
    main()
