#include "mpi.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#define NMAX 3200000
#define Q 28

int main(int argc, char *argv[])
{
        float a[NMAX];
        float b[NMAX];
        float c[NMAX];

        //int* a_loc = NULL, *b_loc = NULL, *c_loc = NULL;
        int ProcRank, ProcNum, i, j, s;
        MPI_Status status;
        double st_time, average_time = 0.0;
        MPI_Init(&argc, &argv);
        MPI_Comm_size(MPI_COMM_WORLD, &ProcNum);
        MPI_Comm_rank(MPI_COMM_WORLD, &ProcRank);
        int count = NMAX / ProcNum;
        if (ProcRank == 0)
        {
                for (i = 0; i < NMAX; ++i)
                {
                        a[i] = 1;
                        b[i] = 1;
                }
        }
        count = NMAX / ProcNum;
        float a_loc[count];
        float b_loc[count];
        float c_loc[count];

        MPI_Scatter(a, count, MPI_FLOAT, a_loc, count, MPI_FLOAT, 0, MPI_COMM_WORLD);
        MPI_Scatter(b, count, MPI_FLOAT, b_loc, count, MPI_FLOAT, 0, MPI_COMM_WORLD);

        if (ProcRank == 0)
        {
                st_time = MPI_Wtime();
        }

        for (i = 0; i < count; ++i)
        {
                //for (j = 0; j < Q; ++j) {
                c_loc[i] = a_loc[i] + b_loc[i];
                //}
        }

        MPI_Gather(c_loc, count, MPI_FLOAT, c, count, MPI_FLOAT, 0, MPI_COMM_WORLD);
        MPI_Barrier(MPI_COMM_WORLD);
        if (ProcRank == 0)
                average_time += MPI_Wtime() - st_time;

        if (ProcRank == 0)
        {
                printf("Total process = %d", ProcNum);
               // printf(" with Q = %d", Q);
                printf("\nMPI time of work is %f\n", average_time);
        }
        // free(a_loc);
        // free(b_loc);
        // free(c_loc);

        MPI_Finalize();

        return 0;
}
