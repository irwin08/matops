import numpy as np
import OperationMatrix as om
from pylatex import Math, Matrix

def loadMatrix():
    with open('matrix.txt') as f:
        lines = f.readlines()
        N = 0
        mat = []
        for line in lines:
            rowstr = line.strip().split()
            # used float instead of double so it'll work over R(for regular old linear algebra) as well as Z
            row = list(map(float, rowstr))
            if N == 0:
                N = len(row)
            else:
                if len(row) != N:
                    raise Exception("Exception: rows and columns of matrix are inconsistent!")
            mat.append(row)
        return om.OperationMatrix(np.array(mat))

if __name__ == '__main__':
    mat = loadMatrix()
    print(mat)
    while True:
        cmd = input('>')
        cmdlist = cmd.split()
        if cmdlist[0].lower() == "swaprows":
            i = int(cmdlist[1])
            j = int(cmdlist[2])
            mat.swapRows(i,j)
            print(mat)
        elif cmdlist[0].lower() == "swapcols":
            i = int(cmdlist[1])
            j = int(cmdlist[2])
            mat.swapCols(i,j)
            print(mat)
        elif cmdlist[0].lower() == "addrow":
            i = int(cmdlist[1])
            j = int(cmdlist[2])
            b = 1
            if(len(cmdlist) > 3):
                b = float(cmdlist[3])
            mat.addRow(i,j,b)
            print(mat)
        elif cmdlist[0].lower() == "addcol":
            i = int(cmdlist[1])
            j = int(cmdlist[2])
            b = 1
            if(len(cmdlist) > 3):
                b = float(cmdlist[3])
            mat.addCol(i,j,b)
            print(mat)
        elif cmdlist[0].lower() == "getlatex":
            print(mat.getLatex())
        elif cmdlist[0].lower() == "getequiv":
            print(mat.getEquivalent())
        elif cmdlist[0].lower() == "getequivtrunc":
            print(mat.getEquivalentTruncated())
            
