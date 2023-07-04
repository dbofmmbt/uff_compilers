/* simplest version of calculator */
%{
#include <stdio.h>
%}


/* declare tokens */
%token NUMBER
%token ADD SUB MUL DIV
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