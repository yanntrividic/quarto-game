'''
Created on Feb 6, 2021

@author: yann
'''

import sys

from pygame import freetype

import pygame as pg
from quarto.constants import (HEIGHT, WIDTH, FONT)
from quarto.game import Game

# TODO: write the doc according to this standard : https://realpython.com/documenting-python-code/#commenting-code-via-type-hinting-python-35
pg.init()
# window_logo = pg.image.load('favicon.png')
# pg.display.set_icon(window_logo)

win = pg.display.set_mode((WIDTH, HEIGHT))  # (width, height)
GAME_FONT = freetype.SysFont(FONT, 24)

fps = 60

pg.display.set_caption('Quarto!')

#  TODO: Add options to startup the program.
#  --players 0 the game is initialized with a duel of humans,
#  --players 1 a duel of level 1 AIs
#  --players 10 a lvl 1 AI against a human (and the AI starts)
#  --gendata "path" runs a series of games automatically to generate data about the performances of the players and
#    saves it in the path file
#  --nbiter 100 is the number of games played
#   (number of pieces put on the board, result (winner or tie, processing time per turn...)


def main():
    """
    The main fonction, the head of the program
    """
    run = True
    clock = pg.time.Clock()

    game = Game(win, GAME_FONT)

    # the game as text in the terminal
    print(game.game_board.__repr__())
    print(game.storage_board.__repr__())

    while run:  # the program will stop when run == false
        clock.tick(fps)  # limits the number of iterations of the while loop

        if not game.winner():
            if not game.is_human_turn():
                game.select()

            for event in pg.event.get():  # checks if anything has happened from the user
                if event.type == pg.QUIT:  # if we click de top right cross, then exit
                    run = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()  # (x, y) pos of the mouse when pressed
                    print("Click " + str(pos))  # everytime the user presses his mouse button, we print click

                    clicked_arrow = game.is_arrow_clicked(pos)  # checks if a player is being swaped
                    if clicked_arrow is not None:
                        game.swap_players(clicked_arrow)

                    row, col = game.get_row_col_from_mouse(pos)
                    print(row, col)
                    if (row, col) != (-1, -1) and game.is_human_turn():  # if pieces has been taken do nothing
                        game.select(row, col)
                        print(game.__repr__())

        else:  # the user can either reset the game or quit
            for event in pg.event.get():  # checks if anything has happened from the user
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()  # (x, y) pos of the mouse when pressed
                    print("Click " + str(pos))  # everytime the user presses his mouse button, we print click
                    if game.is_reset_clicked(pos):
                        game.reset()

        game.update()

    # exit the programme if asked by the user
    pg.quit()
    sys.exit()


# execute the main function
if __name__ == '__main__':
    main()
