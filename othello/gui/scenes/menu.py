import pygame
from collections import OrderedDict
from typing import Dict

from gui.scenes.scene import Scene
from game.game import Game, Color, Difficulty

TEXT_OFFSET_X = 20

DISK_RADIUS = 35
DISK_SPACING = 30

SELECTED_COLOR = (255, 150, 51)
SELECTED_PADDING = 18 # Padding isn't the right word for this, but it's basically extra space?
SELECTED_WIDTH = 5

DIFFICULTY_SPACING = 40

START_BUTTON_COLOR = (255, 150, 51)
START_BUTTON_HOVER_COLOR = (227, 131, 41)
START_BUTTON_TEXT_COLOR = 'white'
START_BUTTON_PADDING = 10

class MenuScene(Scene):
    def build(self, _: dict[str, any]):
        self.selected_color = Color.BLACK
        self.selected_difficulty = Difficulty.EASY

        self.color_rects: Dict[Color, pygame.Rect] = {}
        self.diff_rects: Dict[Difficulty, pygame.Rect] = {}

        self.disk_text = self.fonts.main_font.render('Choose disk color', False, 'white')
        self.diff_text = self.fonts.main_font.render('Choose a difficulty', False, 'white')

        self.difficulties: Dict[Difficulty, pygame.Surface] = OrderedDict()
        self.diff_width_sum = 0

        for diff in Difficulty:
            text = self.fonts.main_font_small.render(diff.value, False, 'white')

            self.diff_width_sum += text.get_size()[0]
            self.difficulties[diff] = text
        

        self.start_text = self.fonts.main_font.render('Start', False, START_BUTTON_TEXT_COLOR)
        self.start_button_rect = None
        self.start_button_hovered = False

        self.volume_button_rect = None

    def draw(self, screen: pygame.Surface):
        screen.fill('purple')

        disk_text_rect = screen.blit(self.disk_text, (TEXT_OFFSET_X, 20))
        screen_rect = screen.get_rect()
        
        black_disk_x = screen_rect.centerx - DISK_RADIUS - DISK_SPACING
        white_disk_x = screen_rect.centerx + DISK_RADIUS + DISK_SPACING
        disk_y = disk_text_rect.bottom + 80

        self.color_rects[Color.BLACK] = pygame.draw.circle(
            screen,
            'black',
            (black_disk_x, disk_y),
            DISK_RADIUS,
        )

        self.color_rects[Color.WHITE] = pygame.draw.circle(
            screen,
            'white',
            (white_disk_x, disk_y),
            DISK_RADIUS,
        )

        selected_circle_x = 0

        if self.selected_color == Color.BLACK:
            selected_circle_x = black_disk_x
        else:
            selected_circle_x = white_disk_x

        pygame.draw.circle(
            screen,
            SELECTED_COLOR,
            (selected_circle_x, disk_y),
            DISK_RADIUS + SELECTED_PADDING,
            SELECTED_WIDTH,
        )
        
        diff_text_offset_y = disk_y + DISK_RADIUS + SELECTED_PADDING + 20
        diff_text_rect = screen.blit(self.diff_text, (TEXT_OFFSET_X, diff_text_offset_y))

        diff_count = len(self.difficulties)
        diff_value_text_x = screen_rect.centerx - (self.diff_width_sum / 2) - ((diff_count - 1) * DIFFICULTY_SPACING) / 2
        diff_value_text_y = diff_text_rect.bottom + 30

        diff_line_bottom = 0

        for diff, text in self.difficulties.items():
            rect = screen.blit(
                text,
                (diff_value_text_x, diff_value_text_y),
            )

            self.diff_rects[diff] = rect
            diff_line_bottom = max(diff_line_bottom, rect.bottom)
            
            text_size = text.get_size()
            
            if self.selected_difficulty == diff:
                pygame.draw.rect(
                    screen,
                    SELECTED_COLOR,
                    (
                        diff_value_text_x - (SELECTED_PADDING / 2),
                        diff_value_text_y - (SELECTED_PADDING / 2),
                        text_size[0] + SELECTED_PADDING,
                        text_size[1] + SELECTED_PADDING,
                    ),
                    SELECTED_WIDTH,
                )

            diff_value_text_x += text_size[0] + DIFFICULTY_SPACING
        
        start_text_size = self.start_text.get_size()

        start_button_width = start_text_size[0] + (START_BUTTON_PADDING * 2)
        start_button_height = start_text_size[1] + (START_BUTTON_PADDING * 2)

        start_button_x = screen_rect.centerx - start_button_width / 2
        start_button_y = diff_line_bottom + 40
        
        start_button_color = START_BUTTON_COLOR

        if self.start_button_hovered:
            start_button_color = START_BUTTON_HOVER_COLOR

        self.start_button_rect = pygame.draw.rect(
            screen,
            start_button_color,
            (
                start_button_x, start_button_y,
                start_button_width, start_button_height
            ),
        )

        screen.blit(
            self.start_text,
            (
                start_button_x + START_BUTTON_PADDING,
                start_button_y + START_BUTTON_PADDING,
            ),
        )

        icon: pygame.Surface = None

        if self.audio.muted:
            icon = self.icons.volume_inactive
        else:
            icon = self.icons.volume_active
        
        icon_size = icon.get_size()

        self.volume_button_rect = screen.blit(
            icon,
            (
                screen_rect.right - icon_size[0] - 20,
                screen_rect.bottom - icon_size[1] - 20
            )
        )
    
    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            for diff, rect in self.diff_rects.items():
                if rect.collidepoint(pos[0], pos[1]):
                    self.selected_difficulty = diff

                    return
            
            for color, rect in self.color_rects.items():
                if rect.collidepoint(pos[0], pos[1]):
                    self.selected_color = color

                    return
            
            if self.start_button_rect.collidepoint(pos[0], pos[1]):
                self.change_scene('game', {
                    'game': Game(self.selected_color, self.selected_difficulty)
                })
            
            if self.volume_button_rect.collidepoint(pos[0], pos[1]):
                self.audio.toggle()
        elif event.type == pygame.MOUSEMOTION and self.start_button_rect is not None:
            pos = pygame.mouse.get_pos()

            if self.start_button_rect.collidepoint(pos[0], pos[1]):
                self.start_button_hovered = True
            else:
                self.start_button_hovered = False
            