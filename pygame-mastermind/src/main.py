"""
This is going to be a gameboy-like Mastermind.
"""

# --- Imports ---
import os, random, sys                          # Standard imports
from enum import Enum

import pygame                                   # 3rd Party imports
import color_codes as cc

# --- Globals --
pygame.init()

WIDTH = 160                                     # Gameboy dimensions
HEIGHT = 144
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Init screen
pygame.display.set_caption("Mastermind")        # Set caption

# Icon loader
icon_path = "..\\assets\\icon.png"
if os.path.exists(icon_path):
    icon = pygame.image.load(icon_path, "img")
    pygame.display.set_icon(icon)
else:
    print("Icon Load failed. Check you are in the right working directory.")

# Colours
BG = cc.BLACK.rgb
FG = cc.EARTH_GREEN.rgb

# Consts
SIZE = 20   # The size in px of each block

# Fonts
pygame.font.init()
TITLE = pygame.font.SysFont("serif", 24)
OPTION = pygame.font.SysFont("serif", 16)
TEXT = pygame.font.SysFont("serif", 8)

# --- Other classes --

# Block patterns
class Patterns(Enum):
    blank = 0
    vertical = 1
    horizontal = 2
    fill = 3
    uparrow = 4

class BoxRenderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def fgborder(self, x, y, w, h):
        pygame.draw.line(self.screen, FG, (x, y), (x + w, y))
        pygame.draw.line(self.screen, FG, (x + w, y), (x + w, y + h))
        pygame.draw.line(self.screen, FG, (x + w, y + h), (x, y + h))
        pygame.draw.line(self.screen, FG, (x, y + h), (x, y))

    def bgborder(self, x, y, w, h):
        pygame.draw.line(self.screen, BG, (x, y), (x + w, y))
        pygame.draw.line(self.screen, BG, (x + w, y), (x + w, y + h))
        pygame.draw.line(self.screen, BG, (x + w, y + h), (x, y + h))
        pygame.draw.line(self.screen, BG, (x, y + h), (x, y))

    def blank(self, x, y, w, h):
        rect = pygame.rect.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, BG, rect)
        self.fgborder(x, y, w, h)

    def fill(self, x, y, w, h):
        self.fgborder(x, y, w, h)
        rect = pygame.rect.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, FG, rect)

    def vertical(self, x, y, w, h):
        rect = pygame.rect.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, BG, rect)
        self.fgborder(x, y, w, h)
        for i in range(w//2):
            pygame.draw.line(
                self.screen, 
                FG, 
                (x + (i * 2), y),
                (x + (i * 2), y + h)
            )

    def horizontal(self, x, y, w, h):
        rect = pygame.rect.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, BG, rect)
        self.fgborder(x, y, w, h)
        for i in range(h//2):
            pygame.draw.line(
                self.screen,
                FG,
                (x, y + (i * 2)),
                (x + w, y + (i * 2))
            )

    def little_border(self, x, y, w, h, size):
        tlx = x + ((w - size) // 2)      # Top left offsets
        tly = y + ((h - size) // 2)
        rect = pygame.rect.Rect(tlx, tly, size, size)
        pygame.draw.rect(WIN, BG, rect)
        pygame.draw.line(self.screen, FG, (tlx, tly), (tlx + size, tly))
        pygame.draw.line(self.screen, FG, (tlx + size, tly), (tlx + size, tly + size))
        pygame.draw.line(self.screen, FG, (tlx + size, tly + size), (tlx, tly + size))
        pygame.draw.line(self.screen, FG, (tlx, tly + size), (tlx, tly))

    def little_fill(self, x, y, w, h, size):
        self.little_border(x, y, w, h, size)

        tlx = x + ((w - size) // 2)      # Top left offsets
        tly = y + ((h - size) // 2)
        rect = pygame.rect.Rect(tlx, tly, size, size)
        pygame.draw.rect(self.screen, FG, rect)

    def little_dot(self, x, y, w, h):
        self.little_fill(x, y, w, h, 3)

    def _single_dot(self, x, y, col):
        pygame.draw.line(self.screen, col, (x, y), (x, y))

    def arrow(self, x, y, col):
        point1 = (x + 10, y + 2)
        point2 = (x + 5, y + 7)
        point3 = (x + 15, y + 7)

        pygame.draw.line(self.screen, col, point1, point2)
        pygame.draw.line(self.screen, col, point2, point3)
        pygame.draw.line(self.screen, col, point3, point1)

    def background(self, x, y, w, h, col1, col2):
        """
        Was going to be a gradient but ended up being something
        quite cool. Not sure how that happened.
        """
        bgrect = pygame.rect.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, col1, bgrect)

        for row in range(h):
            n = h - (h - row)
            for i in range(n):
                l = ((w)/(n))
                pygame.draw.line(
                    self.screen,
                    col2,
                    ((i*l), row),
                    ((i*l) + l - 1.3, row)
                )


br = BoxRenderer(WIN)

# --- Main game class ---
class Mastermind:
    def __init__(self):
        self.board = [
            [Patterns.blank, Patterns.blank, Patterns.blank, Patterns.blank],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]    # Buffer row for arrow
        ]

        self.pattern = []
        for i in range(4):
            index = random.randint(0, 3)
            match index:
                case 0:
                    self.pattern.append(Patterns.blank)
                case 1:
                    self.pattern.append(Patterns.vertical)
                case 2:
                    self.pattern.append(Patterns.horizontal)
                case 3:
                    self.pattern.append(Patterns.fill)

        self.current_row = 0
        self.current_col = 0

        self.option = 0

        self.scores = []

        self.game_ended = False

        self.won = False

        self.main()

    def check_row(self, row):
        fills = []
        blanks = []
        dots = []
        for i, box in enumerate(self.board[row]):
            if self.pattern[i] == self.board[row][i]:
                fills.append("fill")
            elif self.pattern[i] in self.board[row]:
                blanks.append("blank")
            else:
                dots.append("dot")
        
        if fills == ["fill", "fill", "fill", "fill"]:
            self.game_ended = True
            self.won = True

        score = [] + fills + blanks + dots
        self.scores.append(score)
        

    def main(self):
        state = "menu"
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            if self.current_row < 6:
                self.board[self.current_row + 1][self.current_col] = None

            keys = pygame.key.get_pressed()
                # Scroll the menu
            if state == "menu":
                if keys[pygame.K_UP]:
                    if self.option > 0:
                        self.option -= 1
                if keys[pygame.K_DOWN]:
                    if self.option < 2:
                        self.option += 1
                if keys[pygame.K_z]:
                    if self.option == 0:
                        state = "game"
                    elif self.option == 1:
                        state = "controls"
                    elif self.option == 2:
                        running = False
                        pygame.quit()
                        sys.exit()
            
            if state != "menu":
                if keys[pygame.K_ESCAPE]:
                    if state == "game":     # Reset vars on esc
                        self.board = [
                            [Patterns.blank, Patterns.blank, Patterns.blank, Patterns.blank],
                            [None, None, None, None],
                            [None, None, None, None],
                            [None, None, None, None],
                            [None, None, None, None],
                            [None, None, None, None],
                            [None, None, None, None]    # Buffer row for arrow
                        ]
                        self.current_col = 0
                        self.current_row = 0

                        self.pattern = []
                        for i in range(4):
                            index = random.randint(0, 3)
                            match index:
                                case 0:
                                    self.pattern.append(Patterns.blank)
                                case 1:
                                    self.pattern.append(Patterns.vertical)
                                case 2:
                                    self.pattern.append(Patterns.horizontal)
                                case 3:
                                    self.pattern.append(Patterns.fill)

                        self.scores = []

                        self.game_ended = False

                        self.won = False

                    state = "menu"
            
            if state == "game":
                if keys[pygame.K_LEFT]:
                    if self.current_col > 0:
                        self.current_col -= 1
                if keys[pygame.K_RIGHT]:
                    if self.current_col < 3:
                        self.current_col += 1
                if keys[pygame.K_RETURN]:
                    if self.current_row <= 5:
                        self.check_row(self.current_row)
                    if self.current_row < 5:
                        self.current_row += 1
                        self.current_col = 0
                        self.board[self.current_row] = [
                            Patterns.blank, 
                            Patterns.blank, 
                            Patterns.blank, 
                            Patterns.blank
                        ]
                    elif self.current_row == 5:
                        self.current_row += 1
                        self.board[self.current_row] = [None, None, None, None]
                        self.game_ended = True
                if keys[pygame.K_z]:
                    match self.board[self.current_row][self.current_col]:
                        case Patterns.blank:
                            self.board[self.current_row][self.current_col] = Patterns.horizontal
                        case Patterns.horizontal:
                            self.board[self.current_row][self.current_col] = Patterns.vertical
                        case Patterns.vertical:
                            self.board[self.current_row][self.current_col] = Patterns.fill
                        case Patterns.fill:
                            self.board[self.current_row][self.current_col] = Patterns.blank


            WIN.fill(BG)
            
            if state == "menu":
                self.draw_menu()
            elif state == "game":
                if self.current_row < 6: 
                    self.board[self.current_row + 1][self.current_col] = Patterns.uparrow
                self.draw_game()
            elif state == "controls":
                self.draw_controls()

            pygame.display.flip()
            clock.tick(8)

    def draw_menu(self):
        br.background(0, 0, WIDTH, HEIGHT, FG, BG)

        titletxt = "MASTERMIND"
        playtxt = "Play"
        ctrltxt = "Controls"
        exittxt = "Exit"

        match self.option:
            case 0:
                playtxt = "> " + playtxt
            case 1:
                ctrltxt = "> " + ctrltxt
            case 2:
                exittxt = "> " + exittxt    

        title = TITLE.render(titletxt, False, FG, BG)
        play = OPTION.render(playtxt, False, FG, BG)
        controls = OPTION.render(ctrltxt, False, FG, BG)
        exit = OPTION.render(exittxt, False, FG, BG)

        WIN.blit(title, (0, 0))
        br.blank(30, 45, 97, 70)
        WIN.blit(play, (40, 50))
        WIN.blit(controls, (40, 70))
        WIN.blit(exit, (40, 90))

    def draw_game(self):
        br.background(0, 0, WIDTH, HEIGHT, FG, BG)
        self.draw_board()

    def draw_board(self):
        """
        Draws the board to the screen by calling the BoxRenderer
        based off of what values are stored in the board list.
        """
        for i, row in enumerate(self.board):
            y = i * 20
            for j, column in enumerate(row):
                x = j * 20
                match column:
                    case Patterns.blank:
                        br.blank(x, y, SIZE, SIZE)
                    case Patterns.fill:
                        br.fill(x, y, SIZE, SIZE)
                    case Patterns.horizontal:
                        br.horizontal(x, y, SIZE, SIZE)
                    case Patterns.vertical:
                        br.vertical(x, y, SIZE, SIZE)
                    case Patterns.uparrow:
                        br.arrow(x, y, FG)

        if self.scores != []:
            for i, row in enumerate(self.scores):
                y = i * 20
                for j, column in enumerate(row):
                    x = (j * 20) + 80
                    match column:
                        case "fill":
                            br.little_fill(x, y, SIZE, SIZE, 10)
                        case "blank":
                            br.little_border(x, y, SIZE, SIZE, 10)
                        case "dot":
                            br.little_dot(x, y, SIZE, SIZE)

        if self.game_ended == True:
            y = 120
            for j, column in enumerate(self.pattern):
                x = j * 20
                match column:
                    case Patterns.blank:
                        br.blank(x, y, SIZE, SIZE)
                    case Patterns.fill:
                        br.fill(x, y, SIZE, SIZE)
                    case Patterns.horizontal:
                        br.horizontal(x, y, SIZE, SIZE)
                    case Patterns.vertical:
                        br.vertical(x, y, SIZE, SIZE)
                    case Patterns.uparrow:
                        br.arrow(x, y, FG)

            if self.won:
                msg = TITLE.render("WIN", False, FG, BG)  
                WIN.blit(msg, (95, 117)) 
            else:
                msg = TITLE.render("LOSE", False, FG, BG)  
                WIN.blit(msg, (90, 117)) 


    def draw_controls(self):
        br.background(0, 0, WIDTH, HEIGHT, FG, BG)
        br.blank(5, (HEIGHT//3), WIDTH - 10, HEIGHT - 30 - (HEIGHT//3))
        titletxt = "CONTROLS"
        title = TITLE.render(titletxt, False, FG)
        WIN.blit(title, (17, 7))
        optiontxt =  [
            "ESC | Go back",
            "<- -> | Change box",
            "Z | Cycle box type",
            "ENTER | Enter row"
        ]
        for height, item in enumerate(optiontxt):
            line = OPTION.render(item, False, FG)
            WIN.blit(line, (10, (15*height)+(HEIGHT//3)))


# --- Main ---
if __name__ == "__main__":
    Mastermind()