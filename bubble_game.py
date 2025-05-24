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

if os.path.isdir(POKEMON_DIR):
    for img_name in os.listdir(POKEMON_DIR):
        if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(POKEMON_DIR, img_name)
            try:
                img = pygame.image.load(img_path).convert_alpha()
                name = os.path.splitext(img_name)[0].lower()
                pokemon_images.append((img, name))
            except Exception:
                continue
else:
    print(f"Warning: '{POKEMON_DIR}' not found. No Pokémon images loaded.")

class Pokemon:
    def __init__(self, image, name, letter=None):
        self.image = image
        self.name = name
        self.letter = letter
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH-50), -50))
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.y += POKEMON_FALL_SPEED

    def draw(self, surface, show_letter=False):
        surface.blit(self.image, self.rect)
        if show_letter and self.letter:
            txt = font.render(self.letter.upper(), True, BLACK)
            rect = txt.get_rect(center=self.rect.center)
            surface.blit(txt, rect)

def select_difficulty():
    """Display difficulty options and return chosen level (1-4)."""
    while True:
        screen.fill(WHITE)
        prompt = font.render("Select Difficulty (1-4)", True, BLACK)
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode in ("1", "2", "3", "4"):
                    return int(event.unicode)

        clock.tick(30)

def play_game(difficulty):
    pokemons = []
    last_spawn_time = 0
    score = 0
    start_time = pygame.time.get_ticks()
    running = True
    typed_input = ""

    while running:
        dt = clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        elapsed_ms = current_time - start_time
        time_left_ms = TOTAL_TIME_MS - elapsed_ms

        if time_left_ms <= 0:
            break

        if current_time - last_spawn_time >= SPAWN_INTERVAL and pokemon_images:
            img, name = random.choice(pokemon_images)
            letter = random.choice(string.ascii_lowercase) if difficulty == 2 else None
            pokemons.append(Pokemon(img, name, letter))
            last_spawn_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                char = event.unicode.lower()
                if difficulty == 2 and char in string.ascii_lowercase:
                    caught = [p for p in pokemons if p.letter == char]
                    for c in caught:
                        pokemons.remove(c)
                        score += 1
                elif difficulty == 3 and char in string.ascii_lowercase:
                    caught = [p for p in pokemons if p.name.startswith(char)]
                    for c in caught:
                        pokemons.remove(c)
                        score += 1
                elif difficulty == 4:
                    if event.key == pygame.K_BACKSPACE:
                        typed_input = typed_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        typed_input = ""
                    elif char and char in string.ascii_lowercase:
                        typed_input += char
                    for p in pokemons[:]:
                        if typed_input == p.name:
                            pokemons.remove(p)
                            score += 1
                            typed_input = ""
                            break
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
            p.draw(screen, show_letter=(difficulty == 2))

        if difficulty == 4:
            typed_text = font.render(typed_input, True, BLACK)
            screen.blit(typed_text, (10, 90))

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
        difficulty = select_difficulty()
        score = play_game(difficulty)
        if not game_over_screen(score):
            break

    pygame.quit()
    sys.exit()

main()
