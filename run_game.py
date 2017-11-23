import tash_kalar_mechanics
import cards
import util
import agents
import argparse

'''
This script will run an instance of the game of Tash Kalar. Runs on Python 3
Command line arguments:
    num_human_players
        2: p v p
        1: p v ai
        0: ai v ai
'''
parser = argparse.ArgumentParser()
parser.add_argument("-n","--num_human_players",help="2 for p v p, 1 for p v ai, 0 for ai v ai",type=int,default=2)
args = parser.parse_args()

tk = tash_kalar_mechanics.TashKalarGame(verbose=2)

if args.num_human_players == 2:
    blue = agents.HumanAgent(util.BLUE_PLAYER)
    red = agents.HumanAgent(util.RED_PLAYER)
    while True:
        tk.printBoard()
        tk.printGameDetails()
        if tk.isEnd(): break
        current_agent = blue
        if tk.current_player == util.RED_PLAYER: current_agent = red
        action = current_agent.nextAction(tk)
        tk.executeAction(action)
    util.declareWinner(tk)
elif args.num_human_players == 1:
    raise NotImplementedError("No AI yet")
elif args.num_human_players == 0:
    raise NotImplementedError("No AI yet")
else:
    raise Exception("Invalid input 'num_human_players'")

