#include <stdio.h>
#include <vector>
#include <algorithm>
using namespace std;

#define MAX 1100
int cnt[MAX];

int main(){
    int N;
    scanf("%d\n", &N);
    for (int i=0; i<N; i++) {
        int x;
        scanf("%d", &x);
        cnt[x]++;
    }
    for (int i=0; i<MAX; i++) 
        for (int j=0; j<cnt[i]; j++)
                printf("%d\n", i);
}
