import pygame
from pygame.event import Event

from gui.fonts import Fonts
from gui.audio import AudioManager
from gui.scenes.scene import Scene
from game.game import Game, CellState, Color

BACKGROUND_COLOR = 'purple'
CELL_SIZE = 30
CELL_COLOR = (107, 192, 86)
BORDER_SIZE = 3
DISK_RADIUS = 10

SCORE_SCREEN_PADDING = 20
SCORE_Y = 20
SCORE_LABEL_MARGIN = 10

CONTINUE_BUTTON_BACKGROUND_COLOR = (255, 150, 51)
CONTINUE_BUTTON_HOVER_BACKGROUND_COLOR = (227, 131, 41)
CONTINUE_BUTTON_TEXT_COLOR = 'white'
CONTINUE_BUTTON_PADDING = 10

LAST_PLACED_INDICATOR_COLOR = 'red'

AVAILABLE_MOVE_COLORS: dict[Color, any] = {
    Color.BLACK: (40, 40, 40),
    Color.WHITE: (220, 220, 220),
}

COLORS: dict[Color, any] = {
    Color.BLACK: 'black',
    Color.WHITE: 'white',
}

class GameScene(Scene):
    def __init__(self, fonts: Fonts, audio: AudioManager) -> None:
        super().__init__(fonts, audio)

        self.game: Game = None

        self.rows: int = 0
        self.columns: int = 0

    def build(self, params: dict[str, any]):
        self.game = params['game']
        
        self.rows = self.game.rows
        self.columns = self.game.columns

        board_width = BORDER_SIZE * (self.columns + 1) + CELL_SIZE * self.columns
        board_height = BORDER_SIZE * (self.rows + 1) + CELL_SIZE * self.rows

        self.board = pygame.Surface((board_width, board_height))
        self.board.fill(BACKGROUND_COLOR)

        pygame.draw.rect(self.board, 'black', [0, 0, board_width, board_height])

        self.cell_rects: list[list[pygame.Rect]] = []

        for row in range(self.rows):
            self.cell_rects.append([])

            for column in range(self.columns):                
                x = (column + 1) * BORDER_SIZE + CELL_SIZE * column
                y = (row + 1) * BORDER_SIZE + CELL_SIZE * row

                # Draw cell
                self.cell_rects[row].append(pygame.draw.rect(
                    self.board,
                    CELL_COLOR,
                    [x, y, CELL_SIZE, CELL_SIZE],
                ))
        
        self.black_score_label = self.fonts.main_font.render('Black:', False, 'black')
        self.white_score_label = self.fonts.main_font.render('White:', False, 'white')

        self.win_text = self.fonts.main_font.render('You win!', False, 'white')
        self.lose_text = self.fonts.main_font.render('You lose!', False, 'white')
        self.draw_text = self.fonts.main_font.render('It\'s a draw!', False, 'white')

        self.continue_label = self.fonts.main_font.render('Continue', False, CONTINUE_BUTTON_TEXT_COLOR)
        self.continue_button_rect = None
        self.continue_button_hovered = False

        self.volume_button_rect = None

    def draw(self, screen: pygame.Surface):
        screen_rect = screen.get_rect()

        board_rect = self.board.get_rect(center=screen_rect.center)
        self.cell_offset = (board_rect.left, board_rect.top)
        
        screen.fill('purple')
        screen.blit(self.board, board_rect)

        black_score_text = self.fonts.main_font.render(str(self.game.get_count(Color.BLACK)), False, 'black')
        black_score_text_size = black_score_text.get_size()

        white_score_text = self.fonts.main_font.render(str(self.game.get_count(Color.WHITE)), False, 'white')
        white_score_text_size = white_score_text.get_size()
        white_score_label_size = self.white_score_label.get_size()

        # Black score label
        black_score_label_rect = screen.blit(
            self.black_score_label,
            (SCORE_SCREEN_PADDING, SCORE_Y),
        )

        # Black score value
        screen.blit(black_score_text, (black_score_label_rect.right + SCORE_LABEL_MARGIN, SCORE_Y))

        # White score value
        white_score_text_rect = screen.blit(
            white_score_text,
            (screen_rect.right - white_score_text_size[0] - SCORE_SCREEN_PADDING, SCORE_Y),
        )

        # White score label
        screen.blit(
            self.white_score_label,
            (white_score_text_rect.left - white_score_label_size[0] - SCORE_LABEL_MARGIN, SCORE_Y)
        )

        rows = self.game.rows
        columns = self.game.columns

        avail_moves = self.game.available_moves
        last_placed = self.game.last_placed_piece
        
        # print(last_placed)

        for row in range(rows):
            for column in range(columns):
                cell = (row, column)
                cell_state = self.game.get_cell(cell)

                center_x = self.cell_offset[0] + self.cell_rects[row][column].centerx
                center_y = self.cell_offset[1] + self.cell_rects[row][column].centery
                
                if cell_state != CellState.UNOCCUPIED:
                    pygame.draw.circle(
                        screen,
                        COLORS[cell_state.to_color()],
                        (center_x, center_y),
                        DISK_RADIUS,
                    )

                    if last_placed is not None and last_placed[0] == row and last_placed[1] == column:
                        pygame.draw.circle(
                            screen,
                            LAST_PLACED_INDICATOR_COLOR,
                            (center_x, center_y),
                            2
                        )
                elif self.game.is_player_turn() and cell in avail_moves:
                    pygame.draw.circle(
                        screen,
                        AVAILABLE_MOVE_COLORS[self.game.turn],
                        (center_x, center_y),
                        DISK_RADIUS,
                        2
                    )
        
        if self.game.is_over():
            alert_background = pygame.Surface((screen_rect.width, screen_rect.height))

            alert_background.set_alpha(128)
            alert_background.fill('black')

            screen.blit(alert_background, (0, 0))

            alert_text: pygame.Surface = None
            winner = self.game.get_winner()

            if winner == None:
                alert_text = self.draw_text
            elif winner == self.game.min_color:
                alert_text = self.win_text
            else:
                alert_text = self.lose_text

            continue_label_size = self.continue_label.get_size()
            continue_button_width = continue_label_size[0] + (CONTINUE_BUTTON_PADDING * 2)
            continue_button_height = continue_label_size[1] + (CONTINUE_BUTTON_PADDING * 2)

            continue_button_color = CONTINUE_BUTTON_BACKGROUND_COLOR

            if self.continue_button_hovered:
                continue_button_color = CONTINUE_BUTTON_HOVER_BACKGROUND_COLOR

            alert_text_size = alert_text.get_size()
            alert_text_rect = screen.blit(alert_text, (
                screen_rect.centerx - (alert_text_size[0] / 2),
                screen_rect.centery - (alert_text_size[1] / 2) - (continue_button_height / 2)
            ))

            self.continue_button_rect = pygame.draw.rect(
                screen,
                continue_button_color,
                (
                    screen_rect.centerx - (continue_button_width / 2),
                    alert_text_rect.bottom + 20,
                    continue_button_width,
                    continue_button_height,
                ),
            )

            screen.blit(
                self.continue_label,
                (
                    self.continue_button_rect.left + CONTINUE_BUTTON_PADDING,
                    self.continue_button_rect.top + CONTINUE_BUTTON_PADDING,
                ),
            )
        else:
            self.continue_button_rect = None
        
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
    
    def process_event(self, event: Event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            if self.game.is_over():
                if self.continue_button_rect is not None and self.continue_button_rect.collidepoint(pos[0], pos[1]):
                    self.change_scene('menu')
            elif self.game.is_player_turn():
                x = pos[0] - self.cell_offset[0]
                y = pos[1] - self.cell_offset[1]

                for (row, column) in self.game.available_moves:
                    if self.cell_rects[row][column].collidepoint(x, y):
                        self.game.place_cell((row, column))
                
            if self.volume_button_rect.collidepoint(pos[0], pos[1]):
                self.audio.toggle()
        elif event.type == pygame.MOUSEMOTION and self.continue_button_rect is not None:
            pos = pygame.mouse.get_pos()

            if self.continue_button_rect.collidepoint(pos[0], pos[1]):
                self.continue_button_hovered = True
            else:
                self.continue_button_hovered = False
