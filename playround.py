import ruleset
import doublylinkedloops

def PlayNormalRound(Env,Game):
	Game.Broadcast(Env,"ROUND! 0")	#Tell players we are starting a new normal round
	Env.Verbose(1,"Starting normal round...")
					#begin prepare for the round
	ActivePlayers = [x for x in GenerateActivePlayers(Game)]
	PlayerLoop = doublylinkedloops.Cdoubly_linked_loop()
	
	TotalDice=0				#How many dice are there? DO NOT BROADCAST THIS, it is the responsibility of the player to keep track.
	for Player in ActivePlayers:
		TotalDice += Player.I_HandSize
		Player.RollCup()				#All active players roll their dice
		Player.SendCup(Env)				#the server tells each player what they've rolled
		PlayerLoop.AddNode(Player)			#Create a list of all active players for this round
		if PlayerLoop.tail.data.B_StartNext == 1:	#Is this latest node the starting player?
			BiddingPlayerNode = PlayerLoop.tail
			Player.B_StartNext=0
	
	Str_ActivePlayerBroadcast="PLAYERS:"	#start to generate the broadcast string telling people about who is playing this round
	ActivePlayerNode=BiddingPlayerNode
	while 1:
		Str_ActivePlayerBroadcast = Str_ActivePlayerBroadcast + " " + ActivePlayerNode.data.Str_Name
		if ActivePlayerNode.next == BiddingPlayerNode:
			break
		ActivePlayerNode=ActivePlayerNode.next
	Env.Verbose(2,Str_ActivePlayerBroadcast)
	Str_ActivePlayerBroadcast = Str_ActivePlayerBroadcast + "\n"
	Game.Broadcast(Env,Str_ActivePlayerBroadcast)
	
	Env.Verbose(3, "Total dice: %d. Generating valid bids...", TotalDice)
	ValidNormalBids = [x for x in GenerateValidNormalBids(TotalDice)] # Generate an ordered list of all valid bids for this round

	CurrentBid = [0,0]		#Dummy zeroth bid
					#end prepare for the round
	
					#begin run the round
	while 1:
		Env.Verbose(3,"It is %s's bid.",BiddingPlayerNode.data.Str_Name)
		NewBid = BiddingPlayerNode.data.GetBid(Env)	#Get a bid
		if not ((NewBid in ValidNormalBids) and (ValidNormalBids.index(NewBid) > ValidNormalBids.index(CurrentBid))):			#Check bid is legal
			Game.Broadcast(Env,"CHEAT! %s", BiddingPlayerNode.data.Str_Name)
			Env.Verbose(1,"%s has attempted to cheat by bidding %d %d! They have been removed from the game and the round is over.", BiddingPlayerNode.data.Str_Name, NewBid[0], NewBid[1])
			BiddingPlayerNode.data.B_Dead = 1		#Remove them from the game
			Game.I_PlayersLeft-=1				#Reduce number of players
			BiddingPlayerNode.next.data.B_StartNext = 1;	#Player on their left starts next round
			return						#exit without showing dice
		else:
			Env.Verbose(1,"%s has bid %d %d", BiddingPlayerNode.data.Str_Name, NewBid[0], NewBid[1])
			Game.Broadcast(Env,"BID! %s %d %d", BiddingPlayerNode.data.Str_Name, NewBid[0], NewBid[1])
			CurrentBid=NewBid
						#Check for anyone calling "spot on", except player who must bid next, since they are not allowed to do so
		ActivePlayerNode=BiddingPlayerNode.next.next
		while 1:
			if ActivePlayerNode == BiddingPlayerNode.next:
				break
			else:
				NextSpotOn = ActivePlayerNode.data.GetSpotOn(Env)
				if NextSpotOn == 1:	#does ActivePlayerNode.data want to call spot on? Broadcast this
					Env.Verbose(1,"%s says spot on!", ActivePlayerNode.data.Str_Name)
					if EvalSpotOn(Env,ActivePlayers,CurrentBid) == 0:	#If the "spot on" was correct
						Game.Broadcast(Env,"SPOT! %s %d %d %d", ActivePlayerNode.data.Str_Name, CurrentBid[0], CurrentBid[1], 0)	#tell everyone that player gains a die
						Env.Verbose(1,"%s was right! They gain a die", ActivePlayerNode.data.Str_Name)
						GainADie(Game, BiddingPlayerNode.data)		#The correct player gains a die
					else:
						Game.Broadcast(Env,"SPOT! %s %d %d %d", ActivePlayerNode.data.Str_Name, CurrentBid[0], CurrentBid[1], 1)	#tell everyone that player loses a die
						Env.Verbose(1,"%s was wrong! They lose a die", ActivePlayerNode.data.Str_Name)
						LoseADie(Game, ActivePlayerNode.data,ActivePlayerNode.next.data)					#The incorrect player loses a die, pass next player to potentially set new starter
					break
				elif NextSpotOn == 0:
					Env.Verbose(3,"%s does not wish to call 'spot on'.", ActivePlayerNode.data.Str_Name)
				else:
					Env.Verbose(1, "Warning: %s has served a malformed spot on.  Assuming they do not wish to call spot on.", ActivePlayerNode.data.Str_Name)
					
				ActivePlayerNode=ActivePlayerNode.next
		
		NextPlayerDoubt = BiddingPlayerNode.next.data.GetDoubt(Env)
		if NextPlayerDoubt == 1:			#Does the next player want to say "I doubt?"
			Env.Verbose(1,"%s doubts!", BiddingPlayerNode.next.data.Str_Name)
			if EvalIDoubt(Env,ActivePlayers, CurrentBid) == 0:	#If the bid was correct
				Game.Broadcast(Env,"DOUBT! %s 0",BiddingPlayerNode.data.Str_Name)			#tell everyone that BiddingPlayerNode was right
				LoseADie(Game,BiddingPlayerNode.next.data, BiddingPlayerNode.next.next.data)	#Doubter loses a die, pass next player to potentially set new starter
				Env.Verbose(1,"%s was wrong! They lose a die", BiddingPlayerNode.next.data.Str_Name)
				break
			else:							#If the bid was incorrect
				Game.Broadcast(Env,"DOUBT! %s 1",BiddingPlayerNode.data.Str_Name)			#tell everyone that BiddingPlayerNode was wrong
				LoseADie(Game,BiddingPlayerNode.data, BiddingPlayerNode.next.data)	#Doubter loses a die, pass next player to potentially set new starter
				Env.Verbose(1,"%s was wrong! They lose a die", BiddingPlayerNode.data.Str_Name)
				break
		elif NextPlayerDoubt == 0:					#if they do not doubt
			Env.Verbose(3,"%s does not want to call 'I doubt'", BiddingPlayerNode.next.data.Str_Name)
			BiddingPlayerNode=BiddingPlayerNode.next		#advance play
		elif NextPlayerDoubt == -1:					#Error code
			Env.Verbose(1, "Warning %s has served a malformed doubt.  Assuming they do not wish to call Doubt.", BiddingPlayerNode.next.data.Str_Name)
			BiddingPlayerNode=BiddingPlayerNode.next		#advance play

							#end run the round
		Game.BroadcastDice(ActivePlayers)	#Tell everyone what the dice were
		pass					#No cleanup required

