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
    assert len(parser.spritesheet_json["frames"]) == 6
    assert [*parser.spritesheet_json["frames"]] == [
        "hero-idle-0",
        "hero-idle-1",
        "hero-idle-2",
        "hero-idle-3",
        "hero-run-0",
        "hero-run-1",
    ]

    # assert - json frameTags
    assert len(parser.spritesheet_json["meta"]["frameTags"]) == 2
    assert parser.spritesheet_json["meta"]["frameTags"] == [
        {"name": "idle", "from": 0, "to": 3, "direction": "forward"},
        {"name": "run", "from": 4, "to": 5, "direction": "forward"},
    ]


def test_should_build_animation_repository():
    # arrange
    parser = SpriteSheetParser()
    parser.load_spritesheet("hero-idle-test", "tests/resources/")

    # act
    animation_repository = parser.build_animation_repository()

    # assert - loaded animation repository
    assert [*animation_repository.keys()] == ["idle", "run"]
    assert len(animation_repository["idle"]) == 4

    assert animation_repository["idle"][0]["frames"] == 20
    assert animation_repository["idle"][0]["image_id"] == "hero-idle-0"

    assert animation_repository["idle"][1]["frames"] == 20
    assert animation_repository["idle"][1]["image_id"] == "hero-idle-1"

    assert animation_repository["idle"][2]["frames"] == 20
    assert animation_repository["idle"][2]["image_id"] == "hero-idle-2"

    assert animation_repository["idle"][3]["frames"] == 40
    assert animation_repository["idle"][3]["image_id"] == "hero-idle-3"

    assert len(animation_repository["run"]) == 2
    assert animation_repository["run"][0]["frames"] == 10
    assert animation_repository["run"][0]["image_id"] == "hero-run-0"

    assert animation_repository["run"][1]["frames"] == 30
    assert animation_repository["run"][1]["image_id"] == "hero-run-1"
