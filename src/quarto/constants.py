'''
Created on Feb 6, 2021

@author: yann
'''
import pygame as pg

WIDTH, HEIGHT = 1200, 900  # pygame window dimensions
SQUARE_SIZE = WIDTH // 12 # the pygame window's width is composed of 12 small 
BOARDOUTLINE = SQUARE_SIZE // 10    

GROWS, GCOLS = 4, 4  # grid dimensions
GXOFFSET = WIDTH // 2 - SQUARE_SIZE * GCOLS // 2  # centers the grid horizonally
GYOFFSET = SQUARE_SIZE 

SCOLS, SROWS = 8, 2  # storage board dimensions
SXOFFSET = WIDTH // 2 - SQUARE_SIZE * SCOLS // 2
SYOFFSET = HEIGHT - SQUARE_SIZE * (SROWS + 1)

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

LBEIGE = pg.Color('moccasin') #light beige
BEIGE = pg.Color('tan') #beige
LBROWN = pg.Color('darkgoldenrod') #light brown
BROWN = pg.Color('saddlebrown') #brown
DBROWN = pg.Color((41, 21, 10)) #dark brown

WHEAT = pg.Color('wheat')
PAYAYA = pg.Color('papayawhip')

BG = (73, 67, 54) #BackGround
FONT = "freesansbold.ttf" #the font used for the text in the game

PLAYER1 = "PLAYER1" #the two players
PLAYER2 = "PLAYER2"
AI1 = "     AI1" #the 3 artificial intelligence the player can play against
AI2 = "     AI2"
AI3 = "     AI3"
TIE = "TIE" #if there is no winner
