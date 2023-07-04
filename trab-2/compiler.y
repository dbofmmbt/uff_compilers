/* simplest version of calculator */
%{
#include <stdio.h>
%}


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

%token NEWLINE

%%

calclist: /* nothing */
 | calclist exp NEWLINE { printf("= %d\n", $2); }
 ;

exp: factor 
 | exp ADD factor { $$ = $1 + $3; }
 | exp SUB factor { $$ = $1 - $3; }
 ;

factor: term
 | factor MUL term { $$ = $1 * $3; }
 | factor DIV term { $$ = $1 / $3; }
 ;

term: NUMBER
;
%%

main(int argc, char **argv)
{
  yyparse();
}

yyerror(char *s)
{
  fprintf(stderr, "error: %s\n", s);
}