def PlayObligedRound(Env,Game):
	Game.Broadcast("ROUND! 1")	#Tell players we are starting a new obliged round
	Env.Verbose(1,"Starting obliged round...")
	Game.ObligedRoundNext=0		#Our bool has done its job and must be reset
					#begin prepare for the round
	ActivePlayers = [x for x in GenerateActivePlayers(Game)]
	PlayerLoop = doublylinkedloops.Cdoubly_linked_loop()
	
	TotalDice=0				#How many dice are there?
	for Player in ActivePlayers:
		TotalDice += Player.I_HandSize
		Player.RollCup()				#All active players roll their dice
		PlayerLoop.AddNode(Player)			#Create a list of all active players for this round
		if PlayerLoop.tail.data.B_StartNext == 1:	#Is this latest node the starting player?
			BiddingPlayerNode = PlayerLoop.tail
			Player.B_StartNext=0
	
	Str_ActivePlayerBroadcast="PLAYERS:"	#start to generate the broadcast string telling people about who is playing this round
	ActivePlayerNode=BiddingPlayerNode
	while 1:
		Str_ActivePlayerBroadcast = Str_ActivePlayerBroadcast + " " + ActivePlayerNode.data.Str_Name
		if ActivePlayerNode.next == BiddingPlayerNode:
			break
		ActivePlayerNode=ActivePlayerNode.next
	Env.Verbose(2,Str_ActivePlayerBroadcast)
	Game.Broadcast(Env,Str_ActivePlayerBroadcast)

	Env.Verbose(3, "Total dice: %d. Generating valid initial bids...", TotalDice)
	ValidObligedBids = [x for x in GenerateValidObligedBids(TotalDice)] # Generate an ordered list of all valid bids for this round for those that have Player.B_Obliging==1; other bids must "follow suit"

	CurrentBid = [0,0]		#Dummy zeroth bid
					#end prepare for the round
	
					#begin run the round
	while 1:
		Env.Verbose(3,"It is %s's bid.",BiddingPlayerNode.data.Str_Name)
		NewBid = GetBid(Env,BiddingPlayerNode.data)	#Get a bid
		#If the player need not follow suit (i.e. BiddingPlayerNode.data.B_Obliging=1, check as in normal round
		if BiddingPlayerNode.data.B_Obliging == 1:
			if not ((NewBid in ValidObligedBids) and (ValidObligedBids.index(NewBid) > ValidObligedBids.index(CurrentBid))):			#Check bid is legal
				Game.Broadcast(Env,"CHEAT! %s", BiddingPlayerNode.data.Str_Name)
				Env.Verbose(1,"%s has attempted to cheat by bidding %d %d! They have been removed from the game and the round is over.", BiddingPlayerNode.data.Str_Name, NewBid[0], NewBid[1])
				BiddingPlayerNode.data.B_Dead = 1		#Remove them from the game
				Game.I_PlayersLeft-=1				#Reduce number of players
				BiddingPlayerNode.next.data.B_StartNext = 1;	#Player on their left starts next round
				return
			else:
				Env.Verbose(1,"%s has bid %d %d", BiddingPlayerNode.data.Str_Name, NewBid[0], NewBid[1])
				Game.Broadcast(Env,"BID! %s %d %d", BiddingPlayerNode.data.Str_Name, NewBid[0], NewBid[1])
				CurrentBid=NewBid				#Update the bid
		elif not (NewBid[1] != CurrentBid[1] and NewBid[0] > CurrentBid[0]):	#If the player MUST follow suit, check manually
			Game.Broadcast(Env,"CHEAT! %s", BiddingPlayerNode.data.Str_Name)
			Env.Verbose(1,"%s has attempted to cheat by bidding %d %d! They have been removed from the game and the round is over.", BiddingPlayerNode.data.Str_Name, NewBid[0], NewBid[1])
			BiddingPlayerNode.data.B_Dead = 1		#Remove them from the game
			Game.I_PlayersLeft-=1				#Reduce number of players
			BiddingPlayerNode.next.data.B_StartNext = 1;	#Player on their left starts next round
			return						#end round without showing dice
		else:							#If they must follow suit and they have made a valid bid
			Env.Verbose(1,"%s has bid %d %d", BiddingPlayerNode.data.Str_Name, NewBid[0], NewBid[1])
			Game.Broadcast(Env,"BID! %s %d %d", BiddingPlayerNode.data.Str_Name, NewBid[0], NewBid[1])
			CurrentBid=NewBid				#Update the bid
			
						#Check for anyone calling "spot on", except player who must bid next, since they are not allowed to do so
		ActivePlayerNode=BiddingPlayerNode.next.next
		while 1:
			if ActivePlayerNode == BiddingPlayerNode.next:
				break
			else:
				NextSpotOn = ActivePlayerNode.data.GetSpotOn(Env)
				if NextSpotOn == 1:	#does ActivePlayerNode.data want to call spot on?
					Env.Verbose(1,"%s says spot on!", ActivePlayerNode.data.Str_Name)
					if EvalSpotOn(Env,ActivePlayers,CurrentBid) == 0:	#If the "spot on" was correct
						Game.Broadcast(Env,"SPOT! %s %d %d %d", ActivePlayerNode.data.Str_Name, CurrentBid[0], CurrentBid[1], 0)	#tell everyone that player gains a die
						Env.Verbose(1,"%s was right! They gain a die", ActivePlayerNode.data.Str_Name)
						GainADie(Game, BiddingPlayerNode.data)		#The correct player gains a die
					else:
						Game.Broadcast(Env,"SPOT! %s %d %d %d", ActivePlayerNode.data.Str_Name, CurrentBid[0], CurrentBid[1], 1)	#tell everyone that player loses a die
						Env.Verbose(1,"%s was wrong! They lose a die", ActivePlayerNode.data.Str_Name)
						LoseADie(Game, ActivePlayerNode.data,ActivePlayerNode.next.data)					#The incorrect player loses a die, pass next player to potentially set new starter
					return
				elif NextSpotOn==0:
					Env.Verbose(3,"%s does not wish to call 'spot on'.", ActivePlayerNode.data.Str_Name)
				else:
					Env.Verbose(1, "Warning: %s has served a malformed spot on.  Assuming they do not wish to call spot on.", ActivePlayerNode.data.Str_Name)
				ActivePlayerNode=ActivePlayerNode.next
		
		if GetDoubt(Env,BiddingPlayerNode.next.data) == 1:		#Does the next player want to say "I doubt?"
			Env.Verbose(1,"%s doubts!", BiddingPlayerNode.next.data.Str_Name)
			if EvalIDoubt(Env,ActivePlayers, CurrentBid) == 0:	#If the bid was correct
				Game.Broadcast(Env,"DOUBT! %s 0",BiddingPlayerNode.data.Str_Name)			#tell everyone that BiddingPlayerNode was right
				LoseADie(Game,BiddingPlayerNode.next.data, BiddingPlayerNode.next.next.data)	#Doubter loses a die, pass next player to potentially set new starter
				Env.Verbose(1,"%s was wrong! They lose a die", BiddingPlayerNode.next.data.Str_Name)
				return
			else:							#If the bid was incorrect
				Game.Broadcast(Env,"DOUBT! %s 1",BiddingPlayerNode.data.Str_Name)			#tell everyone that BiddingPlayerNode was wrong
				LoseADie(Game,BiddingPlayerNode.data, BiddingPlayerNode.next.data)	#Doubter loses a die, pass next player to potentially set new starter
				Env.Verbose(1,"%s was wrong! They lose a die", BiddingPlayerNode.data.Str_Name)
				return
		else:
			Env.Verbose(3,"%s does not want to call 'I doubt'", BiddingPlayerNode.next.data.Str_Name)
			BiddingPlayerNode=BiddingPlayerNode.next

					#end run the round
		Game.BroadcastDice(ActivePlayers)	#Tell everyone what the dice were
					#No cleanup required


