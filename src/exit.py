"""
Module with functions to handle quitting the game.
"""
import sys

import pygame

from src.inputs import CapturedInput


def exit_if_captured_quit(captured_input: CapturedInput) -> None:
    """
    Exists the game process with a zero status code.
    """

    if captured_input.should_quit:
        pygame.quit()
        sys.exit(0)
