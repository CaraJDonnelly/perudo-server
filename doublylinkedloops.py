
class doubly_linked_loop_item:
	data = None		#Contains data
	next = None		#Contains next node 
	last = None		#Contains previous node

	def __init__(self, Data):
		self.data = Data
	
class Cdoubly_linked_loop:	#This is the circle of players
	head = None		#We have no head node for this is a loop
	tail = None		#But we do want a tail node to know where to insert next
				
				#start list of variables
	
				#end list of variables

				#start list of functions
	def AddNode(self, Data):

		NewNode = doubly_linked_loop_item(Data)
		if(self.tail == None):				#If the list is empty
			NewNode.next = NewNode
			NewNode.last = NewNode
			self.tail = NewNode
			self.head = NewNode
		else:
			NewNode.next = self.tail.next		#The non-distinguished ``head'' node
			self.tail.next = NewNode
			NewNode.last = self.tail
			NewNode.next = self.head
			self.tail = NewNode			#Keep track of last added node
			#WARNING:  These last two lines seem VERY fishy to me, because I don't know enough about
			#Python's pointer structure

		pass
				#end list of functions
	
	
