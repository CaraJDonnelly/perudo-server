import sys					#access the system variables
import socket

class CEnv:
						#start list of flags
	I_Verbose=0				#verbosity
						#verbose? = 1		Print round results etc.
						#very verbose? = 2	Print bids
						#very very verbose? = 3	Print all function calls
						#end list of flags
						
	I_NumberOfPlayers=None				#number of players
	ServerSocket=None				#The server socket
						
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
		else:
			print "You must specify the number of players using -p"
			self.I_NumberOfPlayers = 0					#Guess there aren't any players
			sys.exit();							#...return an error code
		
		#start set up the server socket
		try:
			self.ServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)	#initialise ServerSocket
			self.ServerSocket.bind(("localhost", 1111))				#bind to localhost
			self.ServerSocket.listen(5)						#start listening for connections, 5 should be a fine backlog
			self.Verbose(3,"Server Socket bound")
			#end set up the server socket
		except:
			self.Verbose(1, "Could not bind server socket!")
			sys.exit()
		

	def Verbose(self,I_Verbosity,Str_Print, *PrintfArguments):			#Selective printing based on verbosity
			
		if I_Verbosity <= self.I_Verbose:
			print Str_Print%(PrintfArguments)
			sys.stdout.flush()
	
	def CleanUp(self):
		self.ServerSocket.close()

						#end function definitions
