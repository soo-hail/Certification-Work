// #include <cs50.h>
#include <stdio.h>

void americanCard(long int n);
void masterCard(long int n);
void visa(long int n);

int checkSum(long int n);

int main(void)
{
    long int num = get_long("Number: ");

    long int val = num;

    int count = 0;
    int st = 0; // first two digits
    while (val != 0)
    {
        val = val / 10;
        count++;

        if (val < 100 && val > 10)
        {
            st = val;
        }
    }

    if ((count == 13 || count == 16) && (st >= 40 && st <= 49))
    {
        visa(num);
    }
    else if (count == 15 && (st == 34 || st == 37))
    {
        americanCard(num);
    }
    else if (count == 16 && (st > 50 && st < 56))
    {
        masterCard(num);
    }
    else
    {
        printf("INVALID\n");
    }
}

// AMERICANCARD()
void americanCard(long int n)
{
    if (checkSum(n))
    {
        printf("AMEX\n");
    }
    else
    {
        printf("INVALID\n");
    }
}

// MASTERCARD()
void masterCard(long int n)
{
    if (checkSum(n))
    {
        printf("MASTERCARD\n");
    }
    else
    {
        printf("INVALID\n");
    }
}

// VISA()
void visa(long int n)
{
    printf("");
    if (checkSum(n))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}

// CHECKSUM()
int checkSum(long int n)
{
    int sum1 = 0;
    int sum2 = 0;

    long int val = n;

    int i = 1; // TRACKER FOR "POSITION-OF-DIGIT"
    while (val != 0)
    {
        int rem;

        rem = val % 10;
        val /= 10;

        if (i % 2 == 0)
        {
            int currDigit = rem * 2;

            if (currDigit > 9)
            {
                while (currDigit != 0)
                {
                    rem = currDigit % 10;
                    currDigit /= 10;
                    sum1 += rem;
                }
            }
            else
            {
                sum1 += currDigit;
            }
        }
        else
        {
            sum2 += rem;
        }

        i++; // UPDATE TRACKER
    }

    int total = sum1 + sum2;

    if (total % 10 == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}
