// #include <cs50.h>
#include <stdio.h>
#include <string.h>

struct candidate
{
    char *name;
    int votes;
};

int candidate_count;
struct candidate candidates[9];

bool vote(char *name);
void print_winner(void);

int main(int argc, char *argv[])
{

    candidate_count = argc - 1;

    if (candidate_count < 1 || candidate_count > 9)
    {
        return 1;
    }

    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    for (int i = 0; i < voter_count; i++)
    {
        char *name = get_string("Vote: ");

        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    print_winner();
}

bool vote(char *name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes += 1;
            return true;
        }
    }

    return false;
}

void print_winner(void)
{
    int max = candidates[0].votes;
    for (int i = 0; i < candidate_count; i++)
    {
        if (max < candidates[i].votes)
        {
            max = candidates[i].votes;
        }
    }

    for (int i = 0; i < candidate_count; i++)
    {
        if (max == candidates[i].votes)
        {
            printf("%s\n", candidates[i].name);
        }
    }
}
