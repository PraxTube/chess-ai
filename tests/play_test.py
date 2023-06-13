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


@pytest.mark.timeout(10)
def test_start_fen_koth():
    depths = [1, 2, 3, 4, 5]
    for depth in depths:
        debug_info = DebugInfo(depth)
        fen = "8/6k1/6p1/5p2/2K5/4b1N1/4n3/8 w - - 0 1"
        result, end_board = play.main_loop(depth, debug_info, turn_limit=2, fen=fen)

        assert result == 1, f"Failed at depth: {depth}, {result} == {1}"
        assert "8/6k1/6p1/3K1p2/8/4b1N1/4n3/8 b - - 0 1" == end_board.fen()


@pytest.mark.timeout(5)
def INGORE_test_start_fen_checkmate():
    depth = 4
    debug_info = DebugInfo(depth)
    fen = "8/5p2/5P1p/5PkN/6P1/4N1Rp/7P/6KQ w - - 0 1"
    result, end_board = play.main_loop(depth, debug_info, turn_limit=4, fen=fen)

    assert result == 1
    assert "8/5p2/5P1p/5PkN/6PP/6R1/6p1/6KQ b - - 0 1" == end_board.fen()
