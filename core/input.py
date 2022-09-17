import sdl2
import sdl2.ext
import sdl2.keyboard


class Input:
    __keys = set()

    @classmethod
    def update(cls, event: sdl2.SDL_Event) -> None:
        """ Update the input state. """
        key = event.key.keysym.sym
        repeat = event.key.repeat

        if event.type == sdl2.SDL_KEYDOWN and repeat == 0:
            cls.__keys.add(key)
        elif event.type == sdl2.SDL_KEYUP and repeat == 0:
            cls.__keys.remove(key)

    @classmethod
    def get_key(cls, key: int) -> bool:
        """ Check if a key is pressed. """
        return key in cls.__keys
