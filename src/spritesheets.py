"""
Module with spritesheets utilities.
"""
import json
from typing import Any
from typing import Dict
from typing import List

import pygame
from pygame.surface import Surface

from src.settings import ASSETS_DIR


class SpriteSheet:

    _spritesheet_image: pygame.surface.Surface
    _spritesheet_json: Dict[str, Any]

    def __init__(self, spritesheet_name: str) -> None:
        png_path = ASSETS_DIR.joinpath(f"spritesheets/{spritesheet_name}.png")
        json_path = ASSETS_DIR.joinpath(f"spritesheets/{spritesheet_name}.json")

        self._spritesheet_image = pygame.image.load(png_path)
        self._spritesheet_json = self._load_json(json_path)

    def _load_json(self, json_path: str) -> Dict:
        with open(json_path) as json_file:
            data = json.load(json_file)

        return data

    def get_all(self) -> List[Surface]:
        images: List[Surface] = []

        for _, frame_metadata in self._spritesheet_json["frames"].items():
            frame_x, frame_y = frame_metadata["frame"]["x"], frame_metadata["frame"]["y"]
            frame_width, frame_height = frame_metadata["frame"]["w"], frame_metadata["frame"]["h"]

            rect = pygame.Rect(frame_x, frame_y, frame_width, frame_height)
            image = pygame.Surface(rect.size)  # blank image surface

            image.blit(self._spritesheet_image, (0, 0), rect)  # blit on top of the image surface
            images.append(image)

        return images
