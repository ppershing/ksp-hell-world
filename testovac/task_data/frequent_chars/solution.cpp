#include <stdio.h>
#include <string.h>

char tmp[200000];
int n;
 int cnt[255];
int main() {
  scanf("%d", &n);
  scanf("%s", tmp);
 int l=strlen(tmp);
 for (int i=0; i<l; i++) cnt[tmp[i]]++;
 for (int i='a'; i<='z'; i++)
 	if (cnt[i]>=n)
		printf("%c", (char) i);
 printf("\n");

}
