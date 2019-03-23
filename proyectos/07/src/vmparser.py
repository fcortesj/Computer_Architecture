"""This Module Parse the file and checks the commands, ignore the invalid lines 
    By: Felipe Cortes Jaramillo"""

class Parser:
    #ListS with the arithmetic commands and memory segments
    arithmetic_commands = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
    m_segments = ["local", "argument", "static", "constant", "this", "that", "pointer", "temp"]

    def __init__(self, filename):
        """Constructor of the class"""
        self.filename = open(filename, "r")
        self.currentCommand = None
    
    def __del__(self):
        """Destructor of the class"""
        self.filename.close()

    def hasMoreCommands(self):
        """This method checks if the next line is a command, if it is a comment or a empty line is ignored"""
        currentLine = self.peekLine()
        #Checks if the line is not a comment or new line
        while currentLine.strip()[0:2] == "//" or currentLine == '\n':
            self.filename.readline()
            currentLine = self.peekLine()
        #If the line is empty there is no more commands
        if currentLine is "":
            return False
        else: 
            return True

    def advance(self):
        """This method advance for the next command"""
        self.currentCommand = self.filename.readline().strip()

    def command_type(self):
        """This method returns the type of command that it reads"""
        currentCommand = self.currentCommand
        #We find the comment index and get the command only
        commentIndex = currentCommand.find("//")
        if commentIndex != -1:
            currentCommand = currentCommand[0:commentIndex].strip()
            self.currentCommand = currentCommand
        #Splits the command int parts to get the first one to check what commands is
        partsCommand = currentCommand.split(" ")
        if partsCommand[0] in Parser.arithmetic_commands:
            return "C_ARITHMETIC"
        elif partsCommand[0] == "push":
            return "C_PUSH"
        elif partsCommand[0] == "pop":
            return "C_POP"
        else:
            print("ERROR: ParserError Command {} not Found".format(partsCommand[0]))
            exit(1)
    
    def arg1(self):
        """Returns the first argument of the command"""
        currentCommand = self.currentCommand
        partsCommands = currentCommand.split(" ")
        commandType = self.command_type()
        #We check what type of command we are talking about
        if commandType == "C_PUSH" or commandType == "C_POP":
        #We handle the error with commands push or pop with no argument 1
            try:
                #We check if there is a valid argument with push or pop
                if partsCommands[1] in Parser.m_segments:
                    return partsCommands[1]
                else:
                    print("ERROR: Invalid argument with command {}".format(partsCommands[0]))
                    exit(1)
            except IndexError:
                print("ERROR: There is no argument with command {}".format(partsCommands[0]))
                exit(1)
        elif commandType == "C_ARITHMETIC":
            return partsCommands[0]

    def arg2(self):
        """Returns the second argument of the command"""
        currentCommand = self.currentCommand
        partsCommand = currentCommand.split(" ")
        commandType = self.command_type()
        #We check the command type this only works with pop and push
        if commandType == "C_PUSH" or commandType == "C_POP":
        #Check if exist and argument 2
            try:
                if partsCommand[2].isnumeric():
                    return int(partsCommand[2])
                else:
                    print("ERROR: Second argument is not a number ")
                    exit(1)
            except IndexError:
                print("ERROR: There is no second argument with command {}".format(partsCommand[0]))
                exit(1)
        
    def peekLine(self):
        """This method checks if the the next line is blank or not"""
        #Set cursor in actual position
        actualLine = self.filename.tell()
        #Set new line to check
        nextLine = self.filename.readline()
        #Return the head to the actualLine
        self.filename.seek(actualLine)
        return nextLine 
