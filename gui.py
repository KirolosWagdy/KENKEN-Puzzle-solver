from tkinter import *
import tkinter as tk
from generator import generate_board
from kenken import main_algorithm


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


def merge_cells(board, size):
    points_draw = convert_coord(board, size)
    i = 0
    j = 0
    l = []
    while i < len(points_draw):
        if len(points_draw[i]) > 1:
            while j < len(points_draw[i]) - 1:
                line = get_duplicates(points_draw[i][j], points_draw[i][j + 1])
                if len(line) != 0:
                    l.append(line)
                j += 1
            if len(points_draw[i]) == 4:  # if cages are square
                line = get_duplicates(points_draw[i][0], points_draw[i][3])
                if len(line) != 0:
                    l.append(line)
        j = 0
        i += 1
    return l


def get_coord(t, size):
    step = int(506 / size)
    y = (t[1] - 1) * step
    x = (t[0] - 1) * step
    return (y, x)


def dict_value(diction):
    list1 = []
    list_value = []

    for key, value in diction.items():
        for c in range(len(key)):
            list1.append((key[c], value[c]))

    list1.sort()

    for k in range(len(list1)):
        list_value.append(list1[k][1])
    return list_value


def draw(size):
    global board
    board = generate_board(size)
    points = merge_cells(board, size)
    canvas.delete('all')
    # create squares on board
    count = 0
    step = int(506 / size)
    cage_x = step / 3.25
    cage_x1 = step / 2.5
    cage_y = step / 4
    a = step / 2
    b = step / 2
    font_size = int(((step * 15) / (168)) * 2)
   #draw board squares
    for i in range(0, 506, step):
        for j in range(0, 506, step):
            x = j + step
            y = i + step
            count += 1
            if size == 7 or size == 8 or size == 9:
                canvas.create_rectangle(j, i, x, y, width=4)
            else:
                canvas.create_rectangle(j, i, x, y, width=7)
            if (x > 506) or (y > 506):
                continue
            else:
                a += step
        count -= 1
        a = step / 2
        b += step
    #write operation 
    for i in range(len(board)):
        numb = abs(board[i][2])
        opp = board[i][1]
        textt = str(numb) + opp
        first = board[i][0][0]
        for j in range(len(board[i][0])):            
            mini = min(first, board[i][0][j])
            first = mini
        co = get_coord(mini, size)
        if size == 8 or size == 9:
            position_x = co[0] + cage_x1
            position_y = co[1] + cage_y
        else:
            position_x = co[0] + cage_x
            position_y = co[1] + cage_y
        
        if opp == '.':
            canvas.create_text((position_x, position_y), text=str(numb), font=(f'Helvetica {font_size} bold'))
            # continue
        elif opp == '*':
            opp = '×'
            textt = str(numb) + opp
            canvas.create_text((position_x, position_y), text=textt, font=(f'Helvetica {font_size} bold'))
        elif opp == '/':
            opp = '÷'
            textt = str(numb) + opp
            canvas.create_text((position_x, position_y), text=textt, font=(f'Helvetica {font_size} bold'))
        elif opp == '-':
            opp = '–'
            textt = str(numb) + opp
            canvas.create_text((position_x, position_y), text=textt, font=(f'Helvetica {font_size} bold'))
        else:
            canvas.create_text((position_x, position_y), text=textt, font=(f'Helvetica {font_size} bold'))
    #merge cells - draw cages
    for point in points:
        if size == 7 or size == 8 or size == 9:
            canvas.create_line(point[0][0], point[0][1], point[1][0], point[1][1], width=4, fill="white")
            canvas.create_line(point[0][0], point[0][1], point[1][0], point[1][1])
        else:
            canvas.create_line(point[0][0], point[0][1], point[1][0], point[1][1], width=7, fill="white")
            canvas.create_line(point[0][0], point[0][1], point[1][0], point[1][1])
    #draw outline 
    canvas.create_line(0, 505, 0, 0, width=10)
    canvas.create_line(0, 505, 505, 505, width=10)
    canvas.create_line(0, 0, 505, 0, width=10)
    canvas.create_line(505, 505, 505, 0, width=10)
    canvas.pack()


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


def pop_window():
    pop = tk.Toplevel()
    pop.title("Error")
    pop.geometry("300x150")
    pop.config(bg="white")
    # Create a Label Text
    label = Label(pop, text="Please choose an algorithm \n to solve with.",
    font=('Aerial', 15))
    label.pack(pady=20)
    # Add a Frame
    frame = Frame(pop, bg="gray71")
    frame.pack(pady=10)


def solve():
    bk = False
    fc = False
    ac = False
    flag = 0
    color = ['red', 'blue', '#03c03c']
    if v.get() == 1:
        bk = True
        # print("BT")
        assignment = main_algorithm(size, board, "BT")
    elif v.get() == 2:
        fc = True
        # print("BT+FC")
        assignment = main_algorithm(size, board, "BT+FC")
    elif v.get() == 3:
        ac = True
        # print("BT+AC")
        assignment = main_algorithm(size, board, "BT+AC")
    elif v.get() == 0:
        pop_window()
        flag = 1

    if flag == 0:
        #write solution
        solution = dict_value(assignment)
        count = 0
        step = int(506 / size)
        a = step / 2
        b = step / 1.5
        for i in range(0, 506, step):
            for j in range(0, 506, step):
                x = j + step
                y = i + step
                count += 1
                if (x > 506) or (y > 506):
                    continue
                else:
                    if bk == True:
                        canvas.create_text((a,b), text=solution[count-1], fill=color[0], font=('Helvetica 20'))
                    if fc == True:
                        canvas.create_text((a,b), text=solution[count-1], fill=color[1], font=('Helvetica 20'))
                    if ac == True:
                        canvas.create_text((a,b), text=solution[count-1], fill=color[2], font=('Helvetica 20'))
                    a += step
            count -= 1
            a = step / 2
            b += step
        bk = False
        fc = False
        ac = False
        canvas.pack()


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