def column(matrix):
    columns={}
    U = getU(matrix)
    for i in range(1,len(U)+1):
        columns[i] =[]
        for j in matrix.values():
            columns[i].append(j[i-1])
    return columns

def temp(matrix):
    d={}
    for i in matrix.keys():
        d[chr(i)]=[]
        for j in range(len(matrix[i])):
            if matrix[i][j]==1:
                d[chr(i)].append(j+1)
    return d

def build(template,Set):
    d = {} 
    for i in template.keys():
        d[ord(i)] = [0]*len(Set)
        for j in template[i]:
            d[ord(i)][j-1] = 1

    return d


def appearcheck(verwijderset,checkset):
    for i in checkset:
        if i in verwijderset:
            return False
    return True

def find(S,verwijderU):
    verwijderletters = []
    for j in S.keys():
        if not appearcheck(verwijderU,S[j]):
            verwijderletters.append(ord(j))
    return verwijderletters

def delmatrix(matrix, verwijderU, verwijderletters):
    m = dict(matrix)
    for i in matrix.keys():
        if i in verwijderletters:
            del m[i]

    comp = 0
    for i in m.keys():
        for j in verwijderU:
            del m[i][j-1-comp]
            comp+=1
        comp=0
    for i in m.values():
        if i == []:
            return {}
    return m

def getU(matrix):
    template = temp(matrix)
    U = []
    for i in template.values():
        for j in i:
            U.append(j)
    U = sorted(U)
    U = set(U)
    U = list(U)
    return U
