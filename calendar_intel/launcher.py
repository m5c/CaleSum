"""
Main launcher logic. Created new calendar intel window.
"""

from tkinter import *

from calendar_intel.event_parser import parse_calendar_paste

# Top level window
frame = Tk()
frame.title("TextBox Input")

# Create new window, in middle of screen. See: https://stackoverflow.com/a/14912644/13805480
w = 800  # width for the Tk root
h = 670  # height for the Tk root

# get screen width and height
ws = frame.winfo_screenwidth()  # width of the screen
hs = frame.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

# set the dimensions of the screen
# and where it is placed
frame.geometry('%dx%d+%d+%d' % (w, h, x, y))

# Two sub frames, one above, one below.
top = Frame(frame)
bottom = Frame(frame)
top.pack(side=TOP)
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

# Function for getting Input
# from textbox and printing it
# at label widget
def handle_click():
    raw_calendar_events: str = inputtxt.get(1.0, "end-1c")
    parse_calendar_paste(raw_calendar_events, time_zone_selection.get())

# Menu options
c1 = Checkbutton(frame, text='All Day Events  ')
c1.pack(in_=top, side=LEFT)
c2 = Checkbutton(frame, text='Multi Day Events  ')
c2.pack(in_=top, side=LEFT)
# Timezone
lbl = Label(frame, text="Default Time-Zone: ")
lbl.pack(in_=top, side=LEFT)
OPTIONS = [
"EDT",
"CET"
]
time_zone_selection = StringVar(frame)
time_zone_selection.set(OPTIONS[0])
w = OptionMenu(frame, time_zone_selection, *OPTIONS)
w.pack(in_=top, side=LEFT)


# The actual calendar parser
# Label Creation
lbl = Label(frame, text="Paste Calendar Events Here...")
lbl.pack()

# TextBox Creation
inputtxt = Text(frame,
                   height=45,
                   width=100)
inputtxt.pack()

# Button Creation
printButton = Button(frame,
                        text="Create Breakdown",
                        command=handle_click)
printButton.pack()
frame.mainloop()
