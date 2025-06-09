from customObjects import custom_images, custom_text, custom_button
from particlesystem import particle_system, particle_generator
import random
import pygame
import configparser
from app import config as confige
from app import player
import math

class basic_display:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.objects = []
        self.objects_in_memory = 0


        self.loading_error = custom_text.Custom_text(self, self.game.width/2, self.game.height/2, 'Error, no display found!', text_color='white')
        self.loading_error.hidden = True


    def render(self):
        for obj in self.objects:
            obj.render()

    def events(self, event):
        for obj in self.objects:
            obj.events(event)

    def mainloop(self):
        self.loading_error.hidden = False


class game_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        self.player = player.Player(self.game)

        self.player_text = custom_text.Custom_text(self, self.game.width/2, self.game.height/2, f"{int(self.player.vx)}, {int(self.player.vy)}", text_color='white')


    def mainloop(self):
        self.player.update()
        self.player_text.update_text(f"{int(self.player.vx)}, {int(self.player.vy)}")

    def render(self):
        basic_display.render(self)
        self.player.render()

    def events(self, event):
        basic_display.events(self, event)
        self.player.events(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_display('pause_menu')


class main_menu_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)

        self.particle_system = particle_system.ParticleSystem()

        self.particle_gen = particle_generator.ParticleGenerator(
            self.particle_system,
            game.width / 2, game.height / 2,
            0, -1, 0.5, 0.5, 0, 0, 20, 300, 2, 200, 200, 200, 150, "circle", False, 60)
        self.particle_system.add_generator(self.particle_gen)
        self.particle_gen.start()

        # Create title
        self.title = custom_text.Custom_text(
            self,
            game.width / 2,
            game.height / 4,
            game.title,
            text_color='white',
            font_height=80
        )


        # Create styled buttons with hover effects
        button_width = 220
        button_height = 70
        button_y_start = game.height / 2
        button_spacing = 100

        # Play button
        self.play_button = custom_button.Button(
            self,
            self.play_game,
            game.width / 2 - button_width / 2,
            button_y_start,
            button_width,
            button_height,
            color=(40, 120, 40),
            text="PLAY",
            text_color="white",
            outline_color=(100, 255, 100),
            outline_width=3
        )

        # Options button
        self.options_button = custom_button.Button(
            self,
            self.open_options,
            game.width / 2 - button_width / 2,
            button_y_start + button_spacing,
            button_width,
            button_height,
            color=(40, 40, 120),
            text="OPTIONS",
            text_color="white",
            outline_color=(100, 100, 255),
            outline_width=3
        )

        # Exit button
        self.exit_button = custom_button.Button(
            self,
            self.exit_game,
            game.width / 2 - button_width / 2,
            button_y_start + button_spacing * 2,
            button_width,
            button_height,
            color=(120, 40, 40),
            text="EXIT",
            text_color="white",
            outline_color=(255, 100, 100),
            outline_width=3
        )

        # Version text at bottom
        self.version_text = custom_text.Custom_text(
            self,
            game.width - 50,
            game.height - 20,
            f"v{game.version}",
            text_color=(150, 150, 150),
            font_height=20,
            center=False
        )

    def play_game(self):
        self.game.change_display('game_display')

    def open_options(self):
        self.game.displays['options_display'].from_pause = False
        self.game.change_display('options_display')

    def exit_game(self):
        self.game.run = False

    def render(self):
        self.particle_system.draw(self.screen)
        for obj in self.objects:
            obj.render()



    def mainloop(self):
        self.particle_gen.edit(x=random.randint(0, self.game.width), y=random.randint(0, self.game.height), dvx=(random.uniform(-0.1, 0.1)), dvy=(random.uniform(-0.1, 0.1)), vx=random.uniform(-1, 1), vy=random.uniform(-1, 1), red=random.randint(0, 255), green=random.randint(0, 255), blue=random.randint(0, 255))
        self.particle_system.update(self.game.delta_time)


