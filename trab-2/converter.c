#include "converter.h"
#include <string.h>

int equals(char *a, char *b)
{
    return !strcmp(a, b);
}

Ast *convert(Ast *ast)
{

    for (Node *child = ast->children.first; child; child = child->next)
    {
        Ast *child_node = child->value;

        if (equals("WhileStmt", ast->type))
        {
        }
        else if (equals("ForStmt", ast->type))
        {
        }
        else
        {
            child->value = convert(child->value);
        }
    }

    return ast;
}
