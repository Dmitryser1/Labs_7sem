// Подключение необходимых библиотек
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char* argv[])
{
    int vector_size = 8200000;
    int vector_bytes = vector_size * sizeof(double);
    int vector_length = vector_size;
    // Выделение памяти на хосте для векторов
    double* vector_a = (double*)calloc(vector_length, sizeof(double));
    double* vector_b = (double*)calloc(vector_length, sizeof(double));
    double* vector_c = (double*)calloc(vector_length, sizeof(double));

    // Инициализация векторов
    for(int i = 0; i < vector_length; i++){
        vector_a[i] = (double)(i + 1);
        vector_b[i] = (double)((i + 1) * (i + 1));
    }

    // Суммирование векторов
    clock_t sum_time;
    clock_t start_time = clock();

    // Последовательное суммирование векторов
    for (int k = 0; k < vector_length; k++) {
        vector_c[k] = vector_a[k] + vector_b[k];
    }

    clock_t end_time = clock();
    printf("\nSEQUENTIAL: %.4f second(s)\n", ((double) end_time - start_time) / ((double) CLOCKS_PER_SEC));

    // Вывод первых пяти элементов вектора c
    for(int i = 0; i < 5; i++){
        printf("a: %f + b: %f = c:%f\n", vector_a[i], vector_b[i], vector_c[i]);
    }

    // Освобождение памяти
    free(vector_a);
    free(vector_b);
    free(vector_c);
    return 0;
}