class options_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        self.from_pause = False
        self.game = game
        self.title = custom_text.Custom_text(
            self,
            game.width / 2,
            game.height / 10,
            "Options",
            text_color='white',
            font_height=60
        )


        # Available FPS options
        self.fps_options = [30, 60, 90, 120, 144, 240]
        self.current_fps = self.game.fps

        # Find closest FPS option to current setting
        self.current_fps_index = self.fps_options.index(self.current_fps)

        # Create UI elements
        button_width = 200
        button_height = 50

        # FPS section
        self.fps_text = custom_text.Custom_text(
            self,
            game.width / 2,
            game.height / 2,
            f"FPS: {self.fps_options[self.current_fps_index]}",
            text_color='white',
            font_height=30
        )

        self.fps_left_button = custom_button.Button(
            self,
            self.prev_fps,
            game.width / 2 - button_width - 20,
            game.height / 2 - button_height/2,
            50,
            button_height,
            color=(40, 40, 120),
            text="<",
            text_color="white",
            outline_color=(100, 100, 255),
            outline_width=3
        )

        self.fps_right_button = custom_button.Button(
            self,
            self.next_fps,
            game.width / 2 + button_width - 30,
            game.height / 2 - button_height/2,
            50,
            button_height,
            color=(40, 40, 120),
            text=">",
            text_color="white",
            outline_color=(100, 100, 255),
            outline_width=3
        )

        # Apply button
        self.apply_button = custom_button.Button(
            self,
            self.apply_settings,
            game.width / 2 - button_width / 2,
            game.height * 3 / 4,
            button_width,
            button_height,
            color=(40, 120, 40),
            text="APPLY",
            text_color="white",
            outline_color=(100, 255, 100),
            outline_width=3
        )

        # Back button
        self.back_button = custom_button.Button(
            self,
            self.go_back,
            game.width / 2 - button_width / 2,
            game.height * 3 / 4 + 70,
            button_width,
            button_height,
            color=(120, 40, 40),
            text="BACK",
            text_color="white",
            outline_color=(255, 100, 100),
            outline_width=3
        )



    def prev_fps(self):
        self.current_fps_index = (self.current_fps_index - 1) % len(self.fps_options)
        self.update_fps_text()

    def next_fps(self):
        self.current_fps_index = (self.current_fps_index + 1) % len(self.fps_options)
        self.update_fps_text()

    def update_fps_text(self):
        self.fps_text.update_text(f"FPS: {self.fps_options[self.current_fps_index]}")

    def apply_settings(self):

        new_fps = self.fps_options[self.current_fps_index]

        # Update config file
        config = configparser.ConfigParser()
        config_file = 'config.ini'
        config.read(config_file)


        config['CONFIG']['fps'] = str(new_fps)


        self.game.fps = new_fps
        self.game.debug_items[2].update_text(f'FPS cap: {self.game.fps}')

        confige.read_config()

        with open(config_file, 'w') as f:
            config.write(f)


    def go_back(self):
        if self.from_pause:
            self.game.change_display('pause_menu')
        else:
            self.game.change_display('main_menu')

    def mainloop(self):
        pass


class pause_menu_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)

        # Create semi-transparent overlay
        self.overlay = pygame.Surface((game.width, game.height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))  # Black with 50% opacity

        # Create title
        self.title = custom_text.Custom_text(
            self,
            game.width / 2,
            game.height / 4,
            "Paused",
            text_color='white',
            font_height=60
        )

        # Create buttons
        button_width = 200
        button_height = 60
        button_y_start = game.height / 2
        button_spacing = 80

        # Resume button
        self.resume_button = custom_button.Button(
            self,
            self.resume_game,
            game.width / 2 - button_width / 2,
            button_y_start,
            button_width,
            button_height,
            color=(40, 120, 40),
            text="RESUME",
            text_color="white",
            outline_color=(100, 255, 100),
            outline_width=3
        )

        # Options button
        self.options_button = custom_button.Button(
            self,
            self.open_options,
            game.width / 2 - button_width / 2,
            button_y_start + button_spacing,
            button_width,
            button_height,
            color=(40, 40, 120),
            text="OPTIONS",
            text_color="white",
            outline_color=(100, 100, 255),
            outline_width=3
        )

        # Main menu button
        self.main_menu_button = custom_button.Button(
            self,
            self.go_to_main_menu,
            game.width / 2 - button_width / 2,
            button_y_start + button_spacing * 2,
            button_width,
            button_height,
            color=(120, 40, 40),
            text="MAIN MENU",
            text_color="white",
            outline_color=(255, 100, 100),
            outline_width=3
        )

    def render(self):
        self.game.displays['game_display'].render()

        self.game.screen.blit(self.overlay, (0, 0))

        for obj in self.objects:
            obj.render()

    def resume_game(self):
        self.game.change_display('game_display')

    def open_options(self):
        self.game.displays['options_display'].from_pause = True
        self.game.change_display('options_display')

    def go_to_main_menu(self):
        self.game.change_display('main_menu')

    def mainloop(self):
        pass