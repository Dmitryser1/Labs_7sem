#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NMAX 3200000
#define ITERATIONS 12

int main(int argc, char* argv[]) {
	float i, q, a[NMAX], b[NMAX], sum[NMAX], j;
	double start_time, end_time;

	for (i = 0; i < NMAX; ++i) {
		a[i] = 1;
		b[i] = 1;
	}

	start_time = clock();
	for (j = 0; j < ITERATIONS; ++j) {
		for (i = 0; i < NMAX; ++i) {
			sum[i] = a[i] + b[i];
		}
	}
	end_time = clock();

	printf("\nLinear with N = %d", NMAX);
	printf("\nLINEAR TIME OF WORK IS %f", (end_time - start_time) / CLOCKS_PER_SEC / ITERATIONS);

	return 0;
}
 

