import sys
import os
from antlr4 import *
from jackGrammarLexer import jackGrammarLexer
from jackGrammarParser import jackGrammarParser
from jackGrammarListener import jackGrammarListener
from jackListener import jackListener
from jackErrorHandler import ErrorHandler


def main(argv):
    """ This function is the main. It translates all .jack files into .xml according to the parser and the jackListener """
    #We check if the file ends in .jack else its an error or if it is a directory which contains vm programs
    if len(sys.argv) != 2:
        badusage()
    if sys.argv[1][-5:] != ".jack" and not os.path.isdir(sys.argv[1]) :
        badusage()
    #We get the filename
    filepath = str(sys.argv[1])
    if os.path.isdir(filepath):
        #If it is a directory we search the .jack (files=1) 
        justFile = filepath.split("\\")
        if justFile[-1] != "" and justFile[-1] != " ":
            searchFileDir(filepath)
        else:
            searchFileDir(filepath)
    else:
        #If it is a file then we just pass straight
        translateFile(filepath)



def searchFileDir(path):
    """This Module Search the file which is goind to run the translation depends if it is just one or if not apply the sys.init"""
    #First we initialize a list which will contain all the vm files 
    files = []
    # r=root, d=directories, f = files this loop look for all the files in the directory and add to files the ones that end in .vm
    for r, d, f in os.walk(path):
        for file in f:
            if ".jack" in file:
                files.append(file)

    if len(files) >= 1:
        #Then if there are more than one file we run the sys.init and for each file we run the codewriter
        for jackFiles in files:
            translateFile(os.path.join(r,jackFiles))
    else:
        #If there is no file its is an error
        print("ERROR: There is not .vm Files to translate")
        sys.exit(1)



def translateFile(filepath):
    """ This function translates the file """
    #We fix the name of the file target
    output = filepath[:-5] + ".xml"
    #Then we create the elements necesary to translate the file
    input = FileStream(filepath)
    lexer = jackGrammarLexer(input)
    stream = CommonTokenStream(lexer)
    parser = jackGrammarParser(stream)

    #Remove Error Listener to add ours
    parser.removeErrorListeners()
    parser.addErrorListener(ErrorHandler())

    try:
        tree = parser.classN()
    except  Exception as syntaE:
        print(syntaE)
        sys.exit(-1)
        
    listener = jackListener(output, parser)
    ParseTreeWalker.DEFAULT.walk(listener, tree)


        
def badusage():
    """This method returns bad usage of the jackAnalizerTranslator"""
    print("Usage: python3 jackAnalizer.py <File Name>.jack")
    sys.exit(1)



if __name__ == '__main__':
    main(sys.argv)