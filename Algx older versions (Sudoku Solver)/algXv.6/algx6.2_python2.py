#####################################################
#Made by: Joren Vrancken
#Description: sudoku solver with algorithm X
#Last edit: 03-08-2014: added unkown character and put everything non-function at the bottom
#######################################################
#How to:
#Put your sudoku in the variable named 'sudoku'.
#any known numbers as ints and unknown numbers as "x" with quotes
#######################################################

##unkown/empty digit character
z = 'x'

##sudoku = [
##[z, 8, 1, z, 6, z, z, z, 7],
##[z, z, z, 3, z, 2, 8, z, z],
##[6, z, 7, z, z, 8, z, z, 9],
##[7, z, 4, z, z, z, z, 5, 1],
##[z, 3, z, z, 5, 9, z, z, z],
##[9, 5, z, z, z, z, z, 4, z],
##[z, z, z, z, 2, z, 1, 9, 4],
##[z, z, z, 7, z, 4, 3, z, 5],
##[4, z, 5, z, 3, z, z, z, z]]


sudoku = [
[8, z, z, z, z, z, z, z, z],
[z, z, 3, 6, z, z, z, z, z],
[z, 7, z, z, 9, z, 2, z, z],
[z, 5, z, z, z, 7, z, z, z],
[z, z, z, z, 4, 5, 7, z, z],
[z, z, z, 1, z, z, z, 3, z],
[z, z, 1, z, z, z, z, 6, 8],
[z, z, 8, 5, z, z, z, 1, z],
[z, 9, z, z, z, z, 4, z, z]]

##sudoku = [
##[z, z, z, 7, 1, z, 8, z, z],
##[z, 5, z, z, 6, z, 1, z, z],
##[8, z, 2, z, z, z, z, z, z],
##[z, z, 9, 1, 4, z, z, z, 3],
##[z, z, z, 9, z, 6, 4, z, z],
##[z, z, z, z, 3, 7, 2, 1, z],
##[z, 9, z, 6, z, z, z, 7, z],
##[7, z, z, z, z, 3, z, 5, z],
##[z, z, 5, z, z, z, z, z, z]]


#######################################################
#Don't edit anything beyond this line
#######################################################
from time import time

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
                key = (row, column, value)
                value = [("row", row, value),
                        ("column", column, value),
                        block(key),
                        ("cell", row, column)]
                Set[key] = value
                keys.append(key)
                values += value
    return Set, keys, set(values)

def printsolution(solution,solutioncount):
    """Print out a solution."""
    print "Solution: " + str(solutioncount)
    print "-"*25

    sudostring = ""
    for i in sorted(solution):
        sudostring += str(i[2]) + " "

    solved_sudoku = [sudostring[i:i+18] for i in xrange(0, 81*2, 18)]
    for i in solved_sudoku:
        print i

    print "-"*25

def exactcover(matrix,solutionprocesser):
##Setting variables
##sets containts [ [ rows, main matrix, partial solution ] ]
    sets = [[[],matrix,[]]]
    tempsets = []
    solutioncount = 0
    solved = False
    while solved == False:
##If there are no more sets, the exact cover has been found, thus all the solutions have been found.
        if sets == []:
            solved = True

        for set in sets:
            matrix = set[1]
##Step 1) If the matrix A is empty, the problem is solved; terminate successfully.
            if matrix == {}:
                solution = set[2]
                solutioncount += 1
                solutionprocesser(solution,solutioncount)
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

##Step 3) Choose a row r such that Ar,c = 1 (nondetministically)
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

##Print out the runtime and the amount of solutions.
    print "Solutions: " + str(solutioncount)

if __name__ == "__main__":
    start_time = time()

    print "Starting the sudoku solver"
    print "-----Sudoku to solve-----"
    for row in sudoku:
        string = ""
        for n in row:
            string += str(n)+" "
        print string
    print "-"*25
    print "Solutions"
    print "-"*25

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

    exactcover(matrix,printsolution)

    print "Runtime: " + str(round(time() - start_time,2)) + " seconds."
