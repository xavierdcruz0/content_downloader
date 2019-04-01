import Tkinter as tk
#from tkinter import filedialog
import tkFileDialog
import content_grabber_lib
import os


root = tk.Tk()
root.title("30 works content grabber")

# Add a grid
mainframe = tk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
# mainframe.pack(pady=100, padx=100)

# Create a Tkinter variable to store the day
dayStringVar = tk.StringVar(root)

# Create a variable to store the CSV filepath
excelPathStringVar = tk.StringVar(root)

# Create a variable to store the desired service (downloading or opening links in browser)
optionVar = tk.StringVar(root)
R1 = tk.Radiobutton(root, text="Download content", value="download content", var=optionVar)
R2 = tk.Radiobutton(root, text="Open Link URLs in browser", value="open urls", var=optionVar)
R1.grid(row=3, column=0)
R2.grid(row=3, column=1)

# List with options
choices = ["{:02d}".format(number+1) for number in list(range(30))]
# tkvar.set('Pizza')  # set the default option

dayPopupMenu = tk.OptionMenu(mainframe, dayStringVar, *choices)
tk.Label(mainframe, text="Choose a day").grid(row=1, column=1)
dayPopupMenu.grid(row=2, column=1)

excelPathLabel = tk.Label(mainframe, text="")
excelPathLabel.grid(row=4, column=1)

# on change dropdown value
def change_dropdown(*args):
    print('Selected day: ', dayStringVar.get())

# on selection of service
def change_service(*args):
    print('Selected option: ', optionVar.get())

# on browse for csv button click
def change_excel_path(*args):
    excel_path = tkFileDialog.askopenfilename(initialdir=os.path.expanduser('~'), title="Select file",)
    excelPathStringVar.set(excel_path)
    print('We got a csvpath:', excelPathStringVar.get())
    excelPathLabel.config(text=excelPathStringVar.get())

# make sure user has selected all the stuff
def get_choices():
    day_string = dayStringVar.get()
    excel_path_string = excelPathStringVar.get()
    option = optionVar.get()
    return day_string, excel_path_string, option

def run_grabber():
    day_string, excel_path_string, option = get_choices()
    content_grabber_lib.grab(day_string, excel_path_string, option)

# add a button to browse for the CSV file
browseButton = tk.Button(text="Browse for CSV file...", command=change_excel_path)
browseButton.grid(row=0, column=1)

# add a button to execute download
# goButton = tk.Button(text="Download content", command=lambda: grabber_lib.download_uploaded_works(dayStringVar, csvPathStringVar))
goButton = tk.Button(text="Run", command=run_grabber)
goButton.grid(row=0, column=2)

# link function to change dropdown
dayStringVar.trace('w', change_dropdown)

# link function to change option
optionVar.trace('w', change_service)

root.mainloop()