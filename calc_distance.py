
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
import scipy
from pycuda.compiler import SourceModule

mod = SourceModule(open("calc_distance.cu").read())
vecAdd = mod.get_function("vectorAdd")
L2_norm = mod.get_function("L2_norm")
Normalize = mod.get_function("Normalize_vector")
Cos_dist = mod.get_function("cos_distance2")
Dot_1D = mod.get_function("Dot_product")

def get_distance_parallel(w_1, w_2):
        global mod, vecAdd

        size_of_array =  w_1.size
        number_of_element = w_1.size /300 

        blocksPerGrid =int((number_of_element + 16.0 - 1) / 16);

        #Allocate memory
        C = np.empty(number_of_element).astype(np.float32)
        Count = np.empty(number_of_element).astype(np.int32)


        #Intialize device Data
        A_gpu = cuda.mem_alloc(w_1.nbytes)
        cuda.memcpy_htod(A_gpu, w_1)

        B_gpu = cuda.mem_alloc(w_2.nbytes)
        cuda.memcpy_htod(B_gpu, w_2)

        C_gpu = cuda.mem_alloc(number_of_element*4)

        Count_gpu = cuda.mem_alloc(number_of_element*4)


        #CALL Kernel Functions
        Normalize(A_gpu, block=(256, 1, 1), grid=(number_of_element, 1))
        Normalize(B_gpu, block=(256, 1, 1), grid=(number_of_element, 1))

        Dot_1D(A_gpu, B_gpu, C_gpu, block=(256, 1, 1), grid=(number_of_element, 1))

        Cos_dist(A_gpu,B_gpu, C_gpu, Count_gpu, np.int32(number_of_element), block=(32,16,1), grid=(blocksPerGrid,1))


        #Free the memories
        cuda.memcpy_dtoh(C, C_gpu)
        A_gpu.free()
        B_gpu.free()
        C_gpu.free()
        cuda.memcpy_dtoh(Count, Count_gpu)
        Count_gpu.free()

        # print C
        # print Count
        return Count, C

def check_distance(w1,w2,w3,w4):
    w_1_np = np.array(w1)
    w_2_np = np.array(w2)
    w_3_np = np.array(w3)
    A = np.array(w4)

    B = w_3_np + w_2_np - w_1_np
    print B

    NUMERATOR = np.sum(A * B)
    DENOMINTOR = np.sqrt(np.sum(A*A)) + np.sqrt(np.sum(B * B))

    if (NUMERATOR / DENOMINTOR) > .1:
            return True
    else:
            return False


if __name__ == "__main__":

        w_1 = np.random.rand(300 * 1).astype(np.float32)
        w_2 = np.random.rand(300 * 1).astype(np.float32)

        w_1_norm = w_1/np.linalg.norm(w_1)
        w_2_norm = w_2/np.linalg.norm(w_2)
        print np.dot(w_1_norm, w_2_norm)

        x, cos = get_distance_parallel(w_1, w_2)
        print cos[0]
