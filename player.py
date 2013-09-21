#this is the module file that implements the class CPlayer

import random						#used to roll dice
import sys
import socket

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
	SOCKsocket = None
	SOCKaddress= None
	SOCKbuffer = ""
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
	def __init__(self, Env):				#establish connection
		Env.Verbose(3,"Listening for player connection...")
		(self.socket, self.address) = Env.ServerSocket.accept()
		buffer=self.socket.recv(32)			#get the player name
		if buffer != "PERUDO?\n":			#If they don't want to play perudo, tell us and kill them
			Env.Verbose(1,"Warning!  Unknown application rejected.")
			Env.Verbose(1,"Message: %s.",buffer)
			self.B_Dead=1
			self.I_HandSize=0
			self.Str_Name="ghost"
			self.socket.close()
		else:
			self.socket.send("PERUDO!\n")
			self.Str_Name=self.socket.recv(32)		#get the player name
		pass
	
	def SendCup(self, Env):
		Str_Cup = "DICE: "
		for I_Die in self.LI_Hand:
			Str_Cup = Str_Cup + " %d"%I_Die
		Str_Cup = Str_Cup + "\n"
		try:
			self.socket.send(Str_Cup)
		except socket.error:
			Env.Verbose(1, "Warning!  Could not send cup to %s", self.Str_Name)
		
	def GetCodeWord(self, Env, Str_CodeWord):
		try:								#safely receive data
			self.SOCKbuffer = self.SOCKbuffer +  self.socket.recv(64)
			for NextChunk in self.SOCKbuffer.split("\n"):			#process the buffer, looking for bids
				if NextChunk == None or not (Str_CodeWord in NextChunk):				#if there are no words continue
					continue
				else:
					return NextChunk
		except socket.error:
			Env.Verbose(1,"ERROR: Connection to %s appears closed!.", self.Str_Name)
			return None						#return nothing
		return None							#if we find nothing, return nothing
	
	def GetBid(self,Env):
		self.socket.send("BID?\n")					#Invite the player to bid
		Str_rawBid = self.GetCodeWord(Env, "BID:")			#recieve and search buffer for bid

		try:
			LStr_rawBidWords = Str_rawBid.split()			#Split into words
			NewBid = [int(LStr_rawBidWords[1]),int(LStr_rawBidWords[2])]	#Cast to bid format
			return NewBid				#return the bid
		except (ValueError, AttributeError):				#If Str_rawBid == None or can't cast
			Env.Verbose(1,"ERROR: Malformed bid from %s!  Returning illegal bid.", self.Str_Name)
			return [0,0]				#return an illegal bid
		
	def GetSpotOn(self,Env):
		self.socket.send("SPOT?\n")					#Invite the player to bid
		Str_rawSpot = self.GetCodeWord(Env, "SPOT:")			#recieve and search buffer for bid

		try:
			LStr_rawSpotWords = Str_rawSpot.split()			#Split into words
			NewSpot = int(LStr_rawSpotWords[1])			#Cast to bid format
			return NewSpot						#return the bid
		except (ValueError, AttributeError):				#If Str_rawBid == None or can't cast
			Env.Verbose(1,"ERROR: Malformed spot on from %s!  Returning error.", self.Str_Name)
			return -1				#return an error

	def GetDoubt(self,Env):
		self.socket.send("DOUBT?\n")					#Invite the player to doubt
		Str_rawDoubt = self.GetCodeWord(Env, "DOUBT:")			#recieve and search buffer for doubt
		try:
			LStr_rawDoubtWords = Str_rawDoubt.split()			#Split into words
			Doubt = int(LStr_rawDoubtWords[1])				#Cast to doubt format
			if Doubt == 0 or Doubt == 1:					#Check it's a valid doubt
				return Doubt							#return the doubt
			else:
				raise(ValueError)					#or raise an error code
		except (ValueError, AttributeError):				#If Str_rawDoubt == None or can't cast
			Env.Verbose(1,"ERROR: Malformed doubt from %s!  Returning illegal doubt.", self.Str_Name)
			return -1				#return an illegal bid
	
	def getSpot(self,Env):
		self.socket.send("SPOT?\n")
		Str_rawSpot = self.getCodeWord(Env, "SPOT:")
		try:
			LStr_rawSpotWords = Str_rawSpot.split()				#Split into words
			Spot = int(LStr_rawSpotWords[1])				#Cast to doubt format
			if Spot == 0 or Spot == 1:					#Check it's a valid doubt
				return Spot							#return the doubt
			else:
				raise(ValueError)					#or raise an error code
		except (ValueError, AttributeError):				#If Str_rawDoubt == None or can't cast
			Env.Verbose(1,"ERROR: Malformed \"spot on\" from %s!  Returning illegal spot on.", self.Str_Name)
			return -1				#return an illegal bid
