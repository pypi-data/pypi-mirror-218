import numpy as np
import pandas as pd
import pytest

from gauss_lm_mle import mle_rotated_gaussian


def test_mle_rotated_gaussian():
    # create synthetic image
    image = np.random.normal(size=(100, 100))

    # known parameters
    yxlocs = (np.array([50]), np.array([50]))
    boxsize = 10
    itermax = 100

    # call function
    result = mle_rotated_gaussian(image, yxlocs, boxsize, itermax)

    # check result is a DataFrame with correct shape
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (1, 10)

    # check columns of DataFrame
    expected_columns = [
        "A",
        "bg",
        "x",
        "y",
        "sx",
        "sy",
        "theta",
        "asymmetry",
        "niter",
        "norm2_error",
    ]
    assert list(result.columns) == expected_columns

    # check 'niter' is int
    assert result["niter"].dtype == int
