"""
Main launcher logic. Created new calendar intel window.
"""

from tkinter import *

from calendar_intel import event_miner
from calendar_intel.event_parser import parse_calendar_paste

# Top level window
frame = Tk()
frame.title("Calendar Intel")

# Set app icon
img = Image("photo", file="icon.png")
# frame.iconphoto(True, img) # you may also want to try this.
frame.tk.call('wm','iconphoto', frame._w, img)

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

    # Convert pasted string to list of events
    events: [Event] = parse_calendar_paste(raw_calendar_events, time_zone_selection.get())

    # Filter all events that contradict checkbox selection
    events = event_miner.filter(events, include_all_day.get(), include_multi_day.get())

    # Create event summary (TODO: do something smarter here than just printing all events)
    event_miner.create_stats(events, case_sensitive.get())


# Menu options
## initialize variables:
case_sensitive = IntVar()
include_all_day = IntVar()
include_multi_day = IntVar()
OPTIONS = [
    "EDT",
    "CET"
]
## Create gui elements
c0 = Checkbutton(frame, text='Case sensitive  ', variable=case_sensitive, onvalue=True,
                 offvalue=False)
c0.pack(in_=top, side=LEFT)
c1 = Checkbutton(frame, text='All-day events  ', variable=include_all_day, onvalue=True,
                 offvalue=False)
c1.pack(in_=top, side=LEFT)
c2 = Checkbutton(frame, text='Multi-day events  ', variable=include_multi_day, onvalue=True,
                 offvalue=False)
c2.pack(in_=top, side=LEFT)
# Timezone
lbl = Label(frame, text="Default Time-Zone: ")
lbl.pack(in_=top, side=LEFT)

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
