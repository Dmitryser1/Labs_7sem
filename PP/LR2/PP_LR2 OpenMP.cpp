#include <omp.h>
#include "stdio.h"
#define NMAX 3200000


int main(int argc, char *argv[]) {
    omp_set_num_threads(12);
    int i, j, Q = 12, count, t;
    double sum, full_time = 0;
    double *a = new double[NMAX];
    for (i = 0; i < NMAX; ++i) {
        a[i] = 1;
    }
    double st_time, end_time;
    full_time = 0;
    //reduction
    for (t = 0; t < 12; ++t) {
        st_time = omp_get_wtime();
#pragma omp parallel for shared(a) private(i, j) reduction(+: sum)
        for (i = 0; i < NMAX; i++) {
            for (j = 0; j < Q; ++j) {
                sum += a[i];
            }
        }
        end_time = omp_get_wtime();
        end_time = end_time - st_time;
        full_time += end_time;
    }
    sum = sum / (12 * Q);
    printf("\n\nReduction Q: %d", Q);
    printf("\nTotal Sum = %10.2f", sum);
    printf("\nTIME OF WORK IS %f ", full_time / 12);

    sum = 0;
    full_time = 0;
    //atomic
    for (t = 0; t < 12; ++t) {
        st_time = omp_get_wtime();
#pragma omp parallel for shared(a) private(i, j)
        for (i = 0; i < NMAX; i++) {

            for (j = 0; j < Q; ++j) {
#pragma omp atomic
                sum += a[i];
            }
        }
        end_time = omp_get_wtime();
        end_time = end_time - st_time;
        full_time += end_time;
    }
    sum = sum / (12 * Q);
    printf("\n\nAtomic Q: %d", Q);
    printf("\nTotal Sum = %10.2f", sum);
    printf("\nTIME OF WORK IS %f ", full_time / 12);
    sum = 0;
    full_time = 0;

    //critical
    for (t = 0; t < 12; ++t) {
        st_time = omp_get_wtime();
#pragma omp parallel for shared(a) private(i, j)
        for (i = 0; i < NMAX; i++) {
            for (j = 0; j < Q; ++j) {
#pragma omp critical
                sum += a[i];
            }
        }
        end_time = omp_get_wtime();
        end_time = end_time - st_time;
        full_time += end_time;
    }
    sum = sum / (12 * Q);
    printf("\n\nCritical Q: %d", Q);
    printf("\nTotal Sum = %10.2f", sum);
    printf("\nTIME OF WORK IS %f ", full_time / 12);
    delete a;
    return 0;
}