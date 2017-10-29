#!/usr/bin/env python3
'''
This file holds all the core classes necessary to play a blokus game 
'''

import json


class Piece():
    '''
    A single game piece. 

    Methods:
    collides(self, other) - Returns True if collides with other

    Variables:
    color       - The color of the piece - red, blue, yellow, or green
    value       - The point value of the piece and the amount of squares it has.

    squares     - List of location of all squares relative to an arbitrary 
                    origin square location 
    rotation    - Value from 0-3. An increase of 1 in this value corresponds 
                    with a 90-degree clockwise rotation
    flipped     - True if flipped. Always flipped over y-axis

    corners     - List of location of all squares that would be on a corner

    '''
    
    def __init__(self, color='red', squares=[[0,0]], rotation=0, flipped=False):
        self.color = color
        self.value = len(squares)

        self.squares = squares
        self.edges = self.get_edge_squares()
        self.corners = self.get_corner_squares()

        self.rotation = 0
        self.flipped = False
    
    def get_edge_squares(self):
        '''
        uses the squares list to create a list of squares where other pieces of
        the same color cannot go
        '''
        edges = []
        for square in self.squares[:]:
            # please forgive me
            # finds the adjacent squares to each square
            possible_edges = [[square[0]+a,square[1]+b] for a, b, square in [(1,0,square),(-1,0,square),(0,1,square),(0,-1,square)]]
            for edge in possible_edges:
                if edge not in self.squares:
                    edges.append(edge)
        return edges


    def get_corner_squares(self):
        '''
        uses the squares list and the edges list to create a list of squares
        where other pieces of the same color can go
        '''
        corners = []
        for square in self.squares[:]:
            # please forgive me
            # finds the diagonal squares to each square
            possible_corners = [[square[0]+a,square[1]+b] for a, b, square in [(1,1,square),(1,-1,square),(-1,1,square),(-1,-1,square)]]
            for corner in possible_corners:
                if corner not in self.squares + self.edges:
                    corners.append(corner)
        return corners


    def collides(self, other):
        other_locations = other.square_locations()
        for location in self.square_locations():
            if location in other_locations:
                return False
        return True

    def square_locations(self, origin):
        '''
        Returns a list of the locations of all squares, accounting for origin
        '''
        squares_copy = self.squares[:]

        for square in squares_copy:
            # account for rotation
            # trust me, this works
            if self.rotation % 4 == 1:
                square[0], square[1] = square[1], -square[0]
            if self.rotation % 4 == 2:
                square[0], square[1] = -square[0], -square[1]
            if self.rotation % 4 == 3:
                square[0], square[1] = -square[1], square[0]
            # account for flip
            if self.flipped:
                square[0] *= -1
            # account for origin
            square[0] += origin[0]
            square[1] += origin[1]

        return squares_copy

    def corner_locations(self, origin):
        '''
        Returns a list of the locations of all corners, accounting for origin
        '''
        corners_copy = self.corners[:]

        for corner in corners_copy:
            # account for rotation
            # trust me, this works
            if self.rotation % 4 == 1:
                corner[0], corner[1] = corner[1], -corner[0]
            if self.rotation % 4 == 2:
                corner[0], corner[1] = -corner[0], -corner[1]
            if self.rotation % 4 == 3:
                corner[0], corner[1] = -corner[1], corner[0]
            # account for flip
            if self.flipped:
                corner[0] *= -1
            # account for origin
            corner[0] += origin[0]
            corner[1] += origin[1]

        return corners_copy



class Player():
    '''
    Represents a single player. Used to initialize all the pieces as well.
    Methods:

    Variables:
    color       - blue, yellow, red, green
    score       - a tally of the player's score
    pieces      - A list of all pieces still in the player's hand
    '''
    def __init__(color):
        self.score = 0
        self.color = color
        
        self.pieces = []
        # load data from pieces.json
        with open('pieces.json') as pieces_json:
            pieces = json.load(pieces_json)
            for piece in pieces:
                self.pieces.append(Piece(color=color, squares=piece[0]))



class Board():
    '''
    Represents the game board. Holds a 2d array and associated methods
    Methods:
    is_legal_move(self, piece, origin)
        - Returns True if move is legal. Accounts for corners, adjacency, and overlap
    
    
    Variables:
    spaces      - 2d array that holds pieces
    corners     - 2d array that holds lists of colors that can play for each
                    square
    edges       - 2d array that holds lists of colors that cannot play for
                    each square
    '''
    def __init__(self, length=20, height=20, num_players=4):
        self.spaces = [[None for _ in range(height)] for _ in range(length)]
        self.edges = [[[] for _ in range(height)] for _ in range(length)]
        self.corners = self.edges[:]
        # set the corners to the players
        self.corners[0][0].append('blue')
        self.corners[length-1][height-1].append('red')
        if num_players == 4:
            self.corners[length-1][0].append('yellow')
            self.corners[0][height-1].append('green')


    def is_legal_move(self, piece, origin):
        try:
            has_corner = False
            for location in piece.square_locations(origin):
                # direct overlap
                if self.spaces[location[0]][location[1]]:
                    return False
                # adjacency
                if piece.color in self.edges[location[0]][location[2]]:
                    return False
                # corners
                if piece.color in self.corners[location[0]][location[1]]:
                    has_corner = True
            return has_corner
        except IndexError: # if the move would go outside of the board
            return False