def GenerateValidNormalBids(TotalDice):		#create, in order, a list of all valid bids for this round
						#There feels like there's a much nicer way to write this
	yield [0,0]				#Dummy zeroth bid
	for x in xrange(TotalDice):
		yield  [x+1,2]
		yield  [x+1,3]
		yield  [x+1,4]
		yield  [x+1,5]
		yield  [x+1,6]
		if (x + 1) % 2 == 0:
			yield  [(x + 1)/2,1]
						#Now pad out to the end with the remaining bids on aces
	x=TotalDice
	while 1:
		if (x+1)%2 == 0:
			yield [(x+1)/2, 1]
			if [(x+1)/2,1] == [TotalDice, 1]:
				break
		x+=1
	pass

def GenerateValidObligedBids(TotalDice):		#create, in order, a list of all valid bids for this round
						#Aces are not wild in obliged rounds, so the bidding is ordered numerically
	yield [0,0]				#Dummy zeroth bid
	for x in xrange(TotalDice):
		yield  [x+1,1]
		yield  [x+1,2]
		yield  [x+1,3]
		yield  [x+1,4]
		yield  [x+1,5]
		yield  [x+1,6]
	pass

def GenerateActivePlayers(Game):
	for CurrentPlayer in Game.Players:
		if CurrentPlayer.B_Dead == 0:
			yield CurrentPlayer
	pass


