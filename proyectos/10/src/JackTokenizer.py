""" This Module removes all comments and white spaces from the input stream and breaks it into 
Jack-language tokens of Jack grammar 
By: Felipe Cortes Jaramillo """

import re

class JackTokenizer:

    # Static variables representing the regular expressions of the language using re API
    LEXICAL_ELEMENTS_MATCHES = ['KEYWORD', 'SYMBOL', 'INT_CONST', 'STRING_CONST',
    'IDENTIFIER']
    KEYWORD          = r'(class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)'
    SYMBOL           = r'([{}()[\].,;+\-*/&|<>=~])'
    INT_CONSTANT     = r'([0-9]|[1-8][0-9]|9[0-9]|[1-8][0-9]{2}|9[0-8][0-9]|99[0-9]|[1-8][0-9]{3}|9[0-8][0-9]{2}|99[0-8][0-9]|999[0-9]|[12][0-9]{4}|3[01][0-9]{3}|32[0-6][0-9]{2}|327[0-5][0-9]|3276[0-7])'
    STRING_CONSTANT  = r'\"([^\n]*)\"'
    IDENTIFIER       = r'([A-Za-z_]\w*)'
    LEXICAL_ELEMENTS = r'{}|{}|{}|{}|{}'.format(KEYWORD, SYMBOL, INT_CONSTANT, STRING_CONSTANT, IDENTIFIER)

    MULTILINE_COMMENTS = r'/\*.*?\*/'
    INLINE_COMMENTS = r'//.*\n'


    def __init__(self, input_file):
        """ Constructor opens the input file to be tokenized """
        self.file = open(input_file)

    def __del__(self):
        """ Destructor whichs destroys the object involved """
        self.file.close()

    def hasMoreTokens(self):
        """ Checks if the input has more tokens """
        pass
    
    def peekToken(self):
        """ This method checks if there is a token """
        


