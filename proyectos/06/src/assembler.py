import utils
import tables
import sys
import os

#We initalize the list of A commands and C commands, label List, varaible when start int the RAM and line for tracck the label
listA = {}
listC = {}
labelList = {}
variableStart = 16
lineForLabel = 0

filename = sys.argv[1]                #We especified the filename in the arguments when we run the app


def start_file(filename):   # This method prepare the file to be translated
    file = open(filename)
    prep_file = file.readlines()
    scan_file = []

    #First Pass we arrange the lines and then we create the synbol list tables
    #prep_file = scan_line(prep_file) #Remove the comments from the file
    for line in prep_file:
        line = scan_line(line)
        if line.strip() == '':
            continue
        else:
            scan_file.append(line)

    #Second Pass when we look if the lines that are not label, are command A or command C
    scan_file = scan_commands(scan_file)

    return scan_file



def scan_line(line, op = "//"):
    opIndx = line.find(op)
    if opIndx == -1:  #Doesnt found the op
        line = line.strip()
        line = isLabel(line)
        return line
    elif opIndx == 0: #The comment is on the beginning of the line
        return ''     #Return nothing because it is ignored
    else:
        line = line[:opIndx-1]  #Because there are two elements
        line = line.strip()     #Remove wgite spaces
        line = isLabel(line)
    return line



def scan_commands(file):
    finalFile = []
    for line in file:
        if utils.isA(line):                         #Check if it is A command
            line = isACommand(line)
            finalFile.append(listA.get(line[1:]))   #Add to final resul
        elif utils.isC(line):                       #Check if it is A command
            line = isCCommand(line)
            finalFile.append(listC.get(line))       #Add to final result
        elif utils.isLabel(line):
            continue                                #Already Checked
        else:
            print("ERROR: Syntax Error Command not identified:" + line)
            raise SyntaxError
    return finalFile



def isLabel(line):
    global lineForLabel
    if (utils.isLabel(line)):  # If it is a Label
        binaryCounter = utils.binaryConverter(lineForLabel)
        labelList[line[1:-1]] = binaryCounter  # We set the label WITHOUT the parentesis to his binary number in the list
        return line
    elif line.strip()!= '':                    # If it is not a label and is not a newline it need to count the line
        lineForLabel += 1
        return line
    else:
        return line



def isACommand(line):
    global variableStart
    currentBits = line[1:]  # We ignore the first bit because we know it is a A Command
    if utils.parseInt(currentBits) is not None:  # If after the @ it is a number we just convert the number
        listA[line[1:]] = utils.binaryConverter(int(currentBits))
    elif currentBits in tables.predef_table.keys():  #If after the @ the value is a predefined word we add the value
        listA[line[1:]] = utils.binaryConverter(tables.predef_table[currentBits])
    elif currentBits in labelList.keys():  # If after the @ it is in the labelList we search the value
        listA[line[1:]] = labelList[line[1:]]
    elif currentBits in listA.keys():  # If it is already proceed and we have the variable we ignore it
        return line
    else:  # Finally we add the new variable
        listA[line[1:]] = utils.binaryConverter(variableStart)
        variableStart += 1
    return line


def isCCommand(line):
    semi  = line.find(';')
    equal = line.find('=')

    try:
        if equal != -1 and semi != -1:  #dest=comp;jmp
            dest = line[:equal]
            comp = line[equal+1:semi]
            jump = line[semi+1:]
            a_bit = utils.set_aBit(comp)  #Set A bit from the comp
            listC[line] = "111" + a_bit + tables.comp_table[comp] + tables.dest_table[dest] + tables.jump_table[jump] #We create the command line
        elif equal == -1 and semi != -1:  #comp;jmp
            comp = line[equal+1:semi]
            jump = line[semi+1:]
            a_bit = utils.set_aBit(comp)  #Set A bit from the comp
            listC[line] = "111" + a_bit + tables.comp_table[comp] + tables.dest_table["null"] + tables.jump_table[jump] #We create the command line without dest
        elif equal != -1 and semi == -1:  #dest=comp
            dest = line[:equal]
            comp = line[equal+1:]
            a_bit = utils.set_aBit(comp)  #Set A bit from the comp
            listC[line] = "111" + a_bit + tables.comp_table[comp] + tables.dest_table[dest] + tables.jump_table["null"] #We create the command line without jump
        return line
    except:
        print("ERROR: Syntax Error Not Valid Command Generated")
        raise SyntaxError




def write_file(file):       # This method write the final file in .hack extention
    newFileName = utils.fix_name(filename, op=".")
    newFileName = newFileName+".hack"
    newfile = open(newFileName,'w')

    for lines in file:
        newfile.write(lines+"\n")
    newfile.close()


def main():
    if filename.find(".asm") != -1:
        file = start_file(filename)   #First we analize the labels and arrange the lines and second we form the result and return it
        write_file(file)              #We open the file and write the final result
    else:
        print("ERROR: Not valid file to read")
        exit(-1)



if __name__ == "__main__":
    main()
