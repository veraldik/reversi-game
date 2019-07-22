    #########################################################################################################
    # Project 10
    #   Algorithim
    #     Indexify
    #       create dictionary that contains a letter as a key and its corresponding row
    #       create a tuple that contains the row and column 
    #       returns the row and column for specific index inputs
    #     Deindexify
    #       create dictionary that contains the row as the key and the letter as the value
    #       create a tuple that contains the letter and number
    #       return that letter and number for specific row/col inputs
    #     Initialize
    #       calls reversi.Piece(color) and assigns them to their respective names
    #       initializes a start and move that handle any size board played
    #       places two pieces for each color that are diagonal on the board
    #     Count_pieces
    #       find the total number of balck/white pieces on board
    #       use for loops to iterate through every spot on the board. 
    #       use board attribute to check for a piece, if a piece is there check for the color
    #       count the number of black pieces and white pieces using a counter
    #       return a tuple that contains the number of black pieces first then the white
    #     Get_all_streaks
    #       GIVEN. Returns a dictionary of all capturing streaks in each direction
    #     Get_all_capturing_Cells
    #       Use for loops to iterate through each spot on the board and and check for piece
    #       call get_all_streaks and extend the value to an already initialized list
    #       if the list contains values add to a dictionary that uses the row,col as the key
    #       return the dictionary
    #     Get_hint
    #       initialize two different lists 
    #       iterate through the key and value in the dictionary returned by get_all_capturing_cells
    #       add the key/value to a list (for each empty spot)
    #       sort the list by length first and then alphabetically
    #       iterate through the list and add the (a1) values to a different list and return
    #     Place_and_flip
    #       Checks for errors first, raises ValueError for invalid spaces, occupied spaces or if it is not
    #           a capture
    #       iterate through key/value in the dictionary returned by get_all_streaks and add them to a new list
    #       raise error if the list is empty
    #       place a piece on the row,col passed through the function
    #       flip the pieces that are would capture
    #     Is_game_finished
    #       if the board is full (check using board attribute) return True (causes game to end)
    #       if the board has no more moves for white or black return True (causes game to end)
    #       else return False (ending the game)
    #     Get_winner:
    #       checks for winner by calliing count_pieces and seeing which color has more pieces
    #     Choose_color
    #       asks for user input, asks until user enters appropriate input and then assigns colors respectively
    #           and returns a tuple
    #     Game_play_human
    #       Given. Calls all functions and conducts Reversi
    ###########################################################################################################  


import reversi
import string
import operator
LETTERS = string.ascii_lowercase

def indexify(position):
    '''Converts letter-number position to row-column indices.'''
    RowColumn = {}
    for count,letter in enumerate(LETTERS):
        RowColumn[letter] = count
    
    row = RowColumn[position[0]]
    column = (int(position[1:]))-1
    row_column_tuple = (row,column)
    
    return(row_column_tuple)

def deindexify(row,col):
    '''Converts row-column indices to letter-number position.'''
    LetterNumber = {}
    for count,letter in enumerate(LETTERS):
        LetterNumber[count] = letter
        
    letter = str(LetterNumber[row])
    number = str(col + 1)
    
    letter_number_str = letter+number
    return(letter_number_str)
       
def initialize(board):
    '''Places two black and two white pieces in the middle of the board diagnoally 
    with respect to eachother. Handles any size board.'''
    white,black = reversi.Piece('white'),reversi.Piece('black')
    start = board.length//2
    move = start - 1
    
    board.place(move,move,white)
    board.place(start,start,white)
    board.place(move,start,black)
    board.place(start,move,black)
    
def count_pieces(board):
    '''Counts total numnber of black and white pieces of the board and returns a (black,white).'''
    black,white = 0,0
    for row in range(board.length):
        for col in range(board.length):
            check = board.get(col,row)
            if check != None:
                if check.is_black():
                    black += 1
                else:
                    white += 1
    return(black,white)


def get_all_streaks(board, row, col, piece_arg):
    ''' GIVEN. Finds all capturing streaks if a piece is placed on the row,col position. Returns
        a dictionary of all capturing streaks in all 8 directions (N,S,E,W...)'''
    streaks = {'e': None, 'w': None, 'n': None, 's': None, \
               'ne': None, 'nw': None, 'se': None, 'sw': None}
    
    color = piece_arg.color()
    other_color = 'white' if color == 'black' else 'black'
    # north
    L = []
    c = col
    for r in range(row-1,-1,-1):
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
    else:
        L = [] # streak not terminated with color piece
    streaks['n'] = sorted(L)

#    # east
    L = []
    c = col
    r = row
    for c in range(col+1,board.length):
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
    else:
        L = [] # streak not terminated with color piece
    streaks['e'] = sorted(L)
 
#    # south
    L = []
    c = col
    r = row
    for r in range(row+1,board.length):
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
    else:
        L = [] # streak not terminated with color piece
    streaks['s'] = sorted(L)

