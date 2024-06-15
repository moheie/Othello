import pygame
import os

UNMUTED_VOLUME = 0.1

def get_audio_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'resources', 'audio', filename)

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(UNMUTED_VOLUME)
        
        self.muted = False
    
    def set_file(self, filename: str):
        pygame.mixer.music.load(get_audio_path(filename))
        pygame.mixer.music.play(loops=-1)
    
    def mute(self):
        pygame.mixer.music.set_volume(0)

        self.muted = True
    
    def unmute(self):
        pygame.mixer.music.set_volume(UNMUTED_VOLUME)

        self.muted = False
    
    def toggle(self):
        if self.muted:
            self.unmute()
        else:
            self.mute()