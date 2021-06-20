"""
Module with animation utilities.
"""
import json
from typing import Any
from typing import Dict
from typing import List
from typing import TypedDict

import pygame
from pygame.surface import Surface

from src.settings import ASSETS_DIR

ImageFrames = TypedDict("ImageFrames", {"image_id": str, "image": Surface, "frames": int})
AnimationRepository = Dict[str, List[ImageFrames]]  # main key is the action name for each animation frames
ImageRepository = Dict[str, Surface]  # main key is the id for each image


class SpriteSheetParser:
    """
    Utility class used to parse animations from spritesheets and their position json.
    """

    _spritesheet_image: pygame.surface.Surface
    _spritesheet_json: Dict[str, Any]

    def _load_json(self, json_path: str) -> Dict:
        with open(json_path) as json_file:
            data = json.load(json_file)

        return data

    def load_spritesheet(self, spritesheet_name: str) -> None:
        png_path = ASSETS_DIR.joinpath(f"spritesheets/{spritesheet_name}.png")
        json_path = ASSETS_DIR.joinpath(f"spritesheets/{spritesheet_name}.json")

        self._spritesheet_image = pygame.image.load(png_path)
        self._spritesheet_json = self._load_json(json_path)

    def build_animation_repository(self) -> AnimationRepository:
        animation_repository: AnimationRepository = {}
        meta_tags: List[Dict] = self._spritesheet_json["meta"]["frameTags"]

        # frameTags helper array parsing
        current_frame_tag = 0  # ix of the frameTag array
        animation_action_name = meta_tags[current_frame_tag]["name"]
        next_frame_tag_check = meta_tags[current_frame_tag]["to"] + 1  # 3

        current_frame = 0
        for image_id, frame_metadata in self._spritesheet_json["frames"].items():
            frame_x, frame_y = frame_metadata["frame"]["x"], frame_metadata["frame"]["y"]
            frame_width, frame_height = frame_metadata["frame"]["w"], frame_metadata["frame"]["h"]
            frames_duration = frame_metadata["duration"]

            rect = pygame.Rect(frame_x, frame_y, frame_width, frame_height)
            image = pygame.Surface(rect.size, pygame.SRCALPHA)  # blank image surface

            image.blit(self._spritesheet_image, (0, 0), rect)  # blit on top of the image surface

            if animation_action_name not in animation_repository:
                animation_repository[animation_action_name] = [
                    {"image_id": image_id, "image": image, "frames": frames_duration // 10}
                ]
            else:
                animation_repository[animation_action_name] += [
                    {"image_id": image_id, "image": image, "frames": frames_duration // 10}
                ]

            current_frame += 1

            # advances parsing of the frameTags section
            if current_frame == next_frame_tag_check:
                current_frame_tag += 1

                # nothing more to be parsed
                if current_frame_tag > len(meta_tags) - 1:
                    break

                next_frame_tag_check = meta_tags[current_frame_tag]["to"] + 1
                animation_action_name = meta_tags[current_frame_tag]["name"]

        return animation_repository
