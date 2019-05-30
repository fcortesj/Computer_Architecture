""" This module creates a symbol table which containst the filed, static, arg variables """


class jackSymbolTable:
    """ A symbol table that associates names with information needed for Jack compilation: type, kind, and running index 
        By: Felipe Cortes Jaramillo 
    """

    def __init__(self):
        """ Constructor of the class """
        # Symbol table will be a dictionary which contains a list for each variable, incluid it`s id, type, kind and number depending on it`s kind
        # We will have a global program table, in which every subroutine scope will be contained
        self.symbolTable = {"class": {}, "subroutine": {}}
        # Symbol table running index
        self.counts = {'STATIC': 0, 'FIELD': 0, 'ARG': 0, 'VAR': 0}

    def startRoutine(self):
        """ Starts a new subroutine scope. Erases previous subroutine values """
        self.symbolTable["subroutine"] = {}
        self.counts['ARG'] = 0
        self.counts['VAR'] = 0

    def define(self, name, tipe, kind):
        """ Defines a new identifier of a given name, type, and kind and assigns it a running index """
        if kind == "STATIC": 
            self.symbolTable["class"][name] = [tipe, kind, self.counts['STATIC']]
            self.counts['STATIC'] += 1
        elif kind == "FIELD":
            self.symbolTable["class"][name] = [tipe, kind, self.counts['FIELD']]
            self.counts['FIELD'] += 1
        elif kind == "ARG":
            self.symbolTable["subroutine"][name] = [tipe, kind, self.counts['ARG']]
            self.counts['ARG'] += 1
        elif kind == "VAR":
            self.symbolTable["subroutine"][name] = [tipe, kind,self.counts['VAR']]
            self.counts['VAR'] += 1
    
    def varCount(self, kind):
        """ Returns the number of variables of the given kind already defined in the current scope """
        return self.counts[kind]

    def kindOf(self, name):
        """ Returns the kind of the named identifier in the current scope. Returns NONE if the identifier is unknown in the current scope """
        if name in self.symbolTable["subroutine"]:  
            return self.symbolTable["subroutine"][name][1]
        elif name in self.symbolTable["class"]:
            return self.symbolTable["class"][name][1]
        else:
            return None
        
    def typeOf(self, name):
        """ Returns the type of the named identifier in the current scope """
        if name in self.symbolTable["subroutine"]:  
            return self.symbolTable["subroutine"][name][0]
        elif name in self.symbolTable["class"]:
            return self.symbolTable["class"][name][0]
        else:
            return None

    def indexOf(self, name):
        """ Returns the index assigned to named identifier """
        if name in self.symbolTable["subroutine"]:  
            return self.symbolTable["subroutine"][name][2]
        elif name in self.symbolTable["class"]:
            return self.symbolTable["class"][name][2]
        else:
            return None
