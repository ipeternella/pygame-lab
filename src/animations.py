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

from src.settings import ROOT_DIR

ImageFrames = TypedDict("ImageFrames", {"image_id": str, "image": Surface, "frames": int})
AnimationRepository = Dict[str, List[ImageFrames]]  # main key is the action name for each animation frames


class Animator:
    """
    Class used to generate sprite images according to an animation repository.
    """

    _repository: AnimationRepository
    _image: Surface
    _current_image_position: int
    _image_total_frames: int
    _image_frame_counter: int
    _animation_action: str

    def __init__(self, initial_action: str, animation_repository: AnimationRepository) -> None:
        self._repository = animation_repository
        self._animation_action = initial_action
        self._current_image_position = 0  # index inside action images list
        self._image_frame_counter = 0  # current frame position of the same image
        self._image_total_frames = self._fetch_current_image_total_frames()
        self._image = self._repository[self._animation_action][0]["image"]

    @property
    def image(self) -> Surface:
        return self._image

    def update(self):
        """
        Called once per frame in order to advance the animation state to fetch next frames/images.
        """
        action_image_list = self._repository[self._animation_action]
        self._image = action_image_list[self._current_image_position]["image"]

        self._advance_animation(action_image_list)

    def change_action(self, new_animation_action: str) -> None:
        """
        Changes the current animation action in order to fetch its respective action image list. This method resets
        the animator state only if the new action is different than the current one.
        """
        if new_animation_action != self._animation_action:
            self._animation_action = new_animation_action
            self._image_frame_counter = 0
            self._current_image_position = 0
            self._image_total_frames = self._fetch_current_image_total_frames()

    def _fetch_current_image_total_frames(self) -> int:
        """
        Given the current self._animation_action and self._current_image_position (index inside the action
        list), returns the total number of frames that the current image from the repository should be displayed.

        Example: {"run": [{"image": Surface, "frames": 10}, ...]} <--- returns 10
        """
        return self._repository[self._animation_action][self._current_image_position]["frames"]

    def _advance_animation(self, action_image_list: List[ImageFrames]):
        """
        Advance the current animation frame. If the current image frame (self._image_frame_counter) has reached
        its total frames (self._image_total_frames), then the next image from the repository is fetched by
        advancing self._current_image_position.

        If self._current_image_position > length of the action image list, then the list is repeated by
        setting self._current_image_position = 0, self._image_frame_counter = 0.
        """
        self._image_frame_counter += 1

        # stick to the same animation image until its frames are out in the repository, then advance!
        if self._image_frame_counter > self._image_total_frames:
            self._image_frame_counter = 0
            self._current_image_position += 1

            if self._current_image_position > len(action_image_list) - 1:
                self._current_image_position = 0

            self._image_total_frames = self._fetch_current_image_total_frames()


class SpriteSheetParser:
    """
    Utility class used to parse animations from spritesheets and their position json.
    """

    _spritesheet_image: Surface
    _spritesheet_json: Dict[str, Any]

    @property
    def spritesheet_image(self) -> Surface:
        return self._spritesheet_image

    @property
    def spritesheet_json(self) -> Dict:
        return self._spritesheet_json

    def load_spritesheet(self, spritesheet_name: str, spritesheet_path: str = "assets/spritesheets/") -> None:
        """
        Loads a spritesheet png image and its position json file into the instance's state.
        """
        spritesheet_png_path = ROOT_DIR.joinpath(spritesheet_path, f"{spritesheet_name}.png")
        spritesheet_json_path = ROOT_DIR.joinpath(spritesheet_path, f"{spritesheet_name}.json")

        self._spritesheet_image = pygame.image.load(spritesheet_png_path)
        self._spritesheet_json = self._load_json(spritesheet_json_path)

    def build_animation_repository(self) -> AnimationRepository:
        """
        After having loaded a spritesheet png and its json, this method can be used to build an animation repository
        which is a dictionary in which each key is an animation action (defined by 'frameTags' name). As such, this
        method requires that the spritesheet json contains a frameTag name property. Each group of frames are loaded
        into the animation repository dictionary under their action name (frameTags.name).

        This method is heavily dependent on Aseprite's json format, including the frameTags section.
        """
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

    def _load_json(self, json_path: str) -> Dict:
        """
        Fetches a json file from disk and deserializes it into a dictionary.
        """
        with open(json_path) as json_file:
            data = json.load(json_file)

        return data
