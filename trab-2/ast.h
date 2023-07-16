#ifndef AST
#define AST

#include "list.h"

typedef struct Ast
{
    char *type;
    List children;
} Ast;

void ast_save(Ast *ast, char *file_name);

void ast_add_production(Ast *ast, int n, ...);

Ast ast_new(char *type);

#endif