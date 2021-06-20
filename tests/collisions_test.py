"""
Module with collision tests.
"""
import pygame

from src.collisions import get_collisions


def test_should_detect_collision_between_rects():
    # arrange
    player = pygame.Rect(50, 50, 16, 16)
    platform_1 = pygame.Rect(40, 50, 16, 16)
    platform_2 = pygame.Rect(56, 50, 16, 16)
    platform_3 = pygame.Rect(72, 50, 16, 16)  # should not collide

    # act
    collisions = get_collisions(player, [platform_1, platform_2, platform_3])

    # assert
    assert len(collisions) == 2

    assert collisions[0].x == 40  # should be platform_1
    assert collisions[0].y == 50

    assert collisions[1].x == 56  # should be platform_2
    assert collisions[1].y == 50
