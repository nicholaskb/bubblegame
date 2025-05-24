import pygame
import random
import os

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Falling Game")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)

# Load Pokémon images
base_dir = os.path.dirname(os.path.abspath(__file__))
POKEMON_DIR = os.path.join(base_dir, "pokemon_dataset", "images")
pokemon_images = []

for img_name in os.listdir(POKEMON_DIR):
    if img_name.lower().endswith(".png"):
        img_path = os.path.join(POKEMON_DIR, img_name)
        img = pygame.image.load(img_path).convert_alpha()
        pokemon_images.append(img)

class Pokemon:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH-50), -50))

    def update(self):
        self.rect.y += 2

    def draw(self, screen):
        screen.blit(self.image, self.rect)

pokemons = []
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1500)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_EVENT:
            pokemons.append(Pokemon(random.choice(pokemon_images)))

    screen.fill(WHITE)

    for pkmn in pokemons[:]:
        pkmn.update()
        pkmn.draw(screen)
        if pkmn.rect.top > HEIGHT:
            pokemons.remove(pkmn)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
