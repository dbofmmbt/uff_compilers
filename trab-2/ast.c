#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include "ast.h"

Ast *ast_new(char *type)
{
    Ast *new = malloc(sizeof(Ast));
    *new = (Ast){
        .type = type,
        .children = list_new(),
        .value = NULL,
    };

    return new;
}

Ast *ast_with_value(char *type, void *value)
{
    Ast *ast = ast_new(type);
    ast->value = value;
    return ast;
}

static void ast_add(Ast *ast, Ast *child)
{
    list_add(&ast->children, child);
}

Ast *ast_create_production(char *type, void *value, int n, ...)
{
    Ast *ast = ast_with_value(type, value);

    va_list args;
    va_start(args, n);

    if (ast->children.size > 0)
    {
        printf("unexpected child while adding production\n");
        exit(1);
    }

    for (int i = 0; i < n; i++)
    {
        Ast *child = va_arg(args, Ast *);
        if (child)
        {
            ast_add(ast, child);
        }
    }

    va_end(args);

    return ast;
}

int graphviz_node_count;

static int save_rec(Ast *ast, FILE *f)
{
    int my_id = graphviz_node_count;
    graphviz_node_count += 1;

    if (!ast)
    {
        fprintf(f, "node_%d [label=\"NULL\"]\n", my_id);
        return my_id;
    }

    if (ast->value)
    {
        fprintf(f, "node_%d [label=\"%s (%s)\"]\n", my_id, ast->type, ast->value);
    }
    else
    {
        fprintf(f, "node_%d [label=\"%s\"]\n", my_id, ast->type);
    }

    for (Node *p = ast->children.first; p != NULL; p = p->next)
    {
        int child_id = save_rec(p->value, f);
        fprintf(f, "node_%d -> node_%d\n", my_id, child_id);
    }

    return my_id;
}

void ast_save(Ast *ast, char *file_name)
{
    FILE *f = fopen(file_name, "w");

    graphviz_node_count = 0;
    fprintf(f, "digraph {\n");
    save_rec(ast, f);
    fprintf(f, "}\n");

    fclose(f);
}
