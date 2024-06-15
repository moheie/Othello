import pygame
from typing import Self

from gui.fonts import Fonts
from gui.icons import Icons
from gui.audio import AudioManager
from gui.events import CHANGE_SCENE

class Scene:
    def __init__(self, fonts: Fonts, audio: AudioManager) -> None:
        self.fonts = fonts
        self.audio = audio
        self.icons = Icons.get()

    def build(self, params: dict[str, any]):
        pass

    def draw(self, screen: pygame.Surface):
        pass

    def process_event(self, event: pygame.event.Event):
        pass

    def change_scene(self, scene_name: str, params: dict[str, any] = {}):
        event = pygame.event.Event(CHANGE_SCENE, {
            'scene': scene_name,
            'params': params,
        })

        pygame.event.post(event)