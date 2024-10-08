// #include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h;

    do
    {
        h = get_int("Height: ");
    }
    while (!(h > 0 && h < 9));

    for (int i = 0; i < h; i++) // TO TRACK NO. OF ROWS OF A PYRAMID
    {
        for (int j = 0; j < h - (i + 1); j++) // TO PRINT SPACES
        {
            printf(" ");
        }

        for (int j = 0; j <= i; j++) // TO PRINT FIRST-HALF OF PYRAMID
        {
            printf("#");
        }

        printf("  "); // 2-SPACE GAP BETWEEN THEM

        for (int j = 0; j <= i; j++) // TO PRINT SECOND-HALF OF PYRAMID
        {
            printf("#");
        }

        printf("\n");
    }
}
