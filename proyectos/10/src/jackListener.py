from jackGrammarListener import jackGrammarListener
from jackGrammarParser import jackGrammarParser
import os

class jackListener(jackGrammarListener):

    """
        This class write the xml file form a parser generated. Parse from Jack Program and 
        writes the corresponding xml file.

        By: Felipe Cortes Jaramillo
    """

    keywords = ["class","constructor","function","method","field","static","var","int","char","boolean","void","true","false","null","this","let","do","if","else","while","return"]
    symbol   = ["[","]","{","}","(",")",".",",",";","+","-","*","/","&","|","<",">","=","~"]
    nonTerminal = ["class","classVarDec","subroutineDec","parameterList","subroutineBody","varDec","statements","whileStatement","ifStatement","returnStatement","letStatement","doStatement","expression","term","expressionList"]


    def __init__(self, output, parser):
        """ Constructor of the class receives an output file and a parser """
        self.output = open(output, 'w')
        self.indent_count = 0
        self.parser = parser


    def __del__(self):
        """ Destructor of the class also writes the end of all """
        self.output.close()


    def enterEveryRule(self, ctx):
        """ This method contains all enter rules and write them in the output file (.xml) """
        tag = self.parser.ruleNames[ctx.getRuleIndex()][:-1]
        if tag in jackListener.nonTerminal:
            self.output.write("{}<{}>\n".format(self.current_indent(), self.parser.ruleNames[ctx.getRuleIndex()][:-1]))
            self.increase_indent()
        return super().enterEveryRule(ctx)


    def exitEveryRule(self, ctx):
        """ This method contains all exit rules and write them in the output file (.xml) """
        tag = self.parser.ruleNames[ctx.getRuleIndex()][:-1]
        if tag in jackListener.nonTerminal:
            self.decrease_indent()
            self.output.write("{}</{}>\n".format(self.current_indent(), self.parser.ruleNames[ctx.getRuleIndex()][:-1]))
        return super().exitEveryRule(ctx)


    def visitTerminal(self, node):
        """ This method visits a terminal and writes it in the output file (.xml) """
        terminal = node.getText()
        tag = ""
        #Then we check the conditions to make the tag
        if terminal in jackListener.keywords:
            tag = "keyword"
        elif terminal in jackListener.symbol:
            if terminal == '<':
                terminal = "&lt;"
            if terminal == '>':
                terminal = "&gt;"
            if terminal == '&':
                terminal = "&amp;"
            if terminal == '"':
                terminal = "&quot;"
            tag = "symbol"
        elif  '"' in terminal:
            terminal = terminal[1:-1]
            tag = "stringConstant"
        elif terminal.isdigit():
            number = int(terminal)
            if(number < 0 or number > 32767):
                print("ERROR: Number invalid out of range 0..32767")
                exit(-1)
            tag = "integerConstant"
        else:
            tag = "identifier"
        #Then we write the generated tag
        self.output.write("{}<{}> {} </{}>\n".format(self.current_indent(), tag, terminal, tag))
        return super().visitTerminal(node)


    #Functions to control the indent flow    
    def increase_indent(self):
        """ This function increases the indentiation """
        self.indent_count += 1

    def decrease_indent(self):
        """ This method decresases the indendtation """
        self.indent_count -= 1

    def current_indent(self):
        """ This method return the indentation """
        return '  ' * self.indent_count
