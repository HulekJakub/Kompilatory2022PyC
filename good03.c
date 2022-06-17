#include <stdio.h>
/* Program w C
    git
*/
//Komentarz
#define PAP 2

char b = '3';
const int c = 21;

int main() {
  printf(b);
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

  //komentarz we funkcji
  /* długi komentarz
  we
  funkcji */

  printf("TAK");
  printf("NIE");

  return 0;
}
