#include <stdio.h>
#include <stdarg.h>
#include "list.h"

typedef struct Ast
{
    Ast *parent;
    char *type;
    List children;
} Ast;

static void ast_add(Ast *ast, char *child_type)
{
    Ast *new = malloc(sizeof(Ast));
    *new = (Ast){
        .children = list_new(),
        .parent = ast,
        .type = child_type};

    list_add(&ast->children, new);
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
        char *type = va_arg(args, char *);

        ast_add(ast, type);
    }

    va_end(args);
}

int graphviz_node_count;

void ast_save(Ast *ast, char *file_name)
{
    FILE *f = fopen(file_name, "w");

    graphviz_node_count = 0;
    fprintf(f, "graph {\n");
    save_rec(ast, f);
    fprintf(f, "}\n");

    fclose(f);
}

static int save_rec(Ast *ast, FILE *f)
{
    int my_id = graphviz_node_count;
    graphviz_node_count += 1;

    fprintf(f, "node_%d\n", my_id);
    for (Node *p = ast->children.first; p != NULL; p = p->next)
    {
        int child_id = save_rec(&p->value, f);
        fprintf(f, "node_%d -> node_%d\n", my_id, child_id);
    }

    return my_id;
}
