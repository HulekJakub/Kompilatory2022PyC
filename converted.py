""" Program w C
    git
"""
#Komentarz
#define PAP 2
def add(a: int, b: int):
    return a + b


def main(a: int):
    variable = 1
    variable2 = 3.2
    tab = [float()] * (5)
    if variable > variable2:
        print(variable)
        if variable > variable2:
            print(variable)
        
    
    elif variable2 > variable:
        print(variable2)
    
    elif add(2, 3) == 5:
        print("tak")
    
    #komentarz we funkcji
    """ długi komentarz
      we
      funkcji """
    print("TAK")
    print("NIE")
    return 0


if __name__ == "__main__":
    main()