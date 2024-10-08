#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>
#include <stdint.h>

#include "dictionary.h"

uint32_t COUNT = 0u;

typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}node;

const unsigned int N = 10000;

node *table[N];

void toLower(char *str)
{
    for (size_t i = 0; str[i] != '\0'; i++)
    {
        str[i] = tolower(str[i]);
    }
}

bool check(const char *word)
{
    char copy[LENGTH + 1];
    strcpy(copy, word);
    toLower(copy);

    uint32_t hashIndx = hash(copy);
    node *ptr = table[hashIndx];
    while (ptr != NULL)
    {
        if (strcmp(ptr->word, copy) == 0)
        {
            return true;
        }

        ptr = ptr->next;
    }

    return false;
}

unsigned int hash(const char *word)
{
    unsigned int hashIndx = 0;
    for (size_t i = 0; word[i] != '\0'; i++)
    {
        hashIndx += word[i];
    }

    return hashIndx%N;
}

void insert(char *word) {
    node *newNode = malloc(sizeof(node));

    if (newNode == NULL) {
        return;
    }

    strcpy(newNode->word, word);
    newNode->next = NULL;

    int hashIndx = hash(word);

    if (table[hashIndx] == NULL) {
        table[hashIndx] = newNode;
    } else {
        newNode->next = table[hashIndx];
        table[hashIndx] = newNode;
    }

    COUNT++;
}

void print_rec(node *n)
{
    if (n == NULL)
    {
        return;
    }
    printf("%s -> ", n->word);
    print_rec(n->next);
}

void print_table()
{
    for (size_t i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            print_rec(table[i]);
            printf("\n");
        }
    }
}

bool load(const char *dictionary)
{
    char word[LENGTH + 1];

    FILE *f = fopen(dictionary, "r");
    if(f == NULL){
        return false;
    }

    while (fscanf(f, "%s", word) == 1) { // TO READ EACH WORD AT A TIME.
        toLower(word);
        insert(word);
    }

    fclose(f);

    return true;
}

unsigned int size(void)
{
    return COUNT;
}

bool unload(void)
{
    for (size_t i = 0; i < N; i++)
    {
        node *ptr = table[i];
        node *temp;
        while (ptr != NULL)
        {
            temp = ptr->next;
            free(ptr);
            ptr = temp;
        }

        table[i] = NULL;
    }

    return true;
}
