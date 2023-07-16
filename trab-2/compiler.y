/* simplest version of calculator */
%{
#include <stdio.h>
#include <stdlib.h>
#include "ast.h"
#include "symbol_table.h"

extern FILE *yyin;
extern char * yytext;
%}

%error-verbose

%union {
  char *str;
  int int_val;
  void *ast;
}

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

%token <int_val> NUMBER
%token <str> ID

%type <ast> Program
%type <ast> Function
%type <ast> ArgList
%type <ast> ArgList2
%type <ast> Arg
%type <ast> Declaration
%type <ast> Type
%type <ast> IdentList
%type <ast> IdentList2
%type <ast> Stmt
%type <ast> ForStmt
%type <ast> OptExpr
%type <ast> WhileStmt
%type <ast> IfStmt
%type <ast> ElsePart
%type <ast> CompoundStmt
%type <ast> StmtList
%type <ast> Expr
%type <ast> Rvalue
%type <ast> Rvalue2
%type <ast> Compare
%type <ast> Mag
%type <ast> Mag2
%type <ast> Term
%type <ast> Term2
%type <ast> Factor
%type <ast> Id
%type <ast> Number


%%


// EXAMPLE

Program: Function {
  printf("program\n");
}

Function: Type ID PAREN_LEFT ArgList PAREN_RIGHT CompoundStmt {
  $$ = ast_new("function");
}

ArgList: Arg ArgList2

ArgList2: COMMA Arg ArgList2 | %empty { $$ = NULL; }

Arg: Type ID
Declaration: Type IdentList SEMICOLON

Type: INT | FLOAT | CHAR

IdentList: ID IdentList2

IdentList2: COMMA ID IdentList2 | %empty { $$ = NULL; }

Stmt: ForStmt | WhileStmt | Expr SEMICOLON | IfStmt | CompoundStmt | Declaration | SEMICOLON

ForStmt: FOR PAREN_LEFT Expr SEMICOLON OptExpr SEMICOLON OptExpr PAREN_RIGHT Stmt

OptExpr: Expr | %empty { $$ = NULL; }

WhileStmt: WHILE PAREN_LEFT Expr PAREN_RIGHT Stmt

IfStmt: IF PAREN_LEFT Expr PAREN_RIGHT Stmt ElsePart
  | IF PAREN_LEFT Expr PAREN_RIGHT Stmt

ElsePart: ELSE Stmt

CompoundStmt: CURLY_LEFT StmtList CURLY_RIGHT

StmtList: Stmt StmtList | %empty { $$ = NULL; }

Expr: ID ASSIGN Expr | Rvalue

Rvalue: Mag Rvalue2 {
  Ast *ast = ast_create_production("rvalue", NULL, 2, $1, $2);
  $$ = ast;
  // ast_save(ast, "ast.dot");
}

Rvalue2: Compare Mag Rvalue2 {$$ = ast_create_production("rvalue2", NULL, 3, $1, $2, $3);} | %empty { $$ = NULL; }

Compare: EQ { $$ = ast_create_production("Compare", "EQ", 0); }
  | LT { $$ = ast_create_production("Compare", "LT", 0); }
  | GT { $$ = ast_create_production("Compare", "GT", 0); }
  | LE { $$ = ast_create_production("Compare", "LE", 0); }
  | GE { $$ = ast_create_production("Compare", "GE", 0); }
  | DIF { $$ = ast_create_production("Compare", "DIF", 0); }

Mag: Term Mag2 {$$ = ast_create_production("mag", NULL, 2, $1, $2);}

Mag2:
  | ADD Term Mag2 { $$ = ast_create_production("Mag2", "ADD", 2, $2, $3); }
  | SUB Term Mag2 { $$ = ast_create_production("Mag2", "SUB", 2, $2, $3); }
  | %empty { $$ = NULL; }

Term: Factor Term2 { $$ = ast_create_production("Term", NULL, 2, $1, $2); }

Term2:
  | MUL Factor Term2 { $$ = ast_create_production("Term2", "MUL", 2, $2, $3); }
  | DIV Factor Term2 { $$ = ast_create_production("Term2", "DIV", 2, $2, $3); }
  | %empty { $$ = NULL; }

Factor:
  | PAREN_LEFT Expr PAREN_RIGHT { $$ = ast_create_production("Factor", "WITH_PARENS", 1, $2); }
  | SUB Factor { $$ = ast_create_production("Factor", "SUB", 1, $2); }
  | ADD Factor { $$ = ast_create_production("Factor", "ADD", 1, $2); }
  | Id { $$ = ast_create_production("Factor", NULL, 1, $1); }
  | Number { $$ = ast_create_production("Factor", NULL, 1, $1); ast_save($$, "ast.dot"); }

Id:
  ID { $$ = ast_with_value("ID", strdup(yytext)); }

Number:
  NUMBER { $$ = ast_with_value("NUMBER", strdup(yytext)); }

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
