import pygame

class Player:
    def __init__(self, game):
        self.game = game
        self.width = 10
        self.height = 10
        self.x = 0
        self.y = 0

    def render(self):
        pygame.draw.rect(self.game.screen, (255,255,255), (self.x, self.y, self.width, self.height))

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.x, self.y = pygame.mouse.get_pos()


