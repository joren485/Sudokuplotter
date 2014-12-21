def buildmatrix(S,U):
    rows={}
    length =len(U)        
    for i in S.keys():
        rows[ord(i)]=[0]*length
        for j in range(length):
            if (j+1) in S[i]:
                rows[ord(i)][j] = 1
    return rows

def templatebuild(matrix):
    temp = {}
    for i in matrix.keys():
        temp[chr(i)]= []
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                temp[chr(i)].append(j+1)
    return temp

##U=[1,2,3,4,5,6,7]
##S={
##"D":[3,5,6],
##"E":[2,3,6,7],
##"F":[2,7]}
##rows = buildmatrix(S,U)

def delmatrix(S,U,verwijderU,verwijderletters):
    matrix =buildmatrix(S,U)
    m = dict(matrix)
    for i in matrix.keys():
        if i in verwijderletters:
            del m[i]
            
    comp = 0
    for i in m.keys():
        for j in verwijderU:
            del m[i][j-1-comp]
            comp+=1
        comp =0
    return m
##rows = buildmatrix(U,S)
##verwijderU=[1,4,7]
##S=["A","B","C","E","F"]
##n = delmatrix(rows,U,S)


def appearcheck(verwijderset,checkset):
    for i in verwijderset:
        if i in checkset:
            return False
    return True

def find(S,verwijderU):
    verwijderletters = []
    for j in S.keys():
        if not appearcheck(verwijderU,S[j]):
            verwijderletters.append(j)
    verwijderletters = [ord(i) for i in verwijderletters]
    return verwijderletters


def column(matrix,U):
    columns = {}
    for i in range(1,len(U)+1):
        columns[i]=[]
        for j in matrix.values():
            columns[i].append(j[i-1])
    return columns

##rows = buildmatrix(U,S)
##U=[1,2,3,4,5,6,7]
##col = column(rows,U)

def pot(matrix,S,U):
    master =[]
##    matrix = buildmatrix(U,S)
    columns = column(matrix,U)
    count = [i.count(1) for i in columns.values()]
    if min(count) == 0:
        return 0
    small = count.index(min(count))+1
    for i in range(len(columns[small])):
        if columns[small][i] == 1:
            master.append([chr(i+65),small,S,U])
    return master






