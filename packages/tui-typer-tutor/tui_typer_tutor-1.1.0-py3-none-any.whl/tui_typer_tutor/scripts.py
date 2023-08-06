"""Start the command line program."""

from pathlib import Path

import arguably
from beartype import beartype
from corallium.log import logger

from . import __pkg_name__, __version__
from .app.ttt import TuiTyperTutor
from .core.config import get_config
from .core.uninstall import uninstall as run_uninstall


@arguably.command
def parse_ttt_args(
    *,
    seed_file: str = '',
    version: bool | None = False,
    uninstall: bool | None = False,
) -> None:
    """Practice Touch Typing in your terminal.

    Args:
        seed_file: Optional path to seed file used for generating the prompt.
        version: Show program's version number and exit.
        uninstall: Remove all files created by tui-typer-tutor.

    """
    if version:
        logger.text('Version', pkg_name=__pkg_name__, version=__version__)
    elif uninstall:
        run_uninstall()
    else:
        config = get_config()
        if seed_file:
            config.seed_file = Path(seed_file)
        TuiTyperTutor().run()


@beartype
def start() -> None:
    """CLI Entrypoint."""
    arguably.run()
