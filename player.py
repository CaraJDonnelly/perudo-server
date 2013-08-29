#this is the module file that implements the class CPlayer

import random						#used to roll dice

def ShufflePlayers(Players):			#
	Players=random.shuffle(Players)

class CPlayer:						#Begin class definition

							#Begin variable definitions

							#Perudo variables
	Str_Name=None					#Name of the player
	LI_Hand=[]					#The list of the current dice values rolled
	I_HandSize=5					#The number of dice currently owned by the player
	B_Obliging=0					#Has the player previously had an `obliging round'?
	B_Dead=0					#Has the player lost?
	B_StartNext=0					#Will this player start the next round?

							#Socket variables

							#End variable definitions

							
							#Begin function definitions

							#Perudo functions
							
	def RollCup(self):						#Roll a new set of dice: done once every round
		self.LI_Hand=[]						#Clear the old cup
		for DieValue in self.RollDice(self.I_HandSize):		#Roll the new dice, one by one
			self.LI_Hand = self.LI_Hand + [DieValue]	#Add to the cup

	def RollDice(self, IntNumberOfDice):			#The generator function for function RollCup
		for i in xrange(IntNumberOfDice):
			yield random.randint(1,6)		#Roll a single die

	def LoseADie(self):					#Player loses a die, presumably after being incorrect
		I_HandSize-=1;					
	
	def GainADie(self):					#Player gains a die, presumably after calling "spot on"
		I_HandSize+=1;					
							#socket functions
	def setup(self):				#establish connection 
							#get the player name
		pass
	
							#End function definitions


