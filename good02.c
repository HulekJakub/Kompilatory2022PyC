#include <stdio.h>

int addNumber(int a, int b)
{
    return a + b;
}

int noMainFunction()
{
    int num1 = 2;
    int num2;
    num2 = 3;
    int num3 = addNumber(num1, num2);
    if(num3 == 5)
    {
        printf(num3);
    }
    else if (num3 == 5.0)
    {
        printf(num3);
    }
    else if (num3 == 4)
    {
        printf("Not good, but close.");
    }
    else
    {
        printf("Not good.");
    }
    return 0;
}