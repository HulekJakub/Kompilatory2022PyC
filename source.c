/* Program w C
    git
*/
//Komentarz
#define PAP 2

int add(int a, int b)
{
  return a + b;
}

int main(int a) {
  int variable = 1;
  double variable2 = 3.2;
  double tab[5];

  if(variable > variable2)
  {
    printf(variable);
    if(variable > variable2)
    {
      printf(variable);
    }
  }
  else if (variable2 > variable)
  {
    printf(variable2);
  }
  else if (add(2, 3) == 5)
  {
    printf("tak");
  }

  //komentarz we funkcji
  /* długi komentarz
  we
  funkcji */

  printf("TAK");
  printf("NIE");

  return 0;
}
