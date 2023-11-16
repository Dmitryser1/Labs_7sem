#include "mpi.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctime>

#define NMAX 3200017
#define Q 28

int main(int argc, char *argv[])
{
        srand(time(0));
        float *a = new float[NMAX];
        float *b = new float[NMAX];
        float *c = new float[NMAX];

        double s = 0, j;
        float *a_loc = NULL, *b_loc = NULL, *c_loc = NULL;
        int ProcRank, ProcNum, i;
        int *sendCounts;
        int *displs;
        double st_time, average_time = 0.0;
        MPI_Status status;
        MPI_Init(&argc, &argv);
        for (s = 0; s < 12; ++s)
        {
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

                sendCounts = (int *)malloc(ProcNum * sizeof(int));
                displs = (int *)malloc(ProcNum * sizeof(int));

                for (i = 0; i < ProcNum; ++i)
                {
                        sendCounts[i] = count;
                }

                for (i = 0; i < NMAX % ProcNum; ++i)
                {
                        sendCounts[i] += 1;
                }

                displs[0] = 0;
                for (i = 1; i < ProcNum; ++i)
                {
                        displs[i] = displs[i - 1] + sendCounts[i - 1];
                }

                count = sendCounts[ProcRank];

                a_loc = (float *)malloc(count * sizeof(float));
                b_loc = (float *)malloc(count * sizeof(float));
                c_loc = (float *)malloc(count * sizeof(float));

                MPI_Scatterv(a, sendCounts, displs, MPI_FLOAT, a_loc, count, MPI_FLOAT, 0,
                             MPI_COMM_WORLD);
                MPI_Scatterv(b, sendCounts, displs, MPI_FLOAT, b_loc, count, MPI_FLOAT, 0,
                             MPI_COMM_WORLD);
                if (ProcRank == 0)
                {
                        st_time = MPI_Wtime();
                }
                for (i = 0; i < sendCounts[ProcRank]; ++i)
                {
                        // for (j = 0; j < Q; ++j)
                        // {
                                c_loc[i] = a_loc[i] + b_loc[i];
                        //}
                }

                MPI_Gatherv(c_loc, sendCounts[ProcRank], MPI_FLOAT, c, sendCounts, displs,
                            MPI_FLOAT, 0, MPI_COMM_WORLD);
                MPI_Barrier(MPI_COMM_WORLD);
                if (ProcRank == 0)
                        average_time += MPI_Wtime() - st_time;
                free(a_loc);
                free(b_loc);
                free(c_loc);
                free(sendCounts);
                free(displs);
        }
        if (ProcRank == 0)
        {
                printf("Total process = %d", ProcNum);
                //printf(" with Q = %d", Q);
                printf("\nMPI with Scatterv and Gatherv time of work is %f\n", average_time / 12.0);
        }
        MPI_Finalize();

        return 0;
}