#    # west
    L = []
    c = col
    r = row
    for c in range(col-1,-1,-1):
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
    else:
        L = [] # streak not terminated with color piece
    streaks['w'] = sorted(L)

#    # northeast
    L = []
    c = col
    r = row
    c = col+1
    for r in range(row-1,-1,-1):
        if c == board.length:
            L = []  # terminated without finding color
            break
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
        c += 1
    else:
        L = [] # streak not terminated with color piece
    streaks['ne'] = sorted(L)
        
#    # southeast
    L = []
    c = col
    r = row
    c = col+1
    for r in range(row+1,board.length):
        if c == board.length:
            L = []  # terminated without finding color
            break
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
        c += 1
    else:
        L = [] # streak not terminated with color piece
    streaks['se'] = sorted(L)
                
#    # southwest
    L = []
    c = col
    r = row
    c = col - 1
    for r in range(row+1,board.length):
        if c == -1:
            L = []  # terminated without finding color
            break
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
        c = c - 1
    else:
        L = [] # streak not terminated with color piece
    streaks['sw'] = sorted(L)
    
#    # northwest
    L = []
    c = col
    r = row
    c = col - 1
    for r in range(row-1,-1,-1):
        if c == -1:
            L = []  # terminated without finding color
            break
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
        c = c - 1
    else:
        L = [] # streak not terminated with color piece
    streaks['nw'] = sorted(L)
            
    return streaks
            
def get_all_capturing_cells(board, piece):
    '''Returns list of all capturing streaks found from all empty positions on the board in a dictionary
        Key is the (row,col) position and values are the capturing streaks.'''
    D = {}
    for row in range(board.length):
        for col in range(board.length):
            check = board.get(row,col)
            if check != None:
                continue
            spot,value_list = (row,col), []
            streaks = get_all_streaks(board,row,col,piece)
            for value in streaks.values():
                value_list.extend(sorted(value))
            if len(value_list) > 0:
                D[spot] = sorted(value_list)
    return(D)

def get_hint(board,piece):
    '''Gets the streaks for each empty spot on the board. Sorts list of positions with respect to the 
        total length of the capturing streak and returns it.'''
    sort_list,hint = [],[]
    D = get_all_capturing_cells(board,piece)
    for key,values in D.items():
        info = (len(values)),(deindexify(key[0],key[1]))
        sort_list.append(info)
    b = sorted(sort_list,key=operator.itemgetter(0,1),reverse=True)
    for value in b:
        hint.append(value[1])
    return(hint)

def place_and_flip(board,row,col,piece):
    '''Gets all the capturing streaks from a position row,col then places a piece to that position row,col
        and flips all the pieces along the streak. ValueErrors are thrown if spot is occupied, invalid or 
        not on the board.'''
    invalid = "Can't place {:s} at '{:s}', invalid position. Type 'hint' to get suggestions."
    occupied = "Can't place {:s} at '{:s}', already occupied. Type 'hint' to get suggestions."
    not_capture = "Can't place {:s} at '{:s}', it's not a capture. Type 'hint' to get suggestions."
    streak = []
    streaks = get_all_streaks(board,row,col,piece)
    if row >= board.length and col >= board.length:
        raise ValueError (invalid.format(piece.color()[0].upper(),deindexify(row,col)))
        
    if board.is_free(row,col) != True:
        raise ValueError (occupied.format(piece.color()[0].upper(),deindexify(row,col)))
        
    for key, value in streaks.items():
        streak.extend(value)
    length = len(streak)
    if length == 0:
        raise ValueError (not_capture.format(piece.color()[0].upper(),deindexify(row,col)))
        
    board.place(row,col,piece)
    for row,col in streak:
        board.place(row,col,piece)

def is_game_finished(board):
    '''Checks to see if board is full or if there are no remaining moves left for both colors.'''
    if board.is_full == True:
        return(True)
    white = get_all_capturing_cells(board,reversi.Piece('white'))
    black = get_all_capturing_cells(board,reversi.Piece('black'))
    if len(white) == 0 and len(black) == 0 :
        return(True)
    else:
        return(False)

def get_winner(board):
    '''Gets current winner by comparing number of pieces on the board.'''
    count = count_pieces(board)
    black,white = count[0],count[1]
    if black > white:
        winner = 'black'
    if black < white:
        winner = 'white'
    else:
        winner = 'draw'
    return(winner)
    
def choose_color():
    '''Asks for user input, loops until a valid color (black/white) is entered. Assigns player color respectively.'''
    colors = ("black","white")
    color = input("Pick a color: ")
    while True:
        my_color = color
        if my_color == 'black':
            opponent_color = 'white'
            break
        if my_color == 'white':
            opponent_color = 'black'
            break
        if my_color not in colors:
            print("Wrong color, type only 'black' or 'white', try again.")
            color = input("Enter a color: ")
            
    print("You are '{:s}' and your opponent is '{:s}'.".format(my_color,opponent_color))
    return(my_color,opponent_color)

