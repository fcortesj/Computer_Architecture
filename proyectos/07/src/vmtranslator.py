"""
This Module run all the traduction of the VM program into assembler
This translator uses the parser in codewriter class to read a jack VM language and generate an assembly file
By: Felipe Cortes Jaramillo
"""

#First we import the dependencies that we are gonna use in the translation
import sys
from vmparser import Parser
from codewriter import Codewriter

def main():
    """Main of all the classes it starts parsing the lines of the jack vm language and once it have finished, ti writes the commands in assmebler"""
    #We check if the file ends in .vm else its an error
    if len(sys.argv) != 2 or sys.argv[1][-3:] != ".vm":
        badusage()
    #We get the filename
    filename = str(sys.argv[1])
    #Create the parser
    parser = Parser(filename)
    #We create the codewriter without the .vm extention
    codewriter = Codewriter(filename[0:-3])
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
    #Then we close the codewriter and parser
    del codewriter
    del parser

def badusage():
    """This method returns bad usage of the VM Translator"""
    print("Usage: python3 vmtranslator.py <File Name>.vm")
    sys.exit(1)

if __name__ == "__main__":
    main()


