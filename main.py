#!/usr/bin/env python3

# the * import should be safe because there are no global variables
# in blokus_core
from blokus_core import *
from  tkinter import *
import copy
player, piece, piece_index, move_chosen, board, moves_not_made = [None]*6



def play_game(human_players=4, ai_players=0):
    global status_indicator
    global turn_indicator
    global player
    global piece
    global flip
    global rotation
    global move_chosen
    global board
    global moves_not_made
    global piece_index

    board = Board(human_players)
    game_over = False
    moves_not_made = 0
    while not game_over:
        root.update_idletasks()
        root.update()
        for player in board.players:
            turn_indicator.config(bg=player.color)
            piece = player.pieces[0]
            piece_index = -1
            move_chosen = False
            update_scores()
            refresh(board)
            cycle_piece('')
 
            while not move_chosen:
                root.update_idletasks()
                root.update()
            if moves_not_made >= human_players:
                game_over = True
                break
        
    # finish scoring

    # sort players into list of highest score first
    board.players.sort(key=lambda x: -x.score)
    # print that out, maybe do something else with this later
    status_label.config(text=('Winner: ' + board.players[0].color))
    # TODO: should "probably" also handle ties

def update_scores():
    global board
    global score_display_grid 
    
    for i, player in enumerate(board.players):
        score_display_grid[i].config(text=str(player.score))


def skip_move():
    global move_chosen
    global moves_not_made

    moves_not_made += 1
    move_chosen = True

def choose_move(i, j, e):
    global move_chosen
    global board
    global piece
    global moves_not_made

    if board.is_legal_move(piece, [i,j]):
        # apply move
        for k, l in piece.square_locations([i,j]):
            board.spaces[k][l] = piece.color
        for k, l in piece.corner_locations([i,j]):    
            if -1 < k < 20 and -1 < l < 20:
                board.corners[k][l].append(piece.color)
        for k, l in piece.edge_locations([i,j]):
            if -1 < k < 20 and -1 < l < 20:
                board.edges[k][l].append(piece.color)

        # update score
        if len(player.pieces) == 1 and piece.value == 1:
            player.score += 20
        player.score += piece.value

        # remove piece from hand
        player.pieces.remove(piece)


        moves_not_made = 0
        move_chosen = True

def cycle_piece(event):
    global player
    global piece
    global piece_index
    piece_index = (piece_index + 1) % len(player.pieces)
    piece = player.pieces[piece_index]

    display_piece(piece)

def cycle_position(event):
    global piece

    if piece.rotation < 3:
        piece.rotation += 1
    else:
        piece.rotation = 0
        piece.flipped = False if piece.flipped else True

    display_piece(piece)

def refresh(board):
    global board_grid

    for i, row in enumerate(board.spaces):
        for j, space in enumerate(row):
            board_grid[i][j].config(bg = space)

def display_piece(piece):
    global piece_display_grid

    # make everything black again
    for row in piece_display_grid:
        for square in row:
            square.config(bg='black')

    # actually display the piece
    for x, y in piece.square_locations([4,4]):
        piece_display_grid[x][y].config(bg=piece.color)

if __name__ == '__main__':
    root = Tk()
    root.title('BLOKUS')

    board = Frame(root, bg='black', width=500, height=500)
    board.pack(side=LEFT)
    board_grid = [[None for _ in range(20)] for _ in range(20) ]

    for i,row in enumerate(board_grid):
        for j,column in enumerate(row):
            F = Frame(board,bg='grey', width=int((500/20)-4), height=int((500/20)-4), bd=0)
            F.grid(row=i,column=j,padx=2,pady=2)
            F.bind('<Button-1>',lambda e,i=i,j=j: choose_move(i,j,e))
            row[j] = F

    status_frame = Frame(root, bg='black', width=250, height=500)
    status_frame.pack(side=RIGHT)


    turn_indicator = Frame(status_frame, bg='red', width=250, height=125)
    turn_indicator.grid(row=0, sticky='NESW')

    skip_turn_button = Button(status_frame, text='skip turn', command=skip_move)
    skip_turn_button.grid(row=1)

    piece_display = Frame(status_frame, bg='grey', width=250, height=250)
    piece_display.grid(row=2, pady=(4,3), padx=(4,3))
    piece_display_grid = [[None for _ in range(9)] for _ in range(9)]

    for i,row in enumerate(piece_display_grid):
        for j,column in enumerate(row):
            F = Frame(piece_display,bg='black', width=int(250/9-4), height=int(250/9-4), bd=0)
            F.grid(row=i,column=j,padx=2,pady=2)
            F.bind('<Button-1>', cycle_piece)
            F.bind('<Button-2>', cycle_position)
            row[j] = F

    scores = Frame(status_frame, bg='blue', width=250, height=150)
    scores.grid(row=3)
    
    score_display_grid = ['blue', 'yellow', 'red', 'green']
    for i, color in enumerate(score_display_grid):
        F = Frame(scores, bg=color, width=60, height=150)
        L = Label(F, bg=color, font=('Helvetica', '36'))
        L.pack()
        F.grid(column=i, row=0)
        score_display_grid[i] = L

    # TODO
    status_label_frame = Frame(status_frame, bg='orange', width=250, height=50)
    status_label = Label(status_label_frame, bg='purple', font=('Helvetica', '24'))
    status_label.place(relwidth=1.0, relheight=1.0)
   
    status_label_frame.grid(row=4, sticky='NSEW')


    play_game(4)