def game_play_human():
    '''GIVEN. Calls all functions and conducts the game of Reversi.'''
    """
    This is the main mechanism of the human vs. human game play.
    """
    
    banner = """
     _____                         _ 
    |  __ \                       (_)
    | |__) |_____   _____ _ __ ___ _ 
    |  _  // _ \ \ / / _ \ '__/ __| |
    | | \ \  __/\ V /  __/ |  \__ \ |
    |_|  \_\___| \_/ \___|_|  |___/_|
    
    Developed by The Students Inc.
    CSE231 Spring Semester 2018
    Michigan State University
    East Lansing, MI 48824, USA.
    """

    prompt = "[{:s}'s turn] :> "
    print(banner)
   
    # Choose the color here
    (my_color, opponent_color) = choose_color()
    
    # Take a board of size 8x8
    # Prompt for board size
    size = input("Input a board size: ")
    board = reversi.Board(int(size))
    initialize(board)
    
    # Decide on whose turn, use a variable called 'turn'.
    turn = my_color if my_color == 'white' else opponent_color
    
    # loop until the game is finished
    while not is_game_finished(board):
        try:
            # Count the pieces and assign into piece_count
            piece_count = count_pieces(board)
            
            print("Current board:")
            board.display(piece_count)    
            
            # Get a piece according to turn
            piece = reversi.Piece(turn)

            # Get the command from user using input
            command = input(prompt.format(turn)).lower()
            
            # Now decide on different commands
            if command == 'exit':
                break
            elif command == 'hint':
                print("\tHint: " + ", ".join(get_hint(board, piece)))
            elif command == 'pass':
                hint = get_hint(board, piece)
                if len(hint) == 0:
                    turn = my_color if turn == opponent_color \
                                        else opponent_color
                    print("\tHanded over to \'{:s}\'.".format(turn))
                else:
                    print("\tCan't hand over to opponent, you have moves," + \
                          " type \'hint\'.")
            else:
                    (row, col) = indexify(command)
                    place_and_flip(board, row, col, piece)
                    print("\t{:s} played {:s}.".format(turn, command))
                    turn = my_color if turn == opponent_color \
                                        else opponent_color
        except Exception as err:
            print("Error:", err)
    
    # The loop is over.
    piece_count = count_pieces(board)
    print("Current board:")
    board.display(piece_count)    
    winner = get_winner(board)
    if winner != 'draw':
        diff = abs(piece_count[0] - piece_count[1])
        print("\'{:s}\' wins by {:d}! yay!!".format(winner, diff))
    else:
        print("This game ends in a draw.")
    # --- end of game play ---

def figure_1(board):
    """
    You can use this function to test your program
    """
    board.place(0,0,reversi.Piece('black'))
    board.place(0,3,reversi.Piece('black'))
    board.place(0,4,reversi.Piece('white'))
    board.place(0,5,reversi.Piece('white'))
    board.place(0,6,reversi.Piece('white'))
    board.place(1,1,reversi.Piece('white'))
    board.place(1,3,reversi.Piece('white'))
    board.place(1,5,reversi.Piece('white'))
    board.place(1,6,reversi.Piece('white'))
    board.place(1,7,reversi.Piece('white'))
    board.place(2,2,reversi.Piece('white'))
    board.place(2,3,reversi.Piece('black'))
    board.place(2,4,reversi.Piece('white'))
    board.place(2,5,reversi.Piece('white'))
    board.place(2,7,reversi.Piece('white'))
    board.place(3,0,reversi.Piece('black'))
    board.place(3,1,reversi.Piece('white'))
    board.place(3,2,reversi.Piece('white'))
    board.place(3,4,reversi.Piece('white'))
    board.place(3,5,reversi.Piece('white'))
    board.place(3,6,reversi.Piece('black'))
    board.place(3,7,reversi.Piece('black'))
    board.place(4,0,reversi.Piece('white'))
    board.place(4,2,reversi.Piece('white'))
    board.place(4,4,reversi.Piece('white'))
    board.place(5,0,reversi.Piece('black'))
    board.place(5,2,reversi.Piece('black'))
    board.place(5,3,reversi.Piece('white'))
    board.place(5,5,reversi.Piece('black'))
    board.place(6,0,reversi.Piece('black'))
    board.place(6,1,reversi.Piece('black'))
    board.place(6,3,reversi.Piece('white'))
    board.place(6,6,reversi.Piece('white'))
    board.place(7,1,reversi.Piece('black'))
    board.place(7,2,reversi.Piece('white'))
    board.place(7,3,reversi.Piece('black'))
    board.place(7,7,reversi.Piece('black'))
    
if __name__ == "__main__":
    game_play_human()
    
        
        
        
        


  