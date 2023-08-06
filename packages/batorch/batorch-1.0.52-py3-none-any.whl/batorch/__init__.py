
from pycamia import info_manager

__info__ = info_manager(
    project = 'PyCAMIA',
    package = 'batorch',
    author = 'Yuncheng Zhou',
    create = '2021-12',
    version = '1.0.51',
    contact = 'bertiezhou@163.com',
    keywords = ['torch', 'batch', 'batched data'],
    description = "'batorch' is an extension of package torch, for tensors with batch dimensions. ",
    requires = ['pycamia', 'torch', 'pynvml'],
    update = '2023-07-07 18:16:07'
).check()
__version__ = '1.0.51'

import torch
distributed = torch.distributed
autograd = torch.autograd
random = torch.random
optim = torch.optim
utils = torch.utils
linalg = torch.linalg
# from .torchext import __all__
# for f in __all__:
#     exec(f"from .torchext import {f}")
#     setattr(torch, f, eval(f))

if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
    from .device import MPS
if hasattr(torch, 'cuda') and torch.cuda.is_available():
    from .device import GPU, GPUs

from .device import free_memory_amount, all_memory_amount, AutoDevice
from .tensorfunc import crop_as, pad, decimal, divide, equals, matpow, matprod, dot, down_scale, gaussian_kernel, norm, norm2, Fnorm, Fnorm2, frobenius_norm, meannorm, meannorm2, mean_norm, mean_norm2, Jacobian, grad_image, image_grid, up_scale, one_hot, permute_space, skew_symmetric, cross_matrix, uncross_matrix, summary, display #*
from .optimizer import CSGD, CADAM, Optimization, train, test #*
from .tensor import * # do not expand
from . import nn

import math
e = tensor(math.e)
nan = tensor(math.nan)
inf = tensor(math.inf)
pi = tensor(math.pi)

















































