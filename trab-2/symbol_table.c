#include <stdlib.h>
#include <string.h>
#include "list.h"
#include "symbol_table.h"

SymbolTable table_new()
{
    return (SymbolTable){
        .current_ctx = -1,
        .contexts = list_new()};
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

void ctx_add(Ctx *ctx, Id id)
{
    Id *new_id = malloc(sizeof(Id));
    *new_id = id;

    list_add(&ctx->ids, new_id);
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
