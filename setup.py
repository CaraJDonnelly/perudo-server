import sys					#access the system variables

class CEnv:
						#start list of flags
	I_Verbose=0				#verbosity
						#verbose? = 1		Print round results etc.
						#very verbose? = 2	Print bids
						#very very verbose? = 3	Print all function calls
						#end list of flags
						
	I_NumberOfPlayers=None				#number of players
						
							#begin function definitions
	
	def __init__(self):
		
		if "-h" in sys.argv or "?" in sys.argv:
			print "A simple server application for Perudo.  Options: \n\
				-p 4\tSpecify e.g. 4 players (required)\n\
				-v\tVerbose.  Print round results etc.\n\
				-vv\tVery verbose.  Print round results etc.\n\
				-vvv\tVery very verbose.  Print all function calls\n\
				-h\tPrint this help and exit\n"
			return None

											#Check for verbose level, always take maximum
		if "-v" in sys.argv:
			self.I_Verbose = 1
		if "-vv" in sys.argv:
			self.I_Verbose = 2
		if "-vvv" in sys.argv:
			self.I_Verbose = 3
	
		if "-p" in sys.argv:							#Find the number of players flag -p
			try:
				self.I_NumberOfPlayers = int(sys.argv[sys.argv.index("-p")+1])	#convert the next entry to an int
			except ValueError:
				print "Invalid number of players"

	def Verbose(self,I_Verbosity,Str_Print, *PrintfArguments):			#Selective printing based on verbosity
			
		if I_Verbosity <= self.I_Verbose:
			print Str_Print%(PrintfArguments)
	


						#end function definitions
