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
    char *name;
    int parent;
    int key;
    List ids;
} Ctx;

typedef struct Id
{
    char *name, *type;
} Id;

SymbolTable table_new();
void table_print(SymbolTable);
int table_add_ctx(SymbolTable *table, char* name);
int table_finish_ctx(SymbolTable *table);
Ctx *table_find_ctx(SymbolTable table, int key);
Ctx *table_ctx_current(SymbolTable table);
void ctx_add(Ctx *ctx, Id id);
Id *ctx_find(Ctx ctx, char *name);

void table_add_id(SymbolTable *table, Id id);

#endif