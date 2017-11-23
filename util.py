# util.py includes constants and functions used by both the tash_kalar_mechanics.py file
# and cards.py

# EMPTY indicates no player/no rank on the game board
EMPTY = 0

BLUE_PLAYER = 1
RED_PLAYER = -1

COMMON = 1
HEROIC = 2
MAX_PIECES = 17

BOARD_SIZE = 9

NUM_CARDS = 18
HAND_SIZE = 3

# number of points to trigger the last turns
# 17 is given in the rules, may be changed to accommodate incomplete simulation
ENDGAME_TRIGGER = 17

# ordering matters - proceeds clockwise
CARDINAL_DIRECTIONS = ["N","NE","E","SE","S","SW","W","NW"]


# helper function to check if a coordinate pair lies in one of the four
# corners of the board
def isInCorner(x,y):
    bottom_left = x+y <= 1
    top_right = x+y >= (BOARD_SIZE-1)*2 - 1
    top_left = x <= 1 and y-x >= BOARD_SIZE-2
    bottom_right = x >= BOARD_SIZE-2 and x-y >= BOARD_SIZE-2
    return bottom_left or top_right or top_left or bottom_right

# checks if a particular (x,y) pair is out of bounds
def validCoordinates(x,y):
    if x >= BOARD_SIZE or x < 0: return False
    if y >= BOARD_SIZE or y < 0: return False
    if isInCorner(x,y): return False
    return True

# returns coordinates of an adjacent square based on a direction vector
def getAdjacent(x,y,direction):
    if direction == 'N':
        return (x,y+1)
    elif direction == 'NE':
        return (x+1,y+1)
    elif direction == 'E':
        return (x+1,y)
    elif direction == 'SE':
        return (x+1,y-1)
    elif direction == 'S':
        return (x,y-1)
    elif direction == 'SW':
        return (x-1,y-1)
    elif direction == 'W':
        return (x-1,y)
    elif direction == 'NW':
        return (x-1,y+1)
    elif direction == '':
        return (x,y)

# takes in any one of the cardinal directions 90 degrees (e.g. 'N', or 'SE')
# and returns the next direction clockwise
#   - e.g. 'N' -> 'E'; 'SE' -> 'SW'
def rotateDirectionCW(direction):
    if direction == '': return direction
    # index from 0 to 7
    index = CARDINAL_DIRECTIONS.index(direction)
    new_index = (index + 2) % len(CARDINAL_DIRECTIONS)
    return CARDINAL_DIRECTIONS[new_index]

# returns the cardinal direction 180 degrees from the given direction
def rotateDirection180(direction):
    if direction == '': return direction
    # index from 0 to 7
    index = CARDINAL_DIRECTIONS.index(direction)
    new_index = (index + 4) % len(CARDINAL_DIRECTIONS)
    return CARDINAL_DIRECTIONS[new_index]

# takes in any one of the cardinal directions (e.g. 'N', or 'SE')
# anbd returns the direction mirrored about the north-south vertial axis
#   - e.g. 'N' -> 'N'; 'SE' -> 'SW'
def mirrorDirection(direction):
    if direction == 'N' or direction == 'S' or direction == '':
        return direction
    elif direction == 'E':
        return 'W'
    elif direction == 'W':
        return 'E'
    elif direction == 'NW':
        return 'NE'
    elif direction == 'NE':
        return 'NW'
    elif direction == 'SW':
        return 'SE'
    elif direction == 'SE':
        return 'SW'

# returns the player string associated with a player number
def playerString(player):
    if player == BLUE_PLAYER: return 'Blue Player'
    elif player == RED_PLAYER: return 'Red Player'
    else: return ""

# breaks a tie based on number of upgraded pieces, then total pieces
# otherwise returns tie indicator EMPTY
def tieBreaker(tk):
    red_upgraded_pieces = 0
    blue_upgraded_pieces = 0
    for (x,y,rank) in tk.red_player_pieces:
        if rank > COMMON: red_upgraded_pieces += 1
    for (x,y,rank) in tk.blue_player_pieces:
        if rank > COMMON: blue_upgraded_pieces += 1
    if blue_upgraded_pieces > red_upgraded_pieces: return BLUE_PLAYER
    elif blue_upgraded_pieces < red_upgraded_pieces: return RED_PLAYER

    if len(tk.blue_player_pieces) > len(tk.red_player_pieces): return BLUE_PLAYER
    elif len(tk.blue_player_pieces) < len(tk.red_player_pieces): return RED_PLAYER
    else: return EMPTY

# determines the winner at the end of the game, and prints some messages
# returns the winner, which is the utility of the game (1, 0, or -1)
def declareWinner(tk):
    winner = EMPTY
    if tk.blue_player_score > tk.red_player_score: winner = BLUE_PLAYER
    elif tk.blue_player_score < tk.red_player_score: winner = RED_PLAYER
    else: winner = tieBreaker(tk)
    if tk.verbose > 0:
        print("")
        if winner == EMPTY:
            print("It's a tie!")
        else:
            print("%s wins!" % playerString(winner))
        print("Final score:")
        print("%s: %d        %s: %d" % (playerString(BLUE_PLAYER),tk.blue_player_score, \
            playerString(RED_PLAYER),tk.red_player_score))
    return winner
