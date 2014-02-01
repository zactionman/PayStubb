# PayStubb - A utility for calculating pay over a specified number of hours.
# Written by Zach Leinweber

# Initial draft - non-working version.

from Tkinter import *
from ttk import * 

class App(object):

	def __init__(self, master):
		# Create variables and UI elements.

		# Start with the top Menu Bar
		master.option_add('*tearOff', FALSE)
		menubar = Menu(master)
		# Make a filemenu... though I'm not sure why.
		filemenu = Menu(menubar)
		filemenu.add_command(label="Save", command=self.PlcHldr)
		menubar.add_cascade(label="File", menu=filemenu)
		# Edit Menu
		editmenu = Menu(menubar)
		editmenu.add_command(label="Copy", command=self.PlcHldr)
		menubar.add_cascade(label="Edit", menu=editmenu)
		# Help Menu
		helpmenu = Menu(menubar)		
		helpmenu.add_command(label="About", command=self.PlcHldr)
		menubar.add_cascade(label="Help", menu=helpmenu)
		# Add the menu to master toplevel...
		master['menu'] = menubar

		# Start to initialize vars.
		# These two lists are used to call Wrk_Inp and Wrk_Out via index points.
		# This one is for hours
		self.Wrk_Hrs = ['Reg_Hrs', 'Reg_Hrs2', 'Ovr_Hrs', 'Ovr_Hrs2', 'Hol_Hrs', 'Hol_Hrs2'] 
		# This one is for premiums.
		self.Wrk_Prm = ['Reg_Prm', 'Reg_Prm2', 'Ovr_Prm', 'Ovr_Prm2', 'Hol_Prm', 'Hol_Prm2']
		# These two dicts are used to store user input data and then do math on them.
		# Wrk_Inp stores the variables in the entry fields
		self.Wrk_Inp = {}
		# Wrk_Out stores the actual numbers after the Wrk_Inp.get() is called.
		self.Wrk_Out = {}
		# The body will start off consisting with three frames.  Each with three columns.
		# I'm not sure how this will change going forward as I would like to implement a way
		# for the user to add and remove widgets while the app is running.
		self.frame = Frame(master)
		self.frame.grid(row=0, column=0)
		# Each row will be it's own frame (For hiding purposes to be added later)
		# This tuple is used to store the label names.
		Types = ('Regular', 'Regular2', 'Overtime', 'Overtime2', 'Holiday', 'Holiday2')
		# This list stores all of the content frames.  Each row gets a frame.
		# I did this so that going forward I could easily make a method to hide and show rows.
		self.frames = []
		# This for loop instantiates all of the frames and content that goes in the frame
		# It also ties the Wrk_Inp dict to the entries via DoubleVar()
		for i in range(0, 6):
			self.frames.append('frame')
			self.frames[i] = Frame(self.frame)
			self.frames[i].grid(row=i, column=0)

			self.Wrk_Inp[self.Wrk_Hrs[i]] = DoubleVar()
			self.Wrk_Inp[self.Wrk_Prm[i]] = DoubleVar()

			Label(self.frames[i], text=Types[i], width=15).grid(row=0, column=0)
			Entry(self.frames[i], textvariable=self.Wrk_Inp[self.Wrk_Hrs[i]]).grid(row=0, column=1)
			Entry(self.frames[i], textvariable=self.Wrk_Inp[self.Wrk_Prm[i]]).grid(row=0, column=2)

		# This button calls the calc function... Though at this point it really just prints the hours.
		Button(self.frame, text='Print Hours!', command=self.Calc).grid(row=6, column=0)


	def Get_Input(self):
		# Get the variables from entry fields.
		for Hours in self.Wrk_Hrs:
			n = self.Wrk_Hrs.index(Hours)
			self.Wrk_Out[Hours] = self.Wrk_Inp[Hours].get()
			self.Wrk_Out[self.Wrk_Prm[n]] = ((self.Wrk_Inp[self.Wrk_Prm[n]].get()) / 100)

	def Calc(self):
		# Calculate pay
		self.Get_Input()
		print "No Errors"
		# This is a placeholder until I actually invent a way to get hourly rates from user.
		wage = [20, 20, 30, 30, 50, 50]
		# This will hold the pay rates (Wage * Premium)
		rate = []
		# This will hold amount payed for each type (Rate * Work Hours)
		payed = []
		# This loop populates the rate and payed lists.
		for i in range(0,6):
			rate.append('')
			rate[i] = (wage[i] * self.Wrk_Out[self.Wrk_Prm[i]]) + wage[i]

			payed.append('')
			payed[i] = (rate[i] * self.Wrk_Out[self.Wrk_Hrs[i]]) 
		total = 0
		# To calculate total add together all the indices in payed list.
		for money in payed:
			total += money
		print total

	def PlcHldr(self):
		# This is a dummy Method for testing stuff.
		print "This Works! Yay!"

root = Tk()
root.wm_title('PayStubb')

app = App(root)

root.mainloop()

