#include<stdio.h>
#include<stdlib.h>

int NA, NB;
char A[100+5];
int _A[100+5];
char B[100+5];
int _B[100+5];
char C[100+5];
signed main() {
	scanf("%d %s %d %s", &NA, A, &NB, B);

	int M = NA > NB ? NA : NB;

	for(int i=0;i<NA;i++)
		_A[i] = A[NA-i-1] - '0';
	for(int i=0;i<NB;i++)
		_B[i] = B[NB-i-1] - '0';


	int d = 0;
	for(int i=0;i<M;i++) {
		int res = 0;
		if(i >= NA) {
			res = _B[i] + d;
		} else if(i >= NB) {
			res = _A[i] + d;
		} else {
			//printf("%d\n", i);
			res = _A[i] + _B[i] + d;
		}
		if(res >= 10) {
			d = 1;
			res -= 10;
		} else d = 0;
		C[i] = '0' + res;
		if(i == M-1 && d != 0) M +=1;
	}
	char _C[100+5];
	for(int i=0;i<M;i++)
		_C[i] = C[M-i-1];
	_C[M] = '\0';
	printf("%s", _C);
	return 0;
}
