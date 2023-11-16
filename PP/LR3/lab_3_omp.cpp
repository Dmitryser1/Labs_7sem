#define CHUNK 100
#define NMAX 3200000
#define TNUM 4
#include <omp.h>
#include <stdio.h>

void static_instruction(float *a, float *b)
{
	omp_set_num_threads(TNUM);
	float sum[NMAX];
	int i, t, Q = 28, j;
	double st_time, end_time, full_time = 0;
	for (t = 0; t < 12; ++t)
	{
		st_time = omp_get_wtime();
#pragma omp parallel for shared(a, b, sum) schedule(static, 100)
		for (i = 0; i < NMAX; i++)
		{
			// for (j = 0; j < Q; ++j) {
			sum[i] = a[i] + b[i];
			//}
		}
		end_time = omp_get_wtime();
		end_time = end_time - st_time;
		full_time += end_time;
	}
	printf("Static");
	printf("\nTIME OF WORK IS %f ", full_time / 12);
	printf("\nsum[0]=%f, a[0]=%f b[0]=%f", sum[0], a[0], b[0]);
	printf("\nsum[1]=%f, a[1]=%f, b[1]=%f", sum[1], a[1], b[1]);
	printf("\nsum[2]=%f, a[2]=%f, b[2]=%f", sum[2], a[2], b[2]);
}

void dynamic_instruction(float *a, float *b)
{
	omp_set_num_threads(TNUM);
	float sum[NMAX];
	int i, t, Q = 28, j;
	double st_time, end_time, full_time = 0;
	for (t = 0; t < 12; ++t)
	{
		st_time = omp_get_wtime();
#pragma omp parallel for shared(a, b, sum) schedule(dynamic, 100)
		for (i = 0; i < NMAX; i++)
		{
			// for (j = 0; j < Q; ++j)
			// {
				sum[i] = a[i] + b[i];
			//}
		}
		end_time = omp_get_wtime();
		end_time = end_time - st_time;
		full_time += end_time;
	}
	printf("\nDynamic");
	printf("\nTIME OF WORK IS %f ", full_time / 12);
	printf("\nsum[0]=%f, a[0]=%f, b[0]=%f", sum[0], a[0], b[0]);
	printf("\nsum[1]=%f, a[1]=%f, b[1]=%f", sum[1], a[1], b[1]);
	printf("\nsum[2]=%f, a[2]=%f, b[2]=%f", sum[2], a[2], b[2]);
}

void guided_instruction(float *a, float *b)
{
	omp_set_num_threads(TNUM);
	float sum[NMAX];
	int i, t, Q = 28, j;
	double st_time, end_time, full_time = 0;
	for (t = 0; t < 12; ++t)
	{
		st_time = omp_get_wtime();
#pragma omp parallel for shared(a, b, sum) schedule(guided, 100)
		for (i = 0; i < NMAX; i++)
		{
			// for (j = 0; j < Q; ++j)
			// {
				sum[i] = a[i] + b[i];
			//}
		}
		end_time = omp_get_wtime();
		end_time = end_time - st_time;
		full_time += end_time;
	}
	printf("\nGuided");
	printf("\nTIME OF WORK IS %f ", full_time / 12);
	printf("\nsum[0]=%f, a[0]=%f, b[0]=%f", sum[0], a[0], b[0]);
	printf("\nsum[1]=%f, a[1]=%f, b[1]=%f", sum[1], a[1], b[1]);
	printf("\nsum[2]=%f, a[2]=%f, b[2]=%f", sum[2], a[2], b[2]);
}

int main()
{
	float a[NMAX];
	float b[NMAX];
	int value = 3;
	for (int i = 0; i < NMAX; i++)
	{
		a[i] = 1;
		b[i] = 2;
	}
	static_instruction(a, b);
	dynamic_instruction(a, b);
	guided_instruction(a, b);
	return 0;
}