from state import *
from tkinter import *
from tkinter import messagebox

class TutrisWorld:

	def __init__(self, initial_state, final_state, steps):
		# Consistency checks
		for i in range(len(initial_state.piece_list)):
			if initial_state.piece_list[i].__class__ != final_state.piece_list[i].__class__:
				raise Exception("Initial and final states include different piece classes")
		if not initial_state.is_valid():
			raise Exception("Invalid initial state")
		if not final_state.is_valid():
			raise Exception("Invalid final state")
		# Parameter initialization
		self.state = initial_state
		self.final_state = final_state		
		self.steps = steps
		# Window creation
		self.window = Tk()
		self.window.resizable(False, False)
		self.window.title("Tutris World")
		self.canvas = Canvas(self.window, width=878, height=594)
		self.back_image = PhotoImage(file="img/background.gif")
		self.logo_image = PhotoImage(file="img/tutris.gif")
		self.piece_images = []
		for piece in self.state.piece_list:
			if piece.__class__.__name__ == 'PieceBar':
				self.piece_images.append(PhotoImage(file="img/piece0.gif"))
			elif piece.__class__.__name__ == 'PieceL':
				self.piece_images.append(PhotoImage(file="img/piece1.gif"))
			elif piece.__class__.__name__ == 'PieceS':
				self.piece_images.append(PhotoImage(file="img/piece2.gif"))
			elif piece.__class__.__name__ == 'PieceSquare':
				self.piece_images.append(PhotoImage(file="img/piece3.gif"))
		self.b_next = Button(self.window, text="Next Step", command=self.next_step, font=("Helvetica", 16))
		self.b_next.place(x=770, y=80, anchor=CENTER)
		self.b_auto = Button(self.window, text="Auto Step", command=self.auto_step, font=("Helvetica", 16))
		self.b_auto.place(x=770, y=140, anchor=CENTER)		
		if not self.steps or len(self.steps) == 0:
			self.b_next.config(state=DISABLED)
			self.b_auto.config(state=DISABLED)
		self.l_step = Label(self.window, text="", bg="black", fg="white", font=("Helvetica", 16))
		self.l_step.place(x=770, y=200, anchor=CENTER)
		self.canvas.pack()
		self.draw()
		self.window.mainloop()
		
		
	# NEXT STEP IN THE SOLUTION FOUND
	def next_step(self):
		self.b_next.config(state=DISABLED)
		# NEXT STEP IN THE LIST
		step = self.steps.pop(0)
		self.l_step.config(text=str(step))		
		self.state = self.state.successor(step)
		if self.state == None:
			self.b_auto.config(state=DISABLED)
			messagebox.showerror("Error", "Incorrect action: %s" % str(step))
			return
		# FINISH CONDITIONS (GOAL ACHIEVED vs GOAL NOT ACHIEVED)
		if self.state == self.final_state:
			self.b_next.config(state=DISABLED)
			self.b_auto.config(state=DISABLED)
			self.draw()
			messagebox.showinfo("Finished!", "Goal achieved! :)")
			return
		elif len(self.steps) == 0:
			print(self.state)
			print(self.final_state)
			self.b_next.config(state=DISABLED)
			self.b_auto.config(state=DISABLED)
			self.draw()
			messagebox.showwarning("Finished", "No steps left")
			return
		# REDRAW
		self.draw()		
		self.b_next.config(state=NORMAL)
		self.canvas.update()
		
	
	# AUTO STEP IN THE SOLUTION FOUND
	def auto_step(self):
		self.b_auto.config(state=DISABLED)
		self.b_next.config(state=DISABLED)
		self.canvas.update()
		while self.steps:
			self.next_step()
			self.b_next.config(state=DISABLED)
			self.canvas.update()
			self.canvas.after(200)
		
		
	# DRAWS THE SCENARIO
	def draw(self):
		self.canvas.delete(ALL)
		# BACKGROUND
		self.canvas.create_image(0, 0, image=self.back_image, anchor=NW)
		# LOGO
		self.canvas.create_image(770, 550, image=self.logo_image, anchor=CENTER)
		# PIECES
		for i in range(len(self.state.piece_list)):
			p = self.state.piece_list[i]
			self.canvas.create_image(66 + p.x*66, p.y*66, image=self.piece_images[i], anchor=NW)
		self.canvas.update()
		


if __name__ == "__main__":
	try:
		init_list1 = [PieceBar(1,7), PieceL(1,3), PieceS(4,6), PieceSquare(0,4)]
		init_list2 = [PieceBar(4,6), PieceL(1,5), PieceS(5,4), PieceSquare(0,3)]
		init_list3 = [PieceBar(4,6), PieceL(1,5), PieceS(3,4), PieceSquare(4,2)]
		goal_list = [PieceBar(2,7), PieceL(0,5), PieceS(5,6), PieceSquare(0,6)]
		init_state = TutrisState(init_list1)
		goal_state = TutrisState(goal_list)
		steps = steps = [(1, 'LEFT'), (2, 'RIGHT'), (0, 'RIGHT'), (3, 'DOWN'), (1, 'DOWN'), (3, 'DOWN'), (1, 'DOWN')]
		world = TutrisWorld(init_state, goal_state, steps)
	except Exception as ex:
		print("Error in TutrisWorld -->", ex)
		
