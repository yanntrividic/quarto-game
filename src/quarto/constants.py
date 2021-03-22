'''
Created on Feb 6, 2021

@author: yann
'''
import pygame as pg

WIDTH, HEIGHT = 1200, 900  # pygame window dimensions
SQUARE_SIZE = WIDTH // 12  # the pygame window's width is composed of 12 small
BOARDOUTLINE = SQUARE_SIZE // 10

GROWS, GCOLS = 4, 4  # grid dimensions
GXOFFSET = WIDTH // 2 - SQUARE_SIZE * GCOLS // 2  # centers the grid horizonally
GYOFFSET = SQUARE_SIZE

SCOLS, SROWS = 8, 2  # storage board dimensions
SXOFFSET = WIDTH // 2 - SQUARE_SIZE * SCOLS // 2
SYOFFSET = HEIGHT - SQUARE_SIZE * (SROWS + 1)

TXT_X, TXT_Y = (55, 200)  # coordinates for the text displayed

RESET_X = TXT_X
RESET_Y = TXT_Y + 50
RESET_WIDTH = 200
RESET_HEIGHT = 70

# Coordinates of the arrows
X_LEFT_ARROWS = 930
X_RIGHT_ARROWS = 1075
Y_TOP_ARROWS = TXT_Y + 60
Y_BOT_ARROWS = Y_TOP_ARROWS + 50

# P1COLS, P1ROWS = 2, 1 # player1 rectangle dimensions
# P1XOFFSET = WIDTH - SQUARE_SIZE * (P1COLS + 1)
# P1YOFFSET = SQUARE_SIZE * (P1ROWS + 2)

# P2COLS, P2ROWS = 2, 1 # player2 rectangle dimensions
# P2XOFFSET = P1XOFFSET
# P2YOFFSET = P1YOFFSET + SQUARE_SIZE

# Colors
GREEN = pg.Color('PaleGreen4')  # light green
LGREEN = pg.Color('dark sea green')  # very light green
DGREEN = pg.Color('darkgreen')  # dark green

LBEIGE = pg.Color('moccasin')  # light beige
BEIGE = pg.Color('tan')  # beige
LBROWN = pg.Color('darkgoldenrod')  # light brown
BROWN = pg.Color('saddlebrown')  # brown
DBROWN = pg.Color((41, 21, 10))  # dark brown

WHEAT = pg.Color('wheat')
PAYAYA = pg.Color('papayawhip')
LGRAY = pg.Color((150, 150, 150))

BG = (73, 67, 54)  # BackGround
FONT = "freesansbold.ttf"  # the font used for the text in the game

PLAYER1 = "PLAYER1"  # the two players
PLAYER2 = "PLAYER2"
AI1 = "AI1"  # the 3 artificial intelligence the player can play against
AI2 = "AI2"  # the 3 artificial intelligence the player can play against
TIE = "TIE"  # if there is no winner
