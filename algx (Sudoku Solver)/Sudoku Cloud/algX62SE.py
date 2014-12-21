#####################################################
###SPECIAL SERVER EDITION OF ALGX PROGRAM###
#Made by: Joren Vrancken
#Description: sudoku solver with algorithm X
#Last edit: 03-08-2014: added unkown character and put everything non-function at the bottom
#######################################################
#Don't edit anything beyond this line
#######################################################
def formatsudoku(sudoku):
    sudoku = list(sudoku)
    sudoku = [sudoku[i:i+9] for i in range(0, len(sudoku), 9)]
    return sudoku

def formatsolution(solution):
    return "".join(str(value[2]) for value in sorted(solution))

def block(cell):
    """Calculate the block coordinates of a given cell, and format those into a block contains X tuple."""
    value=[0,0,cell[2]]
    for i in xrange(2):
        if cell[i] < 3:
            value[i] = 1
        if cell[i] >= 3 and cell[i] < 6:
            value[i] = 2
        if cell[i] >= 6:
            value[i] = 3
    return ("block",value[0],value[1],value[2])

def dictcopy(dic):
    """Deepcopy a dict object, with lists as values."""
    keys = list(dic.keys())
    values = [list(i) for i in dic.values()]
    return dict(zip(keys,values))

def sudo2set(sudoku):
    """Create a dict object with as keys (row,column,allpossible values) an as values a list
    containing the following: row contains value, column contains value, block contains value
    and cell is filled. The function also returns a list of all unique keys and values"""

    Set = {}
    keys = []
    values = []
    for row in xrange(9):
        for column in xrange(9):
            value = sudoku[row][column]
            if value == "x":
                for newvalue in xrange(1,10):
                    key = (row,column,newvalue)
                    value = [("row", row, newvalue),
                            ("column", column, newvalue),
                            block(key),
                            ("cell", row, column)]
                    Set[key] = value
                    keys.append(key)
                    values += value

            else:
                value = int(value)
                key = (row, column, value)
                value = [("row", row, value),
                        ("column", column, value),
                        block(key),
                        ("cell", row, column)]
                Set[key] = value
                keys.append(key)
                values += value
    return Set, keys, set(values)


def exactcover(matrix):
##Setting variables
##sets containts [ [ rows, main matrix, partial solution ] ]
    sets = [[[],matrix,[]]]
    all_solutions = []
    tempsets = []
    solved = False
    while solved == False:
##If there are no more sets, the exact cover has been found, thus all the solutions have been found.
        if sets == []:
            solved = True

        for set in sets:
            matrix = set[1]
##Step 1) If the matrix A is empty, the problem is solved; terminate successfully.
            if matrix == {}:
                solutionstring = formatsolution(set[2])
                all_solutions.append(solutionstring)
                continue
##Step 2) Otherwise choose a column c (deterministically)
##Count the 1's in every column.
            columncount = [i.count(1) for i in zip(*matrix.values())]

##Calculate the smallest number of 1's in any column.
            minimum = min(columncount)

##If the minimum is 0, there is no exact cover possible, thus terminate unsuccessfully.
            if minimum == 0:
                continue

##Take (one of) the columns with the fewest 1's.
            first_min_column_index = columncount.index(minimum)

##Step 3) Choose a row r such that Ar,c = 1 (detministically)
            rows = []
            for key in matrix:
                if matrix[key][first_min_column_index] == 1:
                    rows.append(key)
##Step 5) For each column j such that Ar,j = 1,
##              for each row i such that Ai,j = 1,
##                      delete row i from matrix A;
##              delete column j from matrix A.
            for row in rows:

##The matrix in a lot of sets is the same, so first (custom) deepcopy the matrix.
                matrix = dictcopy(set[1])

##For every column in row with the value 1, append to deletecolumns.
                deletecolumns = []
                for i in xrange(len(matrix[row])):
                    if matrix[row][i] == 1:
                        deletecolumns.append(i)
##For every row with the value 1 in a column in deletecolumn, append to deleterows.
                deleterows = []
                for key in matrix:
                    for column in deletecolumns:
                        if matrix[key][column] == 1:
                            deleterows.append(key)
                            break
##Remove the deleterows.
                for deleterow in deleterows:
                    del matrix[deleterow]

##Remove the deletecolumns from the remaining rows. The list is reversed so that the indexes don't change.
                for column in deletecolumns[::-1]:
                    for key in matrix:
                        del matrix[key][column]

##Step 4) Include r in the partial solution.
##Put the potential sets in a temporary list.
                tempsets.append([[],matrix,set[2]+[row]])
##Remove the empty and unsuccessful sets, by only putting the potential sets into the new list.
        sets = [i for i in tempsets]
        tempsets = []
    return all_solutions

def solve(sudoku):

    Set,keys,values = sudo2set(sudoku)

##Create the matrix from Set.
    matrix = {}
    for i in xrange(len(keys)):
        key = keys[i]
        matrix[key]=[]
        for value in values:
            if value in Set[key]:
                matrix[key].append(1)
            else:
                matrix[key].append(0)

    return exactcover(matrix)
