%%cu

#include <cublas_v2.h>
#include <malloc.h>
#include <stdio.h>
#include <stdlib.h>

        __global__ void addKernel(float* c, float* a, float* b, unsigned int size) {
    for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < size; i += blockDim.x * gridDim.x)
        c[i] = a[i] + b[i];
}

int main(int argc, char* argv[])
{
    int GRID_DIM = 2048;
    int BLOCK_DIM = 256;
    int n = 8200000;
    printf("n = %d\n", n);
    printf("BLOCK_DIM = %d, GRID_DIM = %d\n", BLOCK_DIM, GRID_DIM);
    int n2b = n * sizeof(float);

    float* a = (float*)calloc(n, sizeof(float));
    float* b = (float*)calloc(n, sizeof(float));
    float* c = (float*)calloc(n, sizeof(float));
    float* c_ = (float*)calloc(n, sizeof(float));

    for (int i = 0; i < n; i++) {
        a[i] = float(i);
        b[i] = float(i);
    }

    cudaEvent_t start_p, stop_p;
    float cpuTime = 0.0f;
    cudaError_t cuerr = cudaEventCreate(&start_p);
    if (cuerr != cudaSuccess) {
        fprintf(stderr, "Cannot create CUDA start event: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    cuerr = cudaEventCreate(&stop_p);
    if (cuerr != cudaSuccess) {
        fprintf(stderr, "Cannot create CUDA end event: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    cuerr = cudaEventRecord(start_p, 0);
    if (cuerr != cudaSuccess) {
        fprintf(stderr, "Cannot record start_p CUDA event: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }

    for (int i = 0; i < n; i++) {
        c_[i] = a[i] + b[i];
    }

    cuerr = cudaEventRecord(stop_p, 0);
    if (cuerr != cudaSuccess)
    {
        fprintf(stderr, "Cannot record stop_p CUDA event: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    cuerr = cudaEventElapsedTime(&cpuTime, start_p, stop_p);
    cudaEventDestroy(start_p);
    cudaEventDestroy(stop_p);


    float* adev = NULL;
    cuerr = cudaMalloc((void**)&adev, n2b);
    if (cuerr != cudaSuccess) {
        fprintf(stderr, "Cannot allocate device array for a: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    float* bdev = NULL;
    cuerr = cudaMalloc((void**)&bdev, n2b);
    if (cuerr != cudaSuccess) {
        fprintf(stderr, "Cannot allocate device array for b: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    float* cdev = NULL;
    cuerr = cudaMalloc((void**)&cdev, n2b);
    if (cuerr != cudaSuccess) {
        fprintf(stderr, "Cannot allocate device array for c: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    cudaEvent_t start, stop;
    float gpuTime = 0.0f;
    cuerr = cudaEventCreate(&start);
    if (cuerr != cudaSuccess) {
        fprintf(stderr, "Cannot create CUDA start event: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    cuerr = cudaEventCreate(&stop);
    if (cuerr != cudaSuccess) {
        fprintf(stderr, "Cannot create CUDA end event: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    cuerr = cudaMemcpy(adev, a, n2b, cudaMemcpyHostToDevice);
    if (cuerr != cudaSuccess) {
        fprintf(stderr, "Cannot copy a array from host to device: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    cuerr = cudaMemcpy(bdev, b, n2b, cudaMemcpyHostToDevice);
    if (cuerr != cudaSuccess) {
        fprintf(stderr, "Cannot copy b array from host to device: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    cuerr = cudaEventRecord(start, 0);
    if (cuerr != cudaSuccess) {
        fprintf(stderr, "Cannot record start CUDA event: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    addKernel <<< GRID_DIM, BLOCK_DIM >>> (cdev, adev, bdev, n);
    cuerr = cudaGetLastError();
    if (cuerr != cudaSuccess)
    {
        fprintf(stderr, "Cannot launch CUDA kernel: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    cuerr = cudaDeviceSynchronize();
    if (cuerr != cudaSuccess)
    {
        fprintf(stderr, "Cannot synchronize CUDA kernel: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    cuerr = cudaEventRecord(stop, 0);
    if (cuerr != cudaSuccess) {
        fprintf(stderr, "Cannot record stop CUDA event: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    cuerr = cudaMemcpy(c, cdev, n2b, cudaMemcpyDeviceToHost);
    if (cuerr != cudaSuccess)
    {
        fprintf(stderr, "Cannot copy c array from device to host: %s\n",
                cudaGetErrorString(cuerr));
        return 0;
    }
    cuerr = cudaEventElapsedTime(&gpuTime, start, stop);
    printf("seq time: %.9f seconds\n", cpuTime / 1000);
    printf("time spent executing %s: %.9f seconds\n", "kernel", gpuTime / 1000);
    for (int i = 0; i < 5; i++) {
        printf("a: %.2f b: %.2f c: %.2f\n", a[i], b[i], c[i]);
    }
    cudaEventDestroy(start);
    cudaEventDestroy(stop);
    cudaFree(adev);
    cudaFree(bdev);
    cudaFree(cdev);
    free(a);
    free(b);
    free(c);
    free(c_);
    return 0;
}
