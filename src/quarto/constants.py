'''
Created on Feb 6, 2021

@author: yann
'''

import pygame as pg

WIDTH, HEIGHT = 1200, 900  # pygame window dimensions
SQUARE_SIZE = WIDTH // 12

GROWS, GCOLS = 4, 4  # grid dimensions
GXOFFSET = WIDTH // 2 - SQUARE_SIZE * GCOLS // 2  # centers the grid horizonally
GYOFFSET = SQUARE_SIZE

SCOLS, SROWS = 8, 2  # storage board dimensions
SXOFFSET = WIDTH // 2 - SQUARE_SIZE * SCOLS // 2
SYOFFSET = HEIGHT - SQUARE_SIZE * (SROWS + 1)

GREEN = pg.Color('PaleGreen4')  # light green
LGREEN = pg.Color('dark sea green')  # very light green
DGREEN = pg.Color('darkgreen')  # dark green

BG = (73, 67, 54)
