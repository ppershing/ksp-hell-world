#include <stdio.h>

int main() {
 int s=0;
 int i=1;
  while (!feof(stdin)) {
   int d=-1;
   scanf("%1d", &d);
   if (d==-1) break;
   s = (s + 11 + i*d)%11;
   i*=-1;



  }
  if (s) printf("False\n"); else printf("True\n");

}
