from setuptools import setup, Extension
import os

# Compiler flags
cflags = ["-O3", "-funroll-loops", "-Wall"]

# Libraries
libraries = ["gsl", "gslcblas", "m"]

# Include directories
# Modify this as needed if GSL headers are in a different location
include_dirs = ["/opt/homebrew/Cellar/gsl/2.7.1/include"]

# Library directories
# Modify this as needed if GSL libraries are in a different location
library_dirs = ["/opt/homebrew/Cellar/gsl/2.7.1/lib"]

# C extension modules
lm_mle_de_module = Extension(
    "gauss_lm_mle.lm_mle_de",
    sources=["c_src/lm_mle.c", "c_src/gfit.c"],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=libraries,
    extra_compile_args=cflags,
)

# Setup
setup(
    name="gauss-lm-mle",
    version="0.1.2",
    description="MLE Gaussian fitting with Poisson deviates",
    ext_modules=[lm_mle_de_module],
    packages=["gauss_lm_mle"],
    package_data={"gauss_lm_mle": ["c_src/*.h"]},
    install_requires=[  # Add your Python dependencies here
        "numpy",
        "pandas",
        "scipy",
    ],
)
