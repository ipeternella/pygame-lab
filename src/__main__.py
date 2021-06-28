"""
Module with the main game loop.
"""

import pygame
from pygame.sprite import Group
from pygame.surface import Surface
from pygame.time import Clock
from pytmx.pytmx import TiledObjectGroup

from src.animations import SpriteSheetParser
from src.camera import Camera
from src.collidables import Collidable
from src.exit import exit_if_captured_quit
from src.inputs import capture_player_inputs
from src.maps import TiledMap
from src.player import Player
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
    dt = 0

    # main screen
    game_screen: Surface = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    pygame.display.set_caption(WINDOW_TITLE)

    # raw_display is the main blit Surface which is scaled later
    raw_display = pygame.Surface(RAW_DISPLAY_SIZE)

    # maps
    level_01 = TiledMap("tiled-level-01.tmx")
    level_01_img = level_01.build_map()
    camera = Camera(level_01.total_map_width, level_01.total_map_height)

    # other spritesheets and animations
    spritesheet_parser = SpriteSheetParser()

    spritesheet_parser.load_spritesheet("hero")
    player_animations = spritesheet_parser.build_animation_repository()

    # sprites and groups
    collidables = Group()
    all_sprites = Group()

    # objects in objects layer: map parsing
    tile_object: TiledObjectGroup

    for tile_object in level_01.tmx_map.objects:
        if tile_object.name == TMX_OBJECT_PLAYER_NAME:
            player = Player(tile_object.x, tile_object.y, player_animations, all_sprites)

        if tile_object.name == TMX_OBJECT_COLLIDABLE_NAME:
            Collidable(tile_object.x, tile_object.y, tile_object.width, tile_object.height, collidables)

    # main game loop
    while True:
        raw_display.fill(CLEAR_DISPLAY_RGB)  # clears the display
        raw_display.blit(level_01_img, camera.apply_offset(level_01_img.get_rect()))  # shifts by the camera offset

        # input capturing
        captured_input = capture_player_inputs()
        exit_if_captured_quit(captured_input)

        # state update according to inputs
        player.update(captured_input, dt, collidables)
        camera.update(player)

        for sprite in all_sprites:
            raw_display.blit(sprite.image, camera.apply_offset(sprite.rect))

        # scale to the final screen
        scaled_display = pygame.transform.scale(raw_display, WINDOW_SIZE)
        game_screen.blit(scaled_display, (0, 0))

        pygame.display.update()
        dt = game_clock.tick(GAME_FPS) / 1000  # seconds since last frame (last clock tick)


if __name__ == "__main__":
    main()
