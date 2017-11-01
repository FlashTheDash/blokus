#!/usr/bin/env python3
'''
This file holds all the core classes necessary to play a blokus game 
'''

import json
import copy

class Piece():
    '''
    A single game piece. 

    Methods:
    get_edge_squares()
        - returns a list of edges of this piece, only for init
    get_corner_squares() 
        - returns a list of corners of this piece, only for init
    square_locations()
        - returns a list of where the squares would be based on an origin
    edge_locations()
        - square_locations() but for edges
    corner_locations()
        - square_locations() but for corners
    
    Variables:
    color       - The color of the piece - red, blue, yellow, or green
    value       - The point value of the piece and the amount of squares it has
    
    squares     - List of location of all squares relative to an arbitrary 
    corners     - List of location of all squares that would be on a corner
    edges       - List of location of all squares that would be on an edge
                    origin square location 
    rotation    - Value from 0-3. An increase of 1 in this value corresponds 
                    with a 90-degree clockwise rotation
    flipped     - True if flipped. Always flipped over y-axis

     '''
    
    def __init__(self, color='red', squares=[[0,0]], rotation=0, flipped=False):
        self.color = color
        self.value = len(squares)

        self.squares = squares
        self.edges = self.get_edge_squares()
        self.corners = self.get_corner_squares()

        self.rotation = 0
        self.flipped = False

    def __repr__(self):
        return 'Piece: color={}, value={}'.format(self.color, self.value)

    def __str__(self):
        return repr(self)
    
    def __eq__(self, other):
        return self.squares == other.squares

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
        for square in list(self.squares):
            # please forgive me
            # finds the diagonal squares to each square
            possible_corners = [[square[0]+a,square[1]+b] for a, b, square in [(1,1,square),(1,-1,square),(-1,1,square),(-1,-1,square)]]
            for corner in possible_corners:
                if corner not in self.squares + self.edges:
                    corners.append(corner)
        return corners

    def square_locations(self, origin):
        '''
        Returns a list of the locations of all squares, accounting for origin
        '''
        squares_copy = copy.deepcopy(self.squares)
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
        corners = []
        for square in self.square_locations(origin):
            # please forgive me
            # finds the diagonal squares to each square
            # looking back on this, I've gotten far worse
            possible_corners = [[square[0]+a,square[1]+b] for a, b, square in [(1,1,square),(1,-1,square),(-1,1,square),(-1,-1,square)]]
            for corner in possible_corners:
                if corner not in self.square_locations(origin) + self.edge_locations(origin):
                    corners.append(corner)
        print(corners)
        return corners

    def edge_locations(self, origin):
        '''
        Returns a list of the locations of all corners, accounting for origin
        '''
        edges = []
        for square in self.square_locations(origin):
            # please forgive me
            # finds the adjacent squares to each square
            possible_edges = [[square[0]+a,square[1]+b] for a, b, square in [(1,0,square),(-1,0,square),(0,1,square),(0,-1,square)]]
            for edge in possible_edges:
                if edge not in self.square_locations(origin):
                    edges.append(edge)
        return edges


class Player():
    # NOTE: ai players should probably subclass this and override choose_move()
    '''
    Represents a single player. Used to initialize all the pieces as well.
    Methods:
    choose_move(board)
        - chooses a move AND EXECUTES IT to reduce complexity
            remember to add points as appropriate and remove played piece
            from hand
    get_legal_moves(board)
        - returns a list of all legal moves, used by choose_move()

    Variables:
    color       - blue, yellow, red, green
    score       - a tally of the player's score
    pieces      - A list of all pieces still in the player's han
    '''
    def __init__(self, color):
        self.score = 0
        self.color = color
        
        self.pieces = []
        # load data from pieces.json
        with open('pieces.json') as pieces_json:
            pieces = json.load(pieces_json)
            for piece in pieces:
                self.pieces.append(Piece(color=color, squares=piece))

    def __repr__(self):
        return 'Player: color={}, score={}, pieces={}'.format(self.color, self.score, [str(piece) for piece in self.pieces])

    def __str__(self):
        return repr(self)

    def get_legal_moves(self, board):
        # brute force approach
        legal_moves = []

        for piece in enumerate(self.pieces[:]):
            # every rotation
            for rotation in range(4):
                piece[1].rotation = rotation
                # every flip
                for flip in [True, False]:
                    piece[1].flipped = flip
                    # every square
                    for row in range(board.height):
                        for column in range(board.length):
                            if board.is_legal_move(piece[1], [row, column]):
                                legal_moves.append([piece[1], [row, column], rotation, flip])
        # moves are represented as:
        # [index in self.pieces, coords, rotation, flip]
        return legal_moves


    def choose_move(self, board):
        legal_moves = self.get_legal_moves(board)
        if not legal_moves:
            print('no possible moves')
            return False

        move = [Piece(),[-1,-1]]
        while move not in legal_moves:
            print(legal_moves)

            print('\ngimme a move')
            x = int(input('x: '))
            y = int(input('y: '))
            rotation = int(input('rotation: '))
            flip = bool(input('type anything for flip'))
            try:
                piece = self.pieces[int(input('piece index: '))]
            except IndexError:
                continue
    
            move = [piece, [x,y], rotation, flip]
            print(move)
            if bool(input('type something if you want to give up')):
                return False
        
        print('applying move (it\'s valid btw)')
        # apply move
        piece.rotation = rotation
        piece.flip = flip

        for square in piece.square_locations(move[1]):
            board.spaces[square[0]][square[1]] = self.color

        for square in piece.corner_locations(move[1]):
            board.corners[square[0]][square[1]].append(self.color)

        for square in piece.edge_locations(move[1]):
            board.edges[square[0]][square[1]].append(self.color)
        
        # add points
        if len(self.pieces) == 1 and piece.value == 1:
            self.score += 5
        self.score += piece.value

        # remove piece
        self.pieces.remove(move[0])

        return True


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
    def __init__(self, num_players=4, length=20, height=20):
        self.spaces = [[None for _ in range(height)] for _ in range(length)]
        self.edges = [[[] for _ in range(height)] for _ in range(length)]
        self.corners = [[[] for _ in range(height)] for _ in range(length)]
        
        self.height = height
        self.length = length

        self.corners[0][0].append('blue')
        self.corners[length-1][height-1].append('red')
        if num_players == 4:
            self.players = [Player(color) for color in ['blue','yellow','red','green']]
            self.corners[length-1][0].append('yellow')
            self.corners[0][height-1].append('green')
        else:
            self.players = [Player('blue'), Player('red')]

    def is_legal_move(self, piece, origin):
        try:
            has_corner = False
            for location in piece.square_locations(origin):
                # direct overlap
                if self.spaces[location[0]][location[1]]:
                    return False
                # adjacency
                if piece.color in self.edges[location[0]][location[1]]:
                    return False
                # corners
                if piece.color in self.corners[location[0]][location[1]]:
                    has_corner = True
            return has_corner
        except IndexError: # if the move would go outside of the board
            print('index error in is_legal_move')
            return False

