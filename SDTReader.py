
import numpy as np

def load(filename):
    out = dict()
    with open(filename, 'r') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        words = line.split(' ')

        if len(words) == 0 or words[0] == '':
            i += 1
            continue

        if words[0] == '@matrix':
            if len(words) is not 4:
                raise Exception("Syntax error on line {0}: Expected '@matrix <name> <nrows> <ncols>'.".format(i+1))

            name = words[1]
            nrows = int(words[2])
            ncols = int(words[3])

            out[name] = loadMatrix(lines[(i+1):], nrows, ncols)
            i += nrows
        elif words[0] == "@string":
            if len(words) is not 3:
                raise Exception("Syntax error on line {0}: Expected '@string <name> <length>'.".format(i+1))

            name = words[1]
            length = words[2]

            out[name] = loadString(lines[(i+1):], length)
            i += 1
        else:
            raise Exception("Unrecognized data type on line {0}: '{1}'.".format(i+1, words[0]))

        i += 1

    return out

def loadMatrix(lines, nrows, ncols):
    mat = np.zeros((nrows, ncols)) 

    for i in range(0, nrows):
        line = lines[i].split(' ')
        for j in range(0, ncols):
            mat[i,j] = float(line[j])

    return mat

def loadString(lines, length):
    s = ""
    line = lines[0].split(' ')
    for word in line:
        s += chr(int(word))

    return s

