#define BLOCK_SIZE 16

__global__ void transpose(float* A, float* B, int m, int n)
{
	__shared__ float sm[BLOCK_SIZE][BLOCK_SIZE];

	int tx = threadIdx.x; 	int ty = threadIdx.y;
	int bx = blockIdx.x; 	int by = blockIdx.y;

	int row = by * blockDim.y + ty;
	int col = bx * blockDim.x + tx;		

	if(row<m && col <n)
		sm[ty][tx] = A[row*n+col];
	__syncthreads();

	row = bx * blockDim.y + ty;
	col = by * blockDim.x + tx;

	if(row<n && col < m)
		B[row*m+col] = sm[tx][ty];
	__syncthreads();

	return;
}
