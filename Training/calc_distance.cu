#include <stdio.h>
#include <math.h>

#define BLOCK_DIM_X 32 
#define BLOCK_DIM_Y 16 

#define VECTOR_DIM 300
#define PARTITION_DIM 32

__global__ void
vectorAdd(float *A, const float *B,unsigned int numElements)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;

    if (i < numElements)
    {
        A[i] = B[i] - A[i];
    }
}


__global__ void 
L2_norm(float *g_idata, float *g_odata)
{
  __shared__ float sdata[256];

  unsigned int tid = threadIdx.x;

  sdata[tid] = 0;
  float A = g_idata[tid + VECTOR_DIM * blockIdx.x];

  sdata[tid] += A * A; 

  if(tid + blockDim.x < 300){   // blockDimx.x = 256
    A = g_idata[tid + blockDim.x + VECTOR_DIM * blockIdx.x];
    sdata[tid] += A * A;
  }

  __syncthreads();

  if (tid < 128) { sdata[tid] += sdata[tid + 128]; } __syncthreads();
  if (tid < 64) { sdata[tid] += sdata[tid + 64]; } __syncthreads();

  if (tid < 32) {
    sdata[tid] += sdata[tid + 32];
  }
  __syncthreads();
  if(tid < 16){
    sdata[tid] += sdata[tid + 16];
  }
  __syncthreads();
  if(tid < 8){
    sdata[tid] += sdata[tid + 8];
  }
  __syncthreads();
  if(tid < 4){
    sdata[tid] += sdata[tid + 4];
  }
  __syncthreads();
  if(tid < 2){
    sdata[tid] += sdata[tid + 2];
  }
  __syncthreads();
  if(tid < 1){
    sdata[tid] += sdata[tid + 1];
  }
  __syncthreads();

  if (tid == 0){
    // printf("%f",sdata[0]);
   g_odata[blockIdx.x] = sqrtf(sdata[0]);
  }

}
__global__ void 
Dot_product(float *A_input, float *B_input,float * output)
{
  __shared__ float sdata[256];

  unsigned int tid = threadIdx.x;

  sdata[tid] = 0;
  float A = A_input[tid + VECTOR_DIM * blockIdx.x];
  float B = B_input[tid + VECTOR_DIM * blockIdx.x];

  sdata[tid] += A * B; 

  if(tid + blockDim.x < 300){
    A = A_input[tid + blockDim.x + VECTOR_DIM * blockIdx.x];
    B = B_input[tid + blockDim.x + VECTOR_DIM * blockIdx.x];
    sdata[tid] += A * B;
  }

  __syncthreads();

  if (tid < 128) { sdata[tid] += sdata[tid + 128]; } __syncthreads();
  if (tid < 64) { sdata[tid] += sdata[tid + 64]; } __syncthreads();

  if (tid < 32) {
    sdata[tid] += sdata[tid + 32];
  }
  __syncthreads();
  if(tid < 16){
    sdata[tid] += sdata[tid + 16];
  }
  __syncthreads();
  if(tid < 8){
    sdata[tid] += sdata[tid + 8];
  }
  __syncthreads();
  if(tid < 4){
    sdata[tid] += sdata[tid + 4];
  }
  __syncthreads();
  if(tid < 2){
    sdata[tid] += sdata[tid + 2];
  }
  __syncthreads();
  if(tid < 1){
    sdata[tid] += sdata[tid + 1];
  }
  __syncthreads();

  if (tid == 0){
    // printf("%f",sdata[0]);
   output[blockIdx.x] = (sdata[0]);
  }

}



