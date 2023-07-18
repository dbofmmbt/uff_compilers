#include "converter.h"
#include <string.h>

int equals(char *a, char *b)
{
    return !strcmp(a, b);
}

Ast *build_stmt(Ast *inner)
{
    return ast_create_production("Stmt", NULL, 1, inner);
}

Ast *build_goto_stmt(char *label)
{
    return build_stmt(
        ast_create_production(
            "GotoStmt", NULL, 1,
            ast_with_value("Label", label)));
}

Ast *build_label_stmt(char *label)
{
    return build_stmt(
        ast_create_production(
            "LabelStmt", NULL, 1,
            ast_with_value("Label", label)));
}

Ast *build_stmt_list_end(Ast *stmt)
{
    return ast_create_production("StmtList", NULL, 1, stmt);
}

Ast *build_stmt_list(Ast *stmt, Ast *other_list)
{
    return ast_create_production("StmtList", NULL, 2, stmt, other_list);
}

// while (expr) stmt -> { :start; if (expr) stmt; else goto :end; goto :start; :end; }
static Ast *convert_while(Ast *ast)
{
    Ast *original_expr = convert(list_first(&ast->children));
    Ast *original_stmt = convert(list_nth(&ast->children, 1));

    Ast *start_stmt = build_label_stmt(":start");

    Ast *goto_start = build_goto_stmt(":start");
    Ast *goto_end = build_goto_stmt(":end");

    Ast *else_end = ast_create_production("ElsePart", NULL, 1, goto_end);

    Ast *if_stmt =
        build_stmt(ast_create_production("IfStmt", NULL, 3, original_expr, original_stmt, else_end));

    Ast *end_stmt = build_label_stmt(":end");

    Ast *stmt_list = build_stmt_list(
        start_stmt,
        build_stmt_list(
            if_stmt,
            build_stmt_list(
                goto_start,
                build_stmt_list_end(end_stmt))));

    return ast_create_production("CompoundStmt", NULL, 1, stmt_list);
}

// for (expr; optexpr1; optexpr2) stmt -> { expr; :start; if (optexpr1) stmt; else goto :end; optexpr2; goto :start; :end; }
static Ast *convert_for(Ast *ast)
{
    // TODO convert for
    return ast;
}

Ast *convert(Ast *ast)
{

    for (Node *child = ast->children.first; child; child = child->next)
    {
        Ast *child_node = child->value;

        if (equals("WhileStmt", child_node->type))
        {
            child->value = convert_while(child_node);
        }
        else if (equals("ForStmt", child_node->type))
        {
            child->value = convert_for(child_node);
        }
        else
        {
            child->value = convert(child->value);
        }
    }

    return ast;
}
