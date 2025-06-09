import pygame
import os


class SoundManager:
    def __init__(self, game):
        self.game = game
        pygame.mixer.init()

        self.sounds = {}
        self.music = {}

        self.sound_volume = 1.0
        self.music_volume = 1.0

    def load_sound(self, name, path):
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.sound_volume)
            self.sounds[name] = sound
            return True
        except pygame.error:
            print(f"Could not load sound: {path}")
            return False

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"Sound not found: {name}")

    def load_music(self, name, path):
        if os.path.exists(path):
            self.music[name] = path
            return True
        else:
            print(f"Could not find music file: {path}")
            return False

    def play_music(self, name, loops=-1, fade_ms=0):
        if name in self.music:
            try:
                pygame.mixer.music.load(self.music[name])
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loops, fade_ms=fade_ms)
            except pygame.error:
                print(f"Could not play music: {name}")
        else:
            print(f"Music not found: {name}")

    def stop_music(self, fade_ms=0):
        pygame.mixer.music.fadeout(fade_ms)

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()

    def set_sound_volume(self, volume):
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)