__global__ void 
Normalize_vector(float *g_idata)
{
  __shared__ float sdata[256];
  __shared__ float norm;

  unsigned int tid = threadIdx.x;

  sdata[tid] = 0;
  float A = g_idata[tid + VECTOR_DIM * blockIdx.x];

  sdata[tid] += A * A; 

  if(tid + blockDim.x < 300){
    A = g_idata[tid + blockDim.x + VECTOR_DIM * blockIdx.x];
    sdata[tid] += A * A;
  }

  __syncthreads();

  if (tid < 128) { sdata[tid] += sdata[tid + 128]; } __syncthreads();
  if (tid < 64) { sdata[tid] += sdata[tid + 64]; } __syncthreads();

  if (tid < 32) {
    sdata[tid] += sdata[tid + 32];
  }
  __syncthreads();
  if(tid < 16){
    sdata[tid] += sdata[tid + 16];
  }
  __syncthreads();
  if(tid < 8){
    sdata[tid] += sdata[tid + 8];
  }
  __syncthreads();
  if(tid < 4){
    sdata[tid] += sdata[tid + 4];
  }
  __syncthreads();
  if(tid < 2){
    sdata[tid] += sdata[tid + 2];
  }
  __syncthreads();
  if(tid < 1){
    sdata[tid] += sdata[tid + 1];
  }
  __syncthreads();

  if (tid == 0){
    // printf("%f",sdata[0]);
   norm = sqrtf(sdata[0]);
  }
  __syncthreads();

  g_idata[tid + VECTOR_DIM * blockIdx.x] = g_idata[tid + VECTOR_DIM * blockIdx.x]/norm;

  if(tid + blockDim.x < 300){
    g_idata[tid + blockDim.x + VECTOR_DIM * blockIdx.x] = g_idata[tid + blockDim.x + VECTOR_DIM * blockIdx.x]/ norm;
  }

}


__global__ void 
cos_distance(float *A, float *B_L2_NORM, int* Count, unsigned int num_entries)
{
  __shared__ float B_L2_NORM_SHARED;
  __shared__ float B[300];
  __shared__ float AB[16][32];


  int curr_entry = blockDim.y * blockIdx.x + threadIdx.y;
  // printf("%d\n",curr_entry);


  float A_L2_NORM = B_L2_NORM[curr_entry];
  float A_LOCAL[10];

  unsigned int Local_Count = 0;
  



  //Load the current entry
  if(curr_entry < num_entries){

    for(int i = 0; i < VECTOR_DIM;i += PARTITION_DIM){

      if(i+threadIdx.x < VECTOR_DIM){
        A_LOCAL[i / PARTITION_DIM] = A[VECTOR_DIM * curr_entry+i+threadIdx.x];
      }

    }
  }


      __syncthreads();

  //loop through all the entries
  for(unsigned int entry = 0 ; entry < num_entries; entry += 1){
  
    AB[threadIdx.y][threadIdx.x] = 0;

    if (entry < num_entries){

      if(threadIdx.y == 0 && threadIdx.x == 0){
          B_L2_NORM_SHARED = B_L2_NORM[entry];
      }

      int B_index = threadIdx.y * BLOCK_DIM_X + threadIdx.x;
      if( B_index < VECTOR_DIM){
        B[B_index] = A[entry * VECTOR_DIM + B_index];


      }
      __syncthreads();

      for(unsigned int partition = 0; partition < VECTOR_DIM; partition += PARTITION_DIM){
        
        if(partition + threadIdx.x < VECTOR_DIM){
          AB[threadIdx.y][threadIdx.x] += A_LOCAL[partition/PARTITION_DIM] * B[partition + threadIdx.x];
        }
        
      }

      __syncthreads();
      if(threadIdx.x < 16){
        AB[threadIdx.y][threadIdx.x] += AB[threadIdx.y][threadIdx.x+16];
      }
      __syncthreads();
      if(threadIdx.x < 8){
        AB[threadIdx.y][threadIdx.x] += AB[threadIdx.y][threadIdx.x+8];
      }
      __syncthreads();
      if(threadIdx.x < 4){
        AB[threadIdx.y][threadIdx.x] += AB[threadIdx.y][threadIdx.x+4];
      }
      __syncthreads();
      if(threadIdx.x < 2){
        AB[threadIdx.y][threadIdx.x] += AB[threadIdx.y][threadIdx.x+2];
      }
      __syncthreads();
      if(threadIdx.x < 1){
        AB[threadIdx.y][threadIdx.x] += AB[threadIdx.y][threadIdx.x+1];
      }
      __syncthreads();


      if (threadIdx.x == 0 and curr_entry < num_entries){
        // printf("curr_entry %d,%d, %f\n", curr_entry,entry,AB[threadIdx.y][0] /(A_L2_NORM * B_L2_NORM_SHARED));
        if( AB[threadIdx.y][0] / (A_L2_NORM * B_L2_NORM_SHARED) > 0){
          Local_Count += 1;
        }
      }

    }
  }    
  if (threadIdx.x == 0 and curr_entry < num_entries){
    Count[curr_entry] = Local_Count-1;
  }


}




