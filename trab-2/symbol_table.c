#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "list.h"
#include "symbol_table.h"

SymbolTable table_new()
{
    SymbolTable table = (SymbolTable){
        .current_ctx = -1,
        .contexts = list_new()};

    // adding global ctx
    table_add_ctx(&table);

    return table;
}

void table_print(SymbolTable table)
{
    printf("\n-------------- SYMBOL TABLE --------------\n\n");

    for (Node *i = table.contexts.first; i != NULL; i = i->next)
    {
        Ctx *ctx = i->value;
        printf("ctx %d:\n", ctx->key);

        for (Node *j = ctx->ids.first; j != NULL; j = j->next)
        {
            Id *id = j->value;
            printf("    %s: %s\n", id->name, id->type);
        }
        printf("\n");
    }
}

// returns ctx number
int table_add_ctx(SymbolTable *table)
{
    Ctx *new_ctx = malloc(sizeof(Ctx));
    *new_ctx = (Ctx){
        .parent = table->current_ctx,
        .key = table->contexts.size,
        .ids = NULL};

    table->current_ctx = new_ctx->key;
    list_add(&table->contexts, new_ctx);

    return new_ctx->key;
}

int cmp_ctx_key(int key, Ctx *candidate)
{
    return key == candidate->key;
}

Ctx *table_find_ctx(SymbolTable table, int key)
{
    return list_find(&table.contexts, key, cmp_ctx_key);
}

Ctx *table_ctx_current(SymbolTable table)
{
    return table_find_ctx(table, table.current_ctx);
}

int find_id_by_name(char *name, Id *id)
{
    return !strcmp(name, id->name);
}

// NULL if not found
Id *ctx_find(Ctx ctx, char *name)
{
    return list_find(&ctx.ids, name, find_id_by_name);
}

void ctx_add(Ctx *ctx, Id id)
{
    if (ctx_find(*ctx, id.name))
    {
        printf("\e[1;31mSímbolo '%s' já presente no contexto!!!\e[0m\n", id.name);
        exit(1);
    }

    Id *new_id = malloc(sizeof(Id));
    *new_id = id;

    list_add(&ctx->ids, new_id);
}

void table_add_id(SymbolTable *table, Id id)
{
    Ctx *current = table_ctx_current(*table);
    ctx_add(current, id);
}
