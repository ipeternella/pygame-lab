"""
Module with with player input DTOs.
"""
from dataclasses import dataclass

import pygame
from pygame.constants import K_LEFT
from pygame.constants import K_RIGHT
from pygame.constants import K_SPACE
from pygame.constants import KEYDOWN
from pygame.constants import KEYUP
from pygame.constants import QUIT
from pygame.event import Event


@dataclass
class CapturedInput:
    should_quit: bool = False

    moving_left: bool = False
    moving_left_stop: bool = False

    moving_right: bool = False
    moving_right_stop: bool = False

    has_jumped: bool = False


def capture_player_inputs() -> CapturedInput:
    """
    Fetches player inputs from Pygame's input queue.
    """
    captured_input = CapturedInput()
    event: Event

    for event in pygame.event.get():
        if event.type == QUIT:
            captured_input.should_quit = True

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                captured_input.moving_right = True
            if event.key == K_LEFT:
                captured_input.moving_left = True
            if event.key == K_SPACE:
                captured_input.has_jumped = True

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                captured_input.moving_right_stop = True
            if event.key == K_LEFT:
                captured_input.moving_left_stop = True

    return captured_input
