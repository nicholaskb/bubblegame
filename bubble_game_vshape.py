import pygame
import random
import sys
import string

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Letter Bubble Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Game settings
FPS = 60
TOTAL_TIME_MS = 30000     # 30 seconds
SHAPE_LIFESPAN = 5000     # shapes vanish after 5s
SPAWN_INTERVAL = 1000     # new shape every second
DOUBLE_CLICK_THRESHOLD = 300  # 300 ms
RADIUS_MIN, RADIUS_MAX = 30, 100
SHAPE_FALL_SPEED = 3      # how fast shapes fall per frame

WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
PURPLE =(100,   0, 100)

SHAPES = ["circle", "square", "triangle", "diamond"]
COLORS = [RED, GREEN, BLUE, PURPLE]

def spawn_shape():
    """Create a random shape with a random letter."""
    shape_type = random.choice(SHAPES)
    color = random.choice(COLORS)
    radius = random.randint(RADIUS_MIN, RADIUS_MAX)
    x = random.randint(radius, WIDTH - radius)
    y = 0 - radius  # start above the top so it falls down

    # Assign a random uppercase letter
    letter = random.choice(string.ascii_uppercase)

    return {
        "shape": shape_type,
        "color": color,
        "x": x,
        "y": y,
        "radius": radius,
        "spawn_time": pygame.time.get_ticks(),
        "letter": letter
    }

def draw_shape(shape):
    """Draw circle, square, or triangle and letter."""
    stype = shape["shape"]
    color = shape["color"]
    x = shape["x"]
    y = shape["y"]
    r = shape["radius"]

    # Draw shape
    if stype == "circle":
        pygame.draw.circle(screen, color, (x, y), r)
    elif stype == "square":
        pygame.draw.rect(screen, color, (x - r, y - r, 2*r, 2*r))
    elif stype == "triangle":
        pt1 = (x, y - r)
        pt2 = (x - r, y + r)
        pt3 = (x + r, y + r)
        pygame.draw.polygon(screen, color, [pt1, pt2, pt3])
    elif stype == "diamond":
        pt1 = (x, y - r)
        pt2 = (x - r, y)
        pt3 = (x, y + r)
        pt4 = (x + r, y)
        pygame.draw.polygon(screen, color, [pt1, pt2, pt3, pt4])

    # Draw letter (in contrast color, e.g., white)
    text_surf = font.render(shape["letter"], True, WHITE)
    text_rect = text_surf.get_rect(center=(x, y))
    screen.blit(text_surf, text_rect)

def play_game():
    """Play one round. Returns final score."""
    shapes = []
    last_spawn_time = 0
    score = 0

    # For double-click logic
    last_click_time = 0
    last_click_pos = (None, None)

    start_time = pygame.time.get_ticks()
    running = True

    while running:
        dt = clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        # Timer
        elapsed_ms = current_time - start_time
        time_left_ms = TOTAL_TIME_MS - elapsed_ms
        if time_left_ms <= 0:
            time_left_ms = 0
            running = False

        # Spawn shapes
        if current_time - last_spawn_time >= SPAWN_INTERVAL:
            shapes.append(spawn_shape())
            last_spawn_time = current_time

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Get the character of the key pressed
                char = event.unicode.upper()
                if char and char in string.ascii_uppercase:
                    # Find a shape with this letter
                    for s in shapes:
                        if s["letter"] == char:
                            shapes.remove(s)
                            score += 1
                            break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if user clicked on shape
                clicked_shapes = []
                for s in shapes:
                    stype = s["shape"]
                    sx, sy, r = s["x"], s["y"], s["radius"]
                    # circle collision
                    if stype == "circle":
                        dist_sq = (mouse_pos[0] - sx)**2 + (mouse_pos[1] - sy)**2
                        if dist_sq <= r**2:
                            clicked_shapes.append(s)
                    elif stype == "square":
                        if (sx - r <= mouse_pos[0] <= sx + r) and (sy - r <= mouse_pos[1] <= sy + r):
                            clicked_shapes.append(s)
                    elif stype == "triangle":
                        # bounding box approx
                        if (sx - r <= mouse_pos[0] <= sx + r) and (sy - r <= mouse_pos[1] <= sy + r):
                            clicked_shapes.append(s)
                    elif stype == "diamond":
                        # bounding box approx
                        if (sx - r <= mouse_pos[0] <= sx + r) and (sy - r <= mouse_pos[1] <= sy + r):
                            clicked_shapes.append(s)

                if clicked_shapes:
                    shape_clicked = clicked_shapes[0]
                    shapes.remove(shape_clicked)

                    if event.button == 1:  # left-click
                        dist_sq = 999999
                        time_since_last = current_time - last_click_time
                        if last_click_pos[0] is not None and last_click_pos[1] is not None:
                            dx = mouse_pos[0] - last_click_pos[0]
                            dy = mouse_pos[1] - last_click_pos[1]
                            dist_sq = dx*dx + dy*dy
                        # Check double-click
                        if time_since_last <= DOUBLE_CLICK_THRESHOLD and dist_sq < 100:
                            score += 3
                        else:
                            score += 1
                        last_click_time = current_time
                        last_click_pos = mouse_pos

                    elif event.button == 3:  # right-click
                        score += 2

        # Update shapes (falling down)
        for s in shapes:
            s["y"] += SHAPE_FALL_SPEED
        # Remove shapes that moved off bottom
        shapes = [s for s in shapes if s["y"] - s["radius"] < HEIGHT]

        # Remove expired shapes
        shapes = [s for s in shapes if (current_time - s["spawn_time"]) <= SHAPE_LIFESPAN]

        # Draw
        screen.fill(WHITE)

        for s in shapes:
            draw_shape(s)

        # Draw HUD
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        time_left_sec = time_left_ms // 1000
        elapsed_sec = elapsed_ms // 1000
        timer_txt = font.render(f"Time Left: {time_left_sec}s", True, (0, 0, 0))
        screen.blit(timer_txt, (10, 50))
        elapsed_txt = font.render(f"Elapsed: {elapsed_sec}s", True, (0, 0, 0))
        screen.blit(elapsed_txt, (10, 90))

        pygame.display.flip()

    return score

def game_over_screen(final_score):
    """Show final score, ask to replay or quit."""
    waiting = True
    while waiting:
        screen.fill(WHITE)

        txt_gameover = font.render("Time's up! Game Over.", True, (255, 0, 0))
        screen.blit(txt_gameover, (WIDTH//2 - 150, HEIGHT//2 - 60))

        txt_score = font.render(f"Congrats! Your final score: {final_score}", True, (0, 0, 0))
        screen.blit(txt_score, (WIDTH//2 - 180, HEIGHT//2 - 10))

        txt_replay = font.render("Press Y to play again or N to quit.", True, (0, 0, 0))
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

def main_loop():
    """Loop until user quits."""
    while True:
        final_score = play_game()
        replay = game_over_screen(final_score)
        if not replay:
            break

if __name__ == "__main__":
    main_loop()
    pygame.quit()
    sys.exit()
