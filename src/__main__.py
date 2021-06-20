"""
Module with the main game loop.
"""

import pygame
from pygame.surface import Surface
from pygame.time import Clock

from src.animations import AnimationRepository
from src.animations import SpriteSheetParser
from src.collisions import move
from src.exit import exit_if_captured_quit
from src.inputs import capture_player_inputs
from src.maps import load_level_map
from src.maps import render_level_map
from src.player import Player
from src.scrolling import Scroll
from src.settings import GAME_FPS
from src.settings import RAW_DISPLAY_SIZE
from src.settings import WINDOW_SIZE
from src.settings import WINDOW_TITLE
from src.utils import load_image_asset


def main():
    pygame.init()
    game_clock = Clock()

    # main screen
    game_screen: Surface = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    pygame.display.set_caption(WINDOW_TITLE)

    # raw_display is the main blit Surface which is scaled later
    raw_display = pygame.Surface(RAW_DISPLAY_SIZE)

    # images
    grass_img = load_image_asset("img/grass.png")
    dirt_img = load_image_asset("img/dirt.png")

    # level
    level_01 = load_level_map("level-01")

    spritesheet_parser = SpriteSheetParser()

    # loading player's spritesheets
    spritesheet_parser.load_spritesheet("hero-idle")
    idle_repository = spritesheet_parser.build_animation_repository()

    spritesheet_parser.load_spritesheet("hero-run")
    run_repository = spritesheet_parser.build_animation_repository()

    player_animations: AnimationRepository = {**idle_repository, **run_repository}

    # player
    player = Player(50, 50, player_animations)
    scroll = Scroll(0.0, 0.0)

    # main game loop
    while True:
        raw_display.fill((146, 244, 255))  # clears the display
        scroll.update(player.rect.x, player.rect.y)  # update scrolling according to last player's updated position
        tile_rects = render_level_map(raw_display, [dirt_img, grass_img], level_01, player, scroll)

        # input capturing
        captured_input = capture_player_inputs()

        # input handling by entities (updating)
        exit_if_captured_quit(captured_input)
        player.update(captured_input)
        move(player.rect, player.speed, tile_rects)  # update player + collisions

        # scale display is what is blit on the game screen
        raw_display.blit(player.image, (player.rect.x - scroll.offset_x, player.rect.y - scroll.offset_y))
        scaled_display = pygame.transform.scale(raw_display, WINDOW_SIZE)
        game_screen.blit(scaled_display, (0, 0))

        pygame.display.update()
        game_clock.tick(GAME_FPS)


if __name__ == "__main__":
    main()
