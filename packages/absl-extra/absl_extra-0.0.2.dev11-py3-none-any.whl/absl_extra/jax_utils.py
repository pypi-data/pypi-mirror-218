from __future__ import annotations

import functools
import logging
import platform
from typing import Callable, TypeVar

import jax

T = TypeVar("T", bound=Callable)


def requires_gpu(func: T, linux_only: bool = False) -> T:
    """
    Fail if function is executing on host without access to GPU(s).
    Useful for early detecting container runtime misconfigurations.

    Parameters
    ----------
    func:
        Function, which needs hardware acceleration.
    linux_only:
        If set to true, will ignore check on non-linux hosts.


    Returns
    -------

    func:
        Function with the same signature as original one.

    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> R:
        if linux_only and platform.system() != "linux":
            logging.info(
                "Not running on linux, and linux_only==True, ignoring GPU strategy check."
            )
            return func(*args, **kwargs)

        devices = jax.devices()
        logging.info(f"JAX devices -> {devices}")
        if devices[0].device_kind != "gpu":
            raise RuntimeError("No GPU available.")
        return func(*args, **kwargs)

    return wrapper
