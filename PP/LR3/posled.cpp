#include <cstdio>
#include <ctime>

int main(int argc, char* argv[]) {
    int Q = 28;
    int n = 3200000;
    float *a = new float [n], *sum = new float [n], *b = new float [n];
    // инициализация массивов
    for (int j = 0; j < n; j++) {
        a[j] = 1;
        b[j] = 1;
        sum[j] = 0;
    }
    //суммирование векторов
    double st_time, end_time = 0;
    //последовательная программа
    for (int timeCount = 0; timeCount < 12; timeCount++) {
        st_time = clock();
        for (int k = 0; k < n; k++) {
            for (int j = 0; j < Q; j++) {
                sum[k] += a[k] + b[k];
            }
        }
        end_time += clock() - st_time;
    }
    printf("\nSEQUENCE: %f ", end_time / (12 * CLOCKS_PER_SEC));
    printf("\nsum[0]=%f, a[0]=%f, b[0]=%f", sum[0], a[0], b[0]);
    printf("\nsum[1]=%f, a[1]=%f, b[1]=%f", sum[1], a[1], b[1]);
    printf("\nsum[2]=%f, a[2]=%f, b[2]=%f", sum[2], a[2], b[2]);
    return 0;
}
