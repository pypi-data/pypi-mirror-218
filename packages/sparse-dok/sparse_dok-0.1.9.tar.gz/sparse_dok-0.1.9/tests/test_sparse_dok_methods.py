import torch
import numpy as np
from torchtimer import ProfilingTimer

from DOKSparse.sparse_dok import SparseDOKTensor
from DOKSparse.sparse_dok import functions as fs
from DOKSparse.sparse_dok import util

timer = ProfilingTimer()
device = "cuda:0"
sparsity = 0.9
iters = 100
warmup_iters = 3
size = (1000, 1000)

all_dtypes = ["int8", "uint8", "int64", "float32", "float64", "float16", "bool"]


for dtype in all_dtypes:
    dtype = util.str2dtype(dtype)
    if dtype in {torch.float16, torch.float32, torch.float64, torch.bfloat16}:
        a = torch.randn(*size, device=device, dtype=dtype)
    elif dtype == torch.int64:
        a = torch.randint(2 ** 63 - 1, size=size, device=device, dtype=dtype)
    elif dtype == torch.int32:
        a = torch.randint(2 ** 31, size=size, device=device, dtype=dtype)
    elif dtype == torch.int16:
        a = torch.randint(2 ** 15, size=size, device=device, dtype=dtype)
    elif dtype == torch.int8:
        a = torch.randint(2 ** 7, size=size, device=device, dtype=dtype)
    elif dtype == torch.uint8:
        a = torch.randint(2 ** 8, size=size, device=device, dtype=dtype)
    elif dtype == torch.bool:
        a = torch.randint(2, size=size, device=device, dtype=dtype)
    sparsity_mask = torch.rand(*size, device=device) < sparsity
    a[sparsity_mask] = 0

    spa = SparseDOKTensor.from_dense(a)
    
    assert torch.allclose(spa.abs().to_dense(), a.abs()), "abs() failed"
    # print(spa.sin())