#ifndef AST
#define AST

#include "list.h"

typedef struct Ast
{
    char *type;
    void *value;
    List children;
} Ast;

void ast_save(Ast *ast, char *file_name);

Ast *ast_create_production(char*type, void*value, int n, ...);

Ast *ast_new(char *type);
Ast *ast_with_value(char *type, void *value);

#endif