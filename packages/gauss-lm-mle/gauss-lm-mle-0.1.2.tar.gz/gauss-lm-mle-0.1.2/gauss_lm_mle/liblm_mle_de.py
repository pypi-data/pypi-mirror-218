import ctypes
import sys
import os
import numpy as np


def load_library():
    """handle system-specific C-library loading"""
    version_info = sys.version_info
    dir_path = os.path.dirname(os.path.realpath(__file__))
    lib_filename = f"./lm_mle_de.cpython-{version_info.major}{version_info.minor}-darwin.so"
    lib_path = os.path.join(dir_path, lib_filename)

    try:
        lib = ctypes.CDLL(lib_path)
    except OSError as e:
        raise OSError(f"Failed to load shared library {lib_path}.") from e

    lib.fit_rotated_gaussian.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.double, ndim=2, flags="C_CONTIGUOUS"),
        np.ctypeslib.ndpointer(dtype=np.intc, ndim=1, flags="C_CONTIGUOUS"),
        np.ctypeslib.ndpointer(dtype=np.intc, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.double, ndim=2, flags="C_CONTIGUOUS"),
    ]

    lib.fit_rotated_gaussian.restype = None

    lib.fit_gaussian.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.double, ndim=2, flags="C_CONTIGUOUS"),
        np.ctypeslib.ndpointer(dtype=np.intc, ndim=1, flags="C_CONTIGUOUS"),
        np.ctypeslib.ndpointer(dtype=np.intc, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        np.ctypeslib.ndpointer(dtype=np.double, ndim=2, flags="C_CONTIGUOUS"),
    ]

    lib.fit_gaussian.restype = None
    
    return lib
