import sys

import pygame
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import (
    BUTTON_LEFT,
    BUTTON_TOP,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from logger import log_event, log_state
from player import Player
from score import Score
from shot import Shot

print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")

def game(screen):

    clock = pygame.time.Clock()
    dt = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (updatable, drawable, asteroids)
    Player.containers = (updatable, drawable)
    Shot.containers = (updatable, drawable, shots)
    AsteroidField.containers = updatable

    AsteroidField()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Scoring
    score = Score(screen)

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                print("Your Score was:", score.score)
                high_score = score.get_score()
                start_menu(screen, high_score)

            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    score.increase_score()

        for drawables in drawable:
            drawables.draw(screen)

        score.update_score()

        pygame.display.flip()
        dt = clock.tick(60) / 1000


def start_menu(screen, high_score: int = 0):
    pygame.font.init()
    menu_font = pygame.font.Font(None, 50)
    while True:
        screen.fill("black")
        mouse = pygame.mouse.get_pos()

        play_button = pygame.Rect(
            BUTTON_LEFT,
            BUTTON_TOP,
            140,
            50,
        )

        quit_button = pygame.Rect(
            BUTTON_LEFT,
            BUTTON_TOP + 50,
            140,
            50,
        )


        pygame.draw.rect(
            screen, "Grey" if play_button.collidepoint(mouse) else "Black", play_button
        )
        pygame.draw.rect(
            screen, "Grey" if quit_button.collidepoint(mouse) else "Black", quit_button
        )

        play_text = menu_font.render("Play", True, "White")
        quit_text = menu_font.render("Quit", True, "White")

        screen.blit(play_text, (BUTTON_LEFT + 30, BUTTON_TOP + 10))
        screen.blit(quit_text, (BUTTON_LEFT + 30, BUTTON_TOP + 60))


        # HIGH SCORE
        if high_score != 0:
            high_score_text = menu_font.render(f"Score: {high_score}", True, "White")
            screen.blit(high_score_text, (BUTTON_LEFT-20, BUTTON_TOP- 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mouse):
                    game(screen)
                if quit_button.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    start_menu(screen)


if __name__ == "__main__":
    main()
