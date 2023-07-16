#ifndef SYMBOL_TABLE
#define SYMBOL_TABLE

#include "list.h"

typedef struct SymbolTable
{
    int current_ctx;
    List contexts;
} SymbolTable;

typedef struct Ctx
{
    int parent;
    int key;
    List ids;
} Ctx;

typedef struct Id
{
    char *name, *type;
} Id;

SymbolTable table_new();
int table_add_ctx(SymbolTable *table);
Ctx *table_find_ctx(SymbolTable table, int key);
Ctx *table_ctx_current(SymbolTable table);
void ctx_add(Ctx *ctx, Id id);
Id *ctx_find(Ctx ctx, char *name);

#endif