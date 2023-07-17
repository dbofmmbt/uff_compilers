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
void *list_first(List *);
void *list_last(List *);
// 0-based idx. NULL if position doesn't exist
void *list_nth(List *, int idx);
void list_add(List *list, void *value);
void *list_find(List *list, void *value, int (*cmp)(void *value, void *candidate));

#endif