"""
This Module run all the traduction of the VM program into assembler
This translator uses the parser in codewriter class to read a jack VM language and generate an assembly file
By: Felipe Cortes Jaramillo
"""

#First we import the dependencies that we are gonna use in the translation
import sys
import os
from vmparser import Parser
from codewriter import Codewriter

def main():
    """Main of all the classes it starts parsing the lines of the jack vm language and once it have finished, ti writes the commands in assmebler"""
    #We check if the file ends in .vm else its an error or if it is a directory which contains vm programs
    if len(sys.argv) != 2:
        badusage()
    if sys.argv[1][-3:] != ".vm" and not os.path.isdir(sys.argv[1]) :
        badusage()
    #We get the filename
    filepath = str(sys.argv[1])
    if os.path.isdir(filepath):
        #If it is a directory we search the .vm (files=1) or the sys.init (files>1)
        justFile = filepath.split("\\")
        if justFile[-1] != "" and justFile[-1] != " ":
            codewriter = Codewriter("{}\\{}".format(filepath,justFile[-1]))
            searchFileDir(filepath, codewriter)
            del codewriter
        else:
            codewriter = Codewriter("{}\\{}".format(filepath,justFile[-2]))
            searchFileDir(filepath, codewriter)
            del codewriter
    else:
         #If it is a file then we just pass straight
         codewriter = Codewriter(filepath[0:-3])
         translateFile(filepath, codewriter)
         del codewriter


def translateFile(filename, codewriter):
    #Create the parser
    parser = Parser(filename)
    #We set the current file in which we are translating
    codewriter.setFileName(filename[0:-3])
    #Start reading checking if it has more commands advancing and seeing the command
    while parser.hasMoreCommands():
        parser.advance()
        #If it is a arithmetic command we write it or a push or pop command
        if parser.command_type() == "C_ARITHMETIC":
            command = parser.arg1()
            codewriter.writeArithmetic(command)
        elif parser.command_type() == "C_PUSH":
            m_segment = parser.arg1()
            index = parser.arg2()
            codewriter.writePushPop("C_PUSH", m_segment, index)
        elif parser.command_type() == "C_POP":
            m_segment = parser.arg1()
            index = parser.arg2()
            codewriter.writePushPop("C_POP", m_segment, index)
        elif parser.command_type() == "C_LABEL":
            labelName = parser.arg1()
            codewriter.writeLabel(labelName)
        elif parser.command_type() == "C_GOTO":
            destination = parser.arg1()
            codewriter.writeGoto(destination)
        elif parser.command_type() == "C_IF":
            destination = parser.arg1()
            codewriter.writeIf(destination)
        elif parser.command_type() == "C_CALL":
            function_name = parser.arg1()
            nArgs = parser.arg2()
            codewriter.writeCall(function_name, nArgs)
        elif parser.command_type() == "C_RETURN":
            codewriter.writeReturn()
        elif parser.command_type() == "C_FUNCTION":
            function_name = parser.arg1()
            nVars = parser.arg2()
            codewriter.writeFunction(function_name, nVars)
    #Then we close the codewriter and parser
    del parser


def searchFileDir(path, codewriter):
    """This Module Search the file which is goind to run the translation depends if it is just one or if not apply the sys.init"""
    #First we initialize a list which will contain all the vm files 
    files = []
    # r=root, d=directories, f = files this loop look for all the files in the directory and add to files the ones that end in .vm
    for r, d, f in os.walk(path):
        for file in f:
            if ".vm" in file:
                files.append(file)

    if len(files) > 1:
        #Then if there are more than one file we run the sys.init and for each file we run the codewriter
        codewriter.writeInit()
        for vmFiles in files:
            translateFile(os.path.join(r,vmFiles), codewriter)
    elif len(files) == 1:
        #If there is just one file we return the name of the file
        translateFile(os.path.join(r,files[0]), codewriter)
    else:
        #If there is no file its is an error
        print("ERROR: There is not .vm Files to translate")
        sys.exit(1)


def badusage():
    """This method returns bad usage of the VM Translator"""
    print("Usage: python3 vmtranslator.py <File Name>.vm")
    sys.exit(1)


if __name__ == "__main__":
    main()


