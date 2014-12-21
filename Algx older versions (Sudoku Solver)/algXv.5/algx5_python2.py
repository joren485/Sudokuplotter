#######################################################
#Made by: Joren Vrancken
#Description: sudoku solver with algorithm X 
#Last edit: 1-08-2014: small optimalization, rewrote step 5
#######################################################
#How to:
#Put your sudoku in the var named 'sudoku'.
#any known numbers as ints and unknown numbers as "x" with quotes
#######################################################
sudoku =[
['x', 8, 1, 'x', 6, 'x', 'x', 'x', 7],
['x', 'x', 'x', 3, 'x', 2, 8, 'x', 'x'],
[6, 'x', 7, 'x', 'x', 8, 'x', 'x', 9],
[7, 'x', 4, 'x', 'x', 'x', 'x', 5, 1],
['x', 3, 'x', 'x', 5, 9, 'x', 'x', 'x'],
[9, 5, 'x', 'x', 'x', 'x', 'x', 4, 'x'],
['x', 'x', 'x', 'x', 2, 'x', 1, 9, 4],
['x', 'x', 'x', 7, 'x', 4, 3, 'x', 5],
[4, 'x', 5, 'x', 3, 'x', 'x', 'x', 'x']]

#######################################################
#Don't edit anything beyond this line
#######################################################
import time
start_time = time.time()
print "starting the sudoku solver"
print "-----sudoku to solve-----" 
for row in sudoku:
        string = ""
        for n in row:
                string+=str(n)+" "
        print(string)
print "-"*25 
print "Solutions"
print "-"*25 

def block(key):
	value=[0,0,key[2]]
	for i in xrange(2):
		if key[i] < 3:
			value[i] = 1
		if key[i] >= 3 and key[i] < 6:
			value[i] = 2
		if key[i] >= 6:
			value[i] = 3
	return ("block",value[0],value[1],value[2])

def dictcopy(dic):
	keys = list(dic.keys())
	values = [list(i) for i in dic.values()]
	return dict(zip(keys,values))

def sudotoset(sudoku):
	"""Create a dict object with as keys (row,column,allpossible values) an as values a list 
	containing the following: row contains value, column contains value, block contains value 
	and cell is filled"""
	
	set = {}
	for row in xrange(9):
		for column in xrange(9):
			value = sudoku[row][column]
			if value == "x":
				for newvalue in xrange(1,10):
					key = (row,column,newvalue)
					set[key] = [("row",row,newvalue)]
					set[key].append(("column",column,newvalue))
					set[key].append(block(key))
					set[key].append(("cell",row,column))
					
			else:
				key = (row,column,value)	
				set[key] = [("row",row,value)]
                                set[key].append(("column",column,value))
				set[key].append(block(key))
                                set[key].append(("cell",row,column))
	return set


def printsolution(solution,solutioncount):
	print "Solution: " + str(solutioncount)
        print "-"*25
        emptysudo = [[0]*9 for number in xrange(9)]
        for solrow in solution:
		emptysudo[solrow[0]][solrow[1]]=solrow[2]
        for solrow in emptysudo:
		sudostring=""
		for solel in solrow:
				sudostring+=str(solel)+" "
		print(sudostring)
        print("-"*25)

Set = sudotoset(sudoku)
values = []
matrix= {}
keys = list(Set.keys())

for i in keys:
	for j in Set[i]:
		if j not in values:
			values.append(j)

for i in xrange(len(keys)):
	key = keys[i]
	matrix[key]=[]
	for j in values:
		if j in Set[key]:
			matrix[key].append(1)
		else:
			matrix[key].append(0)

sets = [[[],matrix,[]]]	
solution = []
tempsets = []
solutioncount = 0
solved = False
while solved == False:
        if sets == []:
                solved = True
        
	for mx in sets:
                matrix = mx[1]
##Step 1) if the matrix is empty, the problem is solved; terminate successfully. 
		if matrix == {}:
                        solution = mx[2]
			solutioncount += 1
                     	printsolution(solution,solutioncount)
			continue
##Step 2)
		columns = zip(*matrix.values())
		columncount = [i.count(1) for i in columns]
                
		minimum = min(columncount)
		
		if minimum == 0:
                        continue

                first_min_column_index = columncount.index(minimum)
##Step 3)		
		rows = []
		for key in matrix:
			if matrix[key][first_min_column_index] == 1:
				rows.append(key)
##Step 5)
                for row in rows:
                        matrix = dictcopy(mx[1])
                        
			onecount = matrix[row].count(1)
			
			deletecolumns = []
			for i in xrange(len(matrix[row])):
				if matrix[row][i] == 1:
                			deletecolumns.append(i)
			
			deleterows = []
			for key in matrix:
        			for column in deletecolumns:
                			if matrix[key][column] == 1:
                        			deleterows.append(key)
                        			break
			
			for deleterow in deleterows:
        			del matrix[deleterow]

			for column in deletecolumns[::-1]:
        			for key in matrix:
                			del matrix[key][column]
##Step) 4		
			tempsets.append([[],matrix,mx[2]+[row]])
        sets = []
	sets = [i for i in tempsets]
	tempsets = []

runtime = str(time.time() - start_time)
print "Solutions: " + str(solutioncount)
print "Runtime: " + runtime + " seconds."
