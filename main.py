import sys

from core.utilities.sdl_init import initialize_sdl


def main() -> int:
    initialize_sdl()
    start_game()
    return 0


def start_game() -> None:
    """ Start the game. """
    from pong import game
    game.run()


if __name__ == "__main__":
    sys.exit(main())
