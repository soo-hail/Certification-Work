#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float avg = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // CALCULATE AVERAGE
            avg = (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / (float)3.0;

            // CONVERT IMAGE
            image[i][j].rgbtBlue = round(avg);
            image[i][j].rgbtGreen = round(avg);
            image[i][j].rgbtRed = round(avg);
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        int start = 0;
        int end = width - 1;

        while(start < end)
        {
            RGBTRIPLE temp = image[i][start];
            image[i][start] = image[i][end];
            image[i][end] = temp;

            start++;
            end--;
        }
    }

    return;
}

RGBTRIPLE getblurValue(int col, int row, int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE grid[3][3];
    int rSum = 0, gSum = 0, bSum = 0;
    int rAvg, gAvg, bAvg, divider = 0;

    for (int i = row - 1; i < row + 2; i++)
    {
        for (int j = col - 1; j < col + 2; j++)
        {
            if ((i >= 0 && i < height) && (j >= 0 && j < width))
            {
                grid[i - (row - 1)][j - (col - 1)] = image[i][j];
                divider++;
            }
            else
            {
                grid[i - (row - 1)][j - (col - 1)].rgbtRed = 0;
                grid[i - (row - 1)][j - (col - 1)].rgbtGreen = 0;
                grid[i - (row - 1)][j - (col - 1)].rgbtBlue = 0;
            }

        }
    }

    //   TRAVERSE GRID
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            rSum += grid[i][j].rgbtRed;
            gSum += grid[i][j].rgbtGreen;
            bSum += grid[i][j].rgbtBlue;
        }
    }

    rAvg = round((float)rSum / divider);
    gAvg = round((float)gSum / divider);
    bAvg = round((float)bSum / divider);

    RGBTRIPLE avg;

    avg.rgbtRed = (rAvg < 0) ? 0 : (rAvg > 255) ? 255 : rAvg;
    avg.rgbtGreen = (gAvg < 0) ? 0 : (gAvg > 255) ? 255 : gAvg;
    avg.rgbtBlue = (bAvg < 0) ? 0 : (bAvg > 255) ? 255 : bAvg;

    return avg;
}

void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    RGBTRIPLE blurValue;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            blurValue = getblurValue(j, i, height, width, temp);

            image[i][j].rgbtRed = blurValue.rgbtRed;
            image[i][j].rgbtGreen = blurValue.rgbtGreen;
            image[i][j].rgbtBlue = blurValue.rgbtBlue;
        }
    }

    return;
}


// Detect edges

RGBTRIPLE getedgeValue(int x, int y, int height, int width, RGBTRIPLE image[height][width])
{
    int kernalX[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int kernalY[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    RGBTRIPLE sec[3][3];
    int rGx = 0, gGx = 0, bGx = 0, rGy = 0, gGy = 0, bGy = 0, fR, fG, fB;
    RGBTRIPLE edgeValue;

    for (int i = y - 1; i < y + 2; i++)
    {
        for (int j = x - 1; j < x + 2; j++)
        {
            if ((i > - 1 && i < height) && (j > - 1 && j < width))
            {
                sec[i - (y - 1)][j - (x - 1)] = image[i][j];
            }
            else
            {
                sec[i - (y - 1)][j - (x - 1)].rgbtRed = 0;
                sec[i - (y - 1)][j - (x - 1)].rgbtGreen = 0;
                sec[i - (y - 1)][j - (x - 1)].rgbtBlue = 0;
            }

        }
    }

    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            rGx += kernalX[i][j] * sec[i][j].rgbtRed;
            gGx += kernalX[i][j] * sec[i][j].rgbtGreen;
            bGx += kernalX[i][j] * sec[i][j].rgbtBlue;
        }
    }

    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            rGy += kernalY[i][j] * sec[i][j].rgbtRed;
            gGy += kernalY[i][j] * sec[i][j].rgbtGreen;
            bGy += kernalY[i][j] * sec[i][j].rgbtBlue;
        }
    }

    fR = round(sqrt(pow(rGx, 2) + pow(rGy, 2)));
    fG = round(sqrt(pow(gGx, 2) + pow(gGy, 2)));
    fB = round(sqrt(pow(bGx, 2) + pow(bGy, 2)));

    edgeValue.rgbtRed = (fR < 0) ? 0 : (fR > 255) ? 255 : fR;
    edgeValue.rgbtGreen = (fG < 0) ? 0 : (fG > 255) ? 255 : fG;
    edgeValue.rgbtBlue = (fB < 0) ? 0 : (fB > 255) ? 255 : fB;

    return edgeValue;
}

void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE image2[height][width];
    RGBTRIPLE edgeValue;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image2[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            edgeValue = getedgeValue(j, i, height, width, image2);

            image[i][j].rgbtRed = edgeValue.rgbtRed;
            image[i][j].rgbtGreen = edgeValue.rgbtGreen;
            image[i][j].rgbtBlue = edgeValue.rgbtBlue;
        }
    }

    return;
}
