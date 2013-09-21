#!/usr/bin/env python
import player
import playround
import setup
import gamestate



Env = setup.CEnv()				#Process the argv string


NewGame = gamestate.GameState(Env)				#Create the game state, initialise players



Env.Verbose(1,"Game start!")					#Game start!

								
for Player in NewGame.Players:					#just check how many valid players connected
	if Player.B_Dead == 1:
		NewGame.I_PlayersLeft-=1

if NewGame.I_PlayersLeft==0:					#If there are no players, return
	Env.Verbose(1, "No valid players!")
	exit


while NewGame.I_PlayersLeft > 1:				#If there is more than one player, play a round
	if NewGame.B_ObligedRoundNext and NewGame.I_PlayersLeft > 2:
		playround.PlayObligedRound(Env,NewGame)		#An obliged round is played and someone either gains or loses a die.  This rule does not happen if there are only two players left
	else:
		playround.PlayNormalRound(Env,NewGame)		#A normal round is played and someone either gains or loses a die

for Player in NewGame.Players:
	if Player.B_Dead == 0:
		Env.Verbose(1,"The winner was %s.", Player.Str_Name)	#print out the winner

Env.CleanUp();
Env.Verbose(1,"Game finished")				#Game finished

