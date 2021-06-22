"""
Module with animations tests.
"""

from src.animations import SpriteSheetParser


def test_should_load_spritesheet_png_and_json():
    # arrange
    parser = SpriteSheetParser()

    # act
    parser.load_spritesheet("hero-idle-test", "tests/resources/")

    # assert - png
    assert parser.spritesheet_image.get_width() == 64  # 4 frames of 16x16
    assert parser.spritesheet_image.get_height() == 16

    # assert - json frames
    assert len(parser.spritesheet_json["frames"]) == 4
    assert [*parser.spritesheet_json["frames"]] == ["hero-idle-0", "hero-idle-1", "hero-idle-2", "hero-idle-3"]

    # assert - json frameTags
    assert len(parser.spritesheet_json["meta"]["frameTags"]) == 1
    assert parser.spritesheet_json["meta"]["frameTags"] == [
        {"name": "idle", "from": 0, "to": 3, "direction": "forward"}
    ]
