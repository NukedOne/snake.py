import pytest
from snake import application
from snake import core
from snake import user_interface
from tests.fixtures import (
    fake_curses,  # noqa: F401
    fake_stdscr,  # noqa: F401
)
from tests.util import (
    fake_game_over,  # noqa: F401
    fake_getch_app,
    fake_pause,
)


@pytest.mark.parametrize(
    "attr, value",
    [
        ["LINES", user_interface.PLAYGROUND_HEIGHT - 1],
        ["COLS", user_interface.PLAYGROUND_WIDTH - 1],
    ],
)
def test_ensuring_terminal_size(monkeypatch, fake_curses, fake_stdscr, attr, value):  # noqa: F811
    monkeypatch.setattr(fake_curses, attr, value)
    with pytest.raises(AssertionError):
        application.main(fake_stdscr)


def test_user_input(monkeypatch, fake_curses, fake_stdscr):  # noqa: F811
    monkeypatch.setattr(fake_stdscr, "getch", fake_getch_app)
    monkeypatch.setattr(core.Game, "pause", fake_pause)
    with pytest.raises(SystemExit):
        application.main(fake_stdscr)
