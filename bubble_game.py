import pygame
import random
import os
import sys
import string

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Falling Game")

clock = pygame.time.Clock()
FPS = 60

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
PURPLE = (100, 0, 100)
font = pygame.font.SysFont(None, 36)

TOTAL_TIME_MS = 30000
SPAWN_INTERVAL = 1000
POKEMON_FALL_SPEED = 3

# Load Pokémon images
base_dir = os.path.dirname(os.path.abspath(__file__))
POKEMON_DIR = os.path.join(base_dir, "pokemon_dataset", "images")
pokemon_images = []

for img_name in os.listdir(POKEMON_DIR):
    if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(POKEMON_DIR, img_name)
        try:
            img = pygame.image.load(img_path).convert_alpha()
            name = os.path.splitext(img_name)[0].lower()
            pokemon_images.append((img, name))
        except:
            continue

class Pokemon:
    def __init__(self, image, name):
        self.image = image
        self.name = name
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH-50), -50))
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.y += POKEMON_FALL_SPEED

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def play_game():
    pokemons = []
    last_spawn_time = 0
    score = 0
    start_time = pygame.time.get_ticks()
    running = True

    while running:
        dt = clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        elapsed_ms = current_time - start_time
        time_left_ms = TOTAL_TIME_MS - elapsed_ms

        if time_left_ms <= 0:
            break

        if current_time - last_spawn_time >= SPAWN_INTERVAL and pokemon_images:
            img, name = random.choice(pokemon_images)
            pokemons.append(Pokemon(img, name))
            last_spawn_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked = None
                for p in pokemons:
                    if p.rect.collidepoint(mouse_pos):
                        clicked = p
                        break
                if clicked:
                    pokemons.remove(clicked)
                    score += 1

        for p in pokemons:
            p.update()
        pokemons = [p for p in pokemons if p.rect.top < HEIGHT]

        screen.fill(WHITE)
        for p in pokemons:
            p.draw(screen)

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        time_left_sec = time_left_ms // 1000
        timer_text = font.render(f"Time Left: {time_left_sec}s", True, BLACK)
        screen.blit(timer_text, (10, 50))

        pygame.display.flip()

    return score

def game_over_screen(final_score):
    while True:
        screen.fill(WHITE)
        txt_gameover = font.render("Time's up! Game Over.", True, RED)
        screen.blit(txt_gameover, (WIDTH//2 - 150, HEIGHT//2 - 60))

        txt_score = font.render(f"Your final score: {final_score}", True, BLACK)
        screen.blit(txt_score, (WIDTH//2 - 180, HEIGHT//2 - 10))

        txt_replay = font.render("Press Y to play again or N to quit.", True, BLACK)
        screen.blit(txt_replay, (WIDTH//2 - 220, HEIGHT//2 + 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                    return False

        clock.tick(30)

def main():
    while True:
        score = play_game()
        if not game_over_screen(score):
            break

    pygame.quit()
    sys.exit()

main()
