
import torch
import torch.nn as nn
import numpy as np
import math
from tqdm import tqdm
from torchtimer import ProfilingTimer


from DOKSparse.sparse_dok import util
from DOKSparse.sparse_dok import CudaClosedHashmap

device = "cuda:0"
key_type = util.str2dtype("long")
value_type = util.str2dtype("int")
key_shape = [2]
value_shape = [2]
table_size = 10000

hm = CudaClosedHashmap(
  n_buckets=table_size,
  device=device, 
  key_size=math.prod(key_shape),
  rehash_threshold=0.5,
  rehash_factor=2.0, ###
)
# hm.timer.disable()
timer = ProfilingTimer("main")
n_warpmup_iters = 5
# n_iters = 100
n = 1000000
compare_baseline = False

if key_type in {torch.int, torch.long}:
    keys = torch.randint(2 ** 31, size=(n, *key_shape), device=device, dtype=key_type)

elif value_type in {torch.float, torch.double, torch.half}:
    keys = torch.rand(n, *key_shape, device=device, dtype=key_type)

if value_type in {torch.int, torch.long}:
    values = torch.randint(2 ** 20, size=(n, *value_shape), device=device, dtype=value_type)
elif value_type in {torch.float, torch.double, torch.half}:
    values = torch.rand(n, *value_shape, device=device, dtype=value_type)

hm.set(keys, values)

percent_to_del = 0.1
inds_to_remove = (torch.rand(n, device=device) < percent_to_del).nonzero()[:, 0]
keys_to_remove = keys[inds_to_remove]
vals_to_remove = values[inds_to_remove]
print("number of elements in hashmap", hm.n_elements)
print("number of keys to remove", len(inds_to_remove))

is_removed = hm.remove(keys_to_remove)
print("number of elements in hashmap after remove", hm.n_elements)
print("is everything removed:", (~is_removed).sum().item())

rvals, is_found = hm.get(keys)
error = is_found[inds_to_remove].sum()
print("are removed items found:", error.item() == 0)
print("number of removedMarkers", (hm._uuid == -3).sum() )


hm.set(keys_to_remove, vals_to_remove)
print("number of elements in hashmap", hm.n_elements)
print("number of removedMarkers", (hm._uuid == -3).sum() )

rvals, is_found = hm.get(keys)
print("are all keys found:", (~is_found).sum().item() == 0)
print("are all values correct:", torch.allclose(values, rvals))

if key_type in {torch.int, torch.long}:
    new_keys = torch.randint(2 ** 31, size=(n, *key_shape), device=device, dtype=key_type)

elif value_type in {torch.float, torch.double, torch.half}:
    new_keys = torch.rand(n, *key_shape, device=device, dtype=key_type)
hm.set(new_keys, values)
print("number of elements in hashmap", hm.n_elements)
print("number of removedMarkers", (hm._uuid == -3).sum() )
