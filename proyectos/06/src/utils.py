#This file contains helpers that help the process of the assembler

#Helps to get the name of the new file
def fix_name(line, op = "//"):
    opIndx = line.find(op)
    if opIndx == -1:  #Doesnt found the op
        return line

    elif opIndx == 0: #The comment is on the beginning of the line
        return ''     #Return nothing because it is ignored
    else:
        if op == "//":
            line = line[:opIndx-1]  #Because there are two elements
        else:
            line = line[:opIndx]    #If it is other element just remove it
    return line

#Functions to check if is a A command or C command or Label
def isLabel(line):
    if line.find("(") != -1 and line.find(")") != -1:
        return True
    else:
        return False

#Function that checks if it is a A Command
def isA(line):
    if line.find('@') != -1:
        return True
    else:
        return False

#Function that checks if it is a C Command
def isC(line):
    if line.find("(") == -1 and line.find("@") == -1 and line != '':
        return True
    else:
        return False


#Translate number to binary convertion
def binaryConverter(num):
    binaryNum = "{:016b}".format(num)
    return binaryNum

binaryNumber = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]      #First we get the number itself


#Try to parse an Integer for evaluatin porpuses
def parseInt(num):
    try:
        return int(num)
    except ValueError:
        return None

#Find if the a bit is from the A(0) or M(1)
def set_aBit(comp):
    if comp.find('M') != -1:
        return "1"
    else:
        return "0"





