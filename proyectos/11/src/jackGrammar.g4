grammar jackGrammar;

/*
* This file contains the grammar of Jack language,
* So the rules below are the derivation rules of the program.
*/

// Parser Rules

classN         : 'class' classNameN '{' classVarDecN* subroutineDecN* '}';
classVarDecN   : ('static'|'field') typeN varNameN (',' varNameN)* ';';
typeN          : 'int'|'char'|'boolean'|classNameN ;
subroutineDecN  : ('constructor'|'function'|'method') ('void'|typeN) subroutineNameN '(' parameterListN ')' subroutineBodyN ;
parameterListN : ((typeN varNameN) (',' typeN varNameN)*)? ;
subroutineBodyN : '{' varDecN* statementsN '}' ;
varDecN        : 'var' typeN varNameN (',' varNameN)* ';' ;
classNameN     : IDENTIFIER ;
subroutineNameN : IDENTIFIER ;
varNameN       : IDENTIFIER ;

//Statements

statementsN      : statementN* ;
statementN       : letStatementN|ifStatementN|whileStatementN|doStatementN|returnStatementN ;
letStatementN    : 'let' varNameN ('[' expressionN ']')? '=' expressionN ';' ;
ifStatementN     : 'if' '(' expressionN ')' '{' statementsN '}' ('else' '{' statementsN '}')? ;
whileStatementN  : 'while' '(' expressionN ')' '{' statementsN '}';
doStatementN     : 'do' subroutineCallN ';' ;
returnStatementN : 'return' expressionN? ';' ;

//Expressions

expressionN      : termN(opN termN)* ;
termN            : INTEGERCONSTANT|STRINGCONSTANT|keywordConstantN|varNameN|varNameN '[' expressionN ']'|subroutineCallN|'(' expressionN ')'|unaryOpN termN ;
subroutineCallN   : subroutineNameN '(' expressionListN ')'|(classNameN|varNameN) '.' subroutineNameN '(' expressionListN ')' ;
expressionListN  : (expressionN(',' expressionN)*)? ;
opN              : '+'|'-'|'*'|'/'|'&'|'|'|'<'|'>'|'=' ;
unaryOpN         : '-'|'~' ;
keywordConstantN : 'true'|'false'|'null'|'this' ;

//Lexer Rules

INTEGERCONSTANT    : [0-9]+;
STRINGCONSTANT     : '"'~["\n]*'"';
IDENTIFIER         : [A-Za-z_]([0-9a-zA-Z_])*;
WS                 : [ \t\r\n]+ -> channel(HIDDEN);
MULTILINE_COMMENTS : '/*' .*? '*/' -> skip;
INLINE_COMMENTS    : '//' ~[\r\n]* -> skip;
