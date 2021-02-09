'''
Created on Feb 6, 2021

@author: yann
'''

import pygame as pg
from quarto.boards import Board
from quarto.constants import (HEIGHT, WIDTH, BG, BOARDOUTLINE,
                              GROWS, GCOLS, GXOFFSET, GYOFFSET,
                              SROWS, SCOLS, SXOFFSET, SYOFFSET,
                              LGREEN, GREEN, DGREEN)

pg.init()
# window_logo = pg.image.load('favicon.png')
# pg.display.set_icon(window_logo)

win = pg.display.set_mode((WIDTH, HEIGHT))  # (width, height)
fps = 60

pg.display.set_caption('Quarto!')


def main():
    run = True
    clock = pg.time.Clock()

    game_board = Board("GameBoard", False, GROWS, GCOLS, GXOFFSET, GYOFFSET, BOARDOUTLINE, LGREEN, GREEN)
    storage_board = Board("StorageBoard", True, SROWS, SCOLS, SXOFFSET, SYOFFSET, BOARDOUTLINE - 5, LGREEN, GREEN)

    storage_board.move_to_gameboard(game_board, storage_board.board[0][2], 3, 3)

    print(game_board.__repr__())
    print(storage_board.__repr__())

    while run:  # the program will stop when run == false
        clock.tick(fps)  # limits the number of iterations of the while loop
        for event in pg.event.get():  # checks if anything has happened from the user
            if event.type == pg.QUIT:  # if we click de top right cross, then exit
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pass

        win.fill(BG)
        game_board.draw(win)  # draws the cells on the window
        storage_board.draw(win)  # draws the cells on the window

        pg.display.update()  # we need to update the display in order to see changes
    pg.quit()  # clean exit of the program


main()
