#! /usr/bin/python
# PayStubb - A utility for calculating pay over a specified number of hours.
# Written by Zach Leinweber


from Tkinter import *
from ttk import * 
import tkMessageBox

class App(object):

    def __init__(self, master):
        # (1) Initialize menu bar
        master.option_add('*tearOff', FALSE)
        menubar = Menu(master, font='TkMenuFont')
        # Make a filemenu... though I'm not sure why.
        filemenu = Menu(menubar)
        filemenu.add_command(label="Save", command=self.PlcHldr)
        menubar.add_cascade(label="File", menu=filemenu)
        # Edit Menu
        editmenu = Menu(menubar)
        editmenu.add_command(label="Copy", command=self.PlcHldr)
        editmenu.add_command(label="Clear", command=self.ClearFields)
        editmenu.add_separator()
        editmenu.add_command(label="Preferences", command=self.Prefs)
        menubar.add_cascade(label="Edit", menu=editmenu)
        # View Menu
        viewmenu = Menu(menubar)
        viewmenu.add_command(label="Toggle Rows", command=self.Showrows)
        menubar.add_cascade(label="View", menu=viewmenu)
        # Help Menu
        helpmenu = Menu(menubar)        
        helpmenu.add_command(label="About", command=self.AboutPage)
        menubar.add_cascade(label="Help", menu=helpmenu)
        # Add the menu to master toplevel...
        master['menu'] = menubar

        # (2) Initialize instance vars
        # These two lists are used to call Wrk_Inp and Wrk_Out via index points.
        # This one is for hours
        self.Wrk_Hrs = ['Reg_Hrs', 'Reg_Hrs2', 'Ovr_Hrs', 'Ovr_Hrs2',
             'Hol_Hrs', 'Hol_Hrs2'] 
        # This one is for premiums.
        self.Wrk_Prm = ['Reg_Prm', 'Reg_Prm2', 'Ovr_Prm', 'Ovr_Prm2',
             'Hol_Prm', 'Hol_Prm2']
        # These two dicts are used to store user input data and then do math on them.
        # Wrk_Inp stores the variables in the entry fields
        self.Wrk_Inp = {}
        # Wrk_Out stores the actual numbers after the Wrk_Inp.get() is called.
        self.Wrk_Out = {}
        # This is a placeholder until I actually invent a way to get hourly rates from user.
        self.wages = [20, 20, 30, 30, 50, 50]
        # know the row's prevoius state which is importent for hiding/showing rows.
        self.cstate = [1, 1, 1, 1, 1, 1]
        # This contains the variables bound to the checkbuttons in the showline in viewmenu
        # This used to know when the user wants to hide or show a variable.
        self.rstate = []
        # This list is used to store the label names when the program starts.
        # This can be changed later by the user.
        self.lTypes = ['Regular', 'Regular2', 'Overtime', 'Overtime2', 'Holiday', 'Holiday2']
        self.Types = []
        # This sets the initial names for the row labels.
        for i in range(0, 6):
            self.Types.append('type')
            self.Types[i] = StringVar()
            self.Types[i].set(self.lTypes[i])
            # Set base wage (default 20 for all fields)
            self.wages[i] = DoubleVar()
            self.wages[i].set(20.0)
            # Initialize entry variables. These are stored in two dicts.
            self.Wrk_Inp[self.Wrk_Hrs[i]] = DoubleVar()
            self.Wrk_Inp[self.Wrk_Prm[i]] = DoubleVar()
            # This initializes the bound variables for the showline option in viewmenu
            self.rstate.append('')
            self.rstate[i] = IntVar()
            self.rstate[i].set(1)

        # (3) Initialize and draw window body
        # The body will start off consisting with three frames.  Each with three columns.
        self.frame = Frame(master)
        self.frame.grid(row=0, column=0, stick=(N,E,S,W))
        # Create the column labels!
        col_lbl = Frame(self.frame)
        col_lbl.grid(row=0, column=0, columnspan=3, pady=5, padx=10, sticky=(E,W))
        Label(col_lbl, text="Type", font='TkHeadingFont', width=10).grid(row=0, column=0, sticky=W)
        Label(col_lbl, text="Hours", font='TkHeadingFont', width=15).grid(row=0, column=1)
        Label(col_lbl, text="Premium", font='TkHeadingFont', width=8).grid(row=0, column=2, sticky=E)
        col_lbl.columnconfigure((0,1,2), weight=1)
        # Create a seperator.
        Separator(self.frame).grid(row=1, column=0, sticky=(E,W), pady=8, padx=8)
        # This list stores all of the content frames.  Each row gets a frame.
        # I did this so that going forward I could easily make a method to hide and show rows.
        self.frames = [1, 2, 3, 4, 5, 6]
        # This for loop instantiates all of the frames and content that goes in the frame
        # It also ties the Wrk_Inp dict to the entries via DoubleVar()
        for i in range(0, 6):
            # Create each row.
            self.frames[i] = Frame(self.frame)
            self.frames[i].grid(row=(i+2), column=0, columnspan=3, padx=10, sticky=(E,W))
            # Draw label and two entry widgets for each row.
            Label(self.frames[i], textvariable=self.Types[i],
                 width=10).grid(row=0, column=0, sticky=W)
            Entry(self.frames[i], textvariable=self.Wrk_Inp[self.Wrk_Hrs[i]],
                 width=15).grid(row=0, column=1)
            Entry(self.frames[i], textvariable=self. Wrk_Inp[self.Wrk_Prm[i]],
                 width=8).grid(row=0, column=2, sticky=E)
            self.frames[i].columnconfigure((0,1,2), weight=1)
        # Text widget for displaying the output of the program.
        self.tframe = Labelframe(self.frame, text='Results', padding=(4,8))
        self.tframe.grid(row=8, column=0, columnspan=3, pady=8, padx=8, sticky=(N,S,E,W))
        self.text = Text(self.tframe, state='disabled', width=40, height=9) 
        self.text.grid(row=0, column=0, sticky=(N,S,E,W)) 
        self.tframe.columnconfigure(0, weight=1)
        # This button calls the calc function.
        Button(self.frame, text='Calculate!', command=self.Calc).grid(row=9, column=0, pady=12)
        # Resize grip. 
        Sizegrip(master).grid(row=999, column=0, sticky=(S,E))

        # (4) Set window resizing options. (That aren't already set.
        master.columnconfigure(0, weight=4)
        master.rowconfigure(0, weight=4)
        self.frame.columnconfigure(0, weight=4)
        self.frame.rowconfigure(0, weight=2)
        self.frame.rowconfigure((2,3,4,5,6,7,8,9), weight=1)

    def Get_Input(self):
        # Get the variables from entry fields.
        for Hours in self.Wrk_Hrs:
            n = self.Wrk_Hrs.index(Hours)
            self.Wrk_Out[Hours] = self.Wrk_Inp[Hours].get()
            self.Wrk_Out[self.Wrk_Prm[n]] = ((self.Wrk_Inp[self.Wrk_Prm[n]].get()) / 100)
            self.lTypes[n] = self.Types[n].get()

    def Calc(self):
        # Calculate pay
        self.Get_Input()
        print "No Errors"
        # This will hold the pay rates (Wage * Premium)
        rate = []
        # This will hold amount payed for each type (Rate * Work Hours)
        payed = []
        # This loop populates the rate and payed lists.
        for i in range(0,6):
            rate.append('')
            wage = self.wages[i].get()
            rate[i] = (wage * self.Wrk_Out[self.Wrk_Prm[i]]) + wage

            payed.append('')
            payed[i] = (rate[i] * self.Wrk_Out[self.Wrk_Hrs[i]]) 
        total = 0
        # To calculate total add together all the indices in payed list.
        for money in payed:
            total += money
        Ttl_Diag = """For this pay period:
%s = %f
%s = %f
%s = %f
%s = %f
%s = %f
%s = %f

Total = %F""" % (self.lTypes[0], payed[0], self.lTypes[1], payed[1], self.lTypes[2],
             payed[2], self.lTypes[3], payed[3], self.lTypes[4], payed[4],
             self.lTypes[5], payed[5], total)
        self.text['state'] = 'normal'
        self.text.delete(1.0, END)
        self.text.insert(1.0, Ttl_Diag)
        self.text['state'] = 'disabled'

    def ClearFields(self):
        answer = tkMessageBox.askokcancel(title='Clear',
            message='This will clear all input fields', icon='warning')
        if answer:
            for input in range(0, 6):
                self.Wrk_Inp[self.Wrk_Hrs[input]].set(0.0)
                self.Wrk_Inp[self.Wrk_Prm[input]].set(0.0)
        else:
            pass

    def Prefs(self):
        View_Prefs = Toplevel(root)
        nameframe = Labelframe(View_Prefs, text='Row Names', padding=(5,10,10,5))
        nameframe.grid(row=0, column=0)
        wageframe = Labelframe(View_Prefs, text='Wage Rates', padding=(10,10,5,5))
        wageframe.grid(row=0, column=1)
        for i in range(0, 6):
            Entry(nameframe, textvariable=self.Types[i], 
                width=12).grid(row=i, column=0)
            Entry(wageframe, textvariable=self.wages[i],
                width=8).grid(row=i, column=0)

    def Showrows(self):
        # This method is for hiding and showing rows in the application.
        # Greate the window for the menu
        View_Lines = Toplevel(root)
        View_Lines.title('Rows')
        vlframe = Labelframe(View_Lines, text='Toggle Rows', padding=(8,4,40,4))
        vlframe.grid(row=0, column=0, sticky=(N,E,S,W), padx=4, pady=(0,4))
        View_Lines.columnconfigure(0, weight=1); View_Lines.rowconfigure(0, weight=1)
        vlframe.columnconfigure(0, weight=1)
        # place the checkbutton widgets.
        x = 0
        for type in self.Types:
            name = type.get()
            Checkbutton(vlframe, text=name, variable=self.rstate[x],
            onvalue=1, offvalue=0, command=self.Hide).grid(row=x, column=0, sticky=(N,S,W))
            x += 1

    def Hide(self):
        for state in range(0, 6):
            new = self.rstate[state].get()
            if new != self.cstate[state]:
                self.cstate[state] = new
                if new == 0:
                    self.frames[state].grid_remove()
                    self.frame.rowconfigure(state+2, weight=0)
                else:
                    self.frames[state].grid()
                    self.frame.rowconfigure(state+2, weight=1)
            else:
                continue

    def AboutPage(self):
        about_file = open('about.txt')
        about_text = about_file.read()
        about_file.close()
        awindow = Toplevel()
        a_text = Text(awindow, height=15, width=70)
        a_text.grid(row=0, column=0, sticky=(N,E,S,W))
        a_text.insert(1.0, about_text)
        a_text['state'] = 'disabled'

    def PlcHldr(self):
        # This is a dummy Method for testing stuff.
        print "This Works! Yay! - But not implemented yet."

root = Tk()
root.wm_title('PayStubb')

app = App(root)

root.mainloop()

