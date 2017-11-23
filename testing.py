from tash_kalar_mechanics import *
from cards import *
import copy
import agents

tk = TashKalarGame(verbose=2)

tk.placePiece(util.BLUE_PLAYER,util.COMMON,4,4)
tk.placePiece(util.BLUE_PLAYER,util.COMMON,3,5)
tk.placePiece(util.BLUE_PLAYER,util.HEROIC,4,6)
tk.placePiece(util.BLUE_PLAYER,util.COMMON,6,5)
tk.placePiece(util.BLUE_PLAYER,util.COMMON,6,3)
tk.placePiece(util.BLUE_PLAYER,util.COMMON,5,8)
tk.placePiece(util.BLUE_PLAYER,util.HEROIC,3,8)
tk.placePiece(util.BLUE_PLAYER,util.HEROIC,1,4)

tk.placePiece(util.RED_PLAYER,util.COMMON,4,3)
tk.placePiece(util.RED_PLAYER,util.COMMON,5,4)
tk.placePiece(util.RED_PLAYER,util.HEROIC,5,5)
tk.placePiece(util.RED_PLAYER,util.HEROIC,5,6)
tk.placePiece(util.RED_PLAYER,util.HEROIC,7,1)
tk.placePiece(util.RED_PLAYER,util.COMMON,7,1)
tk.placePiece(util.RED_PLAYER,util.COMMON,3,7)
tk.placePiece(util.RED_PLAYER,util.COMMON,5,7)

tk.placePiece(util.RED_PLAYER,util.HEROIC,7,2)
tk.removePiece(7,2)

#tk.blue_player_hand = [1,6,10]
tk.printBoard()
tk.printGameDetails()
tk.getActions()

blue = agents.HumanAgent(util.BLUE_PLAYER)
action = blue.nextAction(tk)
tk.executeAction(tk)

tk.printBoard()
tk.printGameDetails()
print("done")

# prints a single formation
def printFormation(formation,vector):
    temp_game = TashKalarGame()
    #clear the board
    temp_game.removePiece(2,4)
    temp_game.removePiece(6,4)
    for p in range(len(formation)):
        position = formation[p] # should be a tuple
        x = position[0]+4
        y = position[1]+4
        if p == len(formation)-1:
            temp_game.placePiece(util.BLUE_PLAYER,util.HEROIC,x,y)
        else:
            temp_game.placePiece(util.BLUE_PLAYER,util.COMMON,x,y)
    temp_game.printBoard()
    print ("Vector: " + vector)

# debugging tool to print out all the permutations of a card's formation
# pieces used to summon are 'C', summoned being is 'H'
# all formations are with the datum centered at (4,4)
def printAllFormations(card):

    formations,vectors = card.allFormations()
    #vectors = card.allFormations()[1]
    print (formations)

    for i in range(len(formations)):
        printFormation(formations[i],vectors[i])



for i in range(1,19):
    card = ImperialSummoningCard(i)
    #card.printDetails()
    #printFormation(card.formation,card.vector)
    #printAllFormations(card)

    locations = card.getPossibleLocations(util.BLUE_PLAYER,tk.blue_player_pieces,tk.board)
    #locations = card.getPossibleLocations(util.RED_PLAYER,tk.red_player_pieces,tk.board)
    #print "all locations: ",locations

