import sdl2.sdlmixer

from core.content import Content
from core.engine import Engine


class Sound:
    def __init__(self, content_path: str) -> None:
        self._engine = Engine.instance()
        self._audio = Content.load_audio(content_path)

    def play(self):
        """ Play the audio. """
        sdl2.sdlmixer.Mix_PlayChannel(channel=-1, chunk=self._audio, loops=0)
