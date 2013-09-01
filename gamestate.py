import player
import random
import socket


class GameState:		#This keeps track of the players, the person that will start the next round and e.g. whether the next round is an ``obliged'' round
				
				#start list of variables
	Players = []
	I_PlayersLeft = None		#The players still in the game
	B_ObligedRoundNext = 0		#Is the next round an obliged round?  The first round cannot be obliged
	
				#end list of variables

	def __init__(self,Env):
		Env.Verbose(3,"Initialising players")
		for i in xrange(Env.I_NumberOfPlayers):				#Initialise the list of players
			self.Players = self.Players + [player.CPlayer(Env)]	#connect to sockets and get names
		self.I_PlayersLeft = Env.I_NumberOfPlayers			#copy across the number of players

		#TEST CODE BEGINS
		#player.ShufflePlayers(self.Players)				#shuffle the player order after the connections have been established
		

		#StartFirst=random.randint(0,self.I_PlayersLeft-1)		#choose a random starting player for the first round
		StartFirst=0
		#TESTCODE ENDS
		self.Players[StartFirst].B_StartNext=1
		Env.Verbose(1,"%s has won the roll to go first.",self.Players[StartFirst].Str_Name)
	
	def Broadcast(self, Env,rawmsg, *PrintfArguments):			#send a message to all players, even dead ones
		msg = rawmsg % (PrintfArguments)	#Process arguments
		msg = msg + "\n"			#delimit string
		for Player in self.Players:
			try:
				Player.socket.send(msg)	#send to Player
			except socket.error:
				Env.Verbose(1, "Cannot send to %s, no action taken", Player.Str_Name)		#take no action

	def BroadcastDice(self, ActivePlayers):
		for Player in self.Players:
			try:
				for ActivePlayer in ActivePlayers:
					Str_ActivePlayerCup = "AllDice: %s"
					for Die in ActivePlayer.LI_Hand:
						Str_ActivePlayerCup = Str_ActivePlayerCup + " " + str(Die)
					Player.socket.send(Str_ActivePlayerCup)
			except socket.error:
				Env.Verbose(1, "Cannot send to %s, no action taken", Player.Str_Name)		#take no action
				
