import pygame
import os

from typing import Self

def get_font_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'resources', 'fonts', filename)

class Fonts:
    instance: Self = None

    def get() -> Self:
        if Fonts.instance == None:
            Fonts.instance = Fonts()
        
        return Fonts.instance

    def __init__(self):
        self.main_font = pygame.font.Font(get_font_path('Eight-Bit Madness.ttf'), 42)
        self.main_font_small = pygame.font.Font(get_font_path('Eight-Bit Madness.ttf'), 34)
