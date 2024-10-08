// #include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    char *str1 = get_string("Player 1: ");
    char *str2 = get_string("Player 2: ");

    int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

    int score1 = 0;
    int score2 = 0;

    // CALCULATE PLAYER-1 SCORE
    for (int i = 0, len = strlen(str1); i < len; i++)
    {
        char ch = *str1++;

        if (ch >= 65 && ch <= 90)
        {
            score1 += points[ch - 65];
        }
        else if (ch >= 97 && ch <= 122)
        {
            score1 += points[ch - 97];
        }
    }

    // CALCULATE PLAYER-1 SCORE
    for (int i = 0, len = strlen(str2); i < len; i++)
    {
        char ch = *str2++;

        if (ch >= 65 && ch <= 90)
        {
            score2 += points[ch - 65];
        }
        else if (ch >= 97 && ch <= 122)
        {
            score2 += points[ch - 97];
        }
    }

    if (score1 > score2)
    {
        printf("Player 1 wins!...\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!...\n");
    }
    else
    {
        printf("Tie!\n");
    }
}
