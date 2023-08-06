import torch
import numpy as np
from torchtimer import ProfilingTimer

from DOKSparse.sparse_dok import SparseDOKTensor

timer = ProfilingTimer()
device = "cuda:0"
sparsity = 0.9
iters = 100
warmup_iters = 3
shapes = (
    (1000000, 1),
    (100000, 10),
    (10000, 100),
    (1000, 1000),
    (100, 10000),
    (10, 100000),
    (1, 1000000),
    (10, 100, 1000),
    (100, 100, 100),
    (1000, 100, 10),
    (1000, 1, 1000),
    (10, 10, 100, 100),
    (10, 100, 10, 100),
    (100, 10, 100, 10),
    (10, 100, 100, 10),
    (100, 10, 10, 100),
)

for i in range(iters + warmup_iters):
    if i < warmup_iters:
        timer.disable()
    else:
        timer.enable()
    a = torch.rand(1000, 1000, device=device)
    a[a < sparsity] = 0

    spa = SparseDOKTensor.from_dense(a)
    print(spa)

    timer.start("flatten")
    flat_spa = spa.flatten()
    timer.stop("flatten")

    flat_a = a.flatten()
    if not torch.allclose(flat_spa.to_dense(), flat_a):
        print("flatten failed")

    for shape in shapes:
        timer.start(f"reshape: {shape}")
        reshaped_spa = spa.reshape(*shape)
        timer.stop(f"reshape: {shape}")
        reshaped_a = a.reshape(*shape)
        # print(reshaped_spa._nnz(), reshaped_spa.shape, reshaped_spa.indices().shape, reshaped_spa.values().shape)
        # print(reshaped_spa.indices() )
        # print(reshaped_a.to_sparse_coo().indices())
        if not torch.allclose(reshaped_spa.to_dense(), reshaped_a):
            print(f"reshape: {shape} failed")

timer.summarize()