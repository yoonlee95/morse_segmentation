
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
from pycuda.compiler import SourceModule

mod = SourceModule(open("calc_distance.cu").read())
vecAdd = mod.get_function("vectorAdd")
L2_norm = mod.get_function("L2_norm")
Normalize = mod.get_function("Normalize_vector")
Cos_dist = mod.get_function("cos_distance2")
Dot_1D = mod.get_function("Dot_product")

def get_distance_parallel(w_1, w_2):
        global mod, vecAdd

        # w_1 = np.ones(300 * 1).astype(np.float32)
        # w_2 = np.ones(300 * 1).astype(np.float32)

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
        A_gpu.free()
        B_gpu.free()

        cuda.memcpy_dtoh(C, C_gpu)
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

        import timeit
        from vectorize_word import vectorize_word

        setup = "from __main__ import get_distance"
        setup2 = "from __main__ import get_distance_parallel"

        #     w1 = [1,1,1,1]
        #     w2 = [1,1,1,2]
        #     w3 = [-1,1,1,1]
        #     w4 = [1,-1,1,2]

        #     print check_distance(w1,w2,w3,w4)

        #     time =  timeit.timeit("get_distance()"
        #     , setup=setup, number = 100)/100
        #     print time
        WORD_REPR = 'fasttext'
        WORD_REPR_DATA = 'wiki.en.bin'
        # # WORD_REPR = 'word2vec'
        # # WORD_REPR_DATA = 'wiki.en.vec'
        # WORD_REP = vectorize_word(WORD_REPR, WORD_REPR_DATA)
        # # x = np.array(WORD_REP.get_vector('book')).astype(np.float32)
        # # y = np.array(WORD_REP.get_vector('booked')).astype(np.float32)
        # # analogies = [("","","",""),("","","",""),("","","",""),("","","",""),("","","",""),("","","","")]
        # analogies = [("play","played","jump","jumped"), ("play","playing","jump","jumping"),("car","cars","apple","apples"),("jump","car","apple","shoes"),("holy","hello","friend","researcher"),("catch","nut","pineapple","listen")]

        # for a in analogies:
        #         w_1 = []
        #         w_2 = []

        #         w_1.extend(WORD_REP.get_vector(a[0]))
        #         w_2.extend(WORD_REP.get_vector(a[1]))

        #         w_1.extend(WORD_REP.get_vector(a[2]))
        #         w_2.extend(WORD_REP.get_vector(a[3]))
        #         print a
        #         count = get_distance_parallel(np.asarray(w_1, dtype=np.float32), np.asarray(w_2, dtype=np.float32))
        #         print count

        w_1 = []
        w_2 = []
        get_distance_parallel(w_1, w_2)


        # print x
        # print y
        # x = np.concatenate( (x,np.array(WORD_REP.get_vector('room'))))
        # y = np.concatenate( (y,np.array(WORD_REP.get_vector('roomed'))))
        # x = 1
        # y = 1
        # get_distance_parallel()
        graph = []
        # for i in range(200):
        #         x = (i +1)* 200
        #         time =  timeit.timeit("get_distance_parallel("+str(x)+")",
        #         setup=setup2, number = 1)/1
        #         # print time
        #         graph.append((x,time))
        # print graph
                
# w_1 = np.ones(300 * number_of_element).astype(np.float32)
# w_2 = np.ones(300 * number_of_element).astype(np.float32)

# w_1 = np.random.randn(300*number_of_element).astype(np.float32)
# w_2 = np.random.randn(300*number_of_element).astype(np.float32)

# w_1 = np.concatenate((w_1, np.zeros(300))).astype(np.float32)
# w_2 = np.concatenate((w_2, np.zeros(300))).astype(np.float32)
        # cuda.memcpy_dtoh(w_1, A_gpu)