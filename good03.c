#include <stdio.h>
/* Program w C
    git
*/
//Komentarz
#define PAP 2


int main() {
  int variable = 1;
  double variable2 = 3.2;
  double tab[5];

  for(int i=0; i<5; i++)
  {
    tab[i] = i*2;
    printf(tab[i]);
  }

  //komentarz we funkcji
  /* długi komentarz
  we
  funkcji */

  printf("TAK");
  printf("NIE");

  return 0;
}
