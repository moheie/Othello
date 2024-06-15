import pygame
import os
from typing import Self

def get_icon_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'resources', 'icons', filename)

class Icons:
    instance: Self = None

    def get() -> Self:
        if Icons.instance == None:
            Icons.instance = Icons()
        
        return Icons.instance

    def __init__(self):
        self.volume_active = pygame.transform.scale(
            pygame.image.load(get_icon_path("volume-3-white.png")),
            (40, 40)
        )

        self.volume_inactive = pygame.transform.scale(
            pygame.image.load(get_icon_path("volume-x-white.png")),
            (40, 40)
        )
