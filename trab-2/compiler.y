/* simplest version of calculator */
%{
#include <stdio.h>

extern FILE *yyin;
%}

%error-verbose

/* declare tokens */
%token INT
%token FLOAT
%token CHAR

%token FOR
%token WHILE
%token IF
%token ELSE

%token ADD
%token SUB
%token MUL
%token DIV

%token ASSIGN

%token EQ
%token DIF

%token LT
%token GT
%token LE
%token GE

%token COMMA
%token SEMICOLON
%token PAREN_LEFT
%token PAREN_RIGHT
%token CURLY_LEFT
%token CURLY_RIGHT

%token NUMBER
%token ID

%%


// EXAMPLE

Function: Type ID PAREN_LEFT ArgList PAREN_RIGHT CompoundStmt

ArgList: Arg ArgList2

ArgList2: COMMA Arg ArgList2 | %empty

Arg: Type ID
Declaration: Type IdentList SEMICOLON

Type: INT | FLOAT | CHAR

IdentList: ID IdentList2

IdentList2: COMMA ID IdentList2 | %empty

Stmt: ForStmt | WhileStmt | Expr SEMICOLON | IfStmt | CompoundStmt | Declaration | SEMICOLON

ForStmt: FOR PAREN_LEFT Expr SEMICOLON OptExpr SEMICOLON OptExpr PAREN_RIGHT Stmt

OptExpr: Expr | %empty

WhileStmt: WHILE PAREN_LEFT Expr PAREN_RIGHT Stmt

IfStmt: IF PAREN_LEFT Expr PAREN_RIGHT Stmt ElsePart
  | IF PAREN_LEFT Expr PAREN_RIGHT Stmt

ElsePart: ELSE Stmt

CompoundStmt: CURLY_LEFT StmtList CURLY_RIGHT

StmtList: Stmt StmtList | %empty

Expr: ID ASSIGN Expr | Rvalue

Rvalue: Mag Rvalue2

Rvalue2: Compare Mag Rvalue2 | %empty

Compare: EQ
  | LT
  | GT
  | LE
  | GE
  | DIF

Mag: Term Mag2

Mag2: ADD Term Mag2 | SUB Term Mag2 | %empty

Term: Factor Term2

Term2: MUL Factor Term2 | DIV Factor Term2 | %empty

Factor: PAREN_LEFT Expr PAREN_RIGHT
  | SUB Factor
  | ADD Factor
  | ID
  | NUMBER

;
%%

int main(int argc, char **argv)
{
  if (argc != 2) {
    printf("usage: cmd <filename>\n");
    exit(1);
  }
  
  FILE *file = fopen(argv[1], "r");
  if (!file) {
    printf("couldn't open %s\n", argv[1]);
    exit(1);
  }
  yyin = file;

  return yyparse();
}

int yyerror(char *s)
{
  fprintf(stderr, "error: %s\n", s);
}
