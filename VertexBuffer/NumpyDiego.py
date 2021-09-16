
e = 2.718281828459045


def createMatrix(row,colum,dataList):
    matriz = []
    for x in range(row):
        rowList = []
        for y in range(colum):
            rowList.append(dataList[row * x + y])
        matriz.append(rowList)
    return matriz

def cos(angle):
    return (e**(angle*1j)).imag
def sin(angle):
    return (e**(angle*1j)).real

def zeros_matrix(rows, cols):
    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(0.0)
 
    return M

def matrix_vector_multiply(A, B):
    rowsV = len(B)
    colsM = len(A)
    F = [0,0,0,0]

    for i in range(rowsV):
        res = 0
        for j in range(colsM):
            res += A[i][j] * B[j] 
        F[i] = res

    return F

def matrix_multiply(A, B):

    rowsA = len(A)
    colsA = len(A[0])
    colsB = len(B[0])

    C = zeros_matrix(rowsA, colsB)
    for i in range(rowsA):
        for j in range(colsB):
            total = 0
            for ii in range(colsA):
                total += A[i][ii] * B[ii][j]
            C[i][j] = total
 
    return C

# matrix_vector_multiply(
#     [
#         [1,1,1,1],
#         [1,1,1,1],
#         [1,1,1,1],
#         [1,1,1,1]

#     ], [2,0,0,3]

# )