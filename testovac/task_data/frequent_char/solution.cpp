#include <stdio.h>
#include <string.h>

  char tmp[100000];
  int cnt[255];
int main() {
	scanf("%s", tmp);
	int n=strlen(tmp);
	for (int i=0; i<n; i++) cnt[tmp[i]]++;
	int best='a';
	for (int i='a'; i<='z'; i++)
		if (cnt[best] <= cnt[i])
			best=i;
	printf ("%c\n", best);

}
