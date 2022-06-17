#include <stdio.h>

int addNumber(int a, int b)
{
    return a + b;
}

int main()
{
    int num1 = 2;
    int num2;
    num2 = 3;
    int num3 = addNumber(num1, num2);
    if(num3 == 5)
    {
        printf(num3);
    }
    else
    {
        printf("Not good.");
    }
    return 0;
}