from tkinter import *
import tkinter as tk


def selected(event):
    global size
    if clicked.get() == '3x3':
        size = 3
        draw(3)
    elif clicked.get() == '4x4':
        size = 4
        draw(4)
    elif clicked.get() == '5x5':
        size = 5
        draw(5)
    elif clicked.get() == '6x6':
        size = 6
        draw(6)
    elif clicked.get() == '7x7':
        size = 7
        draw(7)
    elif clicked.get() == '8x8':
        size = 8
        draw(8)
    elif clicked.get() == '9x9':
        size = 9
        draw(9)


# root initiallization
root = tk.Tk()
root.title('KENKEN Puzzle Game')
root.geometry("600x700")

#initial value
board=[]
size=3

# canvas for drawing squares of the game
canvas = Canvas(root, width=505, height=505)
canvas.xview_moveto(.5)
canvas.yview_moveto(.5)

# variable to store the clicked value in the select button
option = [
    "3x3",
    "4x4",
    "5x5",
    "6x6",
    "7x7",
    "8x8",
    "9x9",
]
clicked = StringVar()
clicked.set(option[0])

# buttons
drop = OptionMenu(root, clicked, *option)
myButton = Button(root, text="Play", command=begin_game)
solve_button = Button(root, text="Solve", command=solve)
play_again_button = Button(root, text="Play Again", command=play_again)

# show at the beginning
drop.pack(pady=20)
myButton.pack(pady=20)


root.mainloop()