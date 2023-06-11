import pygame
from spimi import SPIMI
from utils import read_txt_files, count_terms
import time

documents = read_txt_files("../documents/")
spimi = SPIMI()

class GUI:
    def __init__(self):
        pygame.init()

        self.BLACK = (22,22,23)
        self.WHITE = (255, 255, 255)
        self.BLUE = (63,133,255)

        self.BG_COLOR = (165,171,181)
        self.WHITE_BG = (241,241,241)
        self.GRAY = (220,220,220)

        self.WINDOW_WIDTH = 1500
        self.WINDOW_HEIGHT = 720

        self.roboto_path = "../others/Lato-Regular.ttf"

        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("SQL Query Simulator")

        pygame.font.init()
        self.font = pygame.font.Font(self.roboto_path, 16)

        self.query = ""
        self.top_k = ""
        self.our_results = []
        self.pg_results = []
        self.our_query_time = 0
        self.pg_query_time = 0
        self.active_field = None

        self.b_result = ""

        self.button_clicked = False
        self.backspace_held = False

        self.n_terms = 0

        self.q_rect = pygame.Rect(35, 140, 640, 60)
        self.k_rect = pygame.Rect(530, 45, 70, 35)
        self.BUTTON_RECT = pygame.Rect(610, 45, 60, 35)

        self.our_results_rect_head = pygame.Rect(35, 215, 640, 100)
        self.our_results_rect = pygame.Rect(35, 315, 640, 330)

        self.pg_results_rect_head =  pygame.Rect(640+35+35, 215, 640, 100)
        self.pg_results_rect = pygame.Rect(640+35+35, 315, 640, 330)

    def draw_text(self, text, x, y, color, font_size=20, box_width=720, box_height=720, opacity=255, bold=False):
        font = pygame.font.Font(self.roboto_path, font_size)
        if bold:
            font.set_bold(True)

        text_lines = []

        # Split the text into multiple lines based on the available width
        words = text.split()
        current_line = ""
        for word in words:
            if font.size(current_line + " " + word)[0] <= box_width:
                current_line += " " + word
            else:
                text_lines.append(current_line.strip())
                current_line = word
        text_lines.append(current_line.strip())

        line_spacing = font.get_linesize()
        total_height = len(text_lines) * line_spacing

        # Check if the text fits within the box height
        if total_height > box_height:
            # Reduce font size to fit the text within the box
            scale_factor = box_height / total_height
            font_size = int(font_size * scale_factor)
            font = pygame.font.Font(None, font_size)
            line_spacing = font.get_linesize()

        # Render and draw each line of text
        for i, line in enumerate(text_lines):
            text_surface = font.render(line, True, color)
            text_surface.set_alpha(opacity)
            self.window.blit(text_surface, (x, y + i * line_spacing))

    def render_results(self):
        for i, result in enumerate(self.our_results):
            self.draw_text(str(result[0]), self.our_results_rect.x + 40, self.our_results_rect.y + 10 + (i * 25), self.BLACK, font_size=14)
            self.draw_text(str(result[1]), self.our_results_rect.x + 150, self.our_results_rect.y + 10 + (i * 25), self.BLACK, font_size=14)

    def perform_search(self):
        # Perform SQL query simulation
        self.our_query_time = 0
        start_time = time.time()
        # Simulate the SQL query and store the results
        self.our_results = spimi.search_query(self.query, documents, self.top_k)
        ans = ""
        for doc_id, document in enumerate(documents):
            if len(self.our_results) > 0 and doc_id == self.our_results[0][0]: #check for existance of results
                self.b_result = document['text']
        # -- Temporally Disabled
        #self.n_terms = count_terms()
        self.our_query_time = round(time.time() - start_time, 5)
        self.render_interface()

    def button_click(self):
        self.button_clicked = True
        self.perform_search()

    def render_interface(self):
        # Background
        self.window.fill(self.BG_COLOR)
        # Main Panel
        curve_surface = pygame.Surface((1335, 650))
        curve_surface.fill(self.WHITE_BG)
        self.window.blit(curve_surface, (30, 35))

        # Top panel
        top_rect = pygame.Rect(30, 35, 650, 1335)
        pygame.draw.rect(self.window, self.WHITE, top_rect)
        self.draw_text("SPIMI Search Engine", top_rect.x + 20, top_rect.y + 17, self.BLACK)

        # Query bar
        query_bar_rect = pygame.Rect(30, 95, 650, 40)
        pygame.draw.rect(self.window, self.WHITE, query_bar_rect)
        pygame.draw.rect(self.window, self.GRAY, query_bar_rect, 1)

        self.draw_text("Query", query_bar_rect.x + 45, query_bar_rect.y + 12, self.BLUE, font_size=12)
        self.draw_text(">", query_bar_rect.x + 22, query_bar_rect.y + 5, self.BLUE, font_size=22)
        self.draw_text("-", query_bar_rect.x + 30, query_bar_rect.y + 9, self.BLUE, font_size=22)
        pygame.draw.rect(self.window, self.BLUE, pygame.Rect(50, 132, 70, 2), 2)

        # Query panel
        pygame.draw.rect(self.window, self.WHITE, self.q_rect)
        if self.active_field == 'query':
            pygame.draw.rect(self.window, self.BLUE, self.q_rect, 1)
        else:
            pygame.draw.rect(self.window, self.GRAY, self.q_rect, 1)

        if self.query == "":
            self.draw_text("Enter query", self.q_rect.x + 10, self.q_rect.y + 10, self.GRAY)
        else:
            self.draw_text(self.query, self.q_rect.x + 10, self.q_rect.y + 10, self.BLACK)

        # Top K panel
        pygame.draw.rect(self.window, self.WHITE, self.k_rect)
        if self.active_field == 'top_k':
            pygame.draw.rect(self.window, self.BLUE, self.k_rect, 1)
        else:
            pygame.draw.rect(self.window, self.GRAY, self.k_rect, 1)

        if self.top_k == "":
            self.draw_text("Top K", self.k_rect.x + 15, self.k_rect.y + 8, self.GRAY, font_size=14)
        else:
            self.draw_text(self.top_k, self.k_rect.x + 15, self.k_rect.y + 8, self.BLUE, font_size=14)

        # Run Button Panel
        pygame.draw.rect(self.window, self.BLUE, self.BUTTON_RECT)

        self.button_text = "Run"
        self.draw_text(self.button_text, self.BUTTON_RECT.x + 15, self.BUTTON_RECT.y + 8, self.WHITE, font_size=14)

        # Results panel
            # Head
        pygame.draw.rect(self.window, self.WHITE, self.our_results_rect_head)
        pygame.draw.rect(self.window, self.GRAY, self.our_results_rect_head, 1)

        pygame.draw.rect(self.window, self.WHITE, self.pg_results_rect_head)
        pygame.draw.rect(self.window, self.GRAY, self.pg_results_rect_head, 1)
            # Body
        pygame.draw.rect(self.window, self.WHITE, self.our_results_rect)
        pygame.draw.rect(self.window, self.GRAY, self.our_results_rect, 1)

        pygame.draw.rect(self.window, self.WHITE, self.pg_results_rect)
        pygame.draw.rect(self.window, self.GRAY, self.pg_results_rect, 1)

        self.draw_text("Results", self.our_results_rect_head.x + 20, self.our_results_rect_head.y + 20, self.BLACK, font_size=20)
        self.draw_text("doc_id", self.our_results_rect_head.x + 22, self.our_results_rect_head.y + 73, self.BLACK, font_size=15)
        self.draw_text("tf-idf", self.our_results_rect_head.x + 200, self.our_results_rect_head.y + 73, self.BLACK, font_size=15)

        self.draw_text("Postgres", self.pg_results_rect_head.x + 20,self.pg_results_rect_head.y + 20 , self.BLACK, font_size=20)
        # --
        self.render_results()
        '''
        if self.b_result == "":
            self.draw_text("Best result:", 55, 620, self.BLACK, opacity=80)
        else:
            self.draw_text(self.b_result, 55, 420, self.BLACK)'''

        self.draw_text(f"Time: {self.our_query_time}s", 55, 655, self.BLACK, font_size=15)
        # -- Temporally Disabled
        #self.draw_text(f"Records Scanned: {self.n_terms}", 255, 655, self.BLACK, font_size=15)

        pygame.display.flip()

    def handle_keyboard_event(self, event):
        if event.key == pygame.K_RETURN:
            self.perform_search()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_BACKSPACE]:
            # Set the flag to indicate backspace is being held down
            self.backspace_held = True
        else:
            # Clear the flag when backspace is released
            self.backspace_held = False

        # Outside the event loop, after handling events
        if self.backspace_held:
            if self.active_field == "query" and len(self.query) > 0:
                self.query = self.query[:-1]
            elif self.active_field == "top_k" and len(self.top_k) > 0:
                self.top_k = self.top_k[:-1]
            self.render_interface()
        else:  # erase characters
            if self.active_field == "query":
                self.query += event.unicode
            elif self.active_field == "top_k":
                self.top_k += event.unicode
            self.render_interface()

    def handle_mouse_event(self, event):
        if self.q_rect.collidepoint(event.pos):
            pygame.event.set_allowed(pygame.KEYDOWN)
            self.active_field = "query"
        elif self.k_rect.collidepoint(event.pos):
            pygame.event.set_allowed(pygame.KEYDOWN)
            self.active_field = "top_k"
        elif self.BUTTON_RECT.collidepoint(event.pos):
            self.button_click()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.button_clicked = False
        else:
            pygame.event.set_blocked(pygame.KEYDOWN)
            self.active_field = None

    def run(self):
        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keyboard_event(event)
                    if event.key == pygame.K_BACKSPACE:
                        self.backspace_held = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        self.backspace_held = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_event(event)
            if self.backspace_held:
                if self.active_field == "query":
                    self.query = self.query[:-1]
                elif self.active_field == "top_k":
                    self.top_k = self.top_k[:-1]
                self.render_interface()
                
            self.render_interface()

        pygame.quit()