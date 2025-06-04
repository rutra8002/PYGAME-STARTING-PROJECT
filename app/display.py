from customObjects import custom_images, custom_text, custom_button
from particlesystem import particle_system, particle_generator
import random

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


class main_menu_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)

        self.particle_system = particle_system.ParticleSystem()

        self.particle_gen = particle_system.ParticleGenerator(
            self.particle_system,
            game.width / 2, game.height / 2,
            0, -1, 0.5, 0.5, 0, 0, 70, 100, 5, 200, 200, 200, 200, "circle", False, 60)
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
        print("Options menu (not implemented)")

    def exit_game(self):
        self.game.run = False

    def render(self):
        self.particle_system.draw(self.screen)
        for obj in self.objects:
            obj.render()



    def mainloop(self):
        self.particle_gen.edit(x=random.randint(0, self.game.width), y=random.randint(0, self.game.height), dvx=(random.uniform(-0.1, 0.1)), dvy=(random.uniform(-0.1, 0.1)), vx=random.uniform(-1, 1), vy=random.uniform(-1, 1), red=random.randint(0, 255), green=random.randint(0, 255), blue=random.randint(0, 255))
        self.particle_system.update(self.game.delta_time)

