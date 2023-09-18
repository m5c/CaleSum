"""
Main launcher logic. Created new calendar intel window.
"""
from tkinter import Frame, TOP, BOTTOM, BOTH, IntVar, Checkbutton, Label, LEFT, StringVar, \
    OptionMenu, Text, Button, END, Event, Tk

from calendar_intel import event_miner
from calendar_intel.event_parser import parse_calendar_paste

# Top level window
frame = Tk()
frame.title("Calendar Intel")

# Set app icon
# Comment this in for run without build
# img = Image("photo", file="icon.png")
# frame.tk.call('wm','iconphoto', frame._w, img)

# Create new window, in middle of screen. See: https://stackoverflow.com/a/14912644/13805480
width: int = 800  # width for the Tk root
height: int = 670  # height for the Tk root

# get screen width and height
ws: int = frame.winfo_screenwidth()  # width of the screen
hs: int = frame.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x_dimensions: int = (ws / 2) - (width / 2)
y_dimensions: int = (hs / 2) - (height / 2)

# set the dimensions of the screen
# and where it is placed
frame.geometry('%dx%d+%d+%d' % (width, height, x_dimensions, y_dimensions))

# Two sub frames, one above, one below.
top = Frame(frame)
bottom = Frame(frame)
top.pack(side=TOP)
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)


# Function for getting Input
# from textbox and printing it
# at label widget
def handle_click():
    """
    Handler for click on parse events button. When clicked this interprets whatever text
    currently is in the main textbox, parses, starts to mine, ...
    """
    raw_calendar_events: str = inputtxt.get(1.0, "end-1c")

    # Convert pasted string to list of events
    events: [Event] = parse_calendar_paste(raw_calendar_events, time_zone_selection.get())

    # Filter all events that contradict checkbox selection
    events = event_miner.event_filter(events, include_all_day.get(), include_multi_day.get())

    # Create event summary (TODO: do something smarter here than just printing all events)
    stats: str = event_miner.create_stats(events, case_sensitive.get())
    print(stats)

    # replace all window content with stats
    for ui_elements in frame.winfo_children():
        ui_elements.destroy()
    text_field = Text(frame, width=100, height=y_dimensions)
    text_field.pack(in_=frame, side=TOP)
    text_field.insert(END, stats)


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
width = OptionMenu(frame, time_zone_selection, *OPTIONS)
width.pack(in_=top, side=LEFT)

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
