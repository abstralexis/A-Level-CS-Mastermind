"""
This is going to be a gameboy-like Mastermind.
"""

# --- Imports ---
import os, random, sys                          # Standard imports
from enum import Enum

import pygame                                   # 3rd Party imports
import color_codes as cc

# --- Globals --        
pygame.init()                                   # Initialise Pygame

WIDTH = 160                                     # Gameboy dimensions
HEIGHT = 144
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Init screen
pygame.display.set_caption("Mastermind")        # Set caption

# Icon loader
icon_path = "..\\assets\\icon.png"
if os.path.exists(icon_path):                   # Safely check if icon is in cwd
    icon = pygame.image.load(icon_path, "img")  # Load image
    pygame.display.set_icon(icon)               # Set as icon       
else:                                           # Warn on file not found
    print("Icon Load failed. Check you are in the right working directory.")

# Colours
BG = cc.BLACK.rgb
FG = cc.EARTH_GREEN.rgb

# Consts
SIZE = 20   # The size in px of each block

# Fonts
pygame.font.init()                          # Initialise fonts module
TITLE = pygame.font.SysFont("serif", 24)    # Load different font sizes
OPTION = pygame.font.SysFont("serif", 16)
TEXT = pygame.font.SysFont("serif", 8)

# --- Other classes --

# Block patterns enum
class Patterns(Enum):
    """
    Holds the patterns for rendering blocks to the screen from
    the board, includes box patterns and the up arrow.
    """
    blank = 0
    vertical = 1
    horizontal = 2
    fill = 3
    uparrow = 4

