"""This module writes the command in assembler once is analized with the parser
   By: Felipe Cortes Jaramillo"""

class Codewriter:

    def __init__(self,output_filename):
        """Constructor of the class"""
        output_final_filename = output_filename + ".asm"
        self.filename = open(output_final_filename, 'w+')
        self.actualFile = None
        self.actualFunction = None
        self.commandCount = 0
        self.returnCounter = 0
    
    def writeInit(self):
        """This Module is the bootstrap code used to initialize VM"""
        #We set the name to sys
        self.setFileName("Sys")
        #Create the list of commands
        assemblerTraduction = []
        #SP = 256
        assemblerTraduction.append("@256")
        assemblerTraduction.append("D=A")
        assemblerTraduction.append("@SP")
        assemblerTraduction.append("M=D")
        #We write in the file the result traduction
        for traducedLines in assemblerTraduction:
            self.filename.write(traducedLines+"\n")
        #Then we call Self.init = invoke sys.init
        self.writeCall("Sys.init",0)

    
    def __del__(self):
        """Destructor of the class"""
        self.filename.close()
    
    def setFileName(self, filename):
        """Informs the current vm file that is being traduced"""
        #We need to extract the last position of the path. This element is the filename
        Splifilename = filename.split("\\")
        Isofilname = Splifilename[-1]
        self.actualFile = Isofilname
    
    def setFunctionName(self, function_name):
        """Informs the current vm function that is being traduced"""
        self.actualFunction = function_name
    
    def writeArithmetic(self, currentCommand):
        """Translates the VM command to Assembler command"""
        #We create the list of the traduction
        assmemblerTraduction = []
        if currentCommand == "add":
            assmemblerTraduction.append("@SP")
            assmemblerTraduction.append("AM=M-1")
            assmemblerTraduction.append("D=M")
            assmemblerTraduction.append("A=A-1")
            assmemblerTraduction.append("M=D+M")
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

        #We get the adress where we going to push/pop
        self.getAdressaAndStore(m_segment,index)
        
        #Then we do the push or pop
        if command_type == "C_PUSH":
            #We load the value itself
            if m_segment == "constant":
                assemblerTraduction.append("D=A")
            #Else we load the memory value
            else:
                assemblerTraduction.append("D=M")
            assemblerTraduction.append("@SP")
            assemblerTraduction.append("A=M")
            assemblerTraduction.append("M=D")
            assemblerTraduction.append("@SP")
            assemblerTraduction.append("M=M+1")
        elif command_type == "C_POP":
            assemblerTraduction.append("D=A")
            assemblerTraduction.append("@R13")
            assemblerTraduction.append("M=D")
            assemblerTraduction.append("@SP")
            assemblerTraduction.append("M=M-1")
            assemblerTraduction.append("A=M")
            assemblerTraduction.append("D=M")
            assemblerTraduction.append("@R13")
            assemblerTraduction.append("A=M")
            assemblerTraduction.append("M=D")
                
        #Finally we write the command that we created
        for traducedLines in assemblerTraduction:
            self.filename.write(traducedLines+"\n")

    def getAdressaAndStore(self, m_segment, index):
        """This module get the adress of the memory segment and write the first part of the output push and pop"""
        #We assign the memory segment that will be writed in order to locate it in the right memory
        assembler_msegment = None
        if m_segment == "argument":
            assembler_msegment = "ARG"
        elif m_segment == "local":
            assembler_msegment = "LCL"
        elif m_segment == "this":
            assembler_msegment = "THIS"
        elif m_segment == "that":
            assembler_msegment = "THAT"

        #This list contains the traduction of the vm command
        assemblerTraduction = []

        #If the segment is argument, local, this or that it means it is a pointer so we get the memmory indside them and add the index to adress
        if m_segment == "argument" or m_segment == "local" or m_segment == "this" or m_segment == "that":
            assemblerTraduction.append("@{}".format(assembler_msegment))
            assemblerTraduction.append("D=M")
            assemblerTraduction.append("@{}".format(index))
            assemblerTraduction.append("A=D+A")
        #Otherwise it means is just a constant to be address, static value, pointer or lcl variable
        elif m_segment == "constant":
            assemblerTraduction.append("@{}".format(index))
        elif m_segment == "static":
            assemblerTraduction.append("@{}.{}".format(self.actualFile, index))
        elif m_segment == "pointer":
            assemblerTraduction.append("@R{}".format(3 + index)) 
        elif m_segment == "temp":
            assemblerTraduction.append("@R{}".format(5 + index))

        #Finally we write the command that we created
        for traducedLines in assemblerTraduction:
            self.filename.write(traducedLines+"\n")

    def writeLabel(self, label):
        """ Writes the assembly code that is the translation of the given "label" command """

        # Label declaration.
        self.filename.write("({}:{})\n".format(self.actualFile.upper(), label.upper()))

    def writeGoto(self, label):
        """ Writes the assembly code that is the translation of the given "goto" command """

        # Create a list to store all the assembly commands and write them later
        translated_commands = []

        # Unconditional jump to the VM command following the label.
        translated_commands.append("@{}:{}".format(self.actualFile.upper(), label.upper()))
        translated_commands.append("0;JMP")

        # Write all the commands stored in the list and write them on the file.
        for line in translated_commands:
            self.filename.write(line + "\n")

    def writeIf(self, label):
        """ Writes the assembly code that is the translation of the given "if-goto" command """

        # Create a list to store all the assembly commands and write them later
        translated_commands = []

        # Pops the topmost stack element.
        # If it's not zero, jumps to the VM command following the label
        translated_commands.append("@SP")
        translated_commands.append("M=M-1")
        translated_commands.append("A=M")
        translated_commands.append("D=M")
        translated_commands.append("@{}:{}".format(self.actualFile.upper(), label.upper()))
        translated_commands.append("D;JNE")

        # Write all the commands stored in the list and write them on the file.
        for line in translated_commands:
            self.filename.write(line + "\n")

    def writeCall(self, function_name, num_args):
        """ Writes the assembly code that is the translation of the given "call" command """

        # Update the current function.
        self.setFunctionName(function_name)

        # Create a list to store all the assembly commands and write them later
        translated_commands = []

        # Store the return address in a local variable to use later.
        return_address = "RETURN_{}{}".format(self.actualFunction.upper(), self.returnCounter)
        self.returnCounter += 1
        # Push the return address
        translated_commands.append("@{}".format(return_address))
        translated_commands.append("D=A")
        translated_commands.append("@SP")
        translated_commands.append("A=M")
        translated_commands.append("M=D")
        translated_commands.append("@SP")
        translated_commands.append("M=M+1")
        # Push LCL
        translated_commands.append("@LCL")
        translated_commands.append("D=M")
        translated_commands.append("@SP")
        translated_commands.append("A=M")
        translated_commands.append("M=D")
        translated_commands.append("@SP")
        translated_commands.append("M=M+1")
        # Push ARG
        translated_commands.append("@ARG")
        translated_commands.append("D=M")
        translated_commands.append("@SP")
        translated_commands.append("A=M")
        translated_commands.append("M=D")
        translated_commands.append("@SP")
        translated_commands.append("M=M+1")
        # Push THIS
        translated_commands.append("@THIS")
        translated_commands.append("D=M")
        translated_commands.append("@SP")
        translated_commands.append("A=M")
        translated_commands.append("M=D")
        translated_commands.append("@SP")
        translated_commands.append("M=M+1")
        # Push THAT
        translated_commands.append("@THAT")
        translated_commands.append("D=M")
        translated_commands.append("@SP")
        translated_commands.append("A=M")
        translated_commands.append("M=D")
        translated_commands.append("@SP")
        translated_commands.append("M=M+1")
        # ARG = SP - n - 5. n being the number of arguments.
        translated_commands.append("@SP")
        translated_commands.append("D=M")
        num = int(num_args) + 5   # n + 5
        translated_commands.append("@{}".format(num))
        translated_commands.append("D=D-A")  # D = SP -(n + 5)
        translated_commands.append("@ARG")
        translated_commands.append("M=D")
        # LCL = SP
        translated_commands.append("@SP")
        translated_commands.append("D=M")
        translated_commands.append("@LCL")
        translated_commands.append("M=D")
        # goto f. f being function_name.
        translated_commands.append("@{}".format(self.actualFunction.upper()))
        translated_commands.append("0;JMP")
        translated_commands.append("({})".format(return_address))

        # Write all the commands stored in the list and write them on the file.
        for line in translated_commands:
            self.filename.write(line + "\n")

    def writeReturn(self):
        """ Writes the assembly code that is the translation of the given "return" command """

        # Create a list to store all the assembly commands and write them later
        translated_commands = []

        # FRAME = LCL  --> R14
        translated_commands.append("@LCL")
        translated_commands.append("D=M")
        translated_commands.append("@R14")  # FRAME
        translated_commands.append("M=D")
        # RET = *(FRAME-5)  --> R15
        translated_commands.append("@R14")  # FRAME
        translated_commands.append("D=M")  # D = FRAME
        translated_commands.append("@5")
        translated_commands.append("D=D-A")
        translated_commands.append("A=D")   # A = FRAME - 5
        translated_commands.append("D=M")   # D = *(FRAME - 5)
        translated_commands.append("@R15")  # RET
        translated_commands.append("M=D")
        # *ARG = pop()
        translated_commands.append("@SP")
        translated_commands.append("M=M-1")
        translated_commands.append("A=M")
        translated_commands.append("D=M")
        translated_commands.append("@ARG")
        translated_commands.append("A=M")
        translated_commands.append("M=D")
        # SP = ARG + 1
        translated_commands.append("@ARG")
        translated_commands.append("D=M")
        translated_commands.append("@SP")
        translated_commands.append("M=D+1")
        # THAT = *(FRAME - 1)
        translated_commands.append("@R14")  # FRAME
        translated_commands.append("D=M")
        translated_commands.append("@1")
        translated_commands.append("D=D-A") # FRAME - 1
        translated_commands.append("A=D")
        translated_commands.append("D=M")   # D = *(FRAME - 1)
        translated_commands.append("@THAT")
        translated_commands.append("M=D")   # THAT = *(FRAME - 1)
        # THIS = (FRAME - 2)
        translated_commands.append("@R14")  # FRAME
        translated_commands.append("D=M")
        translated_commands.append("@2")
        translated_commands.append("D=D-A")  # FRAME - 2
        translated_commands.append("A=D")
        translated_commands.append("D=M")   # D = *(FRAME - 2)
        translated_commands.append("@THIS")
        translated_commands.append("M=D")   # THIS = *(FRAME - 2)
        # ARG = (FRAME - 3)
        translated_commands.append("@R14")  # FRAME
        translated_commands.append("D=M")
        translated_commands.append("@3")
        translated_commands.append("D=D-A")  # FRAME - 3
        translated_commands.append("A=D")
        translated_commands.append("D=M")  # D = *(FRAME - 3)
        translated_commands.append("@ARG")
        translated_commands.append("M=D")   # ARG = *(FRAME - 3)
        # LCL = (FRAME - 4)
        translated_commands.append("@R14")  # FRAME
        translated_commands.append("D=M")
        translated_commands.append("@4")
        translated_commands.append("D=D-A")  # FRAME - 4
        translated_commands.append("A=D")
        translated_commands.append("D=M")   # D = *(FRAME - 4)
        translated_commands.append("@LCL")
        translated_commands.append("M=D")   # LCL = *(FRAME - 4)
        # goto RET
        translated_commands.append("@R15")  # RET 
        translated_commands.append("A=M")
        translated_commands.append("0;JMP")

        # Write all the commands stored in the list and write them on the file.
        for line in translated_commands:
            self.filename.write(line + "\n")

    def writeFunction(self, function_name, num_locals):
        """ Writes the assembly code that is the translation of the given "Function" command. """   

        # Create a list to store all the assembly commands and write them later
        translated_commands = []
        
        # Declare label for function entry.
        translated_commands.append("({})".format(function_name.upper())) 
        # Allocate a memory addres for each local variable.
        for _ in range(num_locals):
            translated_commands.append("@SP")
            translated_commands.append("A=M")
            translated_commands.append("M=0")  
            translated_commands.append("@SP")
            translated_commands.append("M=M+1")   

        # Write all the commands stored in the list and write them on the file.
        for line in translated_commands:
            self.filename.write(line + "\n")
