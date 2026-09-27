import pygame
from constants import SCORE_INCREMENT


class Score:
    def __init__(self, screen: pygame.display):

        pygame.font.init()
        self.screen = screen
        self.score_font = pygame.font.Font(None, 36)
        self.score = 0
        self.score_text = self.score_font.render(
            f"Score: {self.score}", True, (255, 255, 255)
        )
        self.screen.blit(self.score_text, (10, 10))

    def increase_score(self):
        self.score += SCORE_INCREMENT

    def update_score(self):
        self.score_text = self.score_font.render(
            f"Score: {self.score}", True, (255, 255, 255)
        )
        self.screen.blit(self.score_text, (10, 10))
