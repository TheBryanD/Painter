#imports
import tkinter as tk
from tkinter import Entry, StringVar, Variable, font, colorchooser, filedialog
from tkinter.constants import CURRENT, HORIZONTAL, LEFT, ROUND, VERTICAL
import PIL
from PIL import ImageGrab
import socket
import struct
import threading as thread
from _thread import *
import json

#create tkinter window
rootWindow = tk.Tk()
rootWindow.title("Painter")
rootWindow.geometry("1280x720")
    

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def threaded(c):
    while True:
        print()


def setPortAndIp():
    global ip, port
    ip = ipEntry.get()
    port = portEntry.get()        

def create_packet(**kwargs):
    packet = struct.pack("!i", kwargs.get("format"))  # pack the FIN
    packet += struct.pack("!i", kwargs.get("type"))
    packet += struct.pack("!512s", kwargs.get("payload"))
    return packet

def Connect():
    #create variables and a new window for connection
    ip = '192.168.1.107'
    port = 60
    connectWindow = tk.Tk()
    connectWindow.title("Connect")
    connectWindow.geometry("700x500")

    #get the ip and port using entry boxes
    ipLabel = tk.Label(connectWindow, text="IP: ").place(relx=0.1, rely=0.1)
    global ipEntry
    ipEntry = tk.Entry(connectWindow, highlightcolor="#ffffff")
    ipEntry.place(relx=0.2, rely=0.1)
    portLabel = tk.Label(connectWindow, text="Port: ").place(relx=0.1, rely=0.2)
    global portEntry
    portEntry = tk.Entry(connectWindow, highlightcolor="#ffffff")
    portEntry.place(relx=0.2, rely=0.2)
    connectButton = tk.Button(connectWindow, text="Connect", command=lambda : setPortAndIp())
    connectButton.place(relx=0.3, rely=0.25)



    try:
        client.connect((ip, port))
        packetToSend = create_packet(format='iis', type=1, payload=canvas.toDataURL())
        client.sendall(packetToSend)
    except Exception as ex:
        print(ex)
        return

    #Create and send packet to 
    payload = ''
    return





def Save(event):
    file = filedialog.asksaveasfilename(filetypes=[('Portable Network Graphics','*.png')])
    if file:
        x = canvas.winfo_rootx() + canvas.winfo_x()
        y = canvas.winfo_rooty + canvas.winfo_y()
        x1 = x + canvas.winfo_width()
        y1 = y + canvas.winfo_height()

        ImageGrab.grab().crop((x,y,x1,y1)).save(file + '.png')

#Get coords of mouse on created window
def motion(event):
    try:
        #rootWindow.winfo_pointerxy() gives overall coords of whole screen
        cursorPosition = rootWindow.winfo_pointerxy()
        print("X: " + str(cursorPosition[0]) + "\nY: " + str(cursorPosition[1]))
        #Event x and y are local window coords 
        print("Event X: " + str(event.x))
        print("Event Y:" + str(event.y))

        return {event.x, event.y}

    except Exception as ex:
        print(ex)
        return

def locatexy(event):
    global curr_x
    global curr_y 
    curr_y = event.y
    curr_x = event.x
    
def updatePencilScale(event):
    global pencilScaleInt
    pencilScaleInt = pencilScale.get()   

def addLine(event):
    global curr_x, curr_y
    pencilScaleInt = pencilScale.get()
    canvas.create_line(curr_x,curr_y, event.x, event.y, fill=color.get(), tags="line", width=pencilScaleInt, capstyle=ROUND)
    curr_x = event.x
    curr_y = event.y
    
def clearCanvas():
    canvas.delete("all")

def updateEraserScale(event):
    global eraserScaleInt
    eraserScaleInt = eraserScale.get() 

def eraseLine(event):
    global curr_x, curr_y
    eraserScaleInt = eraserScale.get()
    canvas.addtag_enclosed("delete", event.x+eraserScaleInt+10, event.y+eraserScaleInt+10, event.x-eraserScaleInt-10, event.y-eraserScaleInt-10)
    canvas.delete("delete")
    curr_x = event.x
    curr_y = event.y

def getColor(event):
    canvas.addtag_enclosed("colorDropped", event.x+5, event.y+5, event.x-5, event.y-5)
    line = canvas.find_withtag('colorDropped')
    global getColorOn
    getColorOn = True
    
    

# Create a frame for the colors to be selected
colorFrame = tk.Frame(rootWindow)
colorFrame.place(relheight=1, relwidth=0.15)

labelColor = tk.Label(colorFrame, text="Colors", font=("Bastion", 20), fg="#2e1b15", bg="#f5cd9c", padx=100, pady=100)
labelColor.place(relheight=0.1, relwidth=1, rely=0)

#Variable for color
color = tk.StringVar(colorFrame, "black")

#color chooser
def askForColor():
    color.set(colorchooser.askcolor()[1])

