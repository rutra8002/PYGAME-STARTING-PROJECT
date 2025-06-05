from customObjects import custom_images, custom_text, custom_button
from particlesystem import particle_system, particle_generator
import random
import pygame
import configparser
from app import config as confige
from app import player

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
        self.player = player.Player(self)


    def mainloop(self):
        pass

    def render(self):
        basic_display.render(self)
        self.player.render()

    def events(self, event):
        basic_display.events(self, event)
        self.player.events(event)


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

        # Create buttons
        button_width = 200
        button_height = 60
        button_y_start = game.height / 2
        button_spacing = 80

        # Play button
        self.play_button = custom_button.Button(
            self,
            self.play_game,
            game.width / 2 - button_width / 2,
            button_y_start,
            button_width,
            button_height,
            color=(100, 200, 100),
            text="Play",
            text_color="white"
        )

        # Options button
        self.options_button = custom_button.Button(
            self,
            self.open_options,
            game.width / 2 - button_width / 2,
            button_y_start + button_spacing,
            button_width,
            button_height,
            color=(100, 100, 200),
            text="Options",
            text_color="white"
        )

        # Exit button
        self.exit_button = custom_button.Button(
            self,
            self.exit_game,
            game.width / 2 - button_width / 2,
            button_y_start + button_spacing * 2,
            button_width,
            button_height,
            color=(200, 100, 100),
            text="Exit",
            text_color="white"
        )

    def play_game(self):
        self.game.change_display('game_display')

    def open_options(self):
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

        self.game = game
        self.title = custom_text.Custom_text(
            self,
            game.width / 2,
            game.height / 10,
            "Options",
            text_color='white',
            font_height=60
        )

        # Get available resolutions
        self.resolution_options = pygame.display.list_modes()

        # Add current resolution if not in list
        current_res = (self.game.width, self.game.height)
        if current_res not in self.resolution_options:
            self.resolution_options.append(current_res)

        # Sort resolutions by size
        self.resolution_options.reverse()

        # Find index of current resolution
        self.current_res_index = self.resolution_options.index(current_res)

        # Available FPS options
        self.fps_options = [30, 60, 90, 120, 144, 240]
        self.current_fps = self.game.fps

        # Find closest FPS option to current setting
        self.current_fps_index = self.fps_options.index(self.current_fps)

        # Create UI elements
        button_width = 200
        button_height = 50

        # Resolution section
        self.resolution_text = custom_text.Custom_text(
            self,
            game.width / 2,
            game.height / 3,
            f"Resolution: {self.resolution_options[self.current_res_index][0]}x{self.resolution_options[self.current_res_index][1]}",
            text_color='white',
            font_height=30
        )

        self.res_left_button = custom_button.Button(
            self,
            self.prev_resolution,
            game.width / 2 - button_width - 20,
            game.height / 3 - button_height/2,
            50,
            button_height,
            color=(80, 80, 180),
            text="<",
            text_color="white"
        )

        self.res_right_button = custom_button.Button(
            self,
            self.next_resolution,
            game.width / 2 + button_width - 30,
            game.height / 3 - button_height/2,
            50,
            button_height,
            color=(80, 80, 180),
            text=">",
            text_color="white"
        )

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
            color=(80, 80, 180),
            text="<",
            text_color="white"
        )

        self.fps_right_button = custom_button.Button(
            self,
            self.next_fps,
            game.width / 2 + button_width - 30,
            game.height / 2 - button_height/2,
            50,
            button_height,
            color=(80, 80, 180),
            text=">",
            text_color="white"
        )

        # Apply button
        self.apply_button = custom_button.Button(
            self,
            self.apply_settings,
            game.width / 2 - button_width / 2,
            game.height * 3 / 4,
            button_width,
            button_height,
            color=(100, 200, 100),
            text="Apply",
            text_color="white"
        )

        # Back button
        self.back_button = custom_button.Button(
            self,
            self.go_back,
            game.width / 2 - button_width / 2,
            game.height * 3 / 4 + 70,
            button_width,
            button_height,
            color=(200, 100, 100),
            text="Back",
            text_color="white"
        )


    def prev_resolution(self):
        self.current_res_index = (self.current_res_index - 1) % len(self.resolution_options)
        self.update_resolution_text()

    def next_resolution(self):
        self.current_res_index = (self.current_res_index + 1) % len(self.resolution_options)
        self.update_resolution_text()

    def update_resolution_text(self):
        res = self.resolution_options[self.current_res_index]
        self.resolution_text.update_text(f"Resolution: {res[0]}x{res[1]}")

    def prev_fps(self):
        self.current_fps_index = (self.current_fps_index - 1) % len(self.fps_options)
        self.update_fps_text()

    def next_fps(self):
        self.current_fps_index = (self.current_fps_index + 1) % len(self.fps_options)
        self.update_fps_text()

    def update_fps_text(self):
        self.fps_text.update_text(f"FPS: {self.fps_options[self.current_fps_index]}")

    def apply_settings(self):
        # Get selected resolution and FPS
        new_width, new_height = self.resolution_options[self.current_res_index]
        new_fps = self.fps_options[self.current_fps_index]

        # Update config file
        config = configparser.ConfigParser()
        config_file = 'config.ini'
        config.read(config_file)

        config['CONFIG']['width'] = str(new_width)
        config['CONFIG']['height'] = str(new_height)
        config['CONFIG']['fps'] = str(new_fps)

        self.game.width = new_width
        self.game.height = new_height
        self.game.fps = new_fps

        self.game.screen = pygame.display.set_mode((self.game.width, self.game.height))
        self.game.debug_items[2].update_text(f'FPS cap: {self.game.fps}')

        confige.read_config()

        with open(config_file, 'w') as f:
            config.write(f)

        for display in self.game.displays.values():
            display.__init__(self.game)


    def go_back(self):
        self.game.change_display('main_menu')

    def mainloop(self):
        pass