from tkinter import *
import tkinter as tk

def convert_coord(board, size):
    i = 0
    j = 0
    step = int(506 / size)
    l = []
    points_draw = []
    k = []
    while i < len(board):
        cage = board[i][0]
        while j < len(cage):
            y = (cage[j][0] - 1) * step
            x = (cage[j][1] - 1) * step
            # one rectangle
            l.append((x, y))
            l.append((x + step, y))
            l.append((x, y + step))
            l.append((x + step, y + step))
            k.append(l)
            j += 1
            l = []
        points_draw.append(k)
        k = []
        j = 0
        i += 1
    return points_draw


def get_duplicates(x, y):
    temp = x + y
    unique_temp = list(set(temp))
    line = []
    for one in unique_temp:
        count = temp.count(one)
        if count > 1 and one not in line:
            line.append(one)
    return line

    
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

def begin_game():
    algorithm_type1.pack(side=tk.TOP)
    algorithm_type2.pack(side=tk.TOP)
    algorithm_type3.pack(side=tk.TOP)
    solve_button.pack(pady=20, padx=20)
    play_again_button.pack(pady=20, padx=20)
    selected(event=clicked)
    drop.pack_forget()
    myButton.pack_forget()


def play_again():
    algorithm_type1.pack_forget()
    algorithm_type2.pack_forget()
    algorithm_type3.pack_forget()
    canvas.pack_forget()
    solve_button.pack_forget()
    play_again_button.pack_forget()
    drop.pack(pady=20)
    myButton.pack(pady=20)
    v.set(0)


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

# radio buttons for choosing the algorithm
v = IntVar()
v.set(0)
algorithm_type1 = Radiobutton(root, text="Back Tracking", variable=v, value=1)
algorithm_type2 = Radiobutton(root, text="Forward checking", variable=v, value=2)
algorithm_type3 = Radiobutton(root, text="Arc consistency", variable=v, value=3)

root.mainloop()