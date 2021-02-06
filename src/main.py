'''
Created on Feb 6, 2021

@author: yann
'''

import pygame as pg
from quarto.boards import GameBoard, StorageBoard
from quarto.constants import HEIGHT, WIDTH, BG

pg.init()
# window_logo = pg.image.load('favicon.png')
# pg.display.set_icon(window_logo)

# TODO: eventually, we'll have to change the width and height to make it fit our TWO boards
win = pg.display.set_mode((WIDTH, HEIGHT))  # (width, height)
fps = 60

pg.display.set_caption('Quarto!')


def main():
    run = True
    clock = pg.time.Clock()
    game_board = GameBoard()
    storage_board = StorageBoard()
    while run:  # the program will stop when run == false
        clock.tick(fps)  # limits the number of iterations of the while loop
        for event in pg.event.get():  # checks if anything has happened from the user
            if event.type == pg.QUIT:  # if we click de top right cross, then exit
                run = False

        win.fill(BG)
        game_board.draw_cells(win)  # draws the cells on the window
        storage_board.draw(win)  # draws the cells on the window

        pg.display.update()  # we need to update the display in order to see changes
    pg.quit()  # clean exit of the program


main()