def EvalIDoubt(Env,ActivePlayers,CurrentBid, ObligedRound=0):
	Quantity=0
	for Player in ActivePlayers:
		Env.Verbose(1,"%s:",Player.Str_Name)			#Print out everyone's dice
		Env.Verbose(1,''.join('%d ' % num for num in Player.LI_Hand))
		Quantity+=Player.LI_Hand.count(CurrentBid[1])		#Add Players' dice to that
		if(ObligedRound == 0) and (CurrentBid[1] != 1):
			Quantity+=Player.LI_Hand.count(1)			#Add Players' aces to that
	Env.Verbose(1,"There were %d %ds",Quantity,CurrentBid[1])
	if(Quantity >=CurrentBid[0]):					#If bid is correct
		return 0
	else:								#If bid is incorrect
		return 1

def EvalSpotOn(Env,ActivePlayers,CurrentBid, ObligedRound=0):
	Quantity=0
	for Player in ActivePlayers:
		Env.Verbose(1,"%s:",Player.Str_Name)			#Print out everyone's dice
		Env.Verbose(1,''.join('%d ' % num for num in Player.LI_Hand))
		Quantity+=Player.LI_Hand.count(CurrentBid[1])		#Add Players' dice to that
		if(ObligedRound == 0) and (CurrentBid[1] != 1):
			Quantity+=Player.LI_Hand.count(1)			#Add Players' aces to that
	Env.Verbose(1,"There were %d %ds",Quantity,CurrentBid[1])
	if(Quantity == CurrentBid[0]):					#If spot on is correct
		return 0
	else:								#If spot on is incorrect
		return 1

def LoseADie(Game, Loser, LosersLeft):
	Loser.I_HandSize -=1		#Take away the lost die
	if Loser.I_HandSize == 0:	#Are they out of dice?
		Loser.B_Dead = 1	#...then they're out
		Game.I_PlayersLeft -= 1	#...and we have one fewer player
		LosersLeft.B_StartNext = 1	#And the player on their left starts
	elif Loser.I_HandSize == 1 and Loser.B_Obliging == 0:	#Are they entering an obliging round for the first time?
		Loser.B_Obliging=1			#Then they are obliging
		Game.B_ObligedRoundNext=1		#...and the next round is an obliged round...
		Loser.B_StartNext=1			#...and they will start it
	else:
		Loser.B_StartNext=1	#They start the next round

def GainADie(Game,Winner):
	Winner.I_HandSize+=1
