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

# --- Other classes --

# Block patterns
class Patterns(Enum):
    blank = 0
    vertical = 1
    horizontal = 2
    fill = 3

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
        self.fgborder(x, y, w, h)
        for i in range(w//2):
            pygame.draw.line(
                self.screen, 
                FG, 
                (x + (i * 2), y),
                (x + (i * 2), y + h)
            )

    def horizontal(self, x, y, w, h):
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


br = BoxRenderer(WIN)

# --- Main game class ---
class Mastermind:
    def __init__(self):
        self.board = [
            [Patterns.blank, Patterns.horizontal, Patterns.vertical, Patterns.fill],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]

        self.main()

    def main(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            WIN.fill(BG)
            self.draw_board()

            br.little_fill(80, 0, SIZE, SIZE, 10)
            br.little_border(100, 0, SIZE, SIZE, 10)
            br.little_border(120, 0, SIZE, SIZE, 10)
            br.little_dot(140, 0, SIZE, SIZE)

            pygame.display.flip()
            clock.tick(60)

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


# --- Main ---
if __name__ == "__main__":
    Mastermind()