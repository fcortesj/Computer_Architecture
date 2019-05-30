""" This module write the VM commands from a Jack Program  
    By: Felipe Cortes Jaramillo
"""

class jackVMWriter:

    def __init__(self, output):
        """ Constructor of the class """
        self.outputFile = open(output, 'w')
    
    def __del__(self):
        """ Destructor of the class """
        self.outputFile.close()

    def writePush(self, segment, index):
        """ Writes a VM push command """
        if segment == 'CONST':
            segment = 'constant'
        elif segment == 'ARG':
            segment = 'argument'
        
        self.outputFile.write("push {} {}\n".format(segment.lower(), index))

    def writePop(self, segment, index):
        """ Writes a VM pop command """
        if segment == 'CONST':
            segment = 'constant'
        elif segment == 'ARG':
            segment = 'argument'
        
        self.outputFile.write("pop {} {}\n".format(segment.lower(), index))
    
    def writeArithmetic(self, command):
        """ Writes a VM arithmetic command """
        self.outputFile.write(command.lower()+"\n")
    
    def writeLabel(self, label):
        """ Writes a VM label command """
        self.outputFile.write("label {}\n".format(label))
    
    def writeGoto(self, label):
        """ Writes a VM goto command """
        self.outputFile.write("goto {}\n".format(label))
    
    def writeIf(self, label):
        """ Writes a VM if-goto command """
        self.outputFile.write("if-goto {}\n".format(label))

    def writeCall(self, name, nArgs):
        """ Writes a call command """
        self.outputFile.write("call {} {}\n".format(name, nArgs))
    
    def writeFunction(self, name, nLocals):
        """ Writes a function command """
        self.outputFile.write("function {} {}\n".format(name, nLocals))

    def writeReturn(self):
        """ Writes a return command """
        self.outputFile.write("return\n")

        

