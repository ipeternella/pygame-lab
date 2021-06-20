"""
Module with inputs handling tests.
"""
from unittest import mock

from pygame.constants import K_RIGHT
from pygame.constants import K_SPACE
from pygame.constants import KEYDOWN
from pygame.event import Event

from src.inputs import capture_player_inputs


@mock.patch("src.inputs.pygame.event.get")
def test_should_capture_right_keydown(mock_pygame_get):
    # arrange
    mock_input_1 = mock.MagicMock(Event)
    mock_input_2 = mock.MagicMock(Event)

    mock_input_1.type = KEYDOWN
    mock_input_1.key = K_RIGHT

    mock_input_2.type = KEYDOWN
    mock_input_2.key = K_SPACE

    mock_pygame_get.return_value = [mock_input_1, mock_input_2]

    # act
    captured_inputs = capture_player_inputs()

    # assert
    assert captured_inputs.moving_left is False
    assert captured_inputs.moving_right is True
    assert captured_inputs.has_jumped is True
