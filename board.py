import pgzrun
TILE_SIZE = 60
WIDTH = 480
HEIGHT = 480
background = Actor("background")
highlight = Actor("__")
pieces = []
selected = 0
valid_moves = []
takeable = []
black_castle = True
white_castle = True
playing = True
go = "w"
board = [
    ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
    ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
    ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
    ]
for row in range(len(board)):
    for column in range(len(board[row])):
        x = (column * TILE_SIZE)+30
        y = (row * TILE_SIZE)+30
        tile = board[row][column]
        piece = Actor((board[row][column]),(x,y))
        pieces.append(piece)

def move(piece,to):
    global go
    if go == "w":
        go = "b"
    else:
        go = "w"
    img = piece.image
    for i in pieces:
        if piece.pos == i.pos:
            i.image = "__"
            position = find_piece(i)
            x, y = position
            x = int(x)
            y = int(y)
            board[x][y] = "__"
    for i in pieces:
        if i.pos == to:
            i.image = img
            position = find_piece(i)
            x, y = position
            x = int(x)
            y = int(y)
            if board[x][y] == "wk":
                print("Black wins.")
            elif board[x][y] == "bk":
                print("White wins.")
            board[x][y] = img


def draw():
    screen.clear()
    background.draw()
    highlight.draw()
    for take in takeable:
        take.draw()
    for piece in pieces:
        piece.draw()
    for squares in valid_moves:
        squares.draw()

def on_mouse_down(pos, button):
    global selected, go
    if selected != 0:
        for i in range(len(valid_moves)):
            if button == mouse.LEFT and valid_moves[i].collidepoint(pos):
                move(selected, valid_moves[i].pos)
                selected = 0
        for i in range(len(takeable)):
            if button == mouse.LEFT and takeable[i].collidepoint(pos):
                move(selected, takeable[i].pos)
                selected = 0
    else:
        highlight.image = "__"
    valid_moves.clear()
    takeable.clear()
    for piece in pieces:
        if button == mouse.LEFT and piece.collidepoint(pos) and piece.image[0] == go:
            highlight.image = "--"
            highlight.x = piece.x
            highlight.y = piece.y
            selected = piece
            check_valid(piece)
            if piece.image == "__":
                highlight.image = "__"
                selected = 0


def find_piece(piece):
    x = int((piece.y - 30) / 60)
    y = int((piece.x - 30) / 60)
    return (x, y)

def check_valid(piece):
    piece_types = {
        'wr': check_rook_moves,
        'br': check_rook_moves,
        'wb': check_bishop_moves,
        'bb': check_bishop_moves,
        'wq': check_queen_moves,
        'bq': check_queen_moves,
        'wp': check_pawn_moves,
        'bp': check_pawn_moves,
        'wn': check_knight_moves,
        'bn': check_knight_moves,
        'wk': check_king_moves,
        'bk': check_king_moves,
    }
    piece_type = piece.image
    if piece_type[0] == 'b':
        op_colour = 'w'
    else:
        op_colour = 'b'
    if piece_type in piece_types:
        piece_types[piece_type](piece,op_colour)

def check_queen_moves(piece,op_colour):
    check_rook_moves(piece,op_colour)
    check_bishop_moves(piece,op_colour)

def check_rook_moves(piece,op_colour):
    position = find_piece(piece)
    x, y = position
    x = int(x)
    y = int(y)

    # Check valid moves to the left
    for i in range(y - 1, -1, -1):
        current_square = board[x][i]
        if current_square == "__":
            valid_moves.append(Actor(("moves"),(i*60+30,x*60+30)))
        elif current_square[0] == op_colour:
            takeable.append(Actor(("take"),(i*60+30,x*60+30)))
            break
        else:
            break

    # Check valid moves to the right
    for i in range(y + 1, 8):
        current_square = board[x][i]
        if current_square == "__":
            valid_moves.append(Actor(("moves"),(i*60+30,x*60+30)))
        elif current_square[0] == op_colour:
            takeable.append(Actor(("take"),(i*60+30,x*60+30)))
            break
        else:
            break

    # Check valid moves upwards
    for i in range(x - 1, -1, -1):
        current_square = board[i][y]
        if current_square == "__":
            valid_moves.append(Actor(("moves"),(y*60+30,i*60+30)))
        elif current_square[0] == op_colour:
            takeable.append(Actor(("take"),(y*60+30,i*60+30)))
            break
        else:
            break

    # Check valid moves downwards
    for i in range(x + 1, 8):
        current_square = board[i][y]
        if current_square == "__":
            valid_moves.append(Actor(("moves"),(y*60+30,i*60+30)))
        elif current_square[0] == op_colour:
            takeable.append(Actor(("take"),(y*60+30,i*60+30)))
            break
        else:
            break
    #TODO: add castling

