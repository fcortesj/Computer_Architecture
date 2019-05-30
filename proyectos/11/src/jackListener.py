from jackGrammarListener import jackGrammarListener
from jackGrammarParser import jackGrammarParser
from jackVMWriter import jackVMWriter
from jackSymbolTable import jackSymbolTable
import os

class jackListener(jackGrammarListener):

    """
        This class write the xml file form a parser generated. Parse from Jack Program and 
        writes the corresponding xml file.

        By: Felipe Cortes Jaramillo
    """

    CONVERT_KIND = {
        'ARG': 'ARG',
        'STATIC': 'STATIC',
        'VAR': 'LOCAL',
        'FIELD': 'THIS'
    }

    ARITHMETIC = {
        '+': 'ADD',
        '-': 'SUB',
        '=': 'EQ',
        '>': 'GT',
        '<': 'LT',
        '&': 'AND',
        '|': 'OR'
    } 

    ARITHMETIC_UNARY = {
        '-': 'NEG',
        '~': 'NOT'
    }

    keywordConstant = ["true", "false", "null", "this"]

    def __init__(self, parser, vm, symbolTable):
        """ Constructor of the class receives a parser, vmTranslator and a symbolTable """
        self.parser = parser
        self.vm = vm
        self.symbolTable = symbolTable
        self.currentClass = ""
        self.currentSubroutineName = ""
        self.currentSubroutineKind = ""
        self.ifIndex = -1
        self.whileIndex = -1


    def enterClassN(self, ctx):
        self.currentClass = ctx.getChild(1).getText()
        # print(className)
        return super().enterClassN(ctx)
    
    def enterClassVarDecN(self, ctx):
        childCount = 3
        currentKind = ctx.getChild(0).getText()
        currentType = ctx.getChild(1).getText()
        currentSymbolName = ctx.getChild(2).getText()
        #We create the symbol
        self.symbolTable.define(currentSymbolName, currentType, currentKind.upper())

        #TODO: Push the static variables declared in the class
        # if currentKind.upper() == 'STATIC':
        #     self.vm.writePush(currentKind.upper(), self.symbolTable.indexOf(currentSymbolName))

        #Then we check if there is more than one declaration so we can move on in the declarations
        while(ctx.getChild(childCount).getText() != ';'):
            currentSymbolName = ctx.getChild(childCount+1).getText()
            self.symbolTable.define(currentSymbolName, currentType, currentKind.upper())
            #CHECK THIS OUT
            # if currentKind.upper() == 'STATIC':
            #     self.vm.writePush(currentKind.upper(), self.symbolTable.indexOf(currentSymbolName))
            childCount += 2
        return super().enterClassVarDecN(ctx)

    def enterSubroutineDecN(self, ctx):
        subroutineKind = ctx.getChild(0).getText()
        subroutineName = ctx.getChild(2).getText()
        self.currentSubroutineKind = subroutineKind
        self.currentSubroutineName = subroutineName
        #We start a new subroutine
        self.symbolTable.startRoutine()

        if subroutineKind == 'method':
            self.symbolTable.define('instance', self.currentClass, 'ARG')

        if(ctx.getChild(4).getText() != ''):
            self.compileParameterList(ctx.getChild(4))

        #Then we check if there is varDec
        self.compilesubroutineBody(ctx.getChild(6))
        
        return super().enterSubroutineDecN(ctx)


    
    def compileParameterList(self, ctx):
        childCount = ctx.getChildCount()
        currentType = ctx.getChild(0).getText()
        currentName = ctx.getChild(1).getText()
        #We add it into the symbol table
        self.symbolTable.define(currentName, currentType, 'ARG')
        #Then we need to check if there is more
        if childCount > 2:
            for i in range((childCount-2) // 3):
                currentType = ctx.getChild(i*3 + 3).getText()
                currentName = ctx.getChild(i*3 + 4).getText()
                self.symbolTable.define(currentName, currentType, 'ARG')

    def compilesubroutineBody(self, ctx):
        nLocal = 0
        while ctx.getChild(nLocal + 1).getText()[:3] == 'var':
            self.compilevarDec(ctx.getChild(nLocal + 1))
            nLocal += 1
        #We write the function output
        functionName = '{}.{}'.format(self.currentClass, self.currentSubroutineName)
        numLocals = self.symbolTable.varCount('VAR')
        self.vm.writeFunction(functionName, numLocals)
        #Then we push in the stack if its a constructor the object and define in the heap or if it is a method reference the function
        if self.currentSubroutineKind == 'constructor':
            numFields = self.symbolTable.varCount('FIELD')
            self.vm.writePush('CONST', numFields)
            self.vm.writeCall('Memory.alloc', 1)
            self.vm.writePop('POINTER', 0)
        elif self.currentSubroutineKind == 'method':
            self.vm.writePush('ARG', 0)
            self.vm.writePop('POINTER', 0)
        #Then we compile the statements
        self.compileStatemens(ctx.getChild(nLocal + 1))

    def compilevarDec(self, ctx):
        currentType = ctx.getChild(1).getText()
        currentName = ctx.getChild(2).getText()
        #we push the first one of the local variables
        self.symbolTable.define(currentName, currentType, 'VAR')
        #Then we add every symbol if there is left
        childCount = ctx.getChildCount()
        if childCount > 4:
            for i in range((childCount-4) // 2):
                currentName = ctx.getChild(i*2 + 4).getText()
                #Then we push the variable
                self.symbolTable.define(currentName, currentType, 'VAR')

    def compileStatemens(self, ctx):
        childCount = ctx.getChildCount()
        for i in range(childCount):
            currentStatement = ctx.getChild(i)
            if currentStatement.getText()[:3] == 'let':
                self.compileLetStatement(currentStatement.getChild(0))
            elif currentStatement.getText()[:2] == 'if':
                self.compileIfStatement(currentStatement.getChild(0))
            elif currentStatement.getText()[:5] == 'while':
                self.compileWhileStatement(currentStatement.getChild(0))
            elif currentStatement.getText()[:2] == 'do':
                self.compileDoStatement(currentStatement.getChild(0))
            elif currentStatement.getText()[:6] == 'return':
                self.compileReturnStatement(currentStatement.getChild(0))
    
    def compileLetStatement(self, ctx):
        currentName = ctx.getChild(1).getText()
        currentKind = jackListener.CONVERT_KIND[self.symbolTable.kindOf(currentName)]
        currentIndex = self.symbolTable.indexOf(currentName)
        #If it is not found in the symbol table
        if currentIndex == None:
            raise NameError
        
        if ctx.getChild(2).getText() == '[':
            self.compileExpression(ctx.getChild(3))
            self.vm.writePush(currentKind, currentIndex)
            #Then we add the initial position of the array and the length
            self.vm.writeArithmetic('ADD')
            self.vm.writePop('TEMP', 0)
            #Then we compile the expression after the =
            self.compileExpression(ctx.getChild(6))
            self.vm.writePush('TEMP', 0)
            self.vm.writePop('POINTER', 1)
            self.vm.writePop('THAT', 0)
        else:
            #It mean that is not an array
            self.compileExpression(ctx.getChild(3))
            self.vm.writePop(currentKind, currentIndex)

    def compileIfStatement(self, ctx):
        self.ifIndex += 1
        ifIndex = self.ifIndex
        childCount = ctx.getChildCount()
        self.compileExpression(ctx.getChild(2))
        #We check the if statement
        self.vm.writeIf('IF_TRUE{}'.format(ifIndex))
        #Goes to the false or continue true depending of the answer
        self.vm.writeGoto('IF_FALSE{}'.format(ifIndex))
        self.vm.writeLabel('IF_TRUE{}'.format(ifIndex))
        self.compileStatemens(ctx.getChild(5))
        #Goto to the end of the if
        self.vm.writeGoto('IF_END{}'.format(ifIndex))
        #In case of an else
        self.vm.writeLabel('IF_FALSE{}'.format(ifIndex))
        if childCount > 7:
            if ctx.getChild(7).getText() == 'else':
                self.compileStatemens(ctx.getChild(9))
        self.vm.writeLabel('IF_END{}'.format(ifIndex))

    def compileWhileStatement(self, ctx):
        self.whileIndex += 1
        whileIndex = self.whileIndex
        #We write the while start
        self.vm.writeLabel('WHILE{}'.format(whileIndex))
        #We call the expression
        self.compileExpression(ctx.getChild(2))
        #We check the eval condition with inverse logic
        self.vm.writeArithmetic('NOT')
        #We check if the while ends
        self.vm.writeIf('WHILE_END{}'.format(whileIndex))
        #We compile the statments inside the while
        self.compileStatemens(ctx.getChild(5))
        #Then we write the label to repeat the while
        self.vm.writeGoto('WHILE{}'.format(whileIndex))
        self.vm.writeLabel('WHILE_END{}'.format(whileIndex))
        
    def compileDoStatement(self, ctx):
        #We call the function and then we pop the last element in the stack
        self.compileSubroutineCall(ctx.getChild(1))
        self.vm.writePop('TEMP', 0)

    def compileReturnStatement(self, ctx):
        #We check if there is a value, if there is we compile the expression else we push 0 cause there is no value
        childCount = ctx.getChildCount()
        if childCount == 3:
            self.compileExpression(ctx.getChild(1))
        else:
            self.vm.writePush('CONST', 0)
        #Finally we write the return command
        self.vm.writeReturn()

    def compileExpression(self, ctx):
        childCount = ctx.getChildCount()
        #We push the term
        self.compileTerm(ctx.getChild(0))
        for i in range((childCount - 1) // 2):
            #Then we check if there are more terms and we get the operator
            operator = ctx.getChild((i*2) + 1).getText()
            #We calculate the second term and push it into the stack
            self.compileTerm(ctx.getChild((i*2) + 2))
            #Finally we writ ethe operation which we are going to do
            if operator in jackListener.ARITHMETIC.keys():
                self.vm.writeArithmetic(jackListener.ARITHMETIC[operator])
            elif operator == '*':
                self.vm.writeCall('Math.multiply', 2)
            elif operator == '/':
                self.vm.writeCall('Math.divide', 2)

    def compileTerm(self, ctx):
        if ctx.getChild(0).getText().isdigit():
            #Its a integer Constant
            self.vm.writePush('CONST', ctx.getChild(0).getText())
        elif ctx.getChild(0).getText()[0] == '"':
            #Its is a String constant
            self.compileString(ctx.getChild(0).getText())
        elif ctx.getChild(0).getText() in jackListener.keywordConstant:
            #Its is a keyword constant
            self.compileKeyword(ctx.getChild(0).getText())    
        elif ctx.getChild(0).getText() in jackListener.ARITHMETIC_UNARY.keys():
            #If it is a unary operation
            unaryOperation = jackListener.ARITHMETIC_UNARY[ctx.getChild(0).getText()]
            self.compileTerm(ctx.getChild(1))
            self.vm.writeArithmetic(unaryOperation)
        elif ctx.getChild(0).getText() == '(':
            #If it is a (expression)
            self.compileExpression(ctx.getChild(1))
        else:
            #It is a var or a subroutine
            childCount = ctx.getChildCount()
            childCountSubRoutine = ctx.getChild(0).getChildCount()
            if childCount > 1 and ctx.getChild(1).getText() == '[':
                #This an array
                currentArrayName = ctx.getChild(0).getText()
                #We evaluate the expression inside the array [expression]
                self.compileExpression(ctx.getChild(2))
                #Then we find the kind and the index of the array in the simbolTable
                currentArrayKind = self.symbolTable.kindOf(currentArrayName)
                currentArrayIndex = self.symbolTable.indexOf(currentArrayName)
                #We handle the error if we dont found the array
                if currentArrayKind == None or currentArrayIndex == None:
                    raise NameError
                #Then we push the array with the expression calculated
                self.vm.writePush(jackListener.CONVERT_KIND[currentArrayKind], currentArrayIndex)
                self.vm.writeArithmetic('ADD')
                self.vm.writePop('POINTER', 1)
                self.vm.writePush('THAT', 0)
            elif (childCountSubRoutine > 1) and (ctx.getChild(0).getChild(1).getText() == '.' or ctx.getChild(0).getChild(1).getText() == '('):
                #Its a subroutine and we are calling it
                self.compileSubroutineCall(ctx.getChild(0))
            else:
                #Finally its is a variable
                varKind = jackListener.CONVERT_KIND[self.symbolTable.kindOf(ctx.getChild(0).getText())]
                varIndex = self.symbolTable.indexOf(ctx.getChild(0).getText())
                if varIndex == None or varKind == None:
                    raise NameError
                self.vm.writePush(varKind, varIndex)

    def compileSubroutineCall(self, ctx):
        identifier = ctx.getChild(0).getText() #SubroutineName | className | varName
        nArgs = 0
        if ctx.getChild(1).getText() == '(':
            subroutineName = identifier
            functionName = '{}.{}'.format(self.currentClass, subroutineName)
            nArgs += 1
            self.vm.writePush('POINTER', 0)
            #Then we find expression List
            nArgs += self.compileExpressionList(ctx.getChild(2))
        elif ctx.getChild(1).getText() == '.':
            subroutineName = ctx.getChild(2).getText()
            typeIfInstance = self.symbolTable.typeOf(identifier)
            #We check if type is None it is a class else it is an instance
            if typeIfInstance != None:
                #It is an instance
                instanceKind = self.symbolTable.kindOf(identifier)
                instanceIndex = self.symbolTable.indexOf(identifier)
                #We write the instance in the VM
                self.vm.writePush(jackListener.CONVERT_KIND[instanceKind], instanceIndex)
                functionName = '{}.{}'.format(typeIfInstance, subroutineName)
                nArgs += 1
            else:
                #It is a class
                className = identifier
                functionName = '{}.{}'.format(className, subroutineName)
            #Then we find expression List
            nArgs += self.compileExpressionList(ctx.getChild(4))

        #Finally we write the call in the VM
        self.vm.writeCall(functionName, nArgs)
        
    def compileString(self, string):
        pushString = string[1:-1]
        #We push the length of the string
        self.vm.writePush('CONST', len(pushString))
        self.vm.writeCall('String.new', 1)
        #Then for each char we append it and push it (unicode)
        for character in pushString:
            self.vm.writePush('CONST', ord(character))
            self.vm.writeCall('String.appendChar', 2)
    
    def compileKeyword(self, keyword):
        #Then we write the function
        if keyword == 'this':
            self.vm.writePush('POINTER', 0)
        else:
            self.vm.writePush('CONST', 0)
            if keyword == 'true':
                self.vm.writeArithmetic('NOT')
            
    def compileExpressionList(self, ctx):
        #Then we get the number of arguments
        childCount = ctx.getChildCount()
        nArgs = 0
        if childCount > 0:
            #There us one at least
            nArgs += 1
            self.compileExpression(ctx.getChild(0))
            for i in range((childCount-1) // 2):
                self.compileExpression(ctx.getChild(i*2 + 2))
                nArgs += 1
        return nArgs


    
        
    

    

