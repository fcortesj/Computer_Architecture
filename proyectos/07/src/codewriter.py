"""This module writes the command in assembler once is analized with the parser
   By: Felipe Cortes Jaramillo"""

class Codewriter:

    def __init__(self,output_filename):
        """Constructor of the class"""
        output_final_filename = output_filename + ".asm"
        self.filename = open(output_final_filename, 'w+')
        self.actualFile = None
        self.commandCount = 0
    
    def __del__(self):
        """Destructor of the class"""
        self.filename.close()
    
    def setFileName(self, filename):
        """Informs the current vm file that is being traduced"""
        self.actualFile = filename
    
    def writeArithmetic(self, currentCommand):
        """Translates the VM command to Assembler command"""
        #We create the list of the traduction
        assmemblerTraduction = []
        if currentCommand == "add":
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("AM=M-1")
            assmemblerTraduction.append("D=M")
            assmemblerTraduction.append("A=A-1")
            assmemblerTraduction.append("M=M+D")
        elif currentCommand == "sub":
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("AM=M-1")
            assmemblerTraduction.append("D=M")
            assmemblerTraduction.append("A=A-1")
            assmemblerTraduction.append("M=M-D")
        elif currentCommand == "neg":
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("A=M-1")
            assmemblerTraduction.append("M=-M")
        elif currentCommand == "eq":
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("AM=M-1")
            assmemblerTraduction.append("D=M")
            assmemblerTraduction.append("A=A-1")
            assmemblerTraduction.append("D=M-D")
            assmemblerTraduction.append("@FALSE{}".format(self.commandCount))
            assmemblerTraduction.append("D;JNE")
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("A=M-1")
            assmemblerTraduction.append("M=-1")
            assmemblerTraduction.append("@END{}".format(self.commandCount))
            assmemblerTraduction.append("0;JMP")
            assmemblerTraduction.append("(FALSE{})".format(self.commandCount))
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("A=M-1")
            assmemblerTraduction.append("M=0")
            assmemblerTraduction.append("(END{})".format(self.commandCount))
            self.commandCount += 1
        elif currentCommand == "gt":
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("AM=M-1")
            assmemblerTraduction.append("D=M")
            assmemblerTraduction.append("A=A-1")
            assmemblerTraduction.append("D=M-D")
            assmemblerTraduction.append("@FALSE{}".format(self.commandCount))
            assmemblerTraduction.append("D;JLE")
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("A=M-1")
            assmemblerTraduction.append("M=-1")
            assmemblerTraduction.append("@END{}".format(self.commandCount))
            assmemblerTraduction.append("0;JMP")
            assmemblerTraduction.append("(FALSE{})".format(self.commandCount))
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("A=M-1")
            assmemblerTraduction.append("M=0")
            assmemblerTraduction.append("(END{})".format(self.commandCount))
            self.commandCount += 1
        elif currentCommand == "lt":
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("AM=M-1")
            assmemblerTraduction.append("D=M")
            assmemblerTraduction.append("A=A-1")
            assmemblerTraduction.append("D=M-D")
            assmemblerTraduction.append("@FALSE{}".format(self.commandCount))
            assmemblerTraduction.append("D;JGE")
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("A=M-1")
            assmemblerTraduction.append("M=-1")
            assmemblerTraduction.append("@END{}".format(self.commandCount))
            assmemblerTraduction.append("0;JMP")
            assmemblerTraduction.append("(FALSE{})".format(self.commandCount))
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("A=M-1")
            assmemblerTraduction.append("M=0")
            assmemblerTraduction.append("(END{})".format(self.commandCount))
            self.commandCount += 1
        elif currentCommand == "and":
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("AM=M-1")
            assmemblerTraduction.append("D=M")
            assmemblerTraduction.append("A=A-1")
            assmemblerTraduction.append("M=D&M")
        elif currentCommand == "or":
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("AM=M-1")
            assmemblerTraduction.append("D=M")
            assmemblerTraduction.append("A=A-1")
            assmemblerTraduction.append("M=D|M")
        elif currentCommand == "not":
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("A=M-1")
            assmemblerTraduction.append("M=!M")
        #We write in the file the result traduction
        for traducedLines in assmemblerTraduction:
            self.filename.write(traducedLines+"\n")
    
    def writePushPop(self, command_type, m_segment, index):
        """This method writes in assembler the push/pop command"""
        #This list contains the traduction of the vm command
        assemblerTraduction = []
        #We assign the memory segment that will be writed in order to locate it in the right memoru
        assembler_msegment = None
        if m_segment == "argument":
            assembler_msegment = "ARG"
        elif m_segment == "local":
            assembler_msegment = "LCL"
        elif m_segment == "this":
            assembler_msegment = "THIS"
        elif m_segment == "that":
            assembler_msegment = "THAT"
        #Then we search the right location
        if m_segment == "argument" or m_segment == "local" or m_segment == "this" or m_segment == "that":
            if command_type == "C_PUSH":
                assemblerTraduction.append("@{}".format(assembler_msegment))
                assemblerTraduction.append("D=M")
                assemblerTraduction.append("@{}".format(index))
                assemblerTraduction.append("A=D+A")
                assemblerTraduction.append("D=M")
                assemblerTraduction.append("@SP")
                assemblerTraduction.append("A=M")
                assemblerTraduction.append("M=D")
                assemblerTraduction.append("@SP")
                assemblerTraduction.append("M=M+1")
            elif command_type == "C_POP":
                assemblerTraduction.append("@{}".format(assembler_msegment))
                assemblerTraduction.append("D=M")
                assemblerTraduction.append("@{}".format(index))
                assemblerTraduction.append("D=D+A")
                assemblerTraduction.append("@R13")
                assemblerTraduction.append("M=D")
                assemblerTraduction.append("@SP")
                assemblerTraduction.append("AM=M-1")
                assemblerTraduction.append("D=M")
                assemblerTraduction.append("@R13")
                assemblerTraduction.append("A=M")
                assemblerTraduction.append("M=D")
        elif m_segment == "static":
            if command_type == "C_PUSH":
                assemblerTraduction.append("@{}".format(16 + index))
                assemblerTraduction.append("D=M")
                assemblerTraduction.append("@SP")
                assemblerTraduction.append("A=M")
                assemblerTraduction.append("M=D")
                assemblerTraduction.append("@SP")
                assemblerTraduction.append("M=M+1")
            elif command_type == "C_POP":
                assemblerTraduction.append("@SP")
                assemblerTraduction.append("AM=M-1")
                assemblerTraduction.append("D=M")
                assemblerTraduction.append("@{}".format(16 + index))
                assemblerTraduction.append("M=D")
        elif m_segment == "constant":
            if command_type == "C_PUSH":
                assemblerTraduction.append("@{}".format(index))
                assemblerTraduction.append("D=A")
                assemblerTraduction.append("@SP")
                assemblerTraduction.append("A=M")
                assemblerTraduction.append("M=D")
                assemblerTraduction.append("@SP")
                assemblerTraduction.append("M=M+1")
            elif command_type == "C_POP":
                print("ERROR:Cannot Pop into a Constant")
                exit(1)
        elif m_segment == "pointer":
            if command_type == "C_PUSH":
                assemblerTraduction.append("@{}".format(3+index))
                assemblerTraduction.append("D=M")
                assemblerTraduction.append("@SP")
                assemblerTraduction.append("A=M")
                assemblerTraduction.append("M=D")
                assemblerTraduction.append("@SP")
                assemblerTraduction.append("M=M+1")
            elif command_type == "C_POP":
                assemblerTraduction.append("@SP")
                assemblerTraduction.append("AM=M-1")
                assemblerTraduction.append("D=M")
                assemblerTraduction.append("@{}".format(3 + index))
                assemblerTraduction.append("M=D")
        elif m_segment == "temp":
            if command_type == "C_PUSH":
                assemblerTraduction.append("@{}".format(5 + index))
                assemblerTraduction.append("D=M")
                assemblerTraduction.append("@SP")
                assemblerTraduction.append("A=M")
                assemblerTraduction.append("M=D")
                assemblerTraduction.append("@SP")
                assemblerTraduction.append("M=M+1")
            elif command_type == "C_POP":
                assemblerTraduction.append("@SP")
                assemblerTraduction.append("AM=M-1")
                assemblerTraduction.append("D=M")
                assemblerTraduction.append("@{}".format(5 + index))
                assemblerTraduction.append("M=D")
        #Finally we write the command that we created
        for traducedLines in assemblerTraduction:
            self.filename.write(traducedLines+"\n")     
    