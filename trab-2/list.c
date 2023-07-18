#include <stdlib.h>
#include "list.h"

List list_new()
{
    return (List){
        .first = NULL,
        .last = NULL,
        .size = 0};
}

void *list_first(List *list)
{
    if (!list->first)
    {
        return NULL;
    }
    return list->first->value;
}

void *list_last(List *list)
{
    if (!list->last)
    {
        return NULL;
    }
    return list->last->value;
}

void *list_nth(List *list, int idx)
{
    if (list->size <= idx || idx < 0)
    {
        return NULL;
    }

    Node *current = list->first;
    for (int i = 0; i < idx; i++)
    {
        current = current->next;
    }

    return current->value;
}

void list_add(List *list, void *value)
{
    list->size += 1;

    Node *new_node = malloc(sizeof(Node));
    new_node->value = value;
    new_node->next = NULL;

    if (!list->last)
    {
        list->first = new_node;
        list->last = new_node;
        return;
    }

    list->last->next = new_node;
    list->last = new_node;
}

void *list_find(List *list, void *value, int (*cmp)(void *value, void *candidate))
{

    for (Node *current = list->first; current != NULL; current = current->next)
    {
        void *candidate = current->value;
        if (cmp(value, candidate))
        {
            return candidate;
        }
    }

    return NULL;
}