import pygame

from gui.fonts import Fonts
from gui.icons import Icons
from gui.audio import AudioManager
from gui.scenes.scene import Scene
from gui.scenes.menu import MenuScene
from gui.scenes.game import GameScene
from gui.events import CHANGE_SCENE

class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()

        self.audio = AudioManager()
        self.audio.set_file('yoshistudios_8bit_retro_game_loop.mp3')

        self.icons = Icons()

        pygame.display.set_caption('Othello')

        self.fonts = Fonts()
        self.screen = pygame.display.set_mode((520,400))
        self.scenes: dict[str, Scene] = {
            'menu': MenuScene(self.fonts, self.audio),
            'game': GameScene(self.fonts, self.audio),
        }
        
        self.set_scene('menu')
        self.start()
    
    def set_scene(self, scene_name: str, params: dict[str, any] = {}):
        scene = self.scenes[scene_name]
        scene.build(params)

        self.scene = scene
    
    def start(self):
        clock = pygame.time.Clock()

        while True:
            # Process player inputs.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == CHANGE_SCENE:
                    self.set_scene(event.dict['scene'], event.dict['params'])
                else:
                    self.scene.process_event(event)


            self.scene.draw(self.screen)

            pygame.display.flip()  # Refresh on-screen display
            clock.tick(60)
