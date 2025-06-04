from customObjects import custom_images, custom_text, custom_button


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

    def mainloop(self):
        self.loading_error.hidden = True

