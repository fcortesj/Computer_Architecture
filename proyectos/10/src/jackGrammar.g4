grammar jackGrammar;

/*
* This file contains the grammar of Jack language,
* So the rules below are the derivation rules of the program.
*/

// Parser Rules

classN         : 'class' classNameN '{' classVarDecN* subrutineDecN* '}';
classVarDecN   : ('static'|'field') typeN varNameN (',' varNameN)* ';';
typeN          : 'int'|'char'|'boolean'|classNameN ;
subrutineDecN  : ('constructor'|'function'|'method') ('void'|typeN) subrutineNameN '(' parameterListN ')' subrutineBodyN ;
parameterListN : ((typeN varNameN) (',' typeN varNameN)*)? ;
subrutineBodyN : '{' varDecN* statementsN '}' ;
varDecN        : 'var' typeN varNameN (',' varNameN)* ';' ;
classNameN     : IDENTIFIER ;
subrutineNameN : IDENTIFIER ;
varNameN       : IDENTIFIER ;

//Statements

statementsN      : statementN* ;
statementN       : letStatementN|ifStatementN|whileStatementN|doStatementN|returnStatementN ;
letStatementN    : 'let' varNameN ('[' expressionN ']')? '=' expressionN ';' ;
ifStatementN     : 'if' '(' expressionN ')' '{' statementsN '}' ('else' '{' statementsN '}')? ;
whileStatementN  : 'while' '(' expressionN ')' '{' statementsN '}';
doStatementN     : 'do' subrutineCallN ';' ;
returnStatementN : 'return' expressionN? ';' ;

//Expressions

expressionN      : termN(opN termN)* ;
termN            : INTEGERCONSTANT|STRINGCONSTANT|keywordConstantN|varNameN|varNameN '[' expressionN ']'|subrutineCallN|'(' expressionN ')'|unaryOpN termN ;
subrutineCallN   : subrutineNameN '(' expressionListN ')'|(classNameN|varNameN) '.' subrutineNameN '(' expressionListN ')' ;
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
