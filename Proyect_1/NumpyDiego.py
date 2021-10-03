
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

def matrix_multiply_list(arrayMatrix):
    matriz1 = arrayMatrix[0]

    for matrix in arrayMatrix[1:]:
        matrix_result = matrix_multiply(matrix,matriz1)
 
    return matrix_result

def vector_multiply_list(arrayMatrix):
    vector1 = arrayMatrix[0]
    matrix_result = zeros_matrix(4,4)
    matrix_result = matrix_vector_multiply(arrayMatrix[1], vector1)
    for matrix in arrayMatrix[2:]:
        matrix_result = matrix_vector_multiply(matrix, matrix_result)
 
    return matrix_result

# matrix_vector_multiply(
#     [
#         [1,1,1,1],
#         [1,1,1,1],
#         [1,1,1,1],
#         [1,1,1,1]

#     ], [2,0,0,3]

# )