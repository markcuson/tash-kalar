import util


# an abstract class for a player agent, implemented further as either a human or AI
class Agent:


	# obtain the next action to input to the game simulator
	# takes in an instance of TashKalarGame, tk 
	def nextAction(self,tk): raise NotImplementedError("Override me")




class HumanAgent(Agent):
	# specify blue (1) or red (-1) player
	def __init__(self,player):
		self.player = player

	# if the first user argument is 'Place', this function
	# returns a tuple of the parsed input, or the empty tuple
	# for invalid inputs
	def parse_place(self,raw_in):
		if len(raw_in) < 2:
			print("Not enough arguments")
			return ()
		location_list = raw_in[1].split(',')
		if len(location_list) != 2:
			print("Incorrect number of coordinates - should be 2")
			return ()
		try:
			coordinates = [int(i) for i in location_list]
		except ValueError:
			print("Invalid coordinates")
			return ()
		if not util.validCoordinates(coordinates[0],coordinates[1]):
			print("Coordinates out of bounds")
			return ()
		return (raw_in[0],tuple(coordinates))
		

	# if the first user argument is 'Summon', this function
	# returns a tuple of the parsed input, or the empty tuple
	# for invalid inputs
	# NOTE: card dependent
	def parse_summon(self,raw_in):
		if len(raw_in) < 3:
			print("Not enough arguments")
			return ()
		try:
			card_ID = int(raw_in[1])
		except ValueError:
			print("Please input an integer as a card ID")
			return ()
		if card_ID < 1 or card_ID > util.NUM_CARDS:
			print("Invalid card ID. Please pick a number between 1 and %d" % util.NUM_CARDS)
			return ()
		location_list = raw_in[2].split(',')
		if len(location_list) < 2:
			print("Please enter at least 2 coordinates, separated by commas")
			return ()
		try:
			summon_x = int(location_list[0])
			summon_y = int(location_list[1])
		except ValueError:
			print("Invalid coordinates")
			return()
		vector = ""
		if len(location_list) >= 3: vector = location_list[2]

		prefix = [raw_in[0],card_ID,(summon_x,summon_y,vector)]
		# Card-specific inputs:
		if card_ID == 4 or card_ID == 7:
			# cards with no follow-up actions
			return tuple(prefix)
		elif card_ID == 1 or card_ID == 6 or card_ID == 10 or card_ID == 11 or card_ID == 18:
			# cards with one follow-up action
			if len(raw_in) < 4:
				# assume empty string as follow-up
				return tuple(prefix + [""])
			if raw_in[3] not in util.CARDINAL_DIRECTIONS:
				print("For card ID #%s, you need to input one of the cardinal directions, or nothing after the prefix")
				return ()
			return tuple(prefix + [raw_in[3]])
		else:
			print("That card hasn't been implemented yet")
			return ()

	# returns a user specified action, verified legal as an element of 
	# tk.actions
	def nextAction(self,tk):
		assert self.player == tk.current_player, "It's not your turn"
		player_str = util.playerString(self.player)
		print("%s: please input arguments separated by spaces, and (x,y) coordinates separated by commmas" % player_str)
		print("  e.g. 'Place 2,6' -> ('Place',(2,6))")
		print("  e.g. 'Summon 1 2,5 SE' -> ('Summon',1,(2,5,''),'SE')")
		result = ()
		while result not in tk.actions:
			raw_in = input("Input your action arguments: ").split()
			if len(raw_in) == 0:
				print("Not enough arguments")
				continue
			if raw_in[0] == "Place":
				result = self.parse_place(raw_in)
				if result == ():
					continue
			elif raw_in[0] == "Summon":
				result = self.parse_summon(raw_in)
				if result == ():
					continue
			else:
				print("Invalid action type, please choose 'Place' or 'Summon'")
				continue
			print("Your action: %s" % str(result))
			if result not in tk.actions: print("Illegal action (not in tk.actions)")

		return result



class ComputerAgent(Agent):
	# specify blue or red player
	def __init__(self,player):
		self.player = player

	# returns an action from tk.actions based on some algorithm
	def nextAction(self,tk):
		return ()
		# to do
