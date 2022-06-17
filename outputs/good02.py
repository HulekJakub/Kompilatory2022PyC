#include <stdio.h>
def addNumber(a: int, b: int):
    return a + b


def noMainFunction():
    num1 = 2
    num2 = int()
    num2=3
    num3 = addNumber(num1, num2)
    if num3 == 5:
        print(num3)
    
    elif num3 == 5.0:
        print(num3)
    
    elif num3 == 4:
        print("Not good, but close.")
    
    else:
        print("Not good.")
    
    return 0


