'''
Created on Feb 6, 2021

@author: yann
'''

import sys

import pygame.freetype

import pygame as pg
from quarto.constants import (HEIGHT, WIDTH, FONT, TIE)
from quarto.game import Game

# TODO: write the doc according to this standard : https://realpython.com/documenting-python-code/#commenting-code-via-type-hinting-python-35
pg.init()
# window_logo = pg.image.load('favicon.png')
# pg.display.set_icon(window_logo)

win = pg.display.set_mode((WIDTH, HEIGHT))  # (width, height)
GAME_FONT = pygame.freetype.SysFont(FONT, 24)

fps = 60

pg.display.set_caption('Quarto!')


def main():
    """
    The main fonction, the head of the programme
    """
    run = True
    clock = pg.time.Clock()

    game = Game(win)

    #the game as text in the terminal
    print(game.game_board.__repr__())
    print(game.storage_board.__repr__())

    while run:  # the program will stop when run == false
        clock.tick(fps)  # limits the number of iterations of the while loop

        for event in pg.event.get():  # checks if anything has happened from the user
            if event.type == pg.QUIT:  # if we click de top right cross, then exit
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                print("Click")  # everytime the user presses his mouse button, we print click
                pos = pg.mouse.get_pos()  # (x, y) pos of the mouse when pressed
                row, col = game.get_row_col_from_mouse(pos)

                if((row, col) != (-1, -1)):  # if pieces has been taken do nothing
                    game.select(row, col)
                    print(game.__repr__())

                if game.winner():
                    if game.winner() == TIE :
                        print("Nobody won ... it's a TIIIIIIE !!!!!!")
                    else :
                        print("And the winner is... " + game.winner() + "!!!!!!!!")
                    run = False

        game.update(GAME_FONT)  # TODO: find more elegant way to pass this parameter

    #exit the programme if asked by the user
    while True:
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                pygame.quit()
                sys.exit()

#execute the main function
main()
