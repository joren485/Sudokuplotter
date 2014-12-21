#######################################################
#Made by: Joren Vrancken
#Description: sudoku solver with algorithme X 
#Last edit: 02-05-2013: added tutorial
#######################################################
#How to:
#Put your sudoku in the var named 'sudoku'.
#any known numbers as ints and unknown numbers as "x" with quotes
#######################################################
sudoku =[
["x","x","x",8,4,"x","x","x",9], 
["x","x",1,"x","x","x","x","x",5],        
[8,"x","x","x",2,1,4,6,"x"], 
[7,"x",8,"x","x","x","x",9,"x"], 
["x","x","x","x","x","x","x","x","x"], 
["x",5,"x","x","x","x",3,"x",1],  
["x",2,4,9,1,"x","x","x",7], 
[9,"x","x","x","x","x",5,"x","x"],
[3,"x","x","x",8,4,"x","x","x"]]
#######################################################
#Don't edit anything beyond this line
#######################################################
import time        
start_time = time.time()
print("starting the sudoku solver")
print("------sudoku to solve------")
for row in sudoku:
        string = ""
        for n in row:
                string+=str(n)+" "
        print(string)
print("-"*27)
print("Solutions")
print("-"*27)


def block(c):
	x=[0,0,c[2]]
	for i in range(2):
		if c[i] < 3:
			x[i] = 1
		if c[i] >= 3 and c[i] < 6:
			x[i] = 2
		if c[i] >= 6:
			x[i] = 3
	return ("b",x[0],x[1],x[2])

def dictcopy(dic):
	keys = list(dic.keys())
	values = list(dic.values())
	values = [list(i) for i in values]
	return dict(zip(keys,values))

def sudotoset(x):
	d = {}
	for i in range(len(x)):
		for j in range(len(x[i])):
			if x[i][j] == "x":
				for r in range(1,10):
					d[(i,j,r)] = []
			else:
				d[(i,j,x[i][j])]=[]
	for i in d.keys():
		d[i].append(("k",i[0],i[2]))
		d[i].append(("r",i[1],i[2]))
		d[i].append(block(i))
		d[i].append(("v",i[0],i[1]))
	return d

Set = sudotoset(sudoku)
values = []
matrix= {}
keys = sorted(list(Set.keys()))
for i in keys:
	for j in Set[i]:
		if j not in values:
			values.append(j)

for i in range(len(keys)):
	key = keys[i]
	matrix[key]=[]
	for j in values:
		if j in Set[key]:
			matrix[key].append(1)
		else:
			matrix[key].append(0)
del values,keys,Set,sudoku

sets = [[[],matrix,[]]]			
deleted= []
solution = []
step5=[]
solutioncount = 0
solved = False
while solved == False:
        if sets == []:
                solved = True
        for mx in sets:
                matrix = mx[1]
                if matrix == {}:
                        solutioncount+=1
                        print("Solution",solutioncount)
                        print("-"*27)
                        s = [[0]*9 for number in range(9)]
                        for solrow in sorted(mx[2]):
                                s[solrow[0]][solrow[1]]=solrow[2]
                        for solrow in s:
                                sudostring=""
                                for solel in solrow:
                                        sudostring+=str(solel)+" "
                                print(sudostring)
                        print("-"*27)
                        continue
                allcolumncount = []
                for i in range(len(list(matrix.values())[0])):
                        columncount = 0
                        rows = []
                        for j in sorted(matrix.keys()):
                                if matrix[j][i] == 1:
                                        columncount+=1
                                        rows.append(j)
                        allcolumncount.append([columncount,rows])
                columncountmin=[i[0] for i in allcolumncount]
                if min(columncountmin) == 0:
                        continue
                rows = allcolumncount[columncountmin.index(min(columncountmin))][1]
                step5.append([rows,matrix,mx[2]])
        sets = []

        for s in step5:
                for row in s[0]:
                        matrix=dictcopy(s[1])
                        delete=[]
                        for key in sorted(matrix.keys()):
                                for c in range(len(matrix[row])):
                                        if matrix[row][c] == 1 and matrix[key][c] == 1:
                                                delete.append(key)
                                                break
                        for key in delete:
                                del matrix[key]
		
                        delete = sorted([i for i in range(len(s[1][row])) if s[1][row][i] == 1],reverse=True)
                        for key in matrix.keys():
                                for d in delete:
                                        del matrix[key][d]
                        sets.append([[],matrix,s[2]+[row]])
        step5=[]
runtime = str(time.time()- start_time)
print("Solutions: "+str(solutioncount))
print("Runtime: "+runtime+" seconds.")
