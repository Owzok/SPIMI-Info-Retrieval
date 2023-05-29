import pygame
import time

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.font.init()
font = pygame.font.SysFont("Arial", 16)

query = ""
top_k = ""
results = []
query_time = 0
def draw_text(surface, text, x, y, opacity=255):
    text_surface = font.render(text, True, BLACK)
    text_surface.set_alpha(opacity)
    surface.blit(text_surface, (x, y))

def render_results():
    for i, result in enumerate(results):
        draw_text(window, result, 50, 100 + (i * 50))

def render_interface():
    window.fill(WHITE)
    pygame.draw.rect(window, BLACK, (50, 45, 600, 60), 2)
    pygame.draw.rect(window, BLACK, (50, 115, 100, 40), 2)
    render_results()
    
    # Render query input field with placeholder text
    if query == "":
        draw_text(window, "Enter SQL Query", 55, 50, opacity=100)
    else:
        draw_text(window, query, 155, 47)

    # Render top_k input field with placeholder text
    if top_k == "":
        draw_text(window, "Top K", 55, 120, opacity=100)
    else:
        draw_text(window, top_k, 155, 77)

    draw_text(window, "Results:", 55, 190)
    draw_text(window, "Time: {}s".format(query_time), 55, 300)
    pygame.display.flip()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Perform SQL query simulation
                start_time = time.time()
                # Simulate the SQL query and store the results
                query_time = round(time.time() - start_time, 2)
                results = ["Result 1", "Result 2", "Result 3"]  # Example results
                render_interface()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 150 <= event.pos[0] <= 350 and 45 <= event.pos[1] <= 70:
                pygame.event.set_allowed(pygame.KEYDOWN)
            elif 150 <= event.pos[0] <= 200 and 40 <= event.pos[1] <= 115:
                pygame.event.set_allowed(pygame.KEYDOWN)
            else:
                pygame.event.set_blocked(pygame.KEYDOWN)

    render_interface()

# Quit the game
pygame.quit()
