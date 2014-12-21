S={
"A":[1,4,7],    
"B":[1,4],
"C":[4,5,7],
"D":[3,5,6],
"E":[2,3,6,7],
"F":[2,7]}
U = [1,2,3,4,5,6,7]
orgU = [1,2,3,4,5,6,7]

def build(template,Set,orgSet):
    D={}
    dels = []
    
    for i in S.keys():
        D[ord(i)] = [0]*len(orgU)
        for j in S[i]:
            D[ord(i)][j-1] = 1    
    
    if orgU != U:
        for i in orgU:
            if i not in U:
                dels.append(i)
        print(dels)
        comp = 0
        for i in D.keys():
            for j in dels:
                del D[i][j-1-comp]
                comp+=1
            comp=0
    return D

matrix = build(S,U,orgU)

def temp(matrix):
    d ={}
    for i in matrix.keys():
        d[i]=[]
        for j in range(len(matrix[i])):
            if matrix[i][j]==1:
                d[i].append(j+1)
    return d

template = temp(matrix)
for i in template.keys():
    print(i,template[i])

