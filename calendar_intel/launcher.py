"""
Main launcher logic. Created new calendar intel window.
See: https://stackoverflow.com/questions/13258554/convert-unknown-format-strings-to-datetime-objects
"""

import tkinter as tk

from calendar_intel.event_parser import parse_calendar_paste

# Top level window
frame = tk.Tk()
frame.title("TextBox Input")

# Create new window, in middle of screen. See: https://stackoverflow.com/a/14912644/13805480
w = 800  # width for the Tk root
h = 650  # height for the Tk root

# get screen width and height
ws = frame.winfo_screenwidth()  # width of the screen
hs = frame.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

# set the dimensions of the screen
# and where it is placed
frame.geometry('%dx%d+%d+%d' % (w, h, x, y))


# Function for getting Input
# from textbox and printing it
# at label widget

def handle_click():
    raw_calendar_events: str = inputtxt.get(1.0, "end-1c")
    parse_calendar_paste(raw_calendar_events)


# Label Creation
lbl = tk.Label(frame, text="Paste Calendar Events Here...")
lbl.pack()

# TextBox Creation
inputtxt = tk.Text(frame,
                   height=45,
                   width=100)

inputtxt.pack()

# Button Creation
printButton = tk.Button(frame,
                        text="Create Breakdown",
                        command=handle_click)
printButton.pack()

frame.mainloop()
