#include <stdio.h>
""" Program w C
    git
"""
#Komentarz
#define PAP 2
b = '3'
c = 21
def printHello():
    print("Hello")
    return 
    print("Not hello")

def main():
    print(b)
    printHello()
    variable = 1
    variable2 = 3.2
    tab = [float()] * (5)
    i = 0
    while(i < 5):
        tab[i] = i * 2
        print(tab[i])
        while True:
            if variable == 1 and variable2 == 3.2:
                print("OK")
                break
        i += 1
    a = 1
    a = int(input())
    while True:
        a += 1
        if not a <= 1:
            break
    print(a)
    #komentarz we funkcji
    """ długi komentarz
      we
      funkcji """
    print("TAK")
    print("NIE")
    return 0

if __name__ == "__main__":
    main()