import numpy as np
import matplotlib.pyplot as plt
import random

p = 0.8         # Fraction of cells filled
t1 = 3          # Satisfaction threshold
t2 = 5          # Will only be used if t1_ratio is not 1. Second satisfaction Threshold
t1_ratio = 0.8  # When you want 0.8/0.2 ratio of t1 and t2, set this as 0.8
rounds = 1000   # Maximum rounds that should run

x_val = [50,49]
o_val = [100,99]

def generateBoard(x, y):
    board = np.zeros([x,y])
    total_cells = x*y
    filled_cells = int(total_cells*p)
    x_o_pos = random.sample(range(1, total_cells), filled_cells)
    
    flag = True
    for cell in x_o_pos:
        row, col = divmod(cell, x)
        if flag:
            board[row, col] = random.choices(x_val, weights=(t1_ratio, 1-t1_ratio), k=1)[0]
        else:
            board[row, col] = random.choices(o_val, weights=(t1_ratio, 1-t1_ratio), k=1)[0]
        flag = not flag
    return board


def visualizeBoard(board):
    plt.imshow(board)
    plt.show()


def saveBoard(board, i):
    plt.imshow(board)
    file_name = str(i)
    plt.savefig(file_name)


def getUnsatisfiedCells(board, row, unsatis, empty_cell):
    l_row = max(row-1, 0)
    u_row = min(row+2, len(board))

    for col in range(len(board[0])):
        l_col = max(col-1, 0)
        u_col = min(col+2, len(board[0]))
        neighbours = board[l_row:u_row, l_col:u_col].flatten()
        main_val = board[row,col]

        if main_val == 0:
            x_nbrs = np.count_nonzero(neighbours == x_val[0])
            x_nbrs += np.count_nonzero(neighbours == x_val[1])
            o_nbrs = np.count_nonzero(neighbours == o_val[0])
            o_nbrs += np.count_nonzero(neighbours == o_val[1])

            empty_cell = np.concatenate((empty_cell, [[row, col, x_nbrs, o_nbrs]]))
        else:
            is_normal = (main_val%10==0)
            sub_val = (main_val - 1) if (is_normal) else main_val +1
            count = np.count_nonzero(neighbours == main_val) - 1
            count += np.count_nonzero(neighbours == sub_val)
            if (is_normal):
                if (count<t1):
                    unsatis = np.concatenate((unsatis, [[row, col]]))
            else:
                if (count<t2):
                    unsatis = np.concatenate((unsatis, [[row, col]]))
    return unsatis, empty_cell


def getNearestEmptyIndex(board, empty_cell, agent, main_val):
    col = 2 if (main_val in x_val) else 3
    is_normal = (main_val%10)==0
    t = t1 if (is_normal) else t2
    valid_cells = empty_cell[np.where(empty_cell[:,col]>=t)]

    if not (len(valid_cells) > 0):
        return []
    valid_cells = valid_cells[:, 0:2]
    distances = np.sum(valid_cells - agent, axis=1)
    final_cell = valid_cells[np.argmin(distances)]
    
    return np.where(np.all(empty_cell[:,0:2] == final_cell, axis=1))


def swapToNearest(board, empty_cell, agent, main_val):
    nearest_index = getNearestEmptyIndex(board, empty_cell, agent, main_val)
    # print(nearest_index)
    available = False
    if len(nearest_index) > 0:
        board[agent[0], agent[1]] = 0
        nearest_cell = empty_cell[nearest_index[0][0], 0:2]
        board[nearest_cell[0], nearest_cell[1]] = main_val

        empty_cell[nearest_index[0][0], 0:2] = agent
        available = True
    return available
     

def getSatisfactionLists(board):
    not_solved = False
    unsatis = np.array([])
    empty_cell = np.array([])
    once = True
    
    for row in range(len(board)):
        if once:
            unsatis = np.array([[0,0]])
            empty_cell = np.array([[0,0,0,0]])
        unsatis, empty_cell = getUnsatisfiedCells(board, row, unsatis, empty_cell)
        if once:
            unsatis = unsatis[1:]
            empty_cell = empty_cell[1:]
            once = False
    return unsatis, empty_cell


def updateEmptyCell(board, empty_cell):
    for i, cell in enumerate(empty_cell):
        row = cell[0]
        col = cell[1]
        l_row = max(row-1, 0)
        u_row = min(row+2, len(board))
        l_col = max(col-1, 0)
        u_col = min(col+2, len(board[0]))

        neighbours = board[l_row:u_row, l_col:u_col].flatten()

        x_nbrs = np.count_nonzero(neighbours == x_val[0])
        x_nbrs += np.count_nonzero(neighbours == x_val[1])
        o_nbrs = np.count_nonzero(neighbours == o_val[0])
        o_nbrs += np.count_nonzero(neighbours == o_val[1])

        empty_cell[i] = [row, col, x_nbrs, o_nbrs]
        

def manageBoard(board):
    unsatis, empty_cell = getSatisfactionLists(board)
    one_swapped = False
    for i in range(len(unsatis)):
        agent = unsatis[i]
        main_val = board[agent[0], agent[1]]
        swapped = swapToNearest(board, empty_cell, agent, main_val)
        if(swapped):
            one_swapped = True
        updateEmptyCell(board, empty_cell)
    if (len(unsatis) == 0) or (not one_swapped):
        if((len(unsatis) == 0)):
            print("\n\nNo one is unhappy anymore!! :D")
        else:
            print("\n\nNo available free space makes anyone happy anymore. :(")
        return True
    return False


if __name__ == '__main__':

    board = generateBoard(50,50)
    # print(board, "\n\n\n")
    print("Visualizing the board\nPlease close the window to start the code\n\n")
    visualizeBoard(board)

    # saveBoard(board, -1)
    for i in range(rounds):
        if(manageBoard(board)):
            print("\nSolved in ", i, " steps")
            break
        # saveBoard(board, i)

    # print("############")
    # print(board)
    visualizeBoard(board)