def check_bishop_moves(piece, op_colour):
    position = find_piece(piece)
    x, y = position
    x = int(x)
    y = int(y)

    # Check valid moves to the top-left
    for i, j in zip(range(x-1, -1, -1), range(y-1, -1, -1)):
        current_square = board[i][j]
        if current_square == "__":
            valid_moves.append(Actor(("moves"),(j*60+30,i*60+30)))
        elif current_square[0] == op_colour:
            takeable.append(Actor(("take"),(j*60+30,i*60+30)))
            break
        else:
            break

    # Check valid moves to the top-right
    for i, j in zip(range(x-1, -1, -1), range(y+1, 8)):
        current_square = board[i][j]
        if current_square == "__":
            valid_moves.append(Actor(("moves"),(j*60+30,i*60+30)))
        elif current_square[0] == op_colour:
            takeable.append(Actor(("take"),(j*60+30,i*60+30)))
            break
        else:
            break

    # Check valid moves to the bottom-left
    for i, j in zip(range(x+1, 8), range(y-1, -1, -1)):
        current_square = board[i][j]
        if current_square == "__":
            valid_moves.append(Actor(("moves"),(j*60+30,i*60+30)))
        elif current_square[0] == op_colour:
            takeable.append(Actor(("take"),(j*60+30,i*60+30)))
            break
        else:
            break

    # Check valid moves to the bottom-right
    for i, j in zip(range(x+1, 8), range(y+1, 8)):
        current_square = board[i][j]
        if current_square == "__":
            valid_moves.append(Actor(("moves"),(j*60+30,i*60+30)))
        elif current_square[0] == op_colour:
            takeable.append(Actor(("take"),(j*60+30,i*60+30)))
            break
        else:
            break

def check_pawn_moves(piece,op_colour):
    position = find_piece(piece)
    x, y = position
    x = int(x)
    y = int(y)

    #Check moves for white pawn
    if op_colour == "b":
        if board[x-1][y] == "__":
            valid_moves.append(Actor(("moves"),(y*60+30,(x-1)*60+30)))
        if y > 0:
            if board[x-1][y-1][0]=="b":
                takeable.append(Actor(("take"),((y-1)*60+30,(x-1)*60+30))) 
        if y < 7:
            if board[x-1][y+1][0]=="b":
                takeable.append(Actor(("take"),((y+1)*60+30,(x-1)*60+30))) 
        if x == 6 and board[x-2][y] == "__" and board[x-1][y] == "__":
            valid_moves.append(Actor(("moves"),(y*60+30,(x-2)*60+30)))

    #Check moves for black pawn
    else:
        if board[x+1][y] == "__":
            valid_moves.append(Actor(("moves"),(y*60+30,(x+1)*60+30)))
        if y > 0:
            if board[x+1][y-1][0]=="w":
                takeable.append(Actor(("take"),((y-1)*60+30,(x+1)*60+30))) 
        if y < 7:
            if board[x+1][y+1][0]=="w":
                takeable.append(Actor(("take"),((y+1)*60+30,(x+1)*60+30))) 
        if x == 1 and board[x+2][y] == "__" and board[x+1][y] == "__":
            valid_moves.append(Actor(("moves"),(y*60+30,(x+2)*60+30)))
    #TODO: add en passeunt rule
    #TODO: add promotion

def check_knight_moves(piece,op_colour):
    position = find_piece(piece)
    x, y = position
    x = int(x)
    y = int(y)

    #The different offsets for the knight movement
    knight_moves = [
        [ 2, 1],
        [ 2,-1],
        [ 1,-2],
        [ 1, 2],
        [-1, 2],
        [-1,-2],
        [-2, 1],
        [-2,-1]]
    for i in range(len(knight_moves)):
        new_x = x + knight_moves[i][1]
        new_y = y + knight_moves[i][0]
        if new_x<0 or new_x>7 or new_y<0 or new_y>7:
            continue
        if board[new_x][new_y][0] == op_colour:
            takeable.append(Actor(("take"),(new_y*60+30,new_x*60+30))) 
        elif board[new_x][new_y] == "__":
            valid_moves.append(Actor(("moves"),(new_y*60+30,new_x*60+30)))

def check_king_moves(piece,op_colour):
    position = find_piece(piece)
    x, y = position
    x = int(x)
    y = int(y)
    
    #Check squares around king
    for i in range(-1,2):
        for j in range(-1,2):
            new_x = x + i
            new_y = y + j
            if new_x<0 or new_x>7 or new_y<0 or new_y>7 or(i==0 and j==0):
                continue
            if board[new_x][new_y][0] == op_colour:
                takeable.append(Actor(("take"),(new_y*60+30,new_x*60+30))) 
            elif board[new_x][new_y] == "__":
                valid_moves.append(Actor(("moves"),(new_y*60+30,new_x*60+30)))
    #TODO: add castling
    
pgzrun.go()