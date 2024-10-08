#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return 1;
    }

    FILE *f = fopen(argv[1], "r");

    if (f == NULL)
    {
        return 2;
    }

    unsigned char buffer[512];

    int count = -1;

    FILE *img = NULL;

    char *filename = malloc(18 * sizeof(char));

    while (fread(buffer, sizeof(buffer), 1, f) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            count++;

            sprintf(filename, "%03i.jpg", count);

            img = fopen(filename, "w");

        }

        if (img != NULL)
        {
            fwrite(buffer, sizeof(buffer), 1, img);
        }

    }

    free(filename);
    fclose(img);
    fclose(f);

    return 0;
}
