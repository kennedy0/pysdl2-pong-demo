import os
from pathlib import Path


def initialize_sdl() -> None:
    """ Initialize SDL. """
    # DLL path must be set before SDL is imported
    project_root = Path(__file__).parent.parent.parent
    sdl2_dll = project_root / "dll"
    os.environ['PYSDL2_DLL_PATH'] = sdl2_dll.as_posix()

    # Now we can import SDL2 and initialize it
    import sdl2.ext
    sdl2.ext.init()

    import sdl2.sdlimage
    sdl2.sdlimage.IMG_Init(sdl2.sdlimage.IMG_INIT_PNG)

    import sdl2.sdlmixer
    sdl2.sdlmixer.Mix_OpenAudio(
        sdl2.sdlmixer.MIX_DEFAULT_FREQUENCY,
        sdl2.sdlmixer.MIX_DEFAULT_FORMAT,
        sdl2.sdlmixer.MIX_DEFAULT_CHANNELS,
        2048
    )
