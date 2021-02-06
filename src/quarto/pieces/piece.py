'''
Created on Feb 6, 2021

@author: yann
'''


class Piece:
    PADDING = 10  # space between the border of a cell and the piece
    OUTLINE = 2  # outline of the piece
    INNER_PADDING = 3  # space between the hole of the piece (if there is one) and the border of the piece

    def __init__(self, color, shape, size, hole):
        self.size = size
        self.color = color
        self.shape = shape
        self.hole = hole

        self.x = 0
        self.y = 0
        self.calc_pos(True)  # initializes the position of the piece on the board

        self.activated = False  # a piece which hasn't been picked yet in not activated

    # calc_pos calculates the x y position where we need to draw the piece
    # if the game is being initialized, init == true, otherwise it's false
    def calc_pos(self, init):
        if(init):  # when we first initialize the game
            pass
        else:  # when a piece is being put on the board
            pass

    # when a piece has been played on the board, activated == True
    def activate(self):
        self.activated = True

    # displays a piece on the board. Each piece is unique as we have 2^4 caracteristics to represent
    def draw(self, win):
        pass

    # equivalent of Java's toString() method
    def __repr__(self):
        return str(self.size + ", " + self.color + ", " + self.shape + ", " + self.hole + ", " + self.activated)
