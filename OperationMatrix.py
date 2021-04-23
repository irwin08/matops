import numpy as np
from pylatex import Math, Matrix, Command

class OperationMatrix:
    # takes numpy matrix(array)
    def __init__(self, matrix):
        self.matrix = matrix
        self.states = [matrix.copy()]
        # NOTE: elementary goes left to right in order of transformation, NOT final multiplication
        self.elementary = []

    def __str__(self):
        return str(self.matrix)

    def __repr__(self):
        return "OperationMatrix(np.array())"

    def swapRows(self, i, j):
        self.matrix[[i,j],:] = self.matrix[[j,i],:]
        self.states.append(self.matrix.copy())

        rows, cols = self.matrix.shape
        e = np.zeros((rows,rows))
        e[i][i] = -1
        e[j][j] = -1
        e[i][j] = 1
        e[j][i] = 1
        P = np.identity(rows) + e
        self.elementary.append(('l',P))

    def swapCols(self, i, j):
        self.matrix[:,[i,j]] = self.matrix[:,[j,i]]
        self.states.append(self.matrix.copy())

        rows, cols = self.matrix.shape
        e = np.zeros((cols,cols))
        e[i][i] = -1
        e[j][j] = -1
        e[i][j] = 1
        e[j][i] = 1
        P = np.identity(cols) + e
        self.elementary.append(('r',P))

        
        #b is coeff to multiply adding row by
    def addCol(self, i, j, b=1):
        self.matrix[:,j] += (self.matrix[:,i] * b)
        self.states.append(self.matrix.copy())

        rows, cols = self.matrix.shape
        e = np.zeros((cols,cols))
        e[j][i] = b
        T = np.identity(cols) + e
        self.elementary.append(('r',T))
        
    def addRow(self, i, j, b=1):
        self.matrix[j,:] += (self.matrix[i,:] * b)
        self.states.append(self.matrix.copy())

        rows, cols = self.matrix.shape
        # sorry for the confusion, got this backwards when initially designing
        e = np.zeros((rows,rows))
        e[j][i] = b
        T = np.identity(rows) + e
        self.elementary.append(('l',T))

    def multRow(self, i, u):
        self.matrix[i,:] = (self.matrix[i,:]*u)
        self.states.append(self.matrix.copy())

        rows, cols = self.matrix.shape

        e = np.zeros((rows,rows))
        e[i][i] = (1-u)
        D = np.identity(rows) + e
        self.elementary.append(('l',D))

    def multCol(self, i, u):
        self.matrix[i,:] = (self.matrix[:,i]*u)
        self.states.append(self.matrix.copy())

        rows, cols = self.matrix.shape

        e = np.zeros((cols,cols))
        e[i][i] = (1-u)
        D = np.identity(cols) + e
        self.elementary.append(('r',D))

    def undo(self):
        if len(self.states) > 1:
            self.states.pop()
            self.elementary.pop()
            self.matrix = self.states[-1].copy()

    def getLatex(self):
        data = []
        for elem in self.states:
            data.append(Matrix(elem))
            data.append(Command('to'))
        data.pop()
        return Math(data=data).dumps()

    def getEquivalent(self):
        left = []
        right = []
        for elem in self.elementary:
            if(elem[0] == 'l'):
                left.append(elem[1])
            else:
                right.append(elem[1])
        leftWritable = reversed(left)
        data = []
        for mat in leftWritable:
            data.append(Matrix(mat))
        data.append(Matrix(self.states[0]))
        for mat in right:
            data.append(Matrix(mat))
        return Math(data=data).dumps()

    def getEquivalentTruncated(self):
        left = []
        right = []
        print(self.elementary)
        for elem in self.elementary:
            if(elem[0] == 'l'):
                left.append(elem[1])
            else:
                right.append(elem[1])
        leftWritable = reversed(left)
        rows, cols = self.matrix.shape
        leftMat = np.identity(rows)
        rightMat = np.identity(cols)
        for mat in leftWritable:
            leftMat = np.matmul(leftMat, mat)
        for mat in right:
            rightMat = np.matmul(rightMat, mat)
        data = [Matrix(leftMat), Matrix(self.states[0]), Matrix(rightMat)]
        print(left)
        return Math(data=data).dumps()
    
