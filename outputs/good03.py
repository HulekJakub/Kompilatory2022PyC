#include <stdio.h>
""" Program w C
    git
"""
#Komentarz
#define PAP 2
b = '3'
c = 21
def main():
    print(b)
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
    #komentarz we funkcji
    """ długi komentarz
      we
      funkcji """
    print("TAK")
    print("NIE")
    return 0

if __name__ == "__main__":
    main()