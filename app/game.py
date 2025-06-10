import pygame
from app import config, display, sounds
from customObjects import custom_text, custom_images, custom_button

class Game:
    def __init__(self):
        pygame.init()

        config.set_config()

        self.cfg = config.read_config()

        self.version = self.cfg['version']
        self.width = int(self.cfg['width'])
        self.height = int(self.cfg['height'])
        self.fps = float(self.cfg['fps'])
        self.title = self.cfg['title']
        self.fullscreen = int(self.cfg['full-screen'])
        self.enable_debug = int(self.cfg['enable_debug'])
        self.sound_volume = float(self.cfg['sound_volume'])
        self.music_volume = float(self.cfg['music_volume'])

        self.objects_in_memory = 0
        self.clock = pygame.time.Clock()
        self.font = None

        self.delta_time = self.clock.get_time()/ 1000.0

        self.run = True


        self.objects = []

        self.screen = pygame.display.set_mode((self.width, self.height))
        if self.fullscreen:
            pygame.display.toggle_fullscreen()
        pygame.display.set_caption(f"{self.title} (v {self.version})")

        self.sound_manager = sounds.SoundManager(self)

        self.sound_manager.set_sound_volume(self.sound_volume)
        self.sound_manager.set_music_volume(self.music_volume)

        self.sound_manager.load_music("background", "music/InTheBeninging.wav")
        self.sound_manager.play_music("background")

        self.displays = {
            'template_display': display.basic_display(self),
            'game_display': display.game_display(self),
            'main_menu': display.main_menu_display(self),
            'options_display': display.options_display(self),
            'pause_menu': display.pause_menu_display(self)
        }
        self.current_display = self.displays['main_menu']

        self.pointing_at = []


        self.debug = False
        self.debug_items = [custom_text.Custom_text(self, 12, 15, f'Current version: {self.version}', text_color='white', font=self.font, font_height=30,  center=False),
                            custom_text.Custom_text(self, 12, 45, f'Resolution: {self.width}x{self.height}', font=self.font, font_height=30, text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 75, f'FPS cap: {self.fps}', font=self.font, font_height=30,  text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 105, f'FPS: {self.clock.get_fps()}', font=self.font, font_height=30,  text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 135, f'Objects in memory: {self.current_display.objects_in_memory}', font=self.font, font_height=30,  text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 165, f'Current display: {type(self.current_display)}', font=self.font, font_height=30,  text_color='white', center=False)]

        for debug_item in self.debug_items:
            debug_item.hidden = True


    def fade(self, fade_in=True):
        fade_surface = pygame.Surface((self.width, self.height))
        fade_surface.fill((0, 0, 0))
        for alpha in range(0, 255, 5):
            fade_surface.set_alpha(alpha if fade_in else 255 - alpha)
            self.render()
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()

    def change_display(self, new_display):
        self.fade(fade_in=True)

        # Stop music when leaving menu screens
        music_screens = ['main_menu', 'options_display']
        if self.current_display == self.displays['main_menu'] or self.current_display == self.displays[
            'options_display']:
            if new_display not in music_screens:
                self.sound_manager.stop_music(fade_ms=500)

        # Start music when entering menu screens
        if new_display in music_screens:
            if not pygame.mixer.music.get_busy():
                self.sound_manager.play_music("background")

        self.current_display = self.displays[new_display]
        self.fade(fade_in=False)

    def mainloop(self):
        while self.run:
            self.current_display.mainloop()
            self.events()
            self.render()
            self.update()
            self.clock.tick(self.fps)




    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSLASH and self.enable_debug:
                self.debug = not self.debug
                for di in self.debug_items:
                    di.hidden = not di.hidden
            else:
                self.current_display.events(event)

    def render(self):
        self.screen.fill('black')
        self.current_display.render()

        for object in self.objects:
            object.render()



    def update(self):
        self.delta_time = self.clock.get_time()/ 1000.0

        if self.debug:

            self.debug_items[3].update_text(f'FPS: {self.clock.get_fps()}')
            self.debug_items[4].update_text(f'Objects in memory: {self.current_display.objects_in_memory}')
            self.debug_items[5].update_text(f'Current display: {type(self.current_display)}')


        pygame.display.flip()

