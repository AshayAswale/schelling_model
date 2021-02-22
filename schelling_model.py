import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random


p = 0.8
t1 = 4
t2 = 4
x_val = 2
o_val = 4
t1_ratio = 1.0  # When you want 0.8/0.2 ratio of t1 and t2, set this as 0.8

def generateBoard(x, y):
    board = np.zeros([x,y])
    total_cells = x*y
    filled_cells = int(total_cells*p)
    x_o_pos = random.sample(range(1, total_cells), filled_cells)
    flag = True
    for cell in x_o_pos:
        row, col = divmod(cell, x)
        if flag:
            board[row, col] = x_val
        else:
            board[row, col] = o_val
        flag = not flag
    return board


def visualizeBoard(board):
    plt.imshow(board)
    plt.show()


def getUnsatisfiedCells(board, row):
    x_unsatis = []
    o_unsatis = []
    x_sati_cell = []
    o_sati_cell = []
    l_row = max(row-1, 0)
    u_row = min(row+2, len(board))

    for col in range(len(board[0])):
        l_col = max(col-1, 0)
        u_col = min(col+2, len(board[0]))
        neighbours = board[l_row:u_row, l_col:u_col].flatten()
        main_val = board[row,col]
        if main_val == x_val:
            count = np.count_nonzero(neighbours == x_val) - 1
            if count < t1:
                x_unsatis.append(col)
        elif main_val == o_val:
            count = np.count_nonzero(neighbours == o_val) - 1
            if count < t1:
                o_unsatis.append(col)
        else:
            x_nbrs = np.count_nonzero(neighbours == x_val)
            o_nbrs = np.count_nonzero(neighbours == o_val)
            if x_nbrs>=t1:
                x_sati_cell.append(col)
            if o_nbrs>=t1:
                o_sati_cell.append(col)

    # print("Unsatisfied X:", x_unsatis)
    # print("Unsatisfied O:", o_unsatis)
    # print("Poses for   X:", x_sati_cell)
    # print("Poses for   O:", o_sati_cell)
    # print("\n")

    return x_unsatis, o_unsatis, x_sati_cell, o_sati_cell

def switchingAlgo(board, row, val, unsatis, sati_cell, other_sati_cell):
    for uns_cell in unsatis:
        if len(sati_cell)>0:
            cell = sati_cell.pop(0)
            board[row, cell] = val
            board[row, uns_cell] = 0
            if cell in other_sati_cell: other_sati_cell.remove(cell)
        else:
            break

def rearrangeBoardRow(board, row, x_unsatis, o_unsatis, x_sati_cell, o_sati_cell):
    o_sati_cell = switchingAlgo(board, row, x_val, x_unsatis, x_sati_cell, o_sati_cell)
    switchingAlgo(board, row, o_val, o_unsatis, o_sati_cell, x_sati_cell)
        

def manageBoard(board):
    not_solved = False
    for row in range(len(board)):
        x_unsatis, o_unsatis, x_sati_cell, o_sati_cell = getUnsatisfiedCells(board, row)
        rearrangeBoardRow(board, row, x_unsatis, o_unsatis, x_sati_cell, o_sati_cell)
        if(len(x_unsatis)>0 or len(o_unsatis)>0):
            not_solved = True
    return not_solved


if __name__ == '__main__':

    board = generateBoard(50,50)
    # print(board, "\n\n\n")

    visualizeBoard(board)
    not_solved = True
    counter = 0
    sim_counts = 10
    while(not_solved and counter<sim_counts):
        not_solved = manageBoard(board)
        # print(counter)
        counter += 1
    visualizeBoard(board)
