import random
from os import system

# Cell Class with simple functions
class Cell:
	# Cell Initialization and has two main variables, current and next state
	def __init__(self):
		self.current_state = False
		self.next_state = False
	# Returns the character symbol for the current state
	def get_state(self):
		if self.current_state == True:
			return self.get_alive_char()
		else:
			return ' '
	# Returns the Alive character of a Normal Cell ('O')
	def get_alive_char(self):
		return 'O'
	# Sets the current state of the cell to Alive
	def set_state_alive(self):
		self.current_state = True
	# Sets the curren state of the cell to Dead
	def set_state_dead(self):
		self.current_state = False
	# Sets the next state of the cell by the number of neighbors
	## Normal Cell will die if there are more than 4 neighbors or less than 1
	## The Cell will be alive if there are exactly 3 neighbors
	## Cell Remains the same otherwise
	def set_next_state(self,neighbors):
		if ((neighbors >= 4) | (neighbors <= 1)):
			self.next_state = False
		elif ((neighbors == 3) & (self.current_state == False)):
			self.next_state = True
		else:
			self.next_state = self.current_state
	# Updates the current state with the next state
	def update(self):
		self.current_state = self.next_state
		self.next_state = False

# Inherited Cancer Class with slightly modified rules
class Cancer(Cell):
	# Returns the Alive character of a Normal Cell ('X')
	def get_alive_char(self):
		return 'X'
	# Cancer Cell will die if neighbors are more than five or less than one. 
	def set_next_state(self,neighbors):
		if ((neighbors >= 5) | (neighbors <= 1)):
			self.next_state = False
		elif ((neighbors == 3) & (self.current_state == False)):
			self.next_state = True
		else:
			self.next_state = self.current_state

# Board CLass for the Cell Simulation and essentially simulates a character board with some internal functions
class Board:
	# No Input Initialization
	def __init__(self):
		self.row_max = 20
		self.col_max = 75
		self.time = 0
		self.board = []
		self.alive_char = ' '
	# Initialization of Board with Row and Column size
	def __init__(self,row,col):
		self.row_max = row
		self.col_max = col
	# Returns the Number of Alive Cells on Board
	def get_num_cells(self):
		count = 0
		for i in range(self.row_max):
			for j in range(self.col_max):
				if (self.board[i][j].get_state() == self.alive_char):
					count += 1
		return count
	# Returns the Current Number or States
	def get_time(self):
		return self.time
	# Returns the number of neighbors 
	def get_neighbors(self,row,col):
		count = 0
		y_min = -1
		y_max = 1

		if self.board[row][col].get_state() == self.alive_char:
			count -= 1

		if row == 0:
			y_min = 0
		elif row == self.row_max-1:
			y_max = 0

		x_min = -1
		x_max = 1

		if col == 0:
			x_min = 0
		elif col == self.col_max -1:
			x_max = 0

		for y in range (y_min,y_max+1):
			for x in range(x_min,x_max+1):
				if self.board[row+y][col+x].get_state() == self.alive_char:
					count+=1
		#print(count)
		self.board[row][col].set_next_state(count)
	def next_state(self):
		for y in range(self.row_max):
			for x in range(self.col_max):
				self.get_neighbors(y,x)
		self.set_update()
		self.time +=1
	def print(self):
		print("Time:", self.get_time())
		print("Cell Number: ", self.get_num_cells())
		for y in range(self.row_max):
			print(''.join([self.board[y][x].get_state() for x in range(self.col_max)]))
	def seed_cells(self):
		self.time = 0
		lim = int(self.confluence*self.row_max*self.col_max/100)
		count = 0
		while count < lim:
			temp_x = random.randrange(0,self.col_max-1)
			temp_y = random.randrange(0,self.row_max-1)
			#print(temp_x,temp_y)
			if self.board[temp_y][temp_x].get_state() != self.alive_char:
				count += 1
				self.board[temp_y][temp_x].set_state_alive()
	def set_list(self):
		self.board = []
		for y in range(self.row_max):
			self.board.append([Cell() for x in range(self.col_max)])

		#print(len(self.board))
		#print(self.board[0][0])
		self.alive_char = self.board[0][0].get_alive_char()
	def set_state(self,selection,confluence):
		self.selection = selection
		self.confluence = confluence
		self.set_list()
		self.seed_cells()
	def set_update(self):
		for y in range(self.row_max):
			for x in range(self.col_max):
				self.board[y][x].update()

def mainMenu():
	while True:
		sel = int(input("Select your cell type: (1) normal cells or (2) cancer cells: "))
		if sel in range(1,3):
			break
	while True:
		con = int(input("Select the confluence percentage (%): "))
		if con in range(0,101):
			break
	return sel,con

trial = Board(20,75)
sel,con = mainMenu()
trial.set_state(sel,con)
system("cls")
trial.print()
exit = input()
while True:
	if (exit == "q") | (exit == "Q"):
		break 
	system("cls")
	trial.next_state()
	trial.print()
	exit = input()
