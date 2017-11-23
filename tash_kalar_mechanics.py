import random
import cards
import util

# Tash Kalar

class TashKalarGame:
    '''
    This class tracks the general state of the game
        - who is playing
        - which pieces are on the board where
        - which cards are remaining in which decks
        - whose turn it is
        - each player's hand
        - each player's remaining deck
        - number of remaining actions
        - number enemy pieces destroyed this turn?

    Levels of verbosity:
        - verbose = 0 (Default): no greeting, no win details, details give only what is public information that both players can see
        - verbose = 1: includes greeting, details give only what the current player can see
        - verbose = 2: all details
    '''

    def __init__(self,verbose=0):
        # Players: 1 and -1
        self.current_player = util.BLUE_PLAYER
        self.verbose = verbose

        # Turns played
        self.turns_played = 0
        self.remaining_game_actions = 1  # first player gets one action, every other turn starts at 2

        # two variables to track when the end of the game occurs
        self.end_triggered = False
        self.last_player = util.EMPTY

        # the number of enemey (current_player*(-1)) pieces destroyed this turn
        # in list form: (numCommon, numHeroic)
        self.pieces_destroyed = [0,0]


        # player scores
        self.blue_player_score = 0
        self.red_player_score = 0

        # player starting decks (18 cards, card IDs from 1-18)
        self.blue_player_deck = range(1,util.NUM_CARDS+1)
        self.red_player_deck = range(1,util.NUM_CARDS+1)

        # limited decks for testing
        self.blue_player_deck = [1,4,6,7,10,11,18]
        self.red_player_deck = [1,4,6,7,10,11,18]
        self.blue_player_deck = [1,4,6]
        
        random.seed(40)
        random.shuffle(self.blue_player_deck)
        random.shuffle(self.red_player_deck)

        # pull three cards per player
        # make this a set?
        self.blue_player_hand = []
        self.red_player_hand = []
        for i in range(util.HAND_SIZE):
            self.drawCard(util.BLUE_PLAYER)
            self.drawCard(util.RED_PLAYER)

        # store lists of each players' pieces
        # elements of the list take the form: (x,y,rank)
        #   - x and y are the cartesian coordinates of the piece, rank is the rank
        # see self.board for more details
        self.blue_player_pieces = []
        self.red_player_pieces = []     # make these sets?

        # list of actions for any state of the game
        self.actions = []

        # a list of all squares without any pieces, each element is an (x,y) tuple
        self.empty_squares = []

        # the game board as a list of lists
        # x and y cartesian coordinates range from 0 - 8, inclusive
        #   - conceptually, [0,0] is the bottom left
        # three squares in each corner are excluded
        #   e.g. [0,0],[0,1],[1,0] are not valid in the bottom left
        #   these squares have type None in the matrix

        # entries in the matrix can be obtained by self.board[x][y] = (player,piece_rank)
        #   - player = -1,0,1, depending on which player has a piece there (0 if no piece)
        #   - rank = 0,1,2 for no piece, common piece, heroic piece respectively

        # each player starts with one common piece at either [2,4] or [6,4]
        self.board = self.initBoard()
        self.getActions()
        if self.verbose >= 1: self.printGreeting()

    def getPlayerScore(self,player):
        assert player == util.BLUE_PLAYER or player == util.RED_PLAYER, "invalid player number"
        if player == util.BLUE_PLAYER: return self.blue_player_score
        else: return self.red_player_score

    def setPlayerScore(self,player,score):
        assert player == util.BLUE_PLAYER or player == util.RED_PLAYER, "invalid player number"
        if player == util.BLUE_PLAYER: self.blue_player_score = score
        else: self.red_player_score = score

    def getPlayerDeck(self,player):
        assert player == util.BLUE_PLAYER or player == util.RED_PLAYER, "invalid player number"
        if player == util.BLUE_PLAYER: return self.blue_player_deck
        else: return self.red_player_deck

    def getPlayerHand(self,player):
        assert player == util.BLUE_PLAYER or player == util.RED_PLAYER, "invalid player number"
        if player == util.BLUE_PLAYER: return self.blue_player_hand
        else: return self.red_player_hand

    def getPlayerPieces(self,player):
        assert player == util.BLUE_PLAYER or player == util.RED_PLAYER, "invalid player number"
        if player == util.BLUE_PLAYER: return self.blue_player_pieces
        else: return self.red_player_pieces

    # the game ends after each player has taken one final turn after the end has been triggered
    # the end is triggered after either 
    def isEnd(self):
        if self.end_triggered and self.last_player == self.current_player and self.remaining_game_actions == 0:
            return True
        else:
            return False


    # # gets the (player,piece_rank) tuple at the position (x,y) on the board
    # # returns None if the coordinates are out of bounds/in the corners
    # def getBoardSquare(self,x,y):
    #   if x >= util.BOARD_SIZE or x < 0: return None
    #   if y >= util.BOARD_SIZE or y < 0: return None
    #   if util.isInCorner(x,y): return None
    #   return self.board[x][y]

    # creates the board size, excludes corners
    # sets up the starting position of pieces on the game board
    def initBoard(self):
        result = []
        for x in range(util.BOARD_SIZE):
            result.append([])
            for y in range(util.BOARD_SIZE):
                if util.isInCorner(x,y):
                    result[x].append(None)
                elif x==2 and y==4:
                    result[x].append((util.BLUE_PLAYER,util.COMMON))
                    self.blue_player_pieces.append((x,y,util.COMMON))
                elif x==6 and y==4:
                    result[x].append((util.RED_PLAYER,util.COMMON))
                    self.red_player_pieces.append((x,y,util.COMMON))
                else:
                    result[x].append((util.EMPTY,util.EMPTY))
                    self.empty_squares.append((x,y))
        return result

    # given the state of the game (class), return a list of all the possible actions
    # and updates the storage variable self.actions
    # three categories of action:
    #   - place
    #   - summon
    #   - flare (not implemented yet)
    def getActions(self):
        result = []
        # Place actions: ('Place',(x,y))
        for position in self.empty_squares:
            result.append( ('Place',(position[0],position[1])) )

        # Summon actions: ('Summon',ID,(x,y),...)
        # NOTE: ... arguments dependent on card ID
        current_player_hand = self.getPlayerHand(self.current_player)
        current_player_pieces = self.getPlayerPieces(self.current_player)
        for card_ID in current_player_hand:
            card = cards.ImperialSummoningCard(card_ID)
            result += card.getSummonActions(self.current_player,current_player_pieces,self.board)

        # Flare actions: ('Flare',ID,...)
        # NOTE: ... arguments dependend on flare ID
        # TO DO
        self.actions = result
        return result


    # execute action
    #   - tallies destroyed pieces & adds to score, if last action of a turn
    #   - updates actions remaining
    #   - changes current player, if necessary
    #   - replenishes player's hand, if necessary
    #   - alters the game board according to the "action" argument
    def executeAction(self,action):
        assert action in self.actions, "This shouldn't happen... trying to execute an invalid action"
        assert self.remaining_game_actions > 0, "should always have game actions to play"
        current_player_hand = self.getPlayerHand(self.current_player)

        if action[0] == 'Place':
            (x,y) = action[1]
            assert self.board[x][y][0] == util.EMPTY, "not placing on an empty square"
            self.placePiece(self.current_player,util.COMMON,x,y)
            self.remaining_game_actions -= 1
        elif action[0] == 'Summon':
            card = cards.ImperialSummoningCard(action[1])
            (x,y,vector) = action[2]
            # points for summoning onto an enemy
            if self.board[x][y][0] == -1*self.current_player:
                if self.board[x][y][1] == util.COMMON: self.pieces_destroyed[0] += 1
                else: self.pieces_destroyed[1] += 1
            self.placePiece(self.current_player,card.rank,x,y)
            # do card-specific follow-up actions
            if not card.executeSummonAction(action,self): print("summoning failed (check cards.py)")

            # discard summoned card
            current_player_hand.remove(action[1])
            self.remaining_game_actions -= 1
        elif action[0] == 'Flare':
            print("Not implemented yet")
        
        last_turn = self.end_triggered and self.last_player == self.current_player
        if self.remaining_game_actions == 0 and not last_turn:
            self.turns_played += 1
            # turnover
            # replenish hand
            current_player_deck = self.getPlayerDeck(self.current_player)
            while len(current_player_hand) < util.HAND_SIZE:
                if len(current_player_deck) == 0 and not self.end_triggered:
                    self.end_triggered = True
                    self.last_player = self.current_player
                    if self.verbose > 0: print("end of the game triggered")
                if not self.drawCard(self.current_player):
                    break
            # tally destroyed pieces, add to score
            current_player_score = self.getPlayerScore(self.current_player)
            current_player_score += int(self.pieces_destroyed[0]/2 + self.pieces_destroyed[1])
            if current_player_score > util.ENDGAME_TRIGGER:
                self.end_triggered = True
                self.last_player = self.current_player
                print("end of the game triggered")
            self.setPlayerScore(self.current_player,current_player_score)
            self.current_player *= -1
            self.remaining_game_actions = 2
            self.pieces_destroyed = [0,0]

        # update actions
        self.getActions()

    # removes a Card from the player's deck and adds it to their hand
    # returns True if successful, otherwise False if the deck is empty
    def drawCard(self,player):
        #assert player == util.BLUE_PLAYER or player == util.RED_PLAYER, "drawCard: not a valid player number"
        current_player_hand = self.getPlayerHand(player)
        current_player_deck = self.getPlayerDeck(player)
        if len(current_player_deck) == 0: return False
        current_player_hand.append(current_player_deck.pop())
        return True

    # places a player's piece of a particular rank in a particular position.
    # checks only for whether the piece is of a valid rank and is within the legal
    # board limits.
    #   - doesn't check for valid places based on the rules of a card
    #   - if a piece is played beyond the maximum allowed limit, no piece is added (sim rules only)
    def placePiece(self,player,rank,x,y):
        assert util.validCoordinates(x,y), "placePiece: position is out of bounds"
        assert rank == util.COMMON or rank == util.HEROIC, "invalid rank"

        current_player_pieces = self.getPlayerPieces(player)
        if len(current_player_pieces) >= util.MAX_PIECES:
            print("not enough pieces")
            return

        # clear whatever piece may already be on that square
        self.removePiece(x,y)

        current_player_pieces.append((x,y,rank))


        self.board[x][y] = (player,rank)
        if (x,y) in self.empty_squares: self.empty_squares.remove((x,y))

    # removes any piece at a specified position
    # does nothing if called on an empty space
    def removePiece(self,x,y):
        assert util.validCoordinates(x,y), "removePiece: position is out of bounds"

        player = self.board[x][y][0]
        rank = self.board[x][y][1]
        if player == util.EMPTY:
            return
        current_player_pieces = self.getPlayerPieces(player)
        current_player_pieces.remove((x,y,rank))
        
        self.board[x][y] = (util.EMPTY,util.EMPTY)
        if (x,y) not in self.empty_squares: self.empty_squares.append((x,y))

    # prints some graphical representation of the game board
    # defaults to all pieces, can print selectively blue or red pieces only
    #   - blue common: "C"
    #   - blue heroic: "H"
    #   - red common: "c"
    #   - red heroic: "h"
    #   - invalid corner squares: "X"
    def printBoard(self):
        hline = "  " + "-"*(4*util.BOARD_SIZE+1)
        print ("")
        print ("y")
        print (hline)
        for y in range(util.BOARD_SIZE-1,-1,-1):
            row = "%s |" % y
            for x in range(util.BOARD_SIZE):
                square = self.board[x][y]
                add_on = ""
                if util.isInCorner(x,y):
                    row += " X |"
                    continue
                if square[0] == util.EMPTY:
                    add_on = "   |"
                elif square[0] == util.BLUE_PLAYER:
                    if square[1] == util.COMMON: add_on = " C |"
                    elif square[1] == util.HEROIC: add_on = " H |"
                elif square[0] == util.RED_PLAYER:
                    if square[1] == util.COMMON: add_on = " c |"
                    elif square[1] == util.HEROIC: add_on = " h |"
                row += add_on
            print (row)
            print (hline)
        x_axis = "   "
        for x in range(util.BOARD_SIZE):
            x_axis += " %s  " % x
        x_axis += " x"
        print (x_axis)
        print ("")

    # print player decks, pieces, hands, pieces remaining, scores, current player, number of turns
    def printGameDetails(self):
        print ("")
        player_str = util.playerString(self.current_player)
        print ("After %s turns, it is the %s's turn with %d game action(s) remaining." % (self.turns_played,player_str,self.remaining_game_actions))
        print ("Pieces destroyed (common,heroic): %s" % self.pieces_destroyed)
        print ("")
        print ("Blue Player Info:")
        if self.verbose >= 1: print ("Cards in hand: ",self.blue_player_hand)
        if self.verbose >= 2: print ("Cards remaining in deck: ",self.blue_player_deck)
        print ("%d pieces remaining" % (util.MAX_PIECES - len(self.blue_player_pieces)))
        print ("Pieces on the board: ",self.blue_player_pieces)
        print ("Score: ",self.blue_player_score)
        print ("")
        print ("Red Player Info:")
        if self.verbose >= 1: print ("Cards in hand: ",self.red_player_hand)
        if self.verbose >= 2: print ("Cards remaining in deck: ",self.red_player_deck)
        print ("%d pieces remaining" % (util.MAX_PIECES - len(self.red_player_pieces)))
        print ("Pieces on the board: ",self.red_player_pieces)
        print ("Score: ",self.red_player_score)

        print ("")

    # greet the player, explain some stuff about the game/simulator
    def printGreeting(self):
        print ("")
        print ("Welcome to Tash Kalar!")
        print ("In this simulator, blue pieces are represented as uppercase 'C' and 'H' for common and heroic pieces,")
        print ("and red pieces are represented as lowercase 'c' and 'h'.")
        print ("")
