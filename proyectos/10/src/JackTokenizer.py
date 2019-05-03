""" This Module removes all comments and white spaces from the input stream and breaks it into 
Jack-language tokens of Jack grammar 
By: Felipe Cortes Jaramillo """

import re
import itertools

class JackTokenizer:

    # Static variables representing the regular expressions of the language using re API
    LEXICAL_ELEMENTS_MATCHES = ['KEYWORD', 'SYMBOL', 'INT_CONST', 'STRING_CONST',
    'IDENTIFIER']
    KEYWORD          = r'(class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)'
    SYMBOL           = r'([{}()[\].,;+\-*/&|<>=~])'
    INT_CONSTANT     = r'(/d+)'
    STRING_CONSTANT  = r'\"([^\n]*)\"'
    IDENTIFIER       = r'([A-Za-z_]\w*)'
    LEXICAL_ELEMENTS = r'{}|{}|{}|{}|{}'.format(KEYWORD, SYMBOL, INT_CONSTANT, STRING_CONSTANT, IDENTIFIER)

    MULTILINE_COMMENTS = r'/\*[\s\S]*?\*/'
    INLINE_COMMENTS = r'//.*\n?'
    COMMENTS = r'{}|{}'.format(MULTILINE_COMMENTS, INLINE_COMMENTS)


    def __init__(self, input_file):
        """ Constructor opens the input file to be tokenized creates the tokens list and the peekeable tokens """
        self.file = open(input_file, 'r')
        self.tokens = None
        self.peekeable = None
        self.currentToken = None

    def __del__(self):
        """ Destructor whichs destroys the object involved """
        self.file.close()

    def hasMoreTokens(self):
        """ Checks if the input has more tokens """
        try:
            next(self.peekeable)
        except StopIteration:
            return False
        return True

    def advance(self):
        """ This method advance the read header one position """
        self.currentToken = next(self.tokens)

    def tokenType(self):
        """This method returns the token type of the current token analized"""
        tokenT = self.currentToken.groups().index(self.currentToken.group().strip("\""))
        if tokenT == 0:
            return "KEYWORD"
        elif tokenT == 1:
            return "SYMBOL"
        elif tokenT == 2:
            return "INT_CONST"
        elif tokenT == 3:
            return "STRING_CONST"
        elif tokenT == 4:
            return "IDENTIFIER"
    
    def tokenize(self):
        """ This method change the expression to individual tokens which are going to be a filed variable of the class and also we create the peekeable list 
            And removes the comments in line and in block"""
        #Remove inLine comments
        streamNoComments = re.sub(JackTokenizer.COMMENTS, '', self.file.read())
        tokensStream = re.finditer(JackTokenizer.LEXICAL_ELEMENTS,streamNoComments)
        self.peekeable, self.tokens = itertools.tee(tokensStream)

    def keyword(self):
        """ This method returns the keyword of the token if it is a keyword """
        return self.currentToken.group().upper()
    
    def symbol(self):
        """ This method returns the character which is the current Token """
        return self.currentToken.group()
    
    def identifier(self):
        """ This method returns the identifier of the token """
        return self.currentToken.group()
    
    def intVal(self):
        """ This method return the integer value of the token """
        val = int(self.currentToken.group())
        if val < 0 or val > 32767:
            print("ERROR: Integer value {} beyond range".format(val))
            exit(-1)
        else:
            return val
    
    def stringVal(self):
        """ This method returns the string of the token """
        return self.currentToken.group().strip("\"") 

    
# lex = JackTokenizer("Main.jack")
# lex.tokenize()
# while lex.hasMoreTokens():
#     lex.advance()
#     tokent = lex.tokenType()
#     if tokent == "KEYWORD":
#         print(lex.keyword())
#     elif tokent == "SYMBOL":
#         print(lex.symbol())
#     elif tokent == "IDENTIFIER":
#         print(lex.identifier())
#     elif tokent == "STRING_CONST":
#         print(lex.stringVal())
#     elif tokent == "INT_CONST":
#         print(lex.intVal())
