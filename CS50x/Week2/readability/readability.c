// #include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    char *text = "Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversation?'";

    int len = strlen(text);

    // CALCULATE NO-OF LETTER IN GIVEN TEXT
    int letter = 0;
    int words = 0;
    int sent = 0;
    for (int i = 0; i < len; i++)
    {
        char ch = *text++;
        // TO CONSIDER ONLY LETERS FOR COUNT
        if ((ch >= 65 && ch <= 90) || (ch >= 97 && ch <= 122))
        {
            letter++;
        }

        if (ch == ' ')
        {
            words++;
        }

        if (ch == '.' || ch == '!' || ch == '?')
        {
            sent++;
        }
    }

    words = words + 1; // FOR LAST WORD

    float L = (100 / (float) words) * letter;
    float S = (100 / (float) words) * sent;

    float index = 0.0588 * L - 0.296 * S - 15.8;

    int grade = round(index);
    printf("%f %f", L, S);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %d\n", grade);
    }
}
