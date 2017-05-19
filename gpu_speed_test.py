import time
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
from pycuda.compiler import SourceModule

mod = SourceModule(open("gpu.cu").read())
trans_kernel = mod.get_function("transpose")

A_Host = np.ones(10000 * 784).astype(np.float32)
T_Host = np.ones(10000 * 784).astype(np.float32)

A_gpu = cuda.mem_alloc(A_Host.nbytes)
cuda.memcpy_htod(A_gpu, A_Host)

T_gpu = cuda.mem_alloc(T_Host.nbytes)
cuda.memcpy_htod(T_gpu, T_Host)
import time

def test_gpu():
        global mod, vecAdd, A_gpu,T_gpu, A_Host
        m = 10000
        n = 784
        block_size = 16
        block0 = (block_size, block_size, 1)
        grid0 = (n/block_size+1, m/block_size+1,1)
        trans_kernel(A_gpu,T_gpu,np.intc(m),np.intc(n), block=block0, grid = grid0 );


start = time.time()

setup = "from __main__ import test_gpu"


# time =  timeit.timeit("test_gpu()",
# setup=setup, number = 1000)
test_gpu()
end = time.time()
print(end - start)

A_gpu.free()
T_gpu.free()
print "free"

