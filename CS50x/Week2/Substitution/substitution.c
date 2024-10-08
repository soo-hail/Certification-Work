// #include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char *args[])
{
    // ERROR HANDLING
    if (argc != 2)
    {
        printf("Usage: ./substitution key ");
        return 1;
    }

    if (strlen(args[1]) != 26)
    {
        printf("Key must contain 26 characters.");
        return 1;
    }

    char upperCase[26];
    char lowerCase[26];
    int isFound[26] = {0};

    for (int i = 0; i < 26; i++)
    {
        char ch = args[1][i];

        if (ch >= 65 && ch <= 90)
        {
            if (isFound[ch - 'A'] == 1) // HANDLING DUPLICATES
            {
                return 1;
            }

            upperCase[i] = ch;
            lowerCase[i] = ch + 32;
            isFound[ch - 'A'] = 1;
        }
        else if (ch >= 97 && ch <= 122)
        {
            if (isFound[ch - 'a'] == 1) // HANDLING DUPLICATES
            {
                return 1;
            }

            upperCase[i] = ch - 32;
            lowerCase[i] = ch;
            isFound[ch - 'a'] = 1;
        }
        else
        {
            printf("Usage: ./substitution key ");
            return 1;
        }
    }

    char *text = get_string("plaintext: ");
    int len = len = strlen(text);

    printf("ciphertext: ");
    for (int i = 0; i < len; i++)
    {
        char ch = text[i];

        if (ch >= 65 && ch <= 90)
        {
            printf("%c", upperCase[(int) ch - 'A']);
        }
        else if (ch >= 97 && ch <= 122)
        {
            printf("%c", lowerCase[(int) ch - 'a']);
        }
        else
        {
            printf("%c", ch);
        }
    }

    printf("\n");
}
