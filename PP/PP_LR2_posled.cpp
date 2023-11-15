// Подключение необходимых библиотек
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define VECTOR_SIZE 8200000

int main(int argc, char *argv[]) {
    int i, j, num_iterations = 12, count, q = 12;
    double sum, total_time = 0;
    double *vector_a = new double[VECTOR_SIZE];
    // Инициализация вектора a
    for (i = 0; i < VECTOR_SIZE; ++i) {
        vector_a[i] = 1;
    }

    double start_time, end_time;

    sum = 0;
// Последовательное суммирование
    for (count = 0; count < num_iterations; count++) {
        start_time = clock();
        for (i = 0; i < VECTOR_SIZE; i++) {
            for (j = 0; j < q; ++j) {
                sum += vector_a[i];
            }
        }
        end_time = clock();
        end_time = end_time - start_time;
        total_time += end_time;
    }

    sum = sum / (num_iterations * q);
    printf("\nConsistent Q: %d", q);
    printf("\nTotal Sum = %10.2f", sum);
    printf("\nTIME OF WORK IS %f ", total_time / num_iterations);

    sum = 0;
    total_time = 0;

    return 0;
}