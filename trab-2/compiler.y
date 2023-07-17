/* simplest version of calculator */
%{
#include <stdio.h>
#include <stdlib.h>
#include "ast.h"
#include "symbol_table.h"

extern FILE *yyin;
extern char * yytext;

SymbolTable table;

%}

%define parse.error verbose

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

%token NUMBER
%token ID

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
  ast_save($1, "ast.dot");
  table_print(table);
}

Function: Type Id PAREN_LEFT ArgList PAREN_RIGHT CompoundStmt {
  { $$ = ast_create_production("Function", NULL, 4, $1, $2, $4, $6); }
}

ArgList: Arg ArgList2 { $$ = ast_create_production("ArgList", NULL, 2, $1, $2); }

ArgList2: COMMA Arg ArgList2 { $$ = ast_create_production("ArgList2", NULL, 2, $2, $3); } | %empty { $$ = NULL; }

Arg: Type Id { $$ = ast_create_production("Arg", NULL, 2, $1, $2); }
Declaration: Type IdentList SEMICOLON {
    $$ = ast_create_production("Declaration", NULL, 2, $1, $2);
    char *type = ((Ast *) $1)->value;
    printf("variável %s\n", type);

    Ast *ident_list = $2;
    Ast *id_node = list_first(&ident_list->children);

    Id id = (Id){
      .name = id_node->value,
      .type = type,
    };
    table_add_id(&table, id);

    Ast *ident_list_2 = list_nth(&ident_list->children, 1);
    while (ident_list_2 != NULL) {
      Ast *id_node = list_first(&ident_list_2->children);
      Id id = (Id){
        .name = id_node->value,
        .type = type,
      };
      table_add_id(&table, id);

      ident_list_2 = list_nth(&ident_list_2->children, 1);
    }
  }

Type: INT { $$ = ast_create_production("Type", "INT", 0); }
  | FLOAT { $$ = ast_create_production("Type", "FLOAT", 0); }
  | CHAR { $$ = ast_create_production("Type", "CHAR", 0); }

IdentList: Id IdentList2 { $$ = ast_create_production("IdentList", NULL, 2, $1, $2); }

IdentList2: COMMA Id IdentList2 { $$ = ast_create_production("IdentList2", NULL, 2, $2, $3); }
  | %empty { $$ = NULL; }

Stmt: ForStmt { $$ = ast_create_production("Stmt", NULL, 1, $1); }
  | WhileStmt { $$ = ast_create_production("Stmt", NULL, 1, $1); }
  | Expr SEMICOLON { $$ = ast_create_production("Stmt", NULL, 1, $1); }
  | IfStmt { $$ = ast_create_production("Stmt", NULL, 1, $1); }
  | CompoundStmt { $$ = ast_create_production("Stmt", NULL, 1, $1); }
  | Declaration { $$ = ast_create_production("Stmt", NULL, 1, $1); }
  | SEMICOLON { $$ = ast_create_production("Stmt", ";", 0); }

ForStmt: FOR PAREN_LEFT Expr SEMICOLON OptExpr SEMICOLON OptExpr PAREN_RIGHT Stmt {$$ = ast_create_production("ForStmt", NULL, 4, $3, $5, $7, $9);}

OptExpr: Expr {$$ = ast_create_production("OptExpr", NULL, 1, $1);} | %empty { $$ = NULL; }

WhileStmt: WHILE PAREN_LEFT Expr PAREN_RIGHT Stmt {$$ = ast_create_production("WhileStmt", NULL, 2, $3, $5);}

IfStmt: IF PAREN_LEFT Expr PAREN_RIGHT Stmt ElsePart {$$ = ast_create_production("IfStmt", NULL, 3, $3, $5, $6);}
  | IF PAREN_LEFT Expr PAREN_RIGHT Stmt {$$ = ast_create_production("IfStmt", NULL, 2, $3, $5);}

ElsePart: ELSE Stmt {$$ = ast_create_production("ElsePart", NULL, 1, $2);}

CompoundStmt: CURLY_LEFT StmtList CURLY_RIGHT {$$ = ast_create_production("CompoundStmt", NULL, 1, $2);}

StmtList: Stmt StmtList {$$ = ast_create_production("StmtList", NULL, 2, $1, $2);}
  | %empty { $$ = NULL; }

Expr: Id ASSIGN Expr {$$ = ast_create_production("Expr", "assign", 2, $1, $3);}
  | Rvalue {$$ = ast_create_production("Expr", NULL, 1, $1);}

Rvalue: Mag Rvalue2 {
  $$ = ast_create_production("Rvalue", NULL, 2, $1, $2);
}

Rvalue2: Compare Mag Rvalue2 {$$ = ast_create_production("rvalue2", NULL, 3, $1, $2, $3);} | %empty { $$ = NULL; }

Compare: EQ { $$ = ast_create_production("Compare", "EQ", 0); }
  | LT { $$ = ast_create_production("Compare", "LT", 0); }
  | GT { $$ = ast_create_production("Compare", "GT", 0); }
  | LE { $$ = ast_create_production("Compare", "LE", 0); }
  | GE { $$ = ast_create_production("Compare", "GE", 0); }
  | DIF { $$ = ast_create_production("Compare", "DIF", 0); }

Mag: Term Mag2 {$$ = ast_create_production("Mag", NULL, 2, $1, $2);}

Mag2: ADD Term Mag2 { $$ = ast_create_production("Mag2", "ADD", 2, $2, $3); }
  | SUB Term Mag2 { $$ = ast_create_production("Mag2", "SUB", 2, $2, $3); }
  | %empty { $$ = NULL; }

Term: Factor Term2 { $$ = ast_create_production("Term", NULL, 2, $1, $2); }

Term2: MUL Factor Term2 { $$ = ast_create_production("Term2", "MUL", 2, $2, $3); }
  | DIV Factor Term2 { $$ = ast_create_production("Term2", "DIV", 2, $2, $3); }
  | %empty { $$ = NULL; }

Factor: PAREN_LEFT Expr PAREN_RIGHT { $$ = ast_create_production("Factor", "WITH_PARENS", 1, $2); }
  | SUB Factor { $$ = ast_create_production("Factor", "SUB", 1, $2); }
  | ADD Factor { $$ = ast_create_production("Factor", "ADD", 1, $2); }
  | Id { $$ = ast_create_production("Factor", NULL, 1, $1); }
  | Number { $$ = ast_create_production("Factor", NULL, 1, $1); }

Id: ID { $$ = ast_with_value("ID", $<str>1); printf("%s\n", $<str>1); }

Number: NUMBER { $$ = ast_with_value("NUMBER", $<str>1); }

;
%%

int main(int argc, char **argv)
{
  if (argc != 2) {
    printf("usage: cmd <filename>\n");
    exit(1);
  }

  table = table_new();
  
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
