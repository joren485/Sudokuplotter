from matrix import *
import copy
s={"A":[1,3,6],"B":[1,5],"C":[3,7],"D":[2,4,5,7],"E":[1,4],"F":[2,4,6]}
##s={"A":[1,4,7],"B":[1,4],"C":[4,5,7],"D":[3,5,6],"E":[2,3,6,7],"F":[2,7]}

S =copy.deepcopy(s)
U = [1,2,3,4,5,6,7]
masters = [build(S,U)]

sol = []
solved = False
while solved != True:
    if masters == []:
        solved = True
        break
    matrix = masters[0]
    del masters[0]
    S = temp(matrix)
    columns = column(matrix)

    count = [j.count(1) for j in columns.values()]
    if min(count) == 0:
        sol = sol[::-1][:(comp-1)]
        continue
    small = count.index(min(count))+1

    pots = []
    for j in range(len(columns[small])):
        if columns[small][j] == 1:
            pots.append(list(matrix.keys())[j])
    comp=0        
    for j in pots:
        m = copy.deepcopy(matrix)
        sol.append(j)
        numbers = S[chr(j)]
        letters = find(S,numbers)
        for i in letters:
            if i in pots and i != j:
                pots.remove(i)
                n = S[chr(i)]
                l = find(S,n)
                l.remove(i)
                x = copy.deepcopy(m)
                masters.append(delmatrix(x,[],l))
        newmatrix = delmatrix(m,numbers,letters)
        if newmatrix == {}:
            solution = [chr(i) for i in sol]
            for i in sorted(solution):
                print(i,s[i])
            print("-"*20)
            sol =[]
            break
        else:
            masters.insert(comp,newmatrix)
            comp+=1
            


