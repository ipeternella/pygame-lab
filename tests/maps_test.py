"""
Module with map building tests.
"""
from src.maps import load_level_map


def test_should_load_testing_map():
    # act
    tiles_matrix = load_level_map("test-level-01", "tests/resources")

    # assert
    assert len(tiles_matrix) == 3

    assert tiles_matrix[0] == [".", ".", "."]
    assert tiles_matrix[1] == [".", "1", "."]
    assert tiles_matrix[2] == ["1", "0", "1"]