__global__ void 
cos_distance2(float *A, float* B, float *B_L2_NORM, int* Count, unsigned int offset, unsigned int num_entries)
{
  __shared__ float W_2[300];
  __shared__ float W_1[300];
  __shared__ float W_4_W_2[16][32];
  __shared__ float W_4_W_1[16][32];


  int curr_entry = blockDim.y * blockIdx.x + threadIdx.y + offset;

  float A_L2_NORM = B_L2_NORM[curr_entry];
  float W_4_LOCAL[10];

  unsigned int Local_Count = 0;
  



  //Load the current entry
  if(curr_entry < num_entries){

    for(int i = 0; i < VECTOR_DIM;i += PARTITION_DIM){

      if(i+threadIdx.x < VECTOR_DIM){
        W_4_LOCAL[i / PARTITION_DIM] = B[VECTOR_DIM * curr_entry+i+threadIdx.x];
      }

    }
  }


      __syncthreads();

  //loop through all the entries
  for(unsigned int entry = 0 ; entry < num_entries; entry += 1){
  
    W_4_W_2[threadIdx.y][threadIdx.x] = 0;
    W_4_W_1[threadIdx.y][threadIdx.x] = 0;

    if (entry < num_entries){


      int B_index = threadIdx.y * BLOCK_DIM_X + threadIdx.x;
      if( B_index < VECTOR_DIM){
        W_1[B_index] = A[entry * VECTOR_DIM + B_index];
        W_2[B_index] = B[entry * VECTOR_DIM + B_index];


      }
      __syncthreads();

      for(unsigned int partition = 0; partition < VECTOR_DIM; partition += PARTITION_DIM){
        
        if(partition + threadIdx.x < VECTOR_DIM){
          W_4_W_2[threadIdx.y][threadIdx.x] += W_4_LOCAL[partition/PARTITION_DIM] * W_2[partition + threadIdx.x];
          W_4_W_1[threadIdx.y][threadIdx.x] += W_4_LOCAL[partition/PARTITION_DIM] * W_1[partition + threadIdx.x];
        }
        
      }

      __syncthreads();
      if(threadIdx.x < 16){
        W_4_W_2[threadIdx.y][threadIdx.x] += W_4_W_2[threadIdx.y][threadIdx.x+16];
        W_4_W_1[threadIdx.y][threadIdx.x] += W_4_W_1[threadIdx.y][threadIdx.x+16];
      }
      __syncthreads();
      if(threadIdx.x < 8){
        W_4_W_2[threadIdx.y][threadIdx.x] += W_4_W_2[threadIdx.y][threadIdx.x+8];
        W_4_W_1[threadIdx.y][threadIdx.x] += W_4_W_1[threadIdx.y][threadIdx.x+8];
      }
      __syncthreads();
      if(threadIdx.x < 4){
        W_4_W_2[threadIdx.y][threadIdx.x] += W_4_W_2[threadIdx.y][threadIdx.x+4];
        W_4_W_1[threadIdx.y][threadIdx.x] += W_4_W_1[threadIdx.y][threadIdx.x+4];
      }
      __syncthreads();
      if(threadIdx.x < 2){
        W_4_W_2[threadIdx.y][threadIdx.x] += W_4_W_2[threadIdx.y][threadIdx.x+2];
        W_4_W_1[threadIdx.y][threadIdx.x] += W_4_W_1[threadIdx.y][threadIdx.x+2];
      }
      __syncthreads();
      if(threadIdx.x < 1){
        W_4_W_2[threadIdx.y][threadIdx.x] += W_4_W_2[threadIdx.y][threadIdx.x+1];
        W_4_W_1[threadIdx.y][threadIdx.x] += W_4_W_1[threadIdx.y][threadIdx.x+1];
      }
      __syncthreads();


      if (threadIdx.x == 0 and curr_entry < num_entries){
        // printf("curr_entry %d, %f\n", curr_entry,W_4_W_2[threadIdx.y][0] * A_L2_NORM / (W_4_W_2[threadIdx.y][0]) );
        if( W_4_W_2[threadIdx.y][0] * A_L2_NORM / (W_4_W_1[threadIdx.y][0]) > .50){
          Local_Count += 1;
        }
      }

    }
  }    
  if (threadIdx.x == 0 and curr_entry < num_entries){
    Count[curr_entry] = Local_Count;
  }


}
