"""
Module with functions to handle quitting the game.
"""
import sys

import pygame

from src.inputs import CapturedInput


def game_over(captured_input: CapturedInput) -> None:
    if captured_input.should_quit:
        pygame.quit()
        sys.exit(0)