#Buttons
#red 
redButton = tk.Radiobutton(colorFrame, bg="#Ed1010", variable=color, value="#Ed1010", pady=20)
redButton.place(relheight=0.083, relwidth=1, rely=0.1)
#orange
orangeButton = tk.Radiobutton(colorFrame, bg="#Ff851b", variable=color, value="#Ff851b", pady=20)
orangeButton.place(relheight=0.083, relwidth=1,rely=0.183)
#yellow
yellowButton = tk.Radiobutton(colorFrame, bg="#E1ed10", variable=color, value="#E1ed10", pady=20)
yellowButton.place(relheight=0.083, relwidth=1, rely=0.266)
#lime
limeButton = tk.Radiobutton(colorFrame, bg="#2ecc40", variable=color, value="#2ecc40", pady=20)
limeButton.place(relheight=0.083, relwidth=1,rely=0.349)
#green
greenButton = tk.Radiobutton(colorFrame, bg="#20ed10", variable=color, value="#20ed10", pady=20)
greenButton.place(relheight=0.083, relwidth=1,rely=0.432)
#blue
blueButton = tk.Radiobutton(colorFrame, bg="#1075ed", variable=color, value="#1075ed", pady=20)
blueButton.place(relheight=0.083, relwidth=1, rely=0.515)
#Teal
orangeButton = tk.Radiobutton(colorFrame, bg="#39cccc", variable=color, value="#39cccc", pady=20)
orangeButton.place(relheight=0.083, relwidth=1,rely=0.598)
#purple
purpleButton = tk.Radiobutton(colorFrame, bg="#Bb10ed", variable=color, value="#Bb10ed", pady=20)
purpleButton.place(relheight=0.083, relwidth=1,rely=0.681)
#Brown
brownButton = tk.Radiobutton(colorFrame, bg="#8b7355", variable=color, value="#8b7355", pady=20)
brownButton.place(relheight=0.083, relwidth=1, rely=0.764)
#white
whiteButton = tk.Radiobutton(colorFrame, bg="#f8f8ff", variable=color, value="#f8f8ff", pady=20)
whiteButton.place(relheight=0.083, relwidth=1, rely=0.847)
#black
blackButton = tk.Radiobutton(colorFrame, bg="black", variable=color, value="black", pady=20)
blackButton.place(relheight=0.083, relwidth=1, rely=0.93)





#Config
configFrame = tk.Frame(rootWindow, bg="#f5cd9c")
configFrame.place(relheight=1, relwidth=0.10, relx=0.90)

#Eraser Size
eraserScale = tk.Scale(configFrame, from_=100, to=5, tickinterval=5, orient=VERTICAL, command=updateEraserScale, bg="#f5cd9c")
eraserScale.set(1)
eraserScale.place(relheight=0.5, relwidth=0.5, rely=0)
eraserScaleLabel = tk.Label(configFrame, text="Eraser Size", font=("Bastion", 8), bg="#f5cd9c")
eraserScaleLabel.place(relheight=0.1, relwidth=0.5, rely=0.5)

#Pencil Size
pencilScale = tk.Scale(configFrame, from_=100, to=5, tickinterval=5, orient=VERTICAL, command=updatePencilScale, bg="#f5cd9c")
pencilScale.set(1)
pencilScale.place(relheight=0.5, relwidth=0.5, relx=0.5)
pencilScaleLabel = tk.Label(configFrame, text="Pencil Size", font=("Bastion", 8), bg="#f5cd9c")
pencilScaleLabel.place(relheight=0.1, relwidth=0.5, rely=0.5, relx=0.5)

#Color Chooser
colorChooserConfigButton = tk.Button(configFrame, text="Custom Color", command=askForColor, justify=LEFT)
colorChooserConfigButton.place(rely=0.6, relx=0.1)

#Color Dropper
colorDropper = tk.Button(configFrame, text="Dropper", command=getColor)
colorDropper.place(rely=0.7, relx=0.1)

#create a canvas that can be drawn on
canvas = tk.Canvas(rootWindow, bg="#f8f8ff")
canvas.bind('<Motion>', motion)
canvas.bind("<Button-1>", locatexy)
canvas.bind("<B1-Motion>", addLine)
canvas.bind("<Button-3>", locatexy)
canvas.bind("<B3-Motion>", eraseLine)
canvas.place(relheight=1, relwidth=0.75, relx=0.15)



#menu
menubar = tk.Menu(rootWindow, title="Menu")
#Filemenu
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=Save)
filemenu.add_command(label="Connect", command=Connect)
menubar.add_cascade(label="File", menu=filemenu)
#EditMenu
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Clear Canvas", command=clearCanvas)
menubar.add_cascade(label="Edit", menu=editmenu)
rootWindow.config(menu=menubar)
editmenu.add_command(label="Choose Custom Color", command=askForColor)

#main window loop
rootWindow.mainloop()

