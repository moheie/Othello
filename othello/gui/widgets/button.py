import pygame
from typing import Self

from gui.fonts import Fonts

DEFAULT_BACKGROUND_COLOR = (255, 150, 51)
DEFAULT_HOVER_BACKGROUND_COLOR = (227, 131, 41)
DEFAULT_TEXT_COLOR = 'white'
DEFAULT_PADDING = 10

class Button:
    def __init__(self, label: str) -> None:
        self.label = label
        self.background_color: any = DEFAULT_BACKGROUND_COLOR
        self.hover_background_color: any = DEFAULT_HOVER_BACKGROUND_COLOR
        self.text_color: any = DEFAULT_TEXT_COLOR
        self.padding: int = DEFAULT_PADDING
        self.fonts = Fonts.get()

        self.label_surface: pygame.Surface = None
        self.surface: pygame.Surface = None
        
        self.hovered = False

    def get_surface(self):
        if self.surface == None:
            self.build()
        
        return self.surface

    def set_padding(self, padding: int) -> Self:
        self.padding = padding

        return self

    def set_background_color(self, background_color: any) -> Self:
        self.background_color = background_color

        return self
    
    def set_hover_background_color(self, hover_background_color: any) -> Self:
        self.hover_background_color = hover_background_color

        return self
    
    def set_text_color(self, text_color: any) -> Self:
        self.text_color = text_color
        self.build()

        return self
    
    def set_hovered(self, hovered: bool) -> Self:
        if hovered != self.hovered:
            self.hovered = hovered
            self.redraw()
        
        return self
    
    def build(self):
        self.label_surface = self.fonts.main_font.render(self.label, False, self.text_color)
        self.redraw()

    def redraw(self):
        self.surface = self.draw()

    def draw(self) -> pygame.Surface:
        label_size = self.label_surface.get_size()

        width = label_size[0] + (self.padding * 2)
        height = label_size[1] + (self.padding * 2)

        surface = pygame.Surface((width, height))
        bg_color = self.background_color

        if self.hovered and self.hover_background_color is not None:
            bg_color = self.hover_background_color

        pygame.draw.rect(
            surface,
            bg_color,
            (
                0, 0,
                width, height
            ),
        )

        surface.blit(
            self.label_surface,
            (
                self.padding,
                self.padding,
            ),
        )

        return surface