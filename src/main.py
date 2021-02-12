'''
Created on Feb 6, 2021

@author: yann
'''

import pygame as pg
from quarto.constants import (HEIGHT, WIDTH, BG)
from quarto.game import Game

# TODO: write the doc according to this standard : https://realpython.com/documenting-python-code/#commenting-code-via-type-hinting-python-35

pg.init()
# window_logo = pg.image.load('favicon.png')
# pg.display.set_icon(window_logo)

win = pg.display.set_mode((WIDTH, HEIGHT))  # (width, height)
fps = 60

pg.display.set_caption('Quarto!')


def main():
    run = True
    clock = pg.time.Clock()

    game = Game(win)
    win.fill(BG)

    print(game.game_board.__repr__())
    print(game.storage_board.__repr__())

    while run:  # the program will stop when run == false
        clock.tick(fps)  # limits the number of iterations of the while loop
        for event in pg.event.get():  # checks if anything has happened from the user
            if event.type == pg.QUIT:  # if we click de top right cross, then exit
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                row, col = game.storage_board.get_row_col_from_mouse(pos)

                game.select(row, col)
                print(game.__repr__())

        game.update()
    pg.quit()  # clean exit of the program


main()
