#include <stdio.h>
/* Program w C
    git
*/
//Komentarz
#define PAP 2

char b = '3';
const int c = 21;

void printHello()
{
    printf("Hello");
    return;
    printf("Not hello");
}

int main() {
  printf(b);
  printHello();
  int variable = 1;
  double variable2 = 3.2;
  double tab[5];

  for(int i=0; i<5; i++)
  {
    tab[i] = i*2;
    printf(tab[i]);
    while(true)
    {
      if(variable == 1 && variable2 == 3.2)
      {
        printf("OK");
        break;
      }
    }
  }

  int a = 1;
  scanf(&a);
  do
  {
    a += 1;
  }
  while(a <= 1);
  printf(a);

  //komentarz we funkcji
  /* długi komentarz
  we
  funkcji */

  printf("TAK");
  printf("NIE");

  return 0;
}
