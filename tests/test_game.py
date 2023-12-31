import pytest
from snake import core
from tests.fixtures import fake_curses, fake_stdscr  # noqa: F401
from tests.util import fake_getch_pause


def test_pause(monkeypatch, fake_curses, fake_stdscr):  # noqa: F811
    monkeypatch.setattr(fake_stdscr, "getch", fake_getch_pause)
    game = core.Game(fake_stdscr)
    snake_before = game.snake.body
    game.pause()
    assert game.snake.body == snake_before


def test_restart(fake_stdscr):  # noqa: F811
    game = core.Game(fake_stdscr)
    game.restart()
    assert game.food_counter == 0 and game.score == 0


@pytest.mark.parametrize(
    "current, wanted",
    [
        [core.Direction.RIGHT, core.Direction.LEFT],
        [core.Direction.LEFT, core.Direction.RIGHT],
        [core.Direction.UP, core.Direction.DOWN],
        [core.Direction.DOWN, core.Direction.UP],
    ],
)
def test_set_direction(current, wanted, fake_stdscr):  # noqa: F811
    game = core.Game(fake_stdscr)
    game.snake.direction = current
    assert game.set_direction(wanted) is None


@pytest.mark.parametrize(
    "current, valid",
    [
        [core.Direction.UP, [core.Direction.LEFT, core.Direction.RIGHT]],
        [core.Direction.DOWN, [core.Direction.LEFT, core.Direction.RIGHT]],
        [core.Direction.LEFT, [core.Direction.UP, core.Direction.DOWN]],
        [core.Direction.RIGHT, [core.Direction.UP, core.Direction.DOWN]],
    ],
)
def test_set_direction_valid(current, valid, fake_stdscr):  # noqa: F811
    game = core.Game(fake_stdscr)
    for direction in valid:
        game.snake.direction = current
        game.set_direction(direction)
        assert game.snake.direction == direction


@pytest.mark.parametrize(
    "before, after",
    [
        [0, 1],
        [23, 24],
        [99, 0],
    ],
)
def test_handle_food_counter(before, after, fake_stdscr):  # noqa: F811
    game = core.Game(fake_stdscr)
    game.food_counter = before
    game.handle_food()
    assert game.food_counter == after


def test_handle_food_updating_score(fake_stdscr):  # noqa: F811
    game = core.Game(fake_stdscr)
    game.food.coord.y = game.snake.body[-1].y
    game.food.coord.x = game.snake.body[-1].x + 1
    game.snake.move()
    game.handle_food()
    assert game.score == 1 and game.food_counter == 0
