#ifndef LIST
#define LIST

typedef struct Node
{
    void *value;
    struct Node *next;
} Node;

typedef struct List
{
    int size;
    Node *first;
    Node *last;
} List;

List list_new();
void list_add(List *list, void *value);
void *list_find(List *list, void *value, int (*cmp)(void *value, void *candidate));

#endif