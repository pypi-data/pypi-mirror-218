import numpy as np
import torch
from torchtimer import ProfilingTimer

from DOKSparse.sparse_dok import SparseDOKTensor
from DOKSparse.sparse_dok.components.cuda.sparse_dok_tensor_impl import timer as sparse_dok_tensor_impl_timer

timer = ProfilingTimer()
device = "cuda:0"
sparsity = 0.9
iters = 100
warmup_iters = 5
shape = [4096, 4096]
sparse_dok_tensor_impl_timer.disable()

for i in range(iters + warmup_iters):
    if i < warmup_iters:
        timer.disable()
    else:
        timer.enable()
    a = torch.rand(*shape, device=device)
    a[a < sparsity] = 0

    spa = SparseDOKTensor.from_dense(a)
    # selectors = (torch.randint(shape[0], size=(shape[0])), slice(0, 500, None))
    # selectors = (0, slice(None))
    # selectors = (slice(None), 0)
    # selectors = (slice(None), slice(None))
    # selectors = (torch.randint(shape[0], size=(shape[0], 1) ), torch.randint(shape[1], size=(1, shape[1]) ) )
    # selectors = (torch.randint(shape[0], size=(np.prod(shape),)), torch.randint(shape[1], size=(np.prod(shape),)))
    selectors = (torch.randint(shape[0], size=shape), torch.randint(shape[1], size=shape))
    values = torch.rand(*shape, device=device, dtype=spa.dtype)
    values[values < sparsity] = 0

    spa_values = values.to_sparse_coo()

    timer.start("dok get items sparse")
    dok_res_sparse = spa.__spgetitem__(selectors)
    timer.stop("dok get items sparse")

    aranges = [torch.arange(i) for i in shape]
    timer.start("dense get items")
    dense_res = a[selectors]
    # dense_res = a[aranges[0]][:, aranges[1]]
    timer.stop("dense get items")


    timer.start("dok get items dense")
    dok_res_dense = spa[selectors]
    timer.stop("dok get items dense")
    if not torch.allclose(dense_res, dok_res_sparse.to_dense()):
        print(dok_res_sparse.shape, dense_res.shape)
        mask = dense_res != dok_res_sparse.to_dense()
        print("sparse get incorrect! num unequal items:", mask.sum().item(), "out of", mask.numel())
        # print(mask.nonzero())
        print(dok_res_sparse.to_dense()[mask])
        print(dense_res[mask])


    timer.start("dense set items")
    a[selectors] = values
    timer.stop("dense set items")
    
    # timer.start("dok set items dense")
    # spa[selectors] = values
    # timer.stop("dok set items dense")

    timer.start("dok set items sparse")
    spa[selectors] = spa_values
    timer.stop("dok set items sparse")
    
    if not torch.allclose(a, spa.to_dense()):
        mask = a != spa.to_dense()
        # mask = ~mask
        print("sparse_dok_set_sparse incorrect! num unequal items:", mask.sum().item(), "out of", mask.numel())
        print(a[mask])
        print(spa.to_dense()[mask])
        print(spa.values().max())
        # print(spa.indices().unique(dim=-1, return_counts=True)[1].max())
        print("duplicate uuids", spa.storage().uuid().unique(return_counts=True)[1].max())
        # print(spa.indices().shape, a.to_sparse().coalesce().indices().shape )
        


timer.summarize()
sparse_dok_tensor_impl_timer.summarize()