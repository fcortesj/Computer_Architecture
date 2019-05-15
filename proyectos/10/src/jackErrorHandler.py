from antlr4.error.ErrorListener import ErrorListener

class ErrorHandler(ErrorListener):

    def __init__(self):
        super(ErrorHandler, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception("Syntax Error: Token {} couldn`t be recognized in line: {} and column: {} ".format(offendingSymbol.text, line, column))