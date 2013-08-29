import player
import random


class GameState:		#This keeps track of the players, the person that will start the next round and e.g. whether the next round is an ``obliged'' round
				
				#start list of variables
	Players = []
	I_PlayersLeft = None		#The players still in the game
	B_ObligedRoundNext = None	#Is the next round an obliged round?
	
				#end list of variables

	def __init__(self,Env):
		Env.Verbose(3,"Initialising players")
		for i in xrange(Env.I_NumberOfPlayers):				#Initialise the list of players
			self.Players = self.Players + [player.CPlayer()]
		self.I_PlayersLeft = Env.I_NumberOfPlayers			#copy across the number of players

		for CurrentPlayer in self.Players:
			CurrentPlayer.setup()					#connect to sockets and get names
		

		player.ShufflePlayers(self.Players)				#shuffle the player order after the connections have been established
		
		#START TEST CODE
		self.Players[0].Str_Name="Alice"
		self.Players[1].Str_Name="Bob"
		self.Players[2].Str_Name="Charlie"
		self.Players[3].Str_Name="Denise"
		#END TEST CODE

		StartFirst=random.randint(0,self.I_PlayersLeft-1)		#choose a random starting player for the first round
		self.Players[StartFirst].B_StartNext=1
		Env.Verbose(1,"%s has won the roll to go first.",self.Players[StartFirst].Str_Name)

										#the first round cannot be an ``obliged'' round
