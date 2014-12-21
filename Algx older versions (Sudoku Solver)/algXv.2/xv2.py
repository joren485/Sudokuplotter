print("NOOIT AFGEMAAKT zie V3 voor werkend programma")
exit()
sets = {"a":[1,4,7],"b":[1,4],"c":[4,5,7],"d":[3,5,6],"e":[2,3,6,7],"f":[2,7]}
columns = []
for i in sets.values():
    for j in i:
        columns.append(j)
columns = sorted(list(set(columns)))


def settomatrix(Set):
    values = []
    matrix= {}
    keys = sorted(list(Set.keys()))
    
    for i in Set.values():
        for j in i:
            values.append(j)
    values = sorted(list(set(values)))
    
    for i in range(len(keys)):
        key = keys[i]
        matrix[key]=[]
        for j in values:
            if j in Set[key]:
                matrix[key].append(1)
            else:
                matrix[key].append(0)
        
    return matrix


matrixes = [settomatrix(sets)]
solution = []
solved = False
while solved is not True:
    for m in matrixes:
        tempmatrix = m
        if tempmatrix == {}:        
            solved = True
            break
        
        allcolumncount = []
        for i in columns:
            columncount = 0
            rows = []
            for j in sorted(tempmatrix.keys()):
                if tempmatrix[j][i-1] == 1:
                    columncount+=1
                    rows.append(j)
            allcolumncount.append([columncount,rows])
        columncountmin=[]
        for i in allcolumncount:
            columncountmin.append(allcolumncount[0])
        rows = allcolumncount[columncountmin.index(min(columncountmin))][1]
        for i in rows:
            solution.append(i)
        
        
        
    
        
            
        
        
        
        
        
    
    
    
    