class BoxRenderer:
    """
    This is the main graphical rendering part of the game.
    It is called BoxRenderer because it was initially just for
    the boxes in the main gameplay section.
    """
    def __init__(self, screen: pygame.Surface):
        """
        Take in the screen as an argument when initialising an object 
        of BR.        
        """
        self.screen = screen

    def fgborder(self, x, y, w, h):
        """
        Draws a box border at (x, y) of widthxheight wxh
        with the foreground colour that has no fill
        """
        pygame.draw.line(self.screen, FG, (x, y), (x + w, y))
        pygame.draw.line(self.screen, FG, (x + w, y), (x + w, y + h))
        pygame.draw.line(self.screen, FG, (x + w, y + h), (x, y + h))
        pygame.draw.line(self.screen, FG, (x, y + h), (x, y))

    def bgborder(self, x, y, w, h):
        """
        Draws a box at (x, y) of widthxheight wxh
        with the background colour that has no fill
        """
        pygame.draw.line(self.screen, BG, (x, y), (x + w, y))
        pygame.draw.line(self.screen, BG, (x + w, y), (x + w, y + h))
        pygame.draw.line(self.screen, BG, (x + w, y + h), (x, y + h))
        pygame.draw.line(self.screen, BG, (x, y + h), (x, y))

    def blank(self, x, y, w, h):
        """
        Draws a box at (x, y) of widthxheight wxh
        with the foreground colour that has no fill
        """
        rect = pygame.rect.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, BG, rect)
        self.fgborder(x, y, w, h)

    def fill(self, x, y, w, h):
        """
        Draws a box at (x, y) of widthxheight wxh
        with the foreground colour that has fill of
        foreground colour
        """
        self.fgborder(x, y, w, h)
        rect = pygame.rect.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, FG, rect)

    def vertical(self, x, y, w, h):
        """
        Draws a box at (x, y) with widthxheight wxh with
        a border and vertical lines in the foreground colour.
        """
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
        """
        Draws a box at (x, y) with widthxheight wxh with
        a border and horizontal lines in the foreground colour.
        """
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
        """
        Draws a small border in the centre of a box at
        (x,y) wxh with size of size.
        """
        tlx = x + ((w - size) // 2)      # Top left offsets
        tly = y + ((h - size) // 2)
        rect = pygame.rect.Rect(tlx, tly, size, size)
        pygame.draw.rect(WIN, BG, rect)
        pygame.draw.line(self.screen, FG, (tlx, tly), (tlx + size, tly))
        pygame.draw.line(self.screen, FG, (tlx + size, tly), (tlx + size, tly + size))
        pygame.draw.line(self.screen, FG, (tlx + size, tly + size), (tlx, tly + size))
        pygame.draw.line(self.screen, FG, (tlx, tly + size), (tlx, tly))

    def little_fill(self, x, y, w, h, size):
        """
        Draws a small border and fill in the centre of a box at
        (x,y) wxh with size of size.
        """
        self.little_border(x, y, w, h, size)

        tlx = x + ((w - size) // 2)      # Top left offsets
        tly = y + ((h - size) // 2)
        rect = pygame.rect.Rect(tlx, tly, size, size)
        pygame.draw.rect(self.screen, FG, rect)

    def little_dot(self, x, y, w, h):
        """
        Draws a small dot in the centre of a box at
        (x,y) wxh with size of 3.
        """
        self.little_fill(x, y, w, h, 3)

    def _single_dot(self, x, y, col):
        """
        Draws a single dot at certain coordinates.
        """
        pygame.draw.line(self.screen, col, (x, y), (x, y))

    def arrow(self, x, y, col):
        """
        Draw an arrow at the top of a box.
        """
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

        Is a cool background.
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


# Initialise BoxRenderer instance
br = BoxRenderer(WIN)

# --- Main game class ---
class Mastermind:
    """
    This is the main Mastermind game class.
    """
    def __init__(self):
        """
        Load the initial game variables and call main
        """
        self.board = [
            [Patterns.blank, Patterns.blank, Patterns.blank, Patterns.blank],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]    # Buffer row for arrow
        ]

        self.pattern = []                   # Clear pattern array
        for i in range(4):                  # For a width of 4,
            index = random.randint(0, 3)    # Get random pattern index
            match index:                    # Match index and add to pattern
                case 0:
                    self.pattern.append(Patterns.blank)
                case 1:
                    self.pattern.append(Patterns.vertical)
                case 2:
                    self.pattern.append(Patterns.horizontal)
                case 3:
                    self.pattern.append(Patterns.fill)

        # Other var inits
        self.current_row = 0
        self.current_col = 0

        self.option = 0

        self.scores = []

        self.game_ended = False

        self.won = False

        # Call main
        self.main()

    def check_row(self, row):
        """
        Checks the row and adds the scores to a scores list to draw
        """
        # Counting arrays for the types of scoring pegs
        # So that they can be ordered after
        fills = []
        blanks = []
        dots = []

        # Counts the number of each pattern in the target pattern
        num_patterns = {
            Patterns.blank: self.pattern.count(Patterns.blank),
            Patterns.fill: self.pattern.count(Patterns.fill),
            Patterns.horizontal: self.pattern.count(Patterns.horizontal),
            Patterns.vertical: self.pattern.count(Patterns.vertical)
        }

        # Iterate through the row and if the patterns covered count for something is
        # More than 0, append the score then decrease the count. The count helps to
        # Keep the scoring more in line with a more human way of thinking.
        for i, box in enumerate(self.board[row]):
            if self.pattern[i] == self.board[row][i] and num_patterns[self.pattern[i]] > 0:
                fills.append("fill")
                num_patterns[self.pattern[i]] -= 1
            elif self.board[row][i] in self.pattern and num_patterns[self.pattern[i]] > 0:
                blanks.append("blank")
                num_patterns[self.pattern[i]] -= 1
            else:
                dots.append("dot")
        
        # Checks the win
        if fills == ["fill", "fill", "fill", "fill"]:
            self.game_ended = True  # The game has ended
            self.won = True         # AND the user has won

        # Set score and append it to scores array to draw
        score = [] + fills + blanks + dots
        self.scores.append(score)
        

    def main(self):
        """
        Main function
        """
        state = "menu"                          # State machine 
        running = True
        clock = pygame.time.Clock()             # Clock for fps

        # Main loop
        while running:
            # --- Poll events ---
            for event in pygame.event.get():    # Get all events
                if event.type == pygame.QUIT:   # If the big 'X' pressed
                    running = False             # Quit
                    pygame.quit()
                    sys.exit()

            if self.current_row < 6:            # Clear where the arrow is before redraw
                self.board[self.current_row + 1][self.current_col] = None

            keys = pygame.key.get_pressed()     # Get all pressed keys
            # Scroll the menu
            if state == "menu":                 # Menu controls for navigation
                if keys[pygame.K_UP]:
                    if self.option > 0:
                        self.option -= 1
                if keys[pygame.K_DOWN]:
                    if self.option < 2:
                        self.option += 1
                if keys[pygame.K_z]:
                    if self.option == 0:
                        state = "game"          # Example of changing state on select
                    elif self.option == 1:
                        state = "controls"
                    elif self.option == 2:
                        running = False
                        pygame.quit()
                        sys.exit()
            
            if state != "menu":             # Allow escape to be used on any non menu
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
            
            # Main game controls
            if state == "game":
                if keys[pygame.K_LEFT]:         # Go left a col
                    if self.current_col > 0:
                        self.current_col -= 1
                if keys[pygame.K_RIGHT]:        # Go right a col
                    if self.current_col < 3:
                        self.current_col += 1
                if keys[pygame.K_RETURN]:       # Enter row
                    if self.current_row <= 5:   # Check win
                        self.check_row(self.current_row)
                    if self.current_row < 5:    # If not the last row                
                        self.current_row += 1   # Change row and col ptrs
                        self.current_col = 0    # and add clear row
                        self.board[self.current_row] = [
                            Patterns.blank, 
                            Patterns.blank, 
                            Patterns.blank, 
                            Patterns.blank
                        ]
                    elif self.current_row == 5: # If last row (final guess)
                        self.current_row += 1   # Add a clear line below 
                        self.board[self.current_row] = [None, None, None, None]
                        self.game_ended = True  # End game
                if keys[pygame.K_z]:    # Change the pattern stored at current selection
                    match self.board[self.current_row][self.current_col]:
                        case Patterns.blank:
                            self.board[self.current_row][self.current_col] = Patterns.horizontal
                        case Patterns.horizontal:
                            self.board[self.current_row][self.current_col] = Patterns.vertical
                        case Patterns.vertical:
                            self.board[self.current_row][self.current_col] = Patterns.fill
                        case Patterns.fill:
                            self.board[self.current_row][self.current_col] = Patterns.blank

            # --- Drawing ---
            WIN.fill(BG)    # Fill with bg col
            
            if state == "menu":
                self.draw_menu()    # Draw the menu
            elif state == "game":
                if self.current_row < 6:    # Add the arrow to the board
                    self.board[self.current_row + 1][self.current_col] = Patterns.uparrow
                self.draw_game()            # Draw the game
            elif state == "controls":       
                self.draw_controls()        # Draw the controls screen

            pygame.display.flip()           # Update screen
            clock.tick(8)                   # 8 fps

    def draw_menu(self):
        """
        Drawing the menu function
        """
        br.background(0, 0, WIDTH, HEIGHT, FG, BG)  # Draw background

        # Text variables
        titletxt = "MASTERMIND"
        playtxt = "Play"
        ctrltxt = "Controls"
        exittxt = "Exit"

        # Depending on what is selected, indicate with a '>' prepended.
        match self.option:
            case 0:
                playtxt = "> " + playtxt
            case 1:
                ctrltxt = "> " + ctrltxt
            case 2:
                exittxt = "> " + exittxt    

        # Render the texts
        title = TITLE.render(titletxt, False, FG, BG)
        play = OPTION.render(playtxt, False, FG, BG)
        controls = OPTION.render(ctrltxt, False, FG, BG)
        exit = OPTION.render(exittxt, False, FG, BG)

        # Blit the texts to the screen as well as a box around it
        WIN.blit(title, (0, 0))
        br.blank(30, 45, 97, 70)
        WIN.blit(play, (40, 50))
        WIN.blit(controls, (40, 70))
        WIN.blit(exit, (40, 90))

    def draw_game(self):
        """
        Function for drawing during the game
        """
        br.background(0, 0, WIDTH, HEIGHT, FG, BG)  # Draw the background
        self.draw_board()                           # Draw the board

    def draw_board(self):
        """
        Draws the board to the screen by calling the BoxRenderer
        based off of what values are stored in the board list.
        """
        for i, row in enumerate(self.board):        # Iter through board rows
            y = i * 20                              # y coord offset for row
            for j, column in enumerate(row):        # Iter through cols in row
                x = j * 20                          # x coord offset for col in row
                match column:                       # Draw at (x,y) the pattern
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

        if self.scores != []:                       # If scores not empty
            for i, row in enumerate(self.scores):   # Iter through score rows
                y = i * 20                          # y offset for row
                for j, column in enumerate(row):    # Iter through score cols in row
                    x = (j * 20) + 80               # x offset for col in row
                    match column:                   # Draw at (x,y) the correct score box
                        case "fill":
                            br.little_fill(x, y, SIZE, SIZE, 10)
                        case "blank":
                            br.little_border(x, y, SIZE, SIZE, 10)
                        case "dot":
                            br.little_dot(x, y, SIZE, SIZE)

        if self.game_ended == True:                     # On game end
            y = 120                                     # y offset for pattern
            for j, column in enumerate(self.pattern):   # Iter through pattern
                x = j * 20                              # x offset for pattern
                match column:                           # Draw target pattern
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

            if self.won:                                # If the game was won
                msg = TITLE.render("WIN", False, FG, BG)    # WIN screen
                WIN.blit(msg, (95, 117)) 
            else:                                       # If the game was not won
                msg = TITLE.render("LOSE", False, FG, BG)   # LOSE screen
                WIN.blit(msg, (90, 117)) 


    def draw_controls(self):
        """
        Draw the stuff shown on the controls screen.
        """
        # This is all static rendering really, so it does not need much explanation.
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