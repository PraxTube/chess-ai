import pytest

from chess_ai import play
from chess_ai.log import DebugInfo


def test_debug_info():
    depth = 1
    debug_info = DebugInfo(depth)
    play.main_loop(depth, debug_info, turn_limit=3)

    assert debug_info.nodes_searched > 0
    assert debug_info.nodes_searched < 100

    assert isinstance(debug_info.move_details, dict)
    assert 0 == len(debug_info.move_details)

    depth = 1
    debug_info = DebugInfo(depth)
    play.main_loop(depth, debug_info, turn_limit=4)

    assert debug_info.nodes_searched == 0

    assert isinstance(debug_info.move_details, dict)
    assert 0 == len(debug_info.move_details)

    depth = 2
    debug_info = DebugInfo(depth)
    play.main_loop(depth, debug_info, turn_limit=3)

    assert debug_info.nodes_searched > 50
    assert debug_info.nodes_searched < 1000

    assert isinstance(debug_info.move_details, dict)
    assert 1 == len(debug_info.move_details)

    depth = 2
    debug_info = DebugInfo(depth)
    play.main_loop(depth, debug_info, turn_limit=4)

    assert debug_info.nodes_searched == 0

    assert isinstance(debug_info.move_details, dict)
    assert 1 == len(debug_info.move_details)

    depth = 3
    debug_info = DebugInfo(depth)
    play.main_loop(depth, debug_info, turn_limit=3)

    assert debug_info.nodes_searched > 500
    assert debug_info.nodes_searched < 10000

    assert isinstance(debug_info.move_details, dict)
    assert 2 == len(debug_info.move_details)


@pytest.mark.timeout(1)
def test_start_fen():
    depth = 2
    debug_info = DebugInfo(depth)
    fen = "8/6k1/6p1/5p2/2K5/4b1P1/4n3/8 w - - 1 7"
    result = play.main_loop(depth, debug_info, fen=fen)

    assert result == 1
