#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include "ast.h"

Ast ast_new(char *type)
{
    return (Ast){
        .type = type,
        .children = list_new(),
    };
}

static void ast_add(Ast *ast, Ast *child)
{
    list_add(&ast->children, child);
}

void ast_add_production(Ast *ast, int n, ...)
{
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

        ast_add(ast, child);
    }

    va_end(args);
}

int graphviz_node_count;

static int save_rec(Ast *ast, FILE *f)
{
    int my_id = graphviz_node_count;
    graphviz_node_count += 1;

    fprintf(f, "node_%d\n", my_id);
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
    fprintf(f, "graph {\n");
    save_rec(ast, f);
    fprintf(f, "}\n");

    fclose(f);
}
