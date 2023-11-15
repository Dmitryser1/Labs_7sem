#include <cstdio>
#include <cstdlib>
#include "mpi.h"

int main(int argc, char *argv[]) {
    double *a, *b, TotalSum, ProcSum = 0.0;
    int ProcRank, ProcNum, N = 8200000, i, j, Q = 12, k;
    double st_time, end_time;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &ProcNum);
    MPI_Comm_rank(MPI_COMM_WORLD, &ProcRank);
    if (ProcRank == 0) {
        a = static_cast<double *>(malloc(N * sizeof(double)));
        for (i = 0; i < N; ++i) a[i] = 1;
    }
    b = static_cast<double *>(malloc((N / ProcNum) * sizeof(double)));
    MPI_Scatter(a, N / ProcNum, MPI_DOUBLE, b, N / ProcNum, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    if (ProcRank == 0) free(a);
    st_time = MPI_Wtime();
    k = N / ProcNum;
    for (i = 0; i < k; ++i) for (j = 0; j < Q; ++j) ProcSum = ProcSum + b[i];
    ProcSum /= (double) Q;
    MPI_Reduce(&ProcSum, &TotalSum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
    end_time = MPI_Wtime();
    end_time = end_time - st_time;
    if (ProcRank == 0) {
        printf(" Sum = %10.2f", TotalSum);
        printf("\n Time = %f \n", end_time);
    }
    free(b);
    MPI_Finalize();
    return 0;
}