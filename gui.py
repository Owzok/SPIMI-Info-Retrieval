import pygame
import time
from spimi import *
documents = read_txt_files("./documents/")
spimi = SPIMI()

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("SQL Query Simulator")

pygame.font.init()
font = pygame.font.SysFont("Arial", 16)

query = ""
top_k = ""
results = []
query_time = 0
active_field = None

button_rect = pygame.Rect(160, 115, 100, 40)
button_text = "Search"
button_clicked = False

def draw_text(surface, text, x, y, opacity=255):
    text_surface = font.render(text, True, BLACK)
    text_surface.set_alpha(opacity)
    surface.blit(text_surface, (x, y))

def render_results():
    for i, result in enumerate(results):
        draw_text(window, f"{str(result[0])}\t\t{result[1]}", 60, 210 + (i * 20))

'''
def button_click():
    global button_clicked
    button_clicked = True
    results = spimi.search_query(query, documents)
    render_results()
'''

b_result = ""

def render_interface():
    window.fill(WHITE)
    pygame.draw.rect(window, BLACK, (50, 45, 600, 60), 2)
    pygame.draw.rect(window, BLACK, (50, 115, 100, 40), 2)
    render_results()

    pygame.draw.rect(window, GRAY, button_rect)
    draw_text(window, button_text, button_rect.x + 15, button_rect.y + 10)

    if query == "":
        draw_text(window, "Enter SQL Query", 55, 50, opacity=100)
    else:
        draw_text(window, query, 55, 47)

    if b_result == "":
        draw_text(window, "Best result:", 55, 420, opacity=80)
    else:
        draw_text(window, b_result, 55, 420)

    if top_k == "":
        draw_text(window, "Top K", 55, 120, opacity=100)
    else:
        draw_text(window, top_k, 55, 120)
    draw_text(window, "Results:", 55, 190)
    draw_text(window, f"Time: {query_time}s", 55, 400)
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
                query_time = 0
                start_time = time.time()
                # Simulate the SQL query and store the results
                results = spimi.search_query(query, documents, top_k)
                ans = ""
                for doc_id, document in enumerate(documents):
                    if doc_id == results[0][0]:
                        b_result = document['text']
                query_time = round(time.time() - start_time, 5)
                render_interface()

            elif event.key == pygame.K_BACKSPACE:
                if active_field == "query":
                    query = query[:-1]
                elif active_field == "top_k":
                    top_k = top_k[:-1]
                render_interface()
                
            else:
                if active_field == "query":
                    query += event.unicode
                elif active_field == "top_k":
                    top_k += event.unicode
                render_interface()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 50 <= event.pos[0] <= 600 and 45 <= event.pos[1] <= 105:
                pygame.event.set_allowed(pygame.KEYDOWN)
                active_field = "query"
            elif 50 <= event.pos[0] <= 100 and 120 <= event.pos[1] <= 150:
                pygame.event.set_allowed(pygame.KEYDOWN)
                active_field = "top_k"
            elif button_rect.collidepoint(event.pos):
                pass
                #button_click()
            elif event.type == pygame.MOUSEBUTTONUP:
                button_clicked = False
            else:
                pygame.event.set_blocked(pygame.KEYDOWN)
                active_field = None

        render_interface()

pygame.quit()