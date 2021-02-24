import re
import sys
import getopt


def formatString(s):
    upChar = 0
    pos = []
    inChar = False
    l = 0
    for p, i in enumerate(s):
        if i == '\'':
            if inChar:
                pos.append(p)
            else:
                pos.append(p + 1)
            inChar = not inChar
        elif inChar:
            if i.isupper():
                upChar += 1
            l += 1
    if len(pos) >= 2:
        if upChar == l:
            return s[:pos[0]] + s[pos[0]:pos[1]].lower() + s[pos[1]:]
        else:
            return s[:pos[0]] + s[pos[0]].lower() + s[pos[0] + 1:]
    return s


def findRegex(i):
    x = re.search(r'http.*#', i)
    if x:
        return re.sub(x[0], '', i)
    y = re.search(r'http.*/', i)
    if y:
        return re.sub(y[0], '', i)
    return i


if __name__ == "__main__":
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    if not opts:
        print('onto_cleaner.py -i <inputfile> -o <outputfile>')
        exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    fin = open(inputfile, "r")
    data = list(fin)
    fin.close()
    fout = open(outputfile, "w")

    for i in data:
        s = ""
        if not ',' in i:
            s += findRegex(i)
            s = formatString(s)
        else:
            l = i.split(',')
            for j in l:
                fstr1 = findRegex(j)
                # if fstr2:
                #	print('wewe '+fstr2[0])
                fstr1 = formatString(fstr1)
                s += (fstr1) + ','
            s = s[:-1]
        fout.write(s)
    fout.close()
