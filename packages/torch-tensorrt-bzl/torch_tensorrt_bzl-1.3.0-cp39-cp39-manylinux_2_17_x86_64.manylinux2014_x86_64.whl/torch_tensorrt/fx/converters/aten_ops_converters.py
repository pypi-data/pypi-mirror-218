# flake8: noqa
import logging
import math
import operator
import warnings
from typing import cast, Dict, Optional, Sequence, Tuple, Union

import numpy as np

# @manual=//deeplearning/trt/python:py_tensorrt
import tensorrt as trt
import torch
from torch_tensorrt.fx.converters import acc_ops_converters

from ..converter_registry import tensorrt_converter

from ..types import *  # noqa: F403
from torch.fx.immutable_collections import immutable_list
from torch.fx.node import Argument, Target

from ..utils import get_dynamic_dims, torch_dtype_from_trt, torch_dtype_to_trt

from .converter_utils import *  # noqa: F403
import torch_tensorrt.fx.tracer.acc_tracer.acc_utils as acc_utils

_LOGGER: logging.Logger = logging.getLogger(__name__)

## converter list in alphabetic order
@tensorrt_converter(torch.ops.aten.add.Tensor)
def aten_ops_add(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    kwargs_new = {
        "input": args[0],
        "other": args[1],
    }
    return acc_ops_converters.acc_ops_add(network, target, None, kwargs_new, name)


@tensorrt_converter(torch.ops.aten.mean.dim)
@tensorrt_converter(torch.ops.aten._adaptive_avg_pool3d.default)
@tensorrt_converter(torch.ops.aten._adaptive_avg_pool2d.default)
def aten_ops_adaptive_avg_poolnd(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    if target == torch.ops.aten.mean.dim:

        if list(args[1]) != [-1, -2]:
            raise RuntimeError(f"We do not support {target} has dim={args[1]}")
        else:
            output_size = [1, 1]
    else:
        output_size = args[1]

    kwargs_new = {
        "input": args[0],
        "output_size": output_size,
    }
    return acc_ops_converters.acc_ops_adaptive_avg_poolnd(
        network, target, None, kwargs_new, name
    )


@tensorrt_converter(torch.ops.aten.batch_norm)
def aten_ops_batch_norm(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    kwargs_new = {
        "input": args[0],
        "weight": args[1],
        "bias": args[2],
        "running_mean": args[3],
        "running_var": args[4],
        "training": args[5],
        "momentum": args[6],
        "eps": args[7],
    }
    return acc_ops_converters.acc_ops_batch_norm(
        network, target, None, kwargs_new, name
    )


@tensorrt_converter(torch.ops.aten.convolution.default)
def aten_ops_convolution(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    kwargs_new = {
        "input": args[0],
        "weight": args[1],
        "bias": args[2],
        "stride": args[3],
        "padding": args[4],
        "dilation": args[5],
        "groups": args[8],
    }
    # we do not handle transposed.
    if args[6] is True:
        raise RuntimeError(f"Target {target} does not support `transposed=True` ")
    # we do not handle output_padding.
    if args[7] not in ([0], [0, 0], [0, 0, 0]):
        raise RuntimeError(f"Target {target} has non-0 output_padding")
    if len(kwargs_new["stride"]) == 1:
        return acc_ops_converters.acc_ops_conv1d(
            network, target, None, kwargs_new, name
        )
    else:
        return acc_ops_converters.acc_ops_convnd(
            network, target, None, kwargs_new, name
        )


@tensorrt_converter(torch.ops.aten.div.default)
@tensorrt_converter(torch.ops.aten.div.Tensor_mode)
@tensorrt_converter(torch.ops.aten.div.Tensor)
def aten_ops_div(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    kwargs_new = {
        "input": args[0],
        "other": args[1],
    }
    rounding_mode = kwargs.get("rounding_mode")
    if rounding_mode is None:
        return acc_ops_converters.acc_ops_div(network, target, None, kwargs_new, name)
    elif rounding_mode == "floor":
        return acc_ops_converters.acc_ops_floor_div(
            network, target, None, kwargs_new, name
        )
    elif rounding_mode == "trunc":
        return acc_ops_converters.acc_ops_trunc_div(
            network, target, None, kwargs_new, name
        )
    else:
        raise RuntimeError(
            f"Target {target} does not support rounding mode {rounding_mode}"
        )


@tensorrt_converter(torch.ops.aten.floor_divide.default)
def aten_ops_floor_div(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    kwargs_new = {
        "input": args[0],
        "other": args[1],
    }
    return acc_ops_converters.acc_ops_floor_div(network, target, None, kwargs_new, name)


@tensorrt_converter(torch.ops.aten.fmod.Scalar)
@tensorrt_converter(torch.ops.aten.fmod.Tensor)
def aten_ops_fmod(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    kwargs_new = {
        "input": args[0],
        "other": args[1],
    }
    return acc_ops_converters.acc_ops_fmod(network, target, None, kwargs_new, name)


@tensorrt_converter(torch.ops.aten.mm.default)
@tensorrt_converter(torch.ops.aten.addmm.default)
def aten_ops_linear(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    if target == torch.ops.aten.addmm.default:
        kwargs_new = {
            "bias": args[0],
            "input": args[1],
            "weight": args[2],
        }
    elif target == torch.ops.aten.mm.default:
        kwargs_new = {
            "bias": None,
            "input": args[0],
            "weight": args[1],
        }
    return acc_ops_converters.acc_ops_linear(network, target, None, kwargs_new, name)


@tensorrt_converter(torch.ops.aten.max_pool3d)
@tensorrt_converter(torch.ops.aten.max_pool2d)
def aten_ops_max_poolnd(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    kwargs_new = {
        "input": args[0],
        "kernel_size": args[1],
        "stride": args[2]
        if len(args) > 2
        else (None, None)
        if len(args[1]) == 2
        else (None, None, None),
        "padding": args[3]
        if len(args) > 3
        else (0, 0)
        if len(args[1]) == 2
        else (0, 0, 0),
        "dilation": args[4]
        if len(args) > 4
        else (1, 1)
        if len(args[1]) == 2
        else (1, 1, 1),
        "ceil_mode": args[5] if len(args) > 5 else False,
    }
    return acc_ops_converters.acc_ops_max_poolnd(
        network, target, None, kwargs_new, name
    )


@tensorrt_converter(torch.ops.aten.mul.Tensor)
def aten_ops_mul(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    kwargs_new = {
        "input": args[0],
        "other": args[1],
    }
    return acc_ops_converters.acc_ops_mul(network, target, None, kwargs_new, name)


@tensorrt_converter(torch.ops.aten.pow.Tensor_Scalar)
@tensorrt_converter(torch.ops.aten.pow.Tensor_Tensor)
def aten_ops_pow(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    kwargs_new = {
        "input": args[0],
        "exponent": args[1],
    }
    return acc_ops_converters.acc_ops_pow(network, target, None, kwargs_new, name)


@tensorrt_converter(torch.ops.aten.relu.default)
def aten_ops_relu(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    kwargs_new = {
        "input": args[0],
    }
    return acc_ops_converters.acc_ops_relu(network, target, None, kwargs_new, name)


@tensorrt_converter(torch.ops.aten.sub.Tensor)
def aten_ops_sub(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    kwargs_new = {
        "input": args[0],
        "other": args[1],
    }
    return acc_ops_converters.acc_ops_sub(network, target, None, kwargs_new, name)


@tensorrt_converter(torch.ops.aten._unsafe_view.default)
@tensorrt_converter(torch.ops.aten._reshape_alias.default)
@tensorrt_converter(torch.ops.aten.view.default)
def aten_ops_reshape(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    kwargs_new = {
        "input": args[0],
        "acc_out_ty": acc_utils.build_raw_tensor_meta(shape=args[1]),
    }
    return acc_ops_converters.acc_ops_reshape(network, target, None, kwargs_new, name